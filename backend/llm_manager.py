import docker
import requests
import time
import os
from tqdm import tqdm
import json
from typing import Dict
from schemas import PromptData, ResponseData, OutputData, TimingData
import socket
from pathlib import Path

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
            str, (docker.models.containers.Container, int, str)
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
        print("container_name:")
        print(container_name)

        # Grab a random free port
        port = self._get_free_port()

        # Prepare container arguments
        container_args = {
            "image": OLLAMA_IMAGE,
            "name": container_name,
            "ports": {f"{port}/tcp": port},
            "volumes": {
                OLLAMA_MODELS_VOLUME: {"bind": "/root/.ollama", "mode": "rw"}
            },
            "environment": {"OLLAMA_HOST": f"0.0.0.0:{str(port)}"},
            "detach": True,
            "remove": True,
        }

        # Add network only when running in Docker
        if running_in_docker():
            container_args["network"] = "backend"

        container = self.client.containers.run(**container_args)

        container.reload()

        print(f"Ollama is reachable on host port {port}")

        self._wait_for_api(port, container_name)

        # Pull the model inside the container
        self._pull_model(port, model_id, container_name)

        # Track it
        self.active_models[model_id] = (container, port, container_name)
        print(f"Modell {model_id} wurde erfolgreich geladen und ist bereit!")

    def stop_model_container(self, model_id: str) -> None:
        """
        Stops and removes the container for the given model.
        """
        if model_id not in self.active_models:
            print(f"No active container found for '{model_id}'.")
            return
        container, _, _ = self.active_models[model_id]
        print(f"Stopping container for model {model_id}...")
        container.stop()
        del self.active_models[model_id]

    def send_prompt(
        self, prompt_data: PromptData, output_file: str = None
    ) -> ResponseData:
        """
        Sends user prompt (including any source code) to the specified model and returns the LLM output.
        """

        model_id = prompt_data.model.id
        input_ = prompt_data.input

        user_message = input_.user_message
        source_code = input_.source_code
        system_message = input_.system_message
        options = input_.options.dict()  # turn Pydantic object into dict

        # Use rag_prompt if available, else construct full prompt
        full_prompt = (
            prompt_data.rag_prompt
            if prompt_data.rag_prompt
            else f"{input_.user_message}\n{input_.source_code}"
        )

        if model_id not in self.active_models:
            raise ValueError(
                f"Model '{model_id}' is inactive. "
                f"Start it first via start_model_container()."
            )
        _, port, container_name = self.active_models[model_id]
        url = f"{get_base_url(container_name)}:{port}/api/generate"
        print(url)

        payload = {
            "model": model_id,
            "prompt": full_prompt,
            "system": system_message,
            "stream": True,
            "options": options,
        }

        print(f"Sende Anfrage an Modell {model_id}...")
        collected_response = ""
        start_time = time.time()
        try:
            with requests.post(url, json=payload, stream=True) as r:
                if not r.ok:
                    error_detail = r.text
                    try:
                        error_json = r.json()
                        if "error" in error_json:
                            error_detail = error_json["error"]
                    except Exception as e:
                        print(e)
                        pass
                    raise RuntimeError(
                        f"API-Fehler: {r.status_code} - {error_detail}"
                    )

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

        except Exception as e:
            print(f"\nFehler beim Senden des Prompts: {str(e)}")
            raise

        end_loading = time.time()

        output = OutputData(markdown=collected_response)

        end_generation = time.time()

        timing = TimingData(
            loading_time=end_loading - start_time,
            generation_time=end_generation - start_time,
        )

        return ResponseData(
            model=prompt_data.model,
            output=output,
            timing=timing,
        )

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

    def _pull_model(self, port: int, model_name: str, container_name: str):
        """
        Pulls the given model inside the Ollama container.
        """
        print(f"Pulling model: {model_name}")
        url = f"{get_base_url(container_name)}:{port}/api/pull"
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

    def _wait_for_api(self, port: int, container_name: str, timeout=120):
        """
        Waits until the container's API is available or times out.
        """
        start_time = time.time()
        url = f"{get_base_url(container_name)}:{port}/api/tags"
        print(f"Warte auf Ollama API (url {url})...")
        while time.time() - start_time < timeout:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    print(f"Ollama API auf Port {port} ist bereit!")
                    # Zusätzliche Wartezeit für die vollständige Initialisierung
                    time.sleep(5)
                    return
            except requests.exceptions.ConnectionError:
                print(".", end="", flush=True)
                pass
            time.sleep(2)
        raise TimeoutError(
            f"Ollama API wurde nicht rechtzeitig verfügbar (Timeout nach {timeout}s)"
        )

    def _get_free_port(self) -> int:
        """
        Requests an ephemeral port from the OS by binding to port=0,
        then closes the socket. The OS automatically picks a free port.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            port = s.getsockname()[1]
            return port


def running_in_docker():
    return os.getenv("IN_DOCKER") == "true"


def get_base_url(container_name: str):
    if running_in_docker():
        return f"http://{container_name}"
    else:
        return "http://localhost"
