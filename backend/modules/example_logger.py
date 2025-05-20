from modules.base import ModuleBase


class ExampleLogger(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: dict) -> dict:
        print("[Logger] Prompt being sent:")
        print(prompt_data["prompt"])
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        print("[Logger] Response received:")
        print(response_data["response"])
        return response_data
