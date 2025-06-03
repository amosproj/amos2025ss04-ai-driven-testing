from modules.base import ModuleBase


class CalculateCcc(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        return response_data
