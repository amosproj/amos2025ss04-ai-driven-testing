import argparse
import json
import os
import importlib
from llm_manager import LLMManager
from metrics import evaluate_and_save_metrics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"
MODULES_DIR = os.path.join(SCRIPT_DIR, "modules")


def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def load_modules(module_names):
    def snake_to_camel(name: str) -> str:
        return "".join(word.capitalize() for word in name.split("_"))

    modules = []
    for name in module_names:
        try:
            mod = importlib.import_module(f"modules.{name}")
            class_name = snake_to_camel(name)
            cls = getattr(mod, class_name)
            modules.append(cls())
        except Exception as e:
            print(f"Failed to load module '{name}': {e}")
    return modules


def apply_before_modules(modules, prompt):
    for m in modules:
        if m.applies_before():
            prompt = m.process_prompt(prompt)
    return prompt


def apply_after_modules(modules, response, prompt):
    for m in modules:
        if m.applies_after():
            response = m.process_response(response, prompt)
    return response


if __name__ == "__main__":
    # Load allowed models
    config_path = os.path.join(SCRIPT_DIR, ALLOWED_MODELS)
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    loaded_models = data.get("models", [])

    # CLI
    parser = argparse.ArgumentParser(
        description="Run Ollama prompt sending script."
    )
    parser.add_argument(
        "--model", type=int, choices=range(len(loaded_models)), default=0
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "prompt.txt"),
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "output.md"),
    )
    parser.add_argument(
        "--modules",
        type=str,
        default="",
        help="Comma-separated list of modules to apply",
    )
    args = parser.parse_args()

    model = loaded_models[args.model]
    model_id = model["id"]
    model_name = model["name"]

    # Load modules
    selected_modules = [
        m.strip() for m in args.modules.split(",") if m.strip()
    ]
    active_modules = load_modules(selected_modules)

    # Read and pre-process prompt
    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()
    prompt_text = apply_before_modules(active_modules, prompt_text)

    manager = LLMManager()
    try:
        manager.start_model_container(model_id)
        print(f"\n--- Response from {model_name} ---")
        response, loading_time, final_time = manager.send_prompt(
            model_id, prompt_text, output_file=args.output_file
        )

        response = apply_after_modules(active_modules, response, prompt_text)

        evaluate_and_save_metrics(
            response, model_name, final_time, loading_time
        )
        print("")
    finally:
        manager.stop_model_container(model_id)
