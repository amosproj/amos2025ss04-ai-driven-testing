import re
import subprocess
import shutil
import tempfile
import os
from pathlib import Path
from typing import Dict, Any
import warnings

from modules.metrics_collector import MetricsCollector
from modules.text_converter import TextConverter
from modules.execute_tests import ExecuteTests
from modules.base import ModuleBase
from schemas import PromptData, ResponseData, TestExecutionResults


class CleanOutputCode(ModuleBase):
    """Module that ensures outputted test code runs without errors by fixing common issues and using LLM for complex fixes."""

    postprocessing_order = (
        95  # Run after ExecuteTests (99) to use its execution results
    )

    def __init__(self):
        self.max_fix_attempts = 3

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
            warnings.warn("[CleanOutputCode] Missing required file paths, skipping...")
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

    def _apply_manual_fixes_to_file(self, file_path: Path) -> None:
        # TODO!
        """Apply manual fixes directly to the file."""
        with open(file_path, "r") as f:
            content = f.read()

        #fixed_content = self._apply_manual_fixes(content)

        #with open(file_path, "w") as f:
        #    f.write(fixed_content)

    def _restart_with_llm_fix(
        self,
        prompt_path: Path,
        response_path: Path,
        response_data: ResponseData
    ) -> bool:
        """Restart the main.py process with LLM fix prompt."""
        try:
            # Read current files
            with open(response_path, "r") as f:
                test_code = f.read()

            with open(prompt_path, "r") as f:
                prompt_code = f.read()

            # Create fix prompt
            fix_prompt = self._create_fixing_prompt(
                prompt_code, test_code, response_data
            )

            # Create temporary files for the new run
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as source_file:
                source_file.write(fix_prompt)
                temp_source_path = source_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as user_msg_file:
                user_msg_file.write("")  # Empty source code for fix prompt
                temp_user_msg_path = user_msg_file.name

            # Prepare command to restart main.py with qwen3 model
            cmd = [
                "python3",
                str(Path(__file__).parent.parent / "main.py"),
                "--model",
                str(6),
                "--prompt_file",
                temp_user_msg_path,
                "--source_code",
                temp_source_path,
                "--modules",
                "text_converter",
                "execute_tests",
                "clean_output_code",
            ]

            print(
                f"[CleanOutputCode] Restarting main.py with command: {' '.join(cmd)}"
            )
            print("[CleanOutputCode] LLM fix subprocess output (streaming):")
            print("=" * 60)

            # Run the subprocess with streaming output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout for simpler streaming
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True,
                cwd=Path(__file__).parent.parent,
            )

            # Stream output line by line
            try:
                for line in process.stdout:
                    print(
                        line.rstrip()
                    )  # Print each line as it comes, removing trailing newline

                # Wait for process to complete
                return_code = process.wait(timeout=300)  # 5 minute timeout

            except subprocess.TimeoutExpired:
                process.kill()
                print("[CleanOutputCode] Process timed out after 5 minutes")
                return_code = -1

            print("=" * 60)
            print(f"[CleanOutputCode] Process exit code: {return_code}")

            # Clean up temporary files
            os.unlink(temp_user_msg_path)
            os.unlink(temp_source_path)

            if return_code == 0:
                print(
                    "[CleanOutputCode] LLM fix subprocess completed successfully"
                )
                return True
            else:
                print(
                    f"[CleanOutputCode] LLM fix subprocess failed with exit code {return_code}"
                )
                return False

        except Exception as e:
            print(f"[CleanOutputCode] Error during LLM fix restart: {e}")
            return False

    def _create_fixing_prompt(
        self, prompt_code: str, test_code: str, response_data: ResponseData
    ) -> str:
        """Create a prompt for the LLM to fix the code."""
        error_info = self._extract_error_info(response_data)

        return f"""
            I have a Python test file that's failing to execute. Please fix the errors and return the corrected code.

            **Original code under test (prompt.py):**
            ```python
            {prompt_code}
            ```

            **Current test code that has errors:**
            ```python
            {test_code}
            ```

            **Error information:**
            {error_info}

            **Instructions:**
            1. Fix all syntax errors, import errors, and runtime errors
            2. Ensure the test code properly imports from prompt.py
            3. Make sure all test methods are properly structured
            4. Return ONLY the corrected Python code for the test file
            5. Do not include explanations or markdown formatting
            6. Ensure the code follows unittest conventions

            Return the fixed test code:
            """

    def _check_if_needs_fixing(self, response_data: ResponseData) -> bool:
        return self._extract_error_info(response_data) is not None

    def _extract_error_info(self, response_data: ResponseData) -> str:
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
            warnings.warn("test execution information not found in response_data.output.test_execution_results")

        return "\n".join(error_parts)
