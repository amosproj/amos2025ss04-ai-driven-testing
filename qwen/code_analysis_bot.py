# === codeAnalysisBot.py ===

import ollama
from pathlib import Path
from specifications import model_name, code_path
from metrics import measure_generation_time, check_syntax_validity, save_metrics, clean_response_text
from run_tests import run_test_script

# Initialize Ollama client
client = ollama.Client()

# Read source code file
with open(code_path, 'r') as file:
    file_content = file.read()

# Create a meaningful prompt
prompt = (
    "Analyze the following Python code and generate unit tests using Python's unittest framework.\n"
    "Ensure the tests cover all functionalities in the code.\n\n"
    f"{file_content}"
)

# Generate test code and measure time
generated_response, generation_time = measure_generation_time(client, model_name, prompt)

# Save the raw response to a text file
with open('response.txt', 'w', encoding='utf-8') as file:
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
    "Test Output": test_output
}
save_metrics(metrics)

print("Metrics saved in metrics.json!")
