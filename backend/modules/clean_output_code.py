import subprocess
import tempfile
import os
from pathlib import Path
import warnings
import json
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
        prompt_path = (
            Path(prompt_data.prompt_code_path)
            if prompt_data.prompt_code_path
            else None
        )
        response_path = (
            Path(response_data.output.output_code_path)
            if response_data.output.output_code_path
            else None
        )

        if not prompt_path or not response_path or not response_path.exists():
            warnings.warn(
                "[CleanOutputCode] Missing required file paths, skipping..."
            )
            return response_data

        # Check if there are errors that need fixing based on ExecuteTests results
        needs_fixing = self._check_if_needs_fixing(response_data)

        if not needs_fixing:
            print(
                "[CleanOutputCode] Code executed successfully, no fixes needed"
            )
            return response_data

        print("[CleanOutputCode] Execution errors detected, applying fixes...")

        # Apply manual fixes first
        print("[CleanOutputCode] Applying manual fixes...")
        self._apply_manual_fixes_to_file(response_path)

        # For now, always proceed with LLM fix if we detected errors
        # In a more sophisticated implementation, we could re-run ExecuteTests after manual fixes
        print(
            "[CleanOutputCode] Manual fixes applied, proceeding with LLM fix..."
        )
        success = self._restart_with_llm_fix(
            prompt_path, response_path, response_data
        )

        if success:
            print("[CleanOutputCode] LLM fix process initiated")
        else:
            print("[CleanOutputCode] Failed to initiate LLM fix process")

        return response_data

    def _restart_with_llm_fix(
        self,
        prompt_path: Path,
        response_path: Path,
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
                    prompt_code, current_test_code, response_data
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
            return True

        except Exception as e:
            print(f"[CleanOutputCode] Error during LLM fix restart: {e}")
            return False

    def _create_fixing_prompt(
        self, prompt_code: str, test_code: str, response_data: ResponseData
    ) -> str:
        """Create a prompt for the LLM to fix the code."""
        execution_error_info = self._extract_error_info_from_execution(response_data)
        analysis_error_info = self.extract_analysis_error_info(response_data)
        
        # Start building the prompt
        prompt = "I have a Python test file that's failing to execute. Please fix the errors and return the corrected code.\n\n"
        prompt += "**Original code under test (prompt.py):**\n```python\n" + prompt_code + "\n```\n\n"
        prompt += "**Current test code that has errors:**\n```python\n" + test_code + "\n```\n"
        
        # Only include execution error info if it exists
        if execution_error_info is not None and execution_error_info.strip():
            prompt += "\n**Error information that occured during execution:**\n" + execution_error_info + "\n"
            
        # Only include analysis error info if it exists
        if analysis_error_info is not None and analysis_error_info.strip():
            prompt += "\n**Analysis error information:**\n" + analysis_error_info + "\n"
        
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

        
    def _check_if_needs_fixing(self, response_data: ResponseData) -> bool:
        return self._extract_error_info_from_execution(response_data) is not None or response_data.output.test_execution_results is not None
    
    def extract_analysis_error_info(self, response_data: ResponseData) -> str:
        """Extract simple error information from response_data
        for use in UI."""
        

    def _extract_error_info_from_execution(self, response_data: ResponseData) -> str:
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
