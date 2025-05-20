import json
from pathlib import Path


def clean_response_text(response_text):
    """Clean the AI-generated response text from markdown and explanations.

    Processes the raw response from the AI model to extract only the valid
    Python code by removing markdown formatting, code fences, and explanatory
    text that might follow the generated code.

    Args:
        response_text: The raw text response from the AI model

    Returns:
        str: Cleaned Python code ready for execution
    """
    # Find the first occurrence of 'import' and keep everything from there
    import_index = response_text.find("import")
    if import_index != -1:
        response_text = response_text[import_index:]

    # Remove all markdown code fences like ```python or ```
    response_text = response_text.replace("```python", "")
    response_text = response_text.replace("```", "")

    # Optional: If there's any explanation text after the code, cut it
    explanation_markers = [
        "Explanation:",
        "# Explanation",
        "This script defines",
    ]
    for marker in explanation_markers:
        if marker in response_text:
            response_text = response_text.split(marker)[0]

    return response_text.strip()


def check_syntax_validity(file_path):
    """Check if a Python file contains syntactically valid code.

    Attempts to compile the Python code to check for syntax errors
    without executing it.

    Args:
        file_path: Path to the Python file to check

    Returns:
        bool: True if the syntax is valid, False otherwise
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()
        compile(code, str(file_path), "exec")
        print("ran")
        return True
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return False


def save_metrics(metrics, file_name="metrics.json"):
    """Save performance metrics to a JSON file.

    Writes the provided metrics dictionary to a JSON file with formatting
    for improved readability.

    Args:
        metrics: Dictionary containing the metrics to save
        file_name: Name of the file to write to (default: "metrics.json")
    """
    with open(file_name, "w") as f:
        json.dump(metrics, f, indent=4)


def evaluate_and_save_metrics(response_data, model_name):
    # Save generated response to a file
    output_path = Path("generated_test.py")
    cleaned_response = clean_response_text(response_data["response"])
    with open(output_path, "w") as f:
        f.write(cleaned_response)
    syntax_valid = check_syntax_validity(output_path)

    metrics = {
        "Model": model_name,
        "Generation Time (s)": round(response_data["loading_time"], 2),
        "Loading Time (s)": round(response_data["final_time"], 2),
        "Syntax Valid": syntax_valid,
    }
    save_metrics(metrics)
