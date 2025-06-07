from .base import ModuleBase
from mccabe import get_code_complexity
import os
from schemas import PromptData, ResponseData
import sys


class CalculateMcc(ModuleBase):
    order_before = 5
    order_after = 5

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        # Use the cleaned prompt file created by text_converter
        model_id = prompt_data.model.id.replace(":", "_")
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extracted",
        )
        prompt_filename = f"prompt_{model_id}.py"
        prompt_path = os.path.join(output_dir, prompt_filename)
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = prompt_data.input.source_code
        mcc = get_code_complexity(prompt, 0, filename="stdin")
        output_path = os.path.join(output_dir, "mcc-prompt.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"mcc: {mcc}\n")
            f.write(f"prompt_data: {prompt_data}\n")
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        # Use the cleaned response file created by text_converter
        model_id = prompt_data.model.id.replace(":", "_")
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extracted",
        )
        response_filename = f"responce_{model_id}.py"
        response_path = os.path.join(output_dir, response_filename)
        if os.path.exists(response_path):
            with open(response_path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            code = getattr(response_data.output, "code", None) or getattr(
                response_data.output, "markdown", ""
            )
        mcc = get_code_complexity(code, 0, filename="stdin")
        mcc_output_path = os.path.join(output_dir, "mcc-response.txt")
        with open(mcc_output_path, "w", encoding="utf-8") as f:
            f.write(f"mcc: {mcc}\n")
            f.write(f"response_data: {response_data}\n")
        return response_data
