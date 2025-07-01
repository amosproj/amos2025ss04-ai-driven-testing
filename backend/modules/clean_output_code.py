import subprocess
import tempfile
import os
from pathlib import Path
import warnings
import json
import ast
from modules.text_converter import TextConverter
from modules.execute_tests import ExecuteTests
from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class CleanOutputCode(ModuleBase):
    """Module that ensures outputted test code runs without errors by fixing common issues and using LLM for complex fixes."""

    postprocessing_order = (
        95  # Run after ExecuteTests (90) to use its execution results
    )

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return [TextConverter, ExecuteTests]

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:

        # Get paths for prompt and response files
        prompt_path = Path(prompt_data.prompt_code_path)
        response_path = Path(response_data.output.output_code_path)

        # Check if there are errors that need fixing based on ExecuteTests results
        needs_fixing = self._check_if_needs_fixing(prompt_data, response_data)

        if not needs_fixing:
            print(
                "[CleanOutputCode] Code executed successfully, no fixes needed"
            )
            return response_data

        print("[CleanOutputCode] Errors detected, applying fixes...")
        success = self._restart_with_llm_fix(
            prompt_path, response_path, prompt_data, response_data
        )
        return response_data

    def _restart_with_llm_fix(
        self,
        prompt_path: Path,
        response_path: Path,
        prompt_data: PromptData,
        response_data: ResponseData,
    ) -> bool:
        """Restart the main.py process with LLM fix prompt, with iterative fixing."""
        max_llm_attempts = 5  # Maximum number of LLM fix attempts
        response_data_path = (
            Path(__file__).parent.parent
            / "outputs"
            / "latest"
            / "response.json"
        )

        try:
            # Read the original prompt code (this stays constant)
            with open(prompt_path, "r") as f:
                prompt_code = f.read()

            # Start with the current test code
            current_test_code = None
            with open(response_path, "r") as f:
                current_test_code = f.read()

            for attempt in range(1, max_llm_attempts + 1):
                print(
                    f"[CleanOutputCode] LLM fix attempt {attempt}/{max_llm_attempts}"
                )

                # Create fix prompt for current test code
                fix_prompt = self._create_fixing_prompt(
                    prompt_code, current_test_code, prompt_data, response_data
                )

                # Create temporary files for this attempt
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False
                ) as source_file:
                    source_file.write(fix_prompt)
                    temp_source_path = source_file.name

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False
                ) as user_msg_file:
                    user_msg_file.write(
                        ""
                    )  # Empty user message for fix prompt
                    temp_user_msg_path = user_msg_file.name

                # Create output file for this attempt
                output_file = (
                    response_path.parent / f"fixed_attempt_{attempt}.md"
                )

                # Prepare command WITHOUT clean_output_code module
                cmd = [
                    "python3",
                    str(Path(__file__).parent.parent / "main.py"),
                    "--model",
                    str(6),  # Using model 6 (qwen3)
                    "--prompt_file",
                    temp_user_msg_path,
                    "--source_code",
                    temp_source_path,
                    "--modules",
                    "text_converter",
                    "execute_tests",
                    "--output_file",
                    str(output_file),
                ]

                print(
                    f"[CleanOutputCode] Running fix attempt {attempt}: {' '.join(cmd)}"
                )
                print("=" * 60)

                # Run the subprocess with streaming output
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=Path(__file__).parent.parent,
                )

                # Stream output line by line
                try:
                    for line in process.stdout:
                        print(line.rstrip())

                    # Wait for process to complete
                    process.wait(timeout=100)

                except subprocess.TimeoutExpired:
                    process.kill()
                    print(
                        f"[CleanOutputCode] Attempt {attempt} timed out after 5 minutes"
                    )

                print("=" * 60)

                # Clean up temporary files for this attempt
                os.unlink(temp_user_msg_path)
                os.unlink(temp_source_path)

                # Load the JSON file and create ResponseData from the dictionary
                try:
                    with open(response_data_path, "r") as f:
                        response_data_dict = json.load(f)
                    response_data = ResponseData(**response_data_dict)

                    if (
                        response_data.output.test_execution_results.exit_code
                        == 0
                    ):
                        print(f"[CleanOutputCode] Attempt {attempt} succeeded")
                        # If the fix was successful, we can stop here
                        break
                    else:
                        print(
                            f"[CleanOutputCode] Attempt {attempt} failed, retrying..."
                        )
                        response_path = Path(
                            response_data.output.output_code_path
                        )
                        with open(response_path, "r") as f:
                            current_test_code = f.read()
                except Exception as e:
                    raise RuntimeError(
                        f"[CleanOutputCode] Failed to load response data: {e}"
                    ) from e

            print(f"[CleanOutputCode] Completed {attempt} LLM fix attempts")
            if attempt == max_llm_attempts:
                print(
                    "[CleanOutputCode] Maximum LLM fix attempts reached, please check the output manually"
                )
                return False
            return True

        except Exception as e:
            print(f"[CleanOutputCode] Error during LLM fix restart: {e}")
            return False

    def _create_fixing_prompt(
        self, prompt_code: str, test_code: str, prompt_data: PromptData, response_data: ResponseData
    ) -> str:
        """Create a prompt for the LLM to fix the code."""
        execution_error_info = self._extract_error_info_from_execution(
            response_data
        )
        analysis_error_info = self.extract_analysis_error_info(prompt_data, response_data)

        # Start building the prompt
        prompt = "I have a Python test file that's failing to execute. Please fix the errors and return the corrected code.\n\n"
        prompt += (
            "**Original code under test (prompt.py):**\n```python\n"
            + prompt_code
            + "\n```\n\n"
        )
        prompt += (
            "**Current test code that has errors:**\n```python\n"
            + test_code
            + "\n```\n"
        )

        # Only include execution error info if it exists
        if execution_error_info is not None and execution_error_info.strip():
            prompt += (
                "\n**Error information that occured during execution:**\n"
                + execution_error_info
                + "\n"
            )

        # Only include analysis error info if it exists
        if analysis_error_info is not None and analysis_error_info.strip():
            prompt += (
                "\n**Analysis error information:**\n"
                + analysis_error_info
                + "\n"
            )

        # Add instructions
        prompt += """
            **Instructions:**
            1. Fix all syntax errors, import errors, and runtime errors
            2. Ensure the test code properly imports from prompt.py
            3. Make sure all test methods are properly structured
            4. Return ONLY the corrected Python code for the test file
            5. Do not include explanations or markdown formatting
            6. Ensure the code follows unittest conventions

            Return the fixed test code:
            """

        return prompt

    def _check_if_needs_fixing(self, prompt_data: PromptData, response_data: ResponseData) -> bool:
        # Check for execution errors
        execution_errors = self._extract_error_info_from_execution(response_data) is not None
        
        # Check for analysis errors
        analysis_errors = self.extract_analysis_error_info(prompt_data, response_data) is not None
        if analysis_errors:
            print("[CleanOutputCode] Analysis errors detected, needs fixing")
        
        return execution_errors or analysis_errors

    def extract_analysis_error_info(self, prompt_data: PromptData, response_data: ResponseData) -> str:
        """Extract simple error information from response_data
        for use in UI and LLM fixing."""
        try:
            # Get the original prompt code
            prompt_path = Path(prompt_data.prompt_code_path)
            response_path = Path(response_data.output.output_code_path)
                
            # Read both files
            with open(prompt_path, 'r') as f:
                prompt_code = f.read()
                
            with open(response_path, 'r') as f:
                test_code = f.read()
                
            # Initialize error collection
            errors = []
            
            # Check 1: Is the test code just a copy of the prompt?
            if self._is_similar(test_code, prompt_code, threshold=0.7):
                errors.append("The generated test code appears to be mostly a copy of the source code. Please generate proper test cases instead of copying the original code.")
            
            # Check 2: Were methods from the prompt copied into the test?
            prompt_methods = self._extract_method_signatures(prompt_code)
            test_methods = self._extract_method_signatures(test_code)
            
            # Find method signatures that appear in both
            copied_methods = [method for method in prompt_methods if method in test_methods]
            if copied_methods:
                methods_list = ", ".join(f'"{m}"' for m in copied_methods[:3])
                if len(copied_methods) > 3:
                    methods_list += f", and {len(copied_methods) - 3} more"
                errors.append(f"The test code contains {len(copied_methods)} method signatures copied directly from the source code: {methods_list}. Test methods should have unique names, typically starting with 'test_'.")
            
            # Check 3: Empty or placeholder tests
            if "def test_" in test_code.lower():
                # There are test methods, but check if they're empty
                if self._has_empty_test_methods(test_code):
                    errors.append("The test code contains empty or placeholder test methods. Each test method should include proper test logic and assertions.")
            else:
                # No test methods at all
                if "unittest" in test_code.lower() or "class Test" in test_code:
                    errors.append("The test code defines a test class but doesn't contain any test methods (methods starting with 'test_').")

            # Format and return the errors
            if errors:
                return "The following issues were detected in the generated test code:\n- " + "\n- ".join(errors)
            
            return None
            
        except Exception as e:
            warnings.warn(f"[CleanOutputCode] Error in extract_analysis_error_info: {e}")
            return None

    def _extract_error_info_from_execution(
        self, response_data: ResponseData
    ) -> str:
        """Extract error information from response_data."""
        error_parts = []

        if (
            hasattr(response_data.output, "test_execution_results")
            and response_data.output.test_execution_results
        ):
            exec_results = response_data.output.test_execution_results
            if exec_results.exit_code != 0:
                error_parts.append(
                    f"Execution failed with exit code: {exec_results.exit_code}"
                )
                if exec_results.stderr:
                    error_parts.append(f"Stderr: {exec_results.stderr}")
                if exec_results.stdout:
                    error_parts.append(f"Stdout: {exec_results.stdout}")
            else:
                return None
        else:
            warnings.warn(
                "test execution information not found in response_data.output.test_execution_results"
            )

        return "\n".join(error_parts)

    def _is_similar(self, content: str, reference: str, threshold: float = 0.7) -> bool:
        """Check if the content is too similar to the reference code.
        
        Args:
            content: The content to check
            reference: The reference content to compare against
            threshold: The similarity threshold (default 0.7)
            
        Returns:
            True if content is similar to reference beyond the threshold
        """
        # Simple similarity check: If more than threshold % of lines match
        content_lines = set(line.strip() for line in content.split("\n") if line.strip())
        reference_lines = set(line.strip() for line in reference.split("\n") if line.strip())
        
        if not content_lines or not reference_lines:
            return False
            
        # If the content is very short, it's probably not a valid test
        if len(content_lines) < 5:
            return True
            
        # Count matching lines
        matching_lines = content_lines.intersection(reference_lines)
        similarity = len(matching_lines) / max(len(content_lines), len(reference_lines))
        
        return similarity > threshold
    
    def _extract_method_signatures(self, code: str) -> list[str]:
        """Extract method signatures from code."""
        method_signatures = []
        lines = code.split("\n")
        
        for line in lines:
            line = line.strip()
            # Look for method definitions
            if line.startswith("def "):
                # Extract method name
                if "(" in line:
                    method_name = line[4:line.find("(")].strip()
                    method_signatures.append(method_name)
                    
        return method_signatures
        
    def _has_empty_test_methods(self, code: str) -> bool:
        """Check if the code has empty methods."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            print("Invalid Python code.")
            return False

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check if the function has an empty body or only contains pass or Ellipsis
                if not node.body:
                    return True
                if len(node.body) == 1 and isinstance(node.body[0], (ast.Pass, ast.Expr)) and (
                    isinstance(node.body[0], ast.Pass) or
                    (isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant))
                ):
                    return True
        return False
