from modules.base import ModuleBase
import warnings
from modules.calculate_ccc_lib.ccc_calculator_python import (
    get_ccc_for_code as get_ccc_for_code_python,
)
from modules.calculate_ccc_lib.ccc_estimator_general import (
    get_ccc_for_code as get_ccc_for_code_general,
)

# Error handling in this module is a mess, but it works 👍


class CalculateCcc(ModuleBase):
    def __init__(self):
        super().__init__()
        print("CalculateCcc module initialized.")

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:

        source_code = prompt_data.input.source_code
        if not source_code:
            warnings.warn(
                "No source code found in prompt_data.input.source_code. Cannot calculate CCC. "
            )
            return prompt_data

        try:
            ccc = get_ccc_for_code_python(source_code)
            print("Using Python CCC calculator for source code")
        except Exception as e:
            print(f"Python CCC calculator failed: {e}")
            ccc = get_ccc_for_code_general(source_code)
            print("Using general CCC estimator for source code")

        if ccc is None:
            warnings.warn(
                f"Could not calculate CCC for source code {source_code}. "
                "See warnings for more details."
            )
        else:
            print(f"Calculated CCC: {ccc}")

        prompt_data.ccc_complexity = ccc

        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:

        output_code = response_data.output.code
        if not output_code:
            warnings.warn(
                "No code found to be extracted from response.Cannot calculate CCC. Debug the text_converter module for further information. "
            )
            return response_data

        try:
            ccc = get_ccc_for_code_python(output_code)
            print("Using Python CCC calculator for source code")
        except Exception as e:
            print(f"Python CCC calculator failed: {e}")
            ccc = get_ccc_for_code_general(output_code)
            print("Using general CCC estimator for source code")

        if ccc is None:
            warnings.warn(
                f"Could not calculate CCC for code {output_code}. "
                "See warnings for more details."
            )
        else:
            print(f"Calculated CCC: {ccc}")

        response_data.output.ccc_complexity = ccc

        return response_data
