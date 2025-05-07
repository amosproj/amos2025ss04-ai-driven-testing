from llm_manager import LLMManager
from models_allowed import Model

# Provide a list of Model enum members you want to run
REQUESTED_MODELS = [
    Model.MISTRAL,
    Model.DEEPSEEK,
    Model.QWEN,
    Model.GEMMA,
    Model.PHI4,
]
PROMPT = "prompt.txt"

if __name__ == "__main__":
    manager = LLMManager()

    # Start each requested model container
    for model in REQUESTED_MODELS:
        manager.start_model_container(model)

    try:
        with open(PROMPT, "r", encoding="utf-8") as f:
            prompt_text = f.read()
        # Send the same prompt to each active model
        for model in REQUESTED_MODELS:
            print(f"\n--- Response from {model.name} ---")
            manager.send_prompt(model, prompt_text)
            print("")
    finally:
        # Stop all model containers
        for model in REQUESTED_MODELS:
            manager.stop_model_container(model)
