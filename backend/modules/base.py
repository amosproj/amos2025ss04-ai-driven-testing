from abc import ABC, abstractmethod

class ModuleBase(ABC):
    @abstractmethod
    def applies_before(self) -> bool:
        """Return True if the module runs before prompt is sent."""
        pass

    @abstractmethod
    def applies_after(self) -> bool:
        """Return True if the module runs after response is received."""
        pass

    def process_prompt(self, prompt: str) -> str:
        """Optionally modify the prompt."""
        return prompt

    def process_response(self, response: str, prompt: str) -> str:
        """Optionally modify or analyze the response."""
        return response
