import threading
from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class MemoryUsage(ModuleBase):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, container=None, interval=0.5):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.container = container
                    cls._instance.interval = interval
                    cls._instance._stop_event = threading.Event()
                    cls._instance.max_usage = 0
                    cls._instance.thread = threading.Thread(
                        target=cls._instance._monitor, daemon=True
                    )
        return cls._instance

    def __init__(self, container=None, interval=5):
        pass

    @classmethod
    def is_initialized(cls):
        return cls._instance is not None

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> dict:
        pass
    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        peak_mb = self.get_max_usage_mb()
        print(f"Peak memory usage in container : {peak_mb:.2f} MiB")

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def _monitor(self):
        try:
            while not self._stop_event.is_set():
                stats = self.container.stats(stream=False)
                current_usage = stats["memory_stats"]["usage"]
                if current_usage > self.max_usage:
                    self.max_usage = current_usage
                self._stop_event.wait(self.interval)
        except Exception:
            pass

    def get_max_usage_mb(self):
        return self.max_usage / (1024 ** 2)
