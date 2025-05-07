"""Metrics utilities for AI test generation evaluation.

This module provides functions for measuring and evaluating the performance
of AI-generated unit tests. It includes utilities to measure generation time,
validate syntax, clean response text, and save metrics to a file for further
analysis.
"""

import time
import json


def measure_generation_time(client, model_name, prompt):
    """Measure the time taken by the model to generate a response.

    Records the start and end time of the generation process and calculates
    the elapsed time.

    Args:
        client: The Ollama client instance
        model_name: Name of the model to use for generation
        prompt: The prompt to send to the model

    Returns:
        tuple: (generated response text, elapsed time in seconds)
    """
    start_time = time.time()
    response = client.generate(model=model_name, prompt=prompt)
    end_time = time.time()
    return response.response, end_time - start_time


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
