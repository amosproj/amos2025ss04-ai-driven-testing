import re
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any

from modules.metrics_collector import MetricsCollector
from modules.text_converter import TextConverter
from modules.base import ModuleBase
from schemas import PromptData, ResponseData, TestExecutionResults
from llm_manager import LLMManager


class CleanOutputCode(ModuleBase):
    """Module that ensures outputted test code runs without errors by fixing common issues and using LLM for complex fixes."""

    postprocessing_order = 50  # Run after TextConverter (1) and before ExecuteTests (99)

    def __init__(self):
        self.max_fix_attempts = 3

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return [TextConverter, MetricsCollector]

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        # Get paths for prompt and response files
        prompt_path = Path(prompt_data.prompt_code_path) if prompt_data.prompt_code_path else None
        response_path = Path(response_data.output.output_code_path) if response_data.output.output_code_path else None
        
        if not prompt_path or not response_path or not response_path.exists():
            print("[CleanOutputCode] Missing required file paths, skipping...")
            return response_data

        # Create working directory for this test
        work_dir = self._create_work_directory(prompt_path, response_path)
        work_prompt_path = work_dir / "prompt.py"
        work_response_path = work_dir / "test_code.py"

        # Try to execute and fix the code
        success = self._execute_and_fix_code(work_response_path, work_prompt_path, prompt_data.model)
        
        if success:
            # Update response_data with the fixed code
            with open(work_response_path, 'r') as f:
                fixed_code = f.read()
            response_data.output.code = fixed_code
            response_data.output.output_code_path = str(work_response_path)
            print("[CleanOutputCode] Successfully fixed and validated test code")
        else:
            print("[CleanOutputCode] Could not fix all errors in test code")

        return response_data

    def _create_work_directory(self, prompt_path: Path, response_path: Path) -> Path:
        """Create a working directory with prompt and response files."""
        # Use absolute path for the work directory
        backend_dir = Path(__file__).parent.parent
        work_dir = (backend_dir / "outputs" / "clean_code_work").resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy prompt file
        work_prompt_path = work_dir / "prompt.py"
        shutil.copy2(prompt_path, work_prompt_path)
        
        # Copy response file and clean it
        work_response_path = work_dir / "test_code.py"
        with open(response_path, 'r') as f:
            response_content = f.read()
        
        # Apply initial manual fixes
        cleaned_content = self._apply_manual_fixes(response_content)
        
        with open(work_response_path, 'w') as f:
            f.write(cleaned_content)
        
        return work_dir

    def _apply_manual_fixes(self, code: str) -> str:
        """Apply common manual fixes to the code."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip lines that are copying the original prompt code
            if self._is_prompt_duplication(line):
                continue
                
            # Fix common import issues
            line = self._fix_import_issues(line)
            
            fixed_lines.append(line)
        
        # Join lines and apply additional fixes
        fixed_code = '\n'.join(fixed_lines)
        
        # Remove duplicate imports
        fixed_code = self._remove_duplicate_imports(fixed_code)
        
        # Ensure proper unittest structure
        fixed_code = self._ensure_unittest_structure(fixed_code)
        
        return fixed_code

    def _is_prompt_duplication(self, line: str) -> bool:
        """Check if a line is copying from the original prompt."""
        # Common patterns that indicate LLM is copying the prompt
        prompt_indicators = [
            "# Original code:",
            "# Here's the code to test:",
            "# Given code:",
            "# Code under test:",
        ]
        
        stripped_line = line.strip()
        for indicator in prompt_indicators:
            if stripped_line.startswith(indicator):
                return True
        
        return False

    def _fix_import_issues(self, line: str) -> str:
        """Fix common import issues."""
        # Fix relative imports to absolute
        if line.strip().startswith('from . import'):
            line = line.replace('from . import', 'from prompt import')
        elif line.strip().startswith('from .'):
            line = re.sub(r'from \.(\w+)', r'from prompt import \1', line)
        
        # Fix incorrect module references
        line = re.sub(r'from (\w+) import \*', r'from prompt import *', line)
        
        return line

    def _remove_duplicate_imports(self, code: str) -> str:
        """Remove duplicate import statements."""
        lines = code.split('\n')
        imports_seen = set()
        filtered_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('import ', 'from ')):
                if stripped not in imports_seen:
                    imports_seen.add(stripped)
                    filtered_lines.append(line)
            else:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)

    def _ensure_unittest_structure(self, code: str) -> str:
        """Ensure proper unittest structure."""
        if 'import unittest' not in code:
            code = 'import unittest\n' + code
        
        # Add if __name__ == '__main__' block if missing
        if "if __name__ == '__main__':" not in code:
            code += '\n\nif __name__ == "__main__":\n    unittest.main()\n'
        
        return code

    def _execute_and_fix_code(self, test_path: Path, prompt_path: Path, model_meta) -> bool:
        """Execute the code and fix errors iteratively."""
        for attempt in range(self.max_fix_attempts):
            print(f"[CleanOutputCode] Execution attempt {attempt + 1}/{self.max_fix_attempts}")
            
            result = self._run_test_code(test_path)
            
            if result["exit_code"] == 0:
                print("[CleanOutputCode] Code executed successfully!")
                return True
            
            print(f"[CleanOutputCode] Execution failed with exit code {result['exit_code']}")
            print(f"[CleanOutputCode] Error output: {result['stderr']}")
            
            if attempt < self.max_fix_attempts - 1:
                # Try to fix using LLM
                if self._fix_with_llm(test_path, prompt_path, result, model_meta):
                    continue
                else:
                    print("[CleanOutputCode] LLM fix failed, stopping attempts")
                    break
        
        return False

    def _run_test_code(self, test_path: Path) -> Dict[str, Any]:
        """Run the test code and return execution results."""
        # Ensure we use absolute paths for Docker volume mounting
        abs_parent_path = test_path.parent.resolve()
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{abs_parent_path}:/code",
            "python:3.11",
            "python",
            f"/code/{test_path.name}"
        ]
        
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return {
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "status": "success" if completed.returncode == 0 else "failure"
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": "Execution timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Docker execution failed: {e}",
                "status": "error"
            }

    def _fix_with_llm(self, test_path: Path, prompt_path: Path, error_result: Dict, model_meta) -> bool:
        """Use LLM to fix the code based on error messages."""
        try:
            # Read current files
            with open(test_path, 'r') as f:
                test_code = f.read()
            
            with open(prompt_path, 'r') as f:
                prompt_code = f.read()
            
            # Create fix prompt
            fix_prompt = self._create_fix_prompt(prompt_code, test_code, error_result)
            
            # Create prompt data for LLM
            from schemas import InputData, InputOptions
            fix_input = InputData(
                user_message=fix_prompt,
                source_code="",
                system_message="You are a Python expert. Fix the provided test code based on the error messages. Return only the corrected Python code without explanations.",
                options=InputOptions(temperature=0.1, num_ctx=4096)
            )
            
            fix_prompt_data = PromptData(
                model=model_meta,
                input=fix_input
            )
            
            # Get LLM manager and send fix request
            llm_manager = LLMManager()
            
            # Check if model is already running
            if model_meta.id not in llm_manager.active_models:
                print(f"[CleanOutputCode] Starting model {model_meta.id} for fixing...")
                llm_manager.start_model_container(model_meta.id)
            
            print("[CleanOutputCode] Requesting LLM to fix the code...")
            fix_response = llm_manager.send_prompt(fix_prompt_data)
            
            # Extract and save fixed code
            fixed_code = self._extract_code_from_response(fix_response.output.markdown)
            
            if fixed_code:
                with open(test_path, 'w') as f:
                    f.write(fixed_code)
                print("[CleanOutputCode] Applied LLM fix")
                return True
            else:
                print("[CleanOutputCode] No valid code found in LLM response")
                return False
                
        except Exception as e:
            print(f"[CleanOutputCode] Error during LLM fix: {e}")
            return False

    def _create_fix_prompt(self, prompt_code: str, test_code: str, error_result: Dict) -> str:
        """Create a prompt for the LLM to fix the code."""
        return f"""
I have a Python test file that's failing to execute. Please fix the errors and return the corrected code.

**Original code under test (prompt.py):**
```python
{prompt_code}
```

**Current test code (test_code.py):**
```python
{test_code}
```

**Error output:**
```
Exit code: {error_result['exit_code']}
Stderr: {error_result['stderr']}
Stdout: {error_result['stdout']}
```

**Instructions:**
1. Fix all syntax errors, import errors, and runtime errors
2. Ensure the test code properly imports from prompt.py
3. Make sure all test methods are properly structured
4. Return ONLY the corrected Python code for the test file
5. Do not include explanations or markdown formatting
6. Ensure the code follows unittest conventions

Return the fixed test code:
"""

    def _extract_code_from_response(self, response_text: str) -> str:
        """Extract Python code from LLM response."""
        if not response_text:
            return ""
        
        # Try to extract code block
        import re
        code_block_match = re.search(r'```python\s*(.*?)\s*```', response_text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # Try generic code block
        code_block_match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # If no code blocks, assume the entire response is code
        return response_text.strip()
