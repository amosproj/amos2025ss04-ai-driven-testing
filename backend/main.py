import argparse
import os
from llm_manager import LLMManager
from models_allowed import Model

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Run Ollama prompt sending script."
    )
    parser.add_argument(
        "--model",
        type=int,
        choices=range(len(Model)),
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

    try:
        # Get the actual model name from the enum
        model = Model.get_model(args.model)
    except ValueError as e:
        print(e)
        exit(1)

    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    manager = LLMManager()
    try:
        manager.start_model_container(model)
        print(f"\n--- Response from {model.name} ---")
        manager.send_prompt(model, prompt_text)
        print("")
    finally:
        manager.stop_model_container(model)
