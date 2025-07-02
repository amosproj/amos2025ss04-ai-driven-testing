import importlib
import os
from typing import Dict, List, Optional, Any
import re


def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def camel_to_snake(name: str) -> str:
    # Insert underscore before each uppercase letter (except at start), then lowercase all
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


class ModuleManager:
    """Manages and loads analysis modules for the AI testing system."""

    def __init__(self):
        """Initialize the module manager."""
        self.modules = {}
        self.loaded_modules = {}
        self._load_available_modules()

    def _load_available_modules(self):
        """Discover and load available modules from the modules directory."""
        modules_dir = os.path.join(os.path.dirname(__file__), "modules")
        if not os.path.exists(modules_dir):
            return

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    self._load_module(module_name)
                except Exception as e:
                    print(f"Failed to load module '{module_name}': {e}")

    def _load_module(self, module_name: str):
        """Load a specific module by name."""
        try:
            mod = importlib.import_module(f"modules.{module_name}")

            # Try to get the module instance
            if hasattr(mod, "get_module"):
                # Module has a get_module function
                module_instance = mod.get_module()
            else:
                # Try to instantiate the class directly
                class_name = snake_to_camel(module_name)
                cls = getattr(mod, class_name)
                module_instance = cls()

            self.loaded_modules[module_name] = module_instance

            # Use the module's name attribute if available, otherwise use filename
            module_key = getattr(module_instance, "name", module_name)
            self.modules[module_key] = module_instance

        except Exception as e:
            print(f"Failed to load module '{module_name}': {e}")
            raise

    def get_module(self, module_name: str) -> Optional[Any]:
        """Get a loaded module by name."""
        return self.modules.get(module_name)

    def get_available_modules(self) -> List[str]:
        """Get list of available module names."""
        return list(self.modules.keys())

    def apply_before_modules(self, modules_list: List[str], prompt_data):
        """Apply modules that run before test generation."""
        active_modules = [
            self.modules[name] for name in modules_list if name in self.modules
        ]

        # Sort modules by order_before (default to 10 if not present)
        modules_sorted = sorted(
            active_modules, key=lambda m: getattr(m, "order_before", 10)
        )

        for m in modules_sorted:
            if hasattr(m, "applies_before") and m.applies_before():
                if hasattr(m, "process_prompt"):
                    prompt_data = m.process_prompt(prompt_data)

        return prompt_data

    def apply_after_modules(
        self, modules_list: List[str], response_data, prompt_data
    ):
        """Apply modules that run after test generation."""
        active_modules = [
            self.modules[name] for name in modules_list if name in self.modules
        ]

        # Sort modules by order_after (default to 10 if not present)
        modules_sorted = sorted(
            active_modules, key=lambda m: getattr(m, "order_after", 10)
        )

        for m in modules_sorted:
            if hasattr(m, "applies_after") and m.applies_after():
                if hasattr(m, "process_response"):
                    response_data = m.process_response(
                        response_data, prompt_data
                    )

        return response_data


# Legacy functions for backward compatibility
def load_modules(module_names):
    """Legacy function for loading modules."""
    manager = ModuleManager()
    modules = []
    for name in module_names:
        module = manager.get_module(name)
        if module:
            modules.append(module)
    return modules


def apply_before_modules(modules, prompt_data):
    """Legacy function for applying before modules."""
    # Sort modules by order_before (default to 0 if not present)
    modules_sorted = sorted(
        modules, key=lambda m: getattr(m, "order_before", 10)
    )
    for m in modules_sorted:
        if hasattr(m, "applies_before") and m.applies_before():
            if hasattr(m, "process_prompt"):
                prompt_data = m.process_prompt(prompt_data)
    return prompt_data


def apply_after_modules(modules, response_data, prompt_data):
    """Legacy function for applying after modules."""
    # Sort modules by order_after (default to 0 if not present)
    modules_sorted = sorted(
        modules, key=lambda m: getattr(m, "order_after", 10)
    )
    for m in modules_sorted:
        if hasattr(m, "applies_after") and m.applies_after():
            if hasattr(m, "process_response"):
                response_data = m.process_response(response_data, prompt_data)
    return response_data
