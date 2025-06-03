from modules.base import ModuleBase
import warnings
from modules.calculate_ccc_lib.ccc_calculator_python import (
    get_ccc_for_file as get_ccc_for_file_python,
)
from modules.calculate_ccc_lib.ccc_estimator_general import (
    get_ccc_for_file as get_ccc_for_file_general,
)


class CalculateCcc(ModuleBase):
    def __init__(self):
        super().__init__()
        print("CalculateCcc module initialized.")
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        # TODO change once payload PR is merged
        file_path = prompt_data["file_path"]

        if not file_path:
            raise ValueError("Correct File path is required to calculate CCC.")
        if file_path.endswith(".py"):
            ccc = get_ccc_for_file_python(file_path)
        else:
            ccc = get_ccc_for_file_general(file_path)

        if ccc is None:
            warnings.warn(
                f"Could not calculate CCC for file {file_path}. "
                "See warnings for more details."
            )
        else:
            print(f"Calculated CCC for {file_path}: {ccc}")

        # TODO change once payload PR is merged
        prompt_data["ccc"] = ccc

        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        # TODO change once payload PR is merged
        file_path = response_data["file_path"]

        if not file_path:
            raise ValueError("Correct File path is required to calculate CCC.")
        if file_path.endswith(".py"):
            ccc = get_ccc_for_file_python(file_path)
            print(f"Using Python CCC calculator for {file_path}")
        else:
            ccc = get_ccc_for_file_general(file_path)
            print(f"Using general CCC estimator for {file_path}")

        if ccc is None:
            warnings.warn(
                f"Could not calculate CCC for file {file_path}. "
                "See warnings for more details."
            )
        else:
            print(f"Calculated CCC for {file_path}: {ccc}")

        # TODO change once payload PR is merged
        response_data["ccc"] = ccc

        return response_data
