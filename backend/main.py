import argparse
import json
import os
from llm_manager import LLMManager

import docker
import requests
from tqdm import tqdm
import enum
import time

from metrics import evaluate_and_save_metrics

# Configuration
OLLAMA_IMAGE = "ollama/ollama"
OLLAMA_PORT = 11434
OLLAMA_API_URL = f"http://localhost:{OLLAMA_PORT}/api"
OLLAMA_GEN_ENDPOINT = f"{OLLAMA_API_URL}/generate"
OLLAMA_MODELS_VOLUME = os.path.abspath("./ollama-models")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"


class Model(enum.Enum):
    """Enumeration of available language models with their Ollama identifiers.

    Each enum value represents a specific model available through Ollama,
    including its version, quantization parameters, and approximate size.
    """

    MISTRAL = "mistral:7b-instruct-v0.3-q3_K_M"  # 3.52 GB
    DEEPSEEK = "deepseek-coder:6.7b-instruct-q3_K_M"  # 3.30 GB
    QWEN = "qwen2.5-coder:3b-instruct-q8_0"  # 3.29 GB
    GEMMA = "gemma3:4b-it-q4_K_M"  # 3.34 GB
    PHI4 = "phi4-mini:3.8b-q4_K_M"  # 2.49 GB

    @classmethod
    def get_model(cls, number: int) -> str:
        """Get the model identifier string by its index number.

        Args:
            number: Integer index of the model in the enum (0-based)

        Returns:
            str: The model identifier string

        Raises:
            ValueError: If the provided number is out of valid range
        """
        models = list(cls)
        if 0 <= number < len(models):
            return models[number].value
        raise ValueError(
            f"Invalid model number. Choose between 0-{len(models)-1}"
        )


def start_ollama_container():
    """Start and configure the Ollama Docker container.

    Removes any existing Ollama container, pulls the latest image with
    progress tracking, and starts a new container with volume mapping
    for model persistence.

    Returns:
        docker.Container: The running Ollama container instance
    """
    client = docker.from_env()

    try:
        existing = client.containers.get("ollama")
        print("Removing existing 'ollama' container...")
        existing.remove(force=True)
    except docker.errors.NotFound:
        pass

    print("Pulling Ollama image with progress tracking...")
    progress_bars = {}
    last_status_key = None
    printed_lines = 0

    for line in client.api.pull(OLLAMA_IMAGE, stream=True, decode=True):
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
            tqdm.write(f"{layer_id[:10]}: {status}" if layer_id else status)
            last_status_key = status_key
            printed_lines += 1

    for pbar in progress_bars.values():
        pbar.close()

    print("Starting Ollama container...")
    container = client.containers.run(
        OLLAMA_IMAGE,
        name="ollama",
        ports={f"{OLLAMA_PORT}/tcp": OLLAMA_PORT},
        volumes={
            OLLAMA_MODELS_VOLUME: {"bind": "/root/.ollama", "mode": "rw"}
        },
        detach=True,
        remove=True,
    )
    clear_stdout()

    return container


