from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class ExampleLogger(ModuleBase):
    """Einfaches Logging-Modul das Prompt-Eingaben und Antworten in der Konsole ausgibt."""

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        return []

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        print("[Logger] Prompt being sent:")
        print(prompt_data.input)
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        print("[Logger] Response received:")
        print(response_data.output)
        return response_data
