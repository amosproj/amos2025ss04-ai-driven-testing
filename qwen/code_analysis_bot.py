"""Code analysis bot for automated unit test generation.

This module uses the Qwen model via Ollama to analyze Python code and generate
appropriate unit tests. It measures performance metrics like generation time
and validates that the generated tests have valid syntax and can be executed.
The results are saved to a metrics file for further analysis.
"""

from pathlib import Path

import ollama
from metrics import (
    check_syntax_validity,
    clean_response_text,
    measure_generation_time,
    save_metrics,
)
from run_tests import run_test_script
from specifications import code_path, model_name

# Initialize Ollama client
client = ollama.Client()

# Read source code file
with open(code_path, "r") as file:
    file_content = file.read()

# Create a meaningful prompt
prompt = (
    "Analyze the following Python code and generate unit tests using Python's unittest framework.\n"
    "Ensure the tests cover all functionalities in the code.\n\n"
    f"{file_content}"
)

# Generate test code and measure time
generated_response, generation_time = measure_generation_time(
    client, model_name, prompt
)

# Save the raw response to a text file
with open("response.txt", "w", encoding="utf-8") as file:
    file.write(generated_response)

# Save generated response to a file
output_path = Path("generated_test.py")
cleaned_response = clean_response_text(generated_response)
with open(output_path, "w") as f:
    f.write(cleaned_response)

# Validate syntax
syntax_valid = check_syntax_validity(output_path)

# Run tests and capture results
test_executed_successfully, test_output = run_test_script(output_path)

# Save all metrics
metrics = {
    "Model": model_name,
    "Generation Time (s)": round(generation_time, 2),
    "Syntax Valid": syntax_valid,
    "Test Executable": test_executed_successfully,
    "Test Output": test_output,
}
save_metrics(metrics)

print("Metrics saved in metrics.json!")
