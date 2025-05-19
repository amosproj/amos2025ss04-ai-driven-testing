from modules.base import ModuleBase


class ExampleLogger(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt: str) -> str:
        print("[Logger] Prompt being sent:")
        print(prompt)
        return prompt

    def process_response(self, response: str, prompt: str) -> str:
        print("[Logger] Response received:")
        print(response)
        return response