def wait_for_ollama_api(timeout=60):
    """Wait for the Ollama API to become available.

    Attempts to connect to the API endpoint and waits until it responds
    successfully or times out.

    Args:
        timeout: Maximum time to wait in seconds (default: 60)

    Returns:
        bool: True if the API became available

    Raises:
        TimeoutError: If the API doesn't become available within the timeout period
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            r = requests.get(f"{OLLAMA_API_URL}/tags")
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    raise TimeoutError("Ollama API did not become available in time.")


def pull_model(model):
    """Pull a model from Ollama's repository.

    Downloads the specified model with progress tracking.

    Args:
        model: Name of the model to pull (e.g., "deepseek-coder:1.3b")
    """
    print(f"Pulling model: {model}")
    with requests.post(
        f"{OLLAMA_API_URL}/pull", json={"name": model}, stream=True
    ) as r:
        r.raise_for_status()
        pbar = None
        last_status = None
        total_size = 0
        printed_lines = 0

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
                    printed_lines += 1
                    last_status = status

            except json.JSONDecodeError:
                decoded = line.decode("utf-8")
                if decoded != last_status:
                    tqdm.write(decoded)
                    printed_lines += 1
                    last_status = decoded

        if pbar:
            pbar.close()
            clear_stdout()


def send_prompt(prompt, model, output_file, stream=False):
    """Send a prompt to the Ollama API and save the response to a file.

    Structures the prompt with a system message that enforces Markdown output format.
    Can stream responses for real-time display.

    Args:
        prompt: The prompt text to send
        model: The model to use for generation
        output_file: Path where the response should be saved
        stream: Whether to stream the response (default: False)

    Returns:
        str: The generated response text
    """
    # Force a system instruction to make output structured as Markdown
    system_message = (
        "You must respond ONLY in valid Markdown format.\n"
        "Structure it like this:\n\n"
        "# Title\n\n"
        "## Summary\n\n"
        "Summary text here.\n\n"
        "## Code\n\n"
        "Code text here.\n\n"
        "Do not add any other text outside this Markdown structure."
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "system": system_message,
        "seed": 42,
    }

    if stream:
        collected_response = ""
        start_time = time.time()
        with requests.post(
            OLLAMA_GEN_ENDPOINT, json=payload, stream=True
        ) as r:
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

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(collected_response)
        end_time_final = time.time()
        loading_response_time = end_time_loading - start_time
        final_response_time = end_time_final - start_time
        return collected_response, loading_response_time, final_response_time

    else:
        start_time = time.time()
        r = requests.post(OLLAMA_GEN_ENDPOINT, json=payload)
        r.raise_for_status()
        response_text = r.json().get("response", "")
        end_time_loading = time.time()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response_text)
        end_time_final = time.time()
        loading_response_time = end_time_loading - start_time
        final_response_time = end_time_final - start_time

        return response_text, loading_response_time, final_response_time


def clear_stdout():
    """Clear the terminal screen.

    Uses the appropriate system command based on the operating system.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def read_prompt(file):
    """Read prompt content from a file.

    Args:
        file: Path to the prompt file

    Returns:
        str: Content of the prompt file
    """
    with open(file, "r") as f:
        return f.read()

if __name__ == "__main__":
    # Load allowed models from JSON config
    config_path = os.path.join(SCRIPT_DIR, ALLOWED_MODELS)
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    loaded_models = data.get("models", [])

    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Run Ollama prompt sending script."
    )
    parser.add_argument(
        "--model",
        type=int,
        choices=range(len(loaded_models)),
        default=0,
        help="Model selection (default: 0, here mistral AI)",
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "prompt.txt"),
        help="Path to the input prompt file (default: prompt.txt in the same directory)",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "output.md"),
        help="Path to save the output (default: output.md in the same directory)",
    )

    args = parser.parse_args()

    # Select the model based on the user-provided index
    model = loaded_models[args.model]
    model_id = model["id"]
    model_name = model["name"]

    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    manager = LLMManager()
    try:
        manager.start_model_container(model_id)
        print(f"\n--- Response from {model_name} ---")
        manager.send_prompt(
            model_id, prompt_text, output_file=args.output_file
        )
        print("")
        # Get the actual model name from the enum
        model_name = Model.get_model(args.model)
    except ValueError as e:
        print(e)
        exit(1)

    container = start_ollama_container()
    try:
        print("Waiting for Ollama API...")
        wait_for_ollama_api()

        pull_model(model_name)
        clear_stdout()

        print("Sending prompt...")
        prompt = read_prompt(args.prompt_file)
        print(f"Prompt: \n{prompt}")
        print("Answer:")
        response, loading_time, final_time = send_prompt(
            prompt=prompt,
            model=model_name,
            stream=True,
            output_file=args.output_file,
        )
        evaluate_and_save_metrics(
            response, model_name, final_time, loading_time
        )
    finally:
        manager.stop_model_container(model_id)
