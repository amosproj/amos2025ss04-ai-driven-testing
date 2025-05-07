import time
import json


# Measure the generation time of the model output
def measure_generation_time(client, model_name, prompt):
    start_time = time.time()
    response = client.generate(model=model_name, prompt=prompt)
    end_time = time.time()
    return response.response, end_time - start_time


# Check if generated code is syntactically valid
def check_syntax_validity(file_path):
    try:
        with open(file_path, "r") as f:
            code = f.read()
        compile(code, str(file_path), "exec")
        return True
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return False


# Save metrics into a JSON file
def save_metrics(metrics, file_name="metrics.json"):
    with open(file_name, "w") as f:
        json.dump(metrics, f, indent=4)


# Clean the generated response form markdown and explanations
def clean_response_text(response_text):
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
