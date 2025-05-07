import subprocess

# Run the generated test script and capture its output
def run_test_script(test_script_path):
    try:
        result = subprocess.run(
            ["python", str(test_script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr
    except subprocess.TimeoutExpired:
        success = False
        output = "Test execution timed out."
    return success, output
