from .base import ModuleBase
from mccabe import get_code_complexity
import os


class CalculateMcc(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        mcc = calculate_mcc(prompt_data)
        # Use relative path for output_dir
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extracted",
        )
        output_path = os.path.join(output_dir, "mcc-prompt.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"mcc: {mcc}\n")
            f.write(f"prompt_data: {prompt_data}\n")
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        mcc = calculate_mcc(prompt_data)

        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extracted",
        )
        output_path = os.path.join(output_dir, "mcc-response.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"mcc: {mcc}\n")
            f.write(f"response_data: {response_data}\n")
        return response_data


def calculate_mcc(prompt_data: dict) -> float:
    # Use relative path for the test case file
    code_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "..",
        "python-test-cases",
        "test_case_five.py",
    )
    code_path = os.path.abspath(code_path)
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
    complexity = get_code_complexity(code, 0, filename=code_path)
    return complexity


if __name__ == "__main__":
    calculate_mcc({})
