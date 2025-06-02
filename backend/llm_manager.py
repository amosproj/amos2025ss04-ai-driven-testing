import docker
import requests
import time
import os
from tqdm import tqdm
import json
from typing import Dict
import socket

OLLAMA_IMAGE = "ollama/ollama"
OLLAMA_MODELS_VOLUME = os.path.abspath("./ollama-models")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"


class LLMManager:
    """
    Manages multiple Docker containers (one per model) for local LLM execution.
    Provides a unified interface to:
      - Start a container for a given model
      - Pull the model
      - Send prompts
      - Stop the container
    """

    def __init__(self):
        self.client = docker.from_env()
        # Map: model_name -> (container, port)
        self.active_models: Dict[
            str, (docker.models.containers.Container, int)
        ] = {}

    def _verify_model_id(self, model_id: str) -> None:
        """
        Checks whether the provided model_id is valid based on the loaded JSON config.
        Raises ValueError if not found.
        """
        config_path = os.path.join(SCRIPT_DIR, ALLOWED_MODELS)
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        loaded_models = data.get("models", [])

        valid_ids = [model_info["id"] for model_info in loaded_models]
        if model_id not in valid_ids:
            raise ValueError(
                f"Model '{model_id}' is not allowed. Allowed models: {valid_ids}"
            )

    def start_model_container(self, model_id: str) -> None:
        """
        Starts a docker container for a particular model on a unique port.
        """
        self._verify_model_id(model_id)

        container_name = f"ollama_{model_id.replace(':', '_')}"

        # Remove any left-over container with same name
        try:
            existing = self.client.containers.get(container_name)
            existing.remove(force=True)
        except docker.errors.NotFound:
            pass

        print(f"Pulling docker image {OLLAMA_IMAGE} ...")
        self._pull_ollama_image()

        # Grab a random free port
        port = self._get_free_port()

        print(f"Starting container {container_name} on free port {port}...")
        container = self.client.containers.run(
            OLLAMA_IMAGE,
            name=container_name,
            ports={"11434/tcp": port},
            volumes={
                OLLAMA_MODELS_VOLUME: {"bind": "/root/.ollama", "mode": "rw"}
            },
            detach=True,
            remove=True,
        )

        self._wait_for_api(port)

        # Pull the model inside the container
        self._pull_model(port, model_id)

        # Track it
        self.active_models[model_id] = (container, port)

    def stop_model_container(self, model_id: str) -> None:
        """
        Stops and removes the container for the given model.
        """
        if model_id not in self.active_models:
            print(f"No active container found for '{model_id}'.")
            return
        container, _ = self.active_models[model_id]
        print(f"Stopping container for model {model_id}...")
        container.stop()
        del self.active_models[model_id]

    def send_prompt(
        self, model_id: str, prompt: str, output_file: str = None
    ) -> str:
        """
        Sends user prompt (including any source code) to the specified model and returns the LLM output.
        """
        if model_id not in self.active_models:
            raise ValueError(
                f"Model '{model_id}' is inactive. "
                f"Start it first via start_model_container()."
            )
        _, port = self.active_models[model_id]
        url = f"http://localhost:{port}/api/generate"

        # Provide a minimal system instruction
        system_message = (
            "You are a helpful assistant. Provide your answer always in Markdown.\n"
            "Format code blocks appropriately, and do not include text outside valid Markdown."
        )

        payload = {
            "model": model_id,
            "prompt": prompt,
            "system": system_message,
            "stream": True,
            "options": {
                "seed": 42,
                "num_ctx": 4096,  # Default context size, can be adjusted
            },
        }

        collected_response = ""
        start_time = time.time()
        with requests.post(url, json=payload, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode("utf-8")
                    try:
                        chunk_json = json.loads(decoded_chunk)
                        chunk_response = chunk_json.get("response", "")
                        print(chunk_response, end="", flush=True)
                        collected_response += chunk_response
                    except json.JSONDecodeError:
                        continue

        end_time_loading = time.time()
        if not output_file:
            # Generate a default output filename from the model_id
            safe_model_id = model_id.replace(":", "_")
            output_file = "output-" + safe_model_id + ".md"

        output_path = os.path.join(SCRIPT_DIR, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(collected_response)
        end_time_final = time.time()
        loading_response_time = end_time_loading - start_time
        final_response_time = end_time_final - start_time
        return collected_response, loading_response_time, final_response_time

    def _pull_ollama_image(self):
        """
        Pulls the ollama/ollama image with progress tracking.
        """
        progress_bars = {}
        last_status_key = None

        for line in self.client.api.pull(
            OLLAMA_IMAGE, stream=True, decode=True
        ):
            status = line.get("status")
            layer_id = line.get("id")
            progress = line.get("progressDetail", {})
            if layer_id and "current" in progress and "total" in progress:
                current = progress["current"]
                total = progress["total"]
                if layer_id not in progress_bars:
                    progress_bars[layer_id] = tqdm(
                        total=total,
                        desc=f"Layer {layer_id[:10]}",
                        unit="B",
                        unit_scale=True,
                        leave=False,
                    )
                progress_bars[layer_id].n = current
                progress_bars[layer_id].refresh()
            status_key = f"{layer_id}:{status}" if layer_id else status
            if status and status_key != last_status_key:
                tqdm.write(
                    f"{layer_id[:10]}: {status}" if layer_id else status
                )
                last_status_key = status_key
        for pbar in progress_bars.values():
            pbar.close()

    def _pull_model(self, port: int, model_name: str):
        """
        Pulls the given model inside the Ollama container.
        """
        print(f"Pulling model: {model_name}")
        url = f"http://localhost:{port}/api/pull"
        with requests.post(url, json={"name": model_name}, stream=True) as r:
            r.raise_for_status()
            pbar = None
            last_status = None
            total_size = 0
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    status = data.get("status", "")
                    total = data.get("total", total_size) or total_size
                    completed = data.get("completed", 0)
                    if total > total_size:
                        total_size = total
                    if pbar is None and total_size > 0:
                        pbar = tqdm(
                            total=total_size,
                            unit="B",
                            unit_scale=True,
                            desc="Model Download",
                            leave=False,
                        )
                    if pbar and "completed" in data:
                        pbar.n = completed
                        pbar.refresh()
                    if status and status != last_status:
                        tqdm.write(status)
                        last_status = status
                except json.JSONDecodeError:
                    pass
            if pbar:
                pbar.close()

    def _wait_for_api(self, port: int, timeout=60):
        """
        Waits until the container's API is available or times out.
        """
        start_time = time.time()
        url = f"http://localhost:{port}/api/tags"
        while time.time() - start_time < timeout:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    print(f"Ollama API on port {port} is ready!")
                    return
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(2)
        raise TimeoutError("Ollama API did not become available in time.")

    def _get_free_port(self) -> int:
        """
        Requests an ephemeral port from the OS by binding to port=0,
        then closes the socket. The OS automatically picks a free port.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            port = s.getsockname()[1]
            return port
