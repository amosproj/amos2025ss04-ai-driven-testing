from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class Timeout(ModuleBase):

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return False

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        prompt_data.timeout = 30
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        return response_data
