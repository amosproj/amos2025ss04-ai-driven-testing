import os
import subprocess
import shutil
import sys

def main():
    # Read arguments from args_test_llm_all_tests.txt
    if len(sys.argv) == 1:
        args_file = "args_test_llm_all_tests.txt"
        if os.path.exists(args_file):
            with open(args_file, "r") as f:
                args = f.read().strip().split()
            sys.argv = [sys.argv[0]] + args

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python test_llm_all_tests.py <llm_name> [source_dir]")
        sys.exit(1)

    llm_name = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Update source_dir and output_dir to be relative to the parent directory of the script's directory
    parent_dir = os.path.dirname(script_dir)
    source_dir = os.path.join(parent_dir, sys.argv[2]) if len(sys.argv) == 3 else os.path.join(parent_dir, "pythonTestPrograms/correct_python_programs")
    output_dir = os.path.join(parent_dir, f"{llm_name}_unit_tests_for_{os.path.basename(source_dir)}")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each Python file in the source directory
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".py"):
            prompt_file = os.path.join(source_dir, file_name)
            output_file = os.path.join(output_dir, f"test_{file_name}")

            # Create a temporary file for the prompt
            with open(prompt_file, "r") as original_prompt:
                prompt_content = original_prompt.read()

            additional_prompt = "\n# Please generate a test class with unit tests for the above code using unittest. Return a python file containing the original code plus the test so that I just need to run the resulting file and i can see if the tests go through\n"
            temp_prompt_file = os.path.join(output_dir, f"temp_{file_name}")
            with open(temp_prompt_file, "w") as temp_file:
                temp_file.write(prompt_content + additional_prompt)

            # Update the prompt_file to use the temporary file
            prompt_file = temp_prompt_file
            main_script = os.path.join(script_dir, "main.py")

            try:
                result = subprocess.run(
                    ["python3.11", main_script, "--llm_name", llm_name, "--prompt_file", prompt_file, "--output_file", output_file],
                    text=True,
                    check=True
                )

                # Postprocess the output to make it runnable
                processed_output = postprocess_output(output_file)

                # Save the processed output to the new folder
                with open(output_file, "w") as f:
                    f.write(processed_output)

                print(f"Generated unit test for {file_name} -> {output_file}")

            except subprocess.CalledProcessError as e:
                print(f"Error generating unit test for {file_name}: {e.stderr}")
            finally:
                if os.path.exists(temp_prompt_file):
                    os.remove(temp_prompt_file)


def postprocess_output(output_file):
    #read the output file
    with open(output_file, "r") as f:
        output = f.read()
    #only capture the part after the first '```python' and before the last '```'
    start_index = output.find('```python')
    end_index = output.rfind('```')
    if start_index != -1 and end_index != -1:
        output = output[start_index + len('```python'):end_index].strip()
    else:
        print("Error: Could not find the code block in the output. {output} \n\n {llm_name} \n\n {source_dir}")
        return ""
    return output

if __name__ == "__main__":
    main()