import re
import json
import sys
from pathlib import Path
from typing import Optional, Union
import black


from modules.base import ModuleBase


class TextConverter(ModuleBase):

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        # Prefer model id, fallback to model name, then "output"
        model = (
            response_data.get("model") or prompt_data.get("model") or "output"
        )
        if isinstance(model, dict):
            model_id = model.get("id", "output")
        else:
            model_id = str(model)
        safe_model_id = model_id.replace(":", "_")
        output_filename = f"{safe_model_id}.py"
        # Change output_dir to backend/extracted
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

        # get responce from response_data
        code_content = (
            response_data.get("text")
            or response_data.get("code")
            or response_data.get("response")
            or ""
        )
        write_cleaned_python_code_to_file(code_content, output_path)
        return response_data


def clean_response_text(response_text: str) -> str:
    """
    Extracts and cleans all Python code blocks from the input text,
    removing markdown code block markers and trailing explanations.
    Concatenates all code blocks into a single string.
    Formats the result using Black.
    """
    if not response_text or not response_text.strip():
        return "no responce"

    # Find all code blocks marked with ```python ... ```
    code_blocks = re.findall(
        r"```python(.*?)```", response_text, flags=re.DOTALL | re.IGNORECASE
    )

    # If no python code blocks found, try generic code blocks
    if not code_blocks:
        code_blocks = re.findall(
            r"```(.*?)```", response_text, flags=re.DOTALL | re.IGNORECASE
        )

    # If still no code blocks, treat the whole text as a single block
    if not code_blocks:
        code_blocks = [response_text]

    cleaned_blocks = []
    for block in code_blocks:
        # Remove leading/trailing whitespace and empty lines
        cleaned_block = "\n".join(
            line.rstrip()
            for line in block.strip().splitlines()
            if line.strip()
        )
        cleaned_blocks.append(cleaned_block)

    code = "\n\n".join(filter(None, cleaned_blocks))

    # Format the code using Black
    try:
        formatted_code = black.format_str(code, mode=black.Mode())
    except Exception:
        formatted_code = code  # Fallback to unformatted if Black fails

    return formatted_code


def convert_to_python_file(
    input_path: Union[str, Path],
    destination: Optional[Union[str, Path]] = None,
) -> Path:
    """
    Converts a JSON or Markdown file to a Python file and saves it in the destination directory.
    If destination is not provided, saves to /backend/extracted with the same name as the input file.
    Returns the path to the generated Python file.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix == ".json":
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        code = clean_response_text(data.get("code", ""))
    elif input_path.suffix in [".md", ".markdown"]:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        code = clean_response_text(text)
    else:
        raise ValueError(f"Unsupported file type: {input_path.suffix}")

    output_filename = input_path.stem + ".py"
    if destination is not None:
        output_path = Path(destination) / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return write_cleaned_python_code_to_file(code, output_path.name)
    else:
        # Change default output directory to backend/extracted
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename
        return write_cleaned_python_code_to_file(code, output_path)


def write_cleaned_python_code_to_file(
    text: str, destination_path: Path
) -> Path:
    """
    Cleans the input text to extract Python code blocks and writes the result
    to the specified destination_path. Returns the path to the generated file.
    """
    code = clean_response_text(text)
    # Ensure the parent directory exists
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(code)
    return destination_path
