"""
Execute the prompt-response flow, with optional iterations for refinement.

This module handles the main execution logic, including starting the LLM
container, running the prompt through the model for one or more iterations,
and saving the final output.
"""

import module_manager
from llm_manager import LLMManager
from datetime import datetime
import json
from pathlib import Path


def execute_prompt(active_modules, prompt_data, output_file, iterations=1):
    """Execute the prompt-response flow, with optional iterations for refinement."""
    # Process with modules
    prompt_data = module_manager.apply_before_modules(
        active_modules, prompt_data
    )

    # Initialize LLM manager
    manager = LLMManager()
    try:
        manager.start_model_container(prompt_data.model.id)

        for i in range(iterations):
            print(f"\n--- Iteration {i + 1}/{iterations} ---")
            print(f"--- Response from {prompt_data.model.name} ---")

            response_data = manager.send_prompt(prompt_data)

            # Process with modules
            module_manager.apply_after_modules(
                active_modules, response_data, prompt_data
            )

            # Prepare for the next iteration
            if i < iterations - 1:
                new_source_code = (
                    response_data.output.code or response_data.output.markdown
                )
                prompt_data.input.source_code = new_source_code
                prompt_data.input.user_message = "Please review the following code. Fix any errors and improve it by adding comments and docstrings. Return only the complete, corrected Python code in a single markdown block."
                prompt_data.rag_prompt = None
                prompt_data.rag_sources = None

        # === Save output after all modules ===
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        safe_model_id = prompt_data.model.id.replace(":", "_")
        archive_dir = Path("outputs/archive") / f"{timestamp}_{safe_model_id}"
        latest_dir = Path("outputs/latest")

        archive_dir.mkdir(parents=True, exist_ok=True)
        latest_dir.mkdir(parents=True, exist_ok=True)

        # Save response.json
        response_json = response_data.dict()
        for path in [
            archive_dir / "response.json",
            latest_dir / "response.json",
        ]:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(response_json, f, indent=2)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response_data.output.markdown)
    finally:
        print("")
        manager.stop_model_container(prompt_data.model.id)
