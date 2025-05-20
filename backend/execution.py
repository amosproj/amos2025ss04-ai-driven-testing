import module_manager
from llm_manager import LLMManager


def execute_prompt(model, active_modules, prompt_text, output_file):
    """Execute the prompt-response flow."""

    # Read prompt

    model_id = model["id"]
    model_name = model["name"]

    # Prepare data structure
    prompt_data = {
        "model": {"id": model_id, "name": model_name},
        "prompt": prompt_text,
        "metadata": {},
    }

    # Process with modules
    prompt_data = module_manager.apply_before_modules(
        active_modules, prompt_data
    )

    # Initialize LLM manager
    manager = LLMManager()
    try:
        manager.start_model_container(prompt_data["model"]["id"])
        print(f"\n--- Response from {prompt_data['model']['name']} ---")

        # Send prompt
        raw_response, loading_time, final_time = manager.send_prompt(
            prompt_data["model"]["id"],
            prompt_data["prompt"],
            output_file,
        )

        # Create response data structure
        response_data = {
            "response": raw_response,
            "loading_time": loading_time,
            "final_time": final_time,
        }

        # Process with modules
        module_manager.apply_after_modules(
            active_modules, response_data, prompt_data
        )
        print("")
    finally:
        manager.stop_model_container(prompt_data["model"]["id"])
