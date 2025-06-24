import subprocess
import sys
from pathlib import Path
from typing import Union

from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class ExecuteTests(ModuleBase):
    """Executes the generated prompt and response code (typically unittests)."""

    order_after = 99  # Run this late in the chain

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        if prompt_data.prompt_code_path == None:
            prompt_path = Path("extracted/prompt.py").resolve()
        else:
            prompt_path = Path(prompt_data.prompt_code_path)
        if response_data.output.output_code_path == None:
            response_path = Path("extracted/response.py").resolve()
        else:
            response_path = Path(response_data.output.output_code_path)

        self.run_python_file(prompt_path)

        result = self.run_python_file(response_path)
        response_data.output.test_execution_results = result
        return response_data

    def run_python_file(self, path: Union[str, Path]) -> str:
        path = Path(path).resolve()
        if not path.exists():
            return f"File not found: {path}"

        container_path = f"/code/{path.name}"

        cmd = [
            "docker", "run", "--rm",
            "-v", f"{path.parent}:/code",  # mount local dir
            "python:3.11",  # Docker-Image
            "python", container_path
        ]

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
            )
            result = (
                f"[exit code: {completed.returncode}]\n"
                f"--- STDOUT ---\n{completed.stdout}\n"
                f"--- STDERR ---\n{completed.stderr}"
            )
            print(result)
            if completed.returncode == 0:
                return (
                    "[exit code: 0]\n"
                    "Tests ran successfully.\n"
                    f"{completed.stdout}"
                )
            else:
                return (
                    f"[exit code: {completed.returncode}]\n"
                    "Tests failed.\n"
                    "--- STDOUT ---\n"
                    f"{completed.stdout}\n"
                    "--- STDERR ---\n"
                    f"{completed.stderr}"
                )
        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            return f"Docker execution failed: {e}"