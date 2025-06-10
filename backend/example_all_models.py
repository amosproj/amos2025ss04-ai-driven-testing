import os
from llm_manager import LLMManager

# Example list of model IDs to run
REQUESTED_MODELS = [
    "mistral:7b-instruct-v0.3-q3_K_M",
    "deepseek-coder:6.7b-instruct-q3_K_M",
    "qwen2.5-coder:3b-instruct-q8_0",
    "gemma3:4b-it-q4_K_M",
    "phi4-mini:3.8b-q4_K_M",
    "qwen3:4b-q4_K_M",
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT = "prompt.txt"

if __name__ == "__main__":
    manager = LLMManager()

    # Start each requested model container
    for model_id in REQUESTED_MODELS:
        manager.start_model_container(model_id)

    try:
        prompt_path = os.path.join(SCRIPT_DIR, PROMPT)
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_text = f.read()
        # Send the same prompt to each active model
        for model_id in REQUESTED_MODELS:
            print(f"\n--- Response from {model_id} ---")
            manager.send_prompt(model_id, prompt_text)
            print("")
    finally:
        # Stop all model containers
        for model_id in REQUESTED_MODELS:
            manager.stop_model_container(model_id)
