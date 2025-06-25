import subprocess
from pathlib import Path
from typing import Union

from modules.base import ModuleBase
from schemas import PromptData, ResponseData, TestExecutionResults


class ExecuteTests(ModuleBase):
    """Executes the generated prompt and response code (typically unittests)."""

    postprocessing_order = 99  # Run this late in the chain

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        if response_data.output.output_code_path is None:
            response_path = Path("extracted/response.py").resolve()
        else:
            response_path = Path(response_data.output.output_code_path)

        result = self.run_python_file(response_path)
        response_data.output.test_execution_results = TestExecutionResults(
            **result
        )
        return response_data

    def run_python_file(self, path: Union[str, Path]) -> str:
        path = Path(path).resolve()
        if not path.exists():
            return f"File not found: {path}"

        container_path = f"/code/{path.name}"

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{path.parent}:/code",  # mount local dir
            "python:3.11",  # Docker-Image
            "python",
            container_path,
        ]

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            result = {
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "status": "success"
                if completed.returncode == 0
                else "failure",
            }

            print("\n=== Test Execution Output ===")
            print(result)
            print("\n")

            return result

        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            return f"Docker execution failed: {e}"
