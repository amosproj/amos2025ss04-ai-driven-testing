import os
import psutil
from schemas import PromptData, ResponseData
from modules.base import ModuleBase


class MemoryUsage(ModuleBase):
    def __init__(self):
        self._start_memory = None
        self._end_memory = None
        self._process = psutil.Process(os.getpid())

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        self._start_memory = self._process.memory_info().rss / (1024 ** 2)  # in MB
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        self._end_memory = self._process.memory_info().rss / (1024 ** 2)  # in MB
        memory_used = self._end_memory - self._start_memory


        print(f"Memory used during inference: {memory_used:.2f} MB")
        return response_data
