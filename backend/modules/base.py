from abc import ABC, abstractmethod
from schemas import PromptData, ResponseData


class ModuleBase(ABC):
    @abstractmethod
    def applies_before(self) -> bool:
        """Return True if the module runs before prompt is sent."""
        pass

    @abstractmethod
    def applies_after(self) -> bool:
        """Return True if the module runs after response is received."""
        pass

    def dependencies(self) -> list[type["ModuleBase"]]:
        """
        Return a list of other ModuleBase subclasses this module depends on.
        Default is empty.
        """
        return []

    def dependencies_names(self) -> list[str]:
        """
        Return a list of names of other ModuleBase subclasses this module depends on.
        Default is empty.
        """
        return [dep.__name__ for dep in self.dependencies()]

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        """Optionally modify the prompt."""
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """Optionally modify or analyze the response."""
        return response_data
