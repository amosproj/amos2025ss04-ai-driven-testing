from .base import ModuleBase
from mccabe import get_code_complexity
import os
from schemas import PromptData, ResponseData


class CalculateMcc(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        prompt = prompt_data.input.source_code
        mcc = get_code_complexity(prompt, 0, filename="stdin")
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

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        code = response_data.output
        mcc = get_code_complexity(code, 0, filename="stdin")

        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extracted",
        )
        output_path = os.path.join(output_dir, "mcc-response.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"mcc: {mcc}\n")
            f.write(f"response_data: {response_data}\n")
        return response_data


def calculate_mcc(prompt_data: PromptData) -> float:
    # Use the code from prompt_data.input.source_code
    code = prompt_data.input.source_code
    complexity = get_code_complexity(code, 0, filename=None)
    return complexity
