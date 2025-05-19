## 🔌 Modular Plugin System

This project supports a flexible **module interface** that lets you plug in custom functionality before and after the prompt is sent to the LLM.

Modules can be used for tasks such as logging, prompt modification, postprocessing the response, or collecting additional metrics.

---

### ✅ How to Use

Add the `--modules` flag to the CLI:

```bash
python main.py --model 0 --modules example_logger
```

You can pass multiple modules seperated by spaces:

```bash
python main.py --model 0 --modules logger grammar_corrector metrics_collector
```

---

### 🧱 Module Structure

Each module must:
- Live in the `modules/` folder
- Inherit from `ModuleBase`
- Be named using `snake_case.py`
- Contain a class with the `CamelCase` equivalent of the filename

Example:

**modules/example_logger.py**

```python
from modules.base import ModuleBase

class ExampleLogger(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt: str) -> str:
        print("[Logger] Prompt:")
        print(prompt)
        return prompt

    def process_response(self, response: str, prompt: str) -> str:
        print("[Logger] Response:")
        print(response)
        return response
```

---

### ⚙️ Base Module Interface

**modules/base.py**

```python
from abc import ABC, abstractmethod

class ModuleBase(ABC):
    @abstractmethod
    def applies_before(self) -> bool:
        pass

    @abstractmethod
    def applies_after(self) -> bool:
        pass

    def process_prompt(self, prompt: str) -> str:
        return prompt

    def process_response(self, response: str, prompt: str) -> str:
        return response
```

---

### 🧩 Adding New Modules

1. Create a file in `modules/` (e.g., `my_module.py`)
2. Add a class `MyModule` that inherits from `ModuleBase`
3. Return `True` from `applies_before()` and/or `applies_after()`
4. Implement `process_prompt()` and/or `process_response()`
5. Run your script using:

```bash
python main.py --modules my_module
```
