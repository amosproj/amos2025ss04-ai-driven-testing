"""Code analysis bot for automated unit test generation.

This module uses the Qwen model via Ollama to analyze Python code and generate
appropriate unit tests. It measures performance metrics like generation time
and validates that the generated tests have valid syntax and can be executed.
The results are saved to a metrics file for further analysis.
It also monitors Docker container performance.
"""

import time
import json
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
from performance_monitor import PerformanceMonitor

# Initialize performance monitor
monitor = PerformanceMonitor()

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

# Collect baseline performance snapshot before test
baseline = monitor.capture_performance_snapshot()

# Generate test code and measure time
generated_response, generation_time = measure_generation_time(
    client, model_name, prompt
)

# Collect performance snapshot after test
post_execution = monitor.capture_performance_snapshot()

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
    "Performance": {
        "system_before": baseline["system"],
        "system_after": post_execution["system"],
        "containers_before": baseline["containers"],
        "containers_after": post_execution["containers"],
        "cpu_delta": post_execution["system"]["cpu_percent"] - baseline["system"]["cpu_percent"],
        "memory_delta_gb": round(post_execution["system"]["memory_used_gb"] - baseline["system"]["memory_used_gb"], 2),
    }
}
save_metrics(metrics)

# Save performance metrics separately for analysis
performance_data = {
    "timestamp": time.time(),
    "model": model_name,
    "system_metrics": {
        "before": baseline["system"],
        "after": post_execution["system"],
    },
    "container_metrics": {
        "before": baseline["containers"],
        "after": post_execution["containers"],
    }
}
monitor.save_performance_metrics(performance_data, "docker_performance.json")

print("Metrics saved in metrics.json!")
print("Docker performance metrics saved in docker_performance.json!")
