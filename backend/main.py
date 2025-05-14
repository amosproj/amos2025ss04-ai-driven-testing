import argparse
import json
import os
from llm_manager import LLMManager
from metrics import evaluate_and_save_metrics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"

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
    parser.add_argument(
        "--print_output",
        type=bool,
        default=False,
        help="Print the output to the console (default: False)",
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
        response, loading_time, final_time = manager.send_prompt(
            model_id,
            prompt_text,
            output_file=args.output_file,
            print_output=args.print_output,
        )
        evaluate_and_save_metrics(
            response, model_name, final_time, loading_time
        )
        print("")
    finally:
        manager.stop_model_container(model_id)
