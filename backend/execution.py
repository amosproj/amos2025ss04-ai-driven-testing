"""
This module orchestrates the prompt execution flow.

It handles the logic for sending prompts to the LLM, managing
iterative refinement passes, and saving the final results.
"""
import json
from datetime import datetime
from pathlib import Path

import module_manager
from llm_manager import LLMManager


def execute_prompt(active_modules, prompt_data, output_file, iterations=1):
    """Execute the prompt-response flow, with optional iterations."""
    manager = LLMManager()
    try:
        manager.start_model_container(prompt_data.model.id)

        # This will hold the latest response data
        response_data = None

        for i in range(iterations):
            print(f"--- Starting Iteration {i + 1}/{iterations} ---")

            # On the first iteration, the prompt_data is used as is.
            # On subsequent iterations, the prompt_data will have been modified.

            # 1. Process with "before" modules
            current_prompt_data = module_manager.apply_before_modules(
                active_modules, prompt_data
            )

            # 2. Send the prompt to the LLM
            print(
                f"\n--- Response from {current_prompt_data.model.name} (Pass {i+1}) ---"
            )
            response_data = manager.send_prompt(current_prompt_data)

            # 3. Process with "after" modules
            response_data = module_manager.apply_after_modules(
                active_modules, response_data, current_prompt_data
            )

            # 4. Prepare for the next iteration (if it's not the last one)
            if i < iterations - 1:
                print("\n--- Preparing for next iteration ---")
                # The output of this pass becomes the input for the next pass.
                # The 'text_converter' module should have populated the 'code' field.
                new_source_code = (
                    response_data.output.code or response_data.output.markdown
                )

                # Update the prompt_data for the next loop
                prompt_data.input.source_code = new_source_code
                prompt_data.input.user_message = (
                    "Please review the following Python code that was generated. "
                    "If you find any errors, fix them. If there are no errors, "
                    "improve the code by adding comments, docstrings, or improving clarity. "
                    "Return only the complete, corrected, and improved Python code in a single markdown block."
                )
                # Clear any RAG-specific fields to avoid re-injecting old context
                prompt_data.rag_prompt = None
                prompt_data.rag_sources = None

        # After all iterations, save the final result
        if response_data:
            # The saving logic from your original execute_prompt function
            # can be called here on the final `response_data`.
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            safe_model_id = prompt_data.model.id.replace(":", "_")
            archive_dir = (
                Path("outputs/archive") / f"{timestamp}_{safe_model_id}"
            )
            latest_dir = Path("outputs/latest")

            archive_dir.mkdir(parents=True, exist_ok=True)
            latest_dir.mkdir(parents=True, exist_ok=True)

            # Save final response.json and markdown output
            response_json = response_data.dict()
            for path in [
                archive_dir / "response.json",
                latest_dir / "response.json",
            ]:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(response_json, f, indent=2)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response_data.output.markdown)

            print(f"\n--- Final output saved to {output_file} ---")

    finally:
        print("")
        manager.stop_model_container(prompt_data.model.id)
