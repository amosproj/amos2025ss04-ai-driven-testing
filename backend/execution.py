"""Execution module for processing prompts and managing LLM interactions."""
import module_manager
from llm_manager import LLMManager
from export_manager import ExportManager
from schemas import PromptData, ModelMeta, InputData, InputOptions
from datetime import datetime
import json
from pathlib import Path


def execute_prompt(
    model,
    active_modules,
    prompt_text,
    output_file,
    export_format="markdown",
    export_all=False,
):
    """Execute the prompt-response flow."""
    # Read prompt

    model_id = model["id"]
    model_name = model["name"]

    prompt_data = PromptData(
        model=ModelMeta(id=model_id, name=model_name),
        input=InputData(
            user_message="Was macht dieser Code?",
            source_code=prompt_text,
            system_message="You are a helpful assistant. Provide your answer always in Markdown.\n"
            "Format code blocks appropriately, and do not include text outside valid Markdown.",
            options=InputOptions(num_ctx=4096),
        ),
    )

    # Process with modules
    prompt_data = module_manager.apply_before_modules(
        active_modules, prompt_data
    )

    # Initialize LLM manager
    manager = LLMManager()
    try:
        manager.start_model_container(prompt_data.model.id)
        print(f"\n--- Response from {prompt_data.model.name} ---")

        response_data = manager.send_prompt(prompt_data)

        # Process with modules
        module_manager.apply_after_modules(
            active_modules, response_data, prompt_data
        )

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

        # Write output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response_data.output.markdown)

        # === Export functionality ===
        if export_format or export_all:
            export_manager = ExportManager()

            # Get the content to export (assuming response_data has a 'content' or 'response' field)
            export_content = getattr(
                response_data, "content", None
            ) or getattr(response_data, "response", str(response_data))

            if export_all:
                # Export in all formats
                print("Exporting in all formats...")
                export_files = export_manager.export_all_formats(
                    export_content,
                    base_filename=f"{timestamp}_{safe_model_id}",
                )
                for format_name, file_path in export_files.items():
                    print(f"  {format_name.upper()}: {file_path}")
            else:
                # Export in specified format
                print(f"Exporting in {export_format} format...")
                export_filename = (
                    f"{timestamp}_{safe_model_id}.{export_format}"
                )
                if export_format == "json":
                    export_filename = (
                        f"{timestamp}_{safe_model_id}_formatted.json"
                    )

                export_path = export_manager.export_content(
                    export_content, export_format, export_filename
                )
                print(f"  Exported to: {export_path}")

    finally:
        print("")
        manager.stop_model_container(prompt_data.model.id)


def execute_prompt_new(active_modules, prompt_data, output_file):
    """Execute the prompt-response flow (new version for API compatibility)."""
    # Process with modules
    prompt_data = module_manager.apply_before_modules(
        active_modules, prompt_data
    )

    # Initialize LLM manager
    manager = LLMManager()
    try:
        manager.start_model_container(prompt_data.model.id)
        print(f"\n--- Response from {prompt_data.model.name} ---")

        response_data = manager.send_prompt(prompt_data)

        # Process with modules
        module_manager.apply_after_modules(
            active_modules, response_data, prompt_data
        )

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
