"""Script for batch execution of test creation across multiple LLM models.

This module reads a list of language models from a configuration file and
sequentially runs the test generation process for each model, providing
a convenient way to evaluate and compare different models' test outputs.
"""

import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
test_script = os.path.join(script_dir, "test_llm_all_tests.py")

llm_list_file = "llm_list.txt"

with open(llm_list_file, "r") as file:
    llm_models = [line.strip() for line in file if line.strip()]

for model in llm_models:
    print(f"Running tests for model: {model}")
    subprocess.run(["python3.11", test_script, model], check=True)

print("All tests completed.")
