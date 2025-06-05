from base import ModuleBase
from mccabe import get_code_complexity


class ExampleLogger(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        mcc = calculate_mcc(prompt_data)
        return prompt_data, mcc

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        mcc = calculate_mcc(prompt_data)
        return response_data, mcc


def calculate_mcc(prompt_data: dict) -> float:
    # Set specific path for now. Fix this later.
    code_path = "/home/lisa/Documents/AMOS3/amos2025ss04-ai-driven-testing/python-test-cases/test_case_five.py"  # res = 7

    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
    print(code)
    complexity = get_code_complexity(code, 0, filename=code_path)
    print(complexity)
    return complexity


if __name__ == "__main__":
    calculate_mcc({})
