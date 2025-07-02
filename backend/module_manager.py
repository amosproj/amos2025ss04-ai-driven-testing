"""Module manager for dynamic loading and management of processing modules."""
import importlib
import os
from typing import Dict, List, Optional, Any
<<<<<<< HEAD
import re


COMMAND_ORDER = False
=======
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)


def snake_to_camel(name: str) -> str:
    """Convert snake_case to CamelCase."""
    return "".join(word.capitalize() for word in name.split("_"))


<<<<<<< HEAD
def camel_to_snake(name: str) -> str:
    # Insert underscore before each uppercase letter (except at start), then lowercase all
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


class ModuleManager:
    """Manages and loads analysis modules for the AI testing system."""

=======
class ModuleManager:
    """Manages and loads analysis modules for the AI testing system."""
    
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
    def __init__(self):
        """Initialize the module manager."""
        self.modules = {}
        self.loaded_modules = {}
        self._load_available_modules()
<<<<<<< HEAD

=======
    
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
    def _load_available_modules(self):
        """Discover and load available modules from the modules directory."""
        modules_dir = os.path.join(os.path.dirname(__file__), "modules")
        if not os.path.exists(modules_dir):
            return
<<<<<<< HEAD

=======
        
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    self._load_module(module_name)
                except Exception as e:
                    print(f"Failed to load module '{module_name}': {e}")
<<<<<<< HEAD

=======
    
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
    def _load_module(self, module_name: str):
        """Load a specific module by name."""
        try:
            mod = importlib.import_module(f"modules.{module_name}")
<<<<<<< HEAD

            # Try to get the module instance
            if hasattr(mod, "get_module"):
=======
            
            # Try to get the module instance
            if hasattr(mod, 'get_module'):
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
                # Module has a get_module function
                module_instance = mod.get_module()
            else:
                # Try to instantiate the class directly
                class_name = snake_to_camel(module_name)
                cls = getattr(mod, class_name)
                module_instance = cls()
<<<<<<< HEAD

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

=======
            
            self.loaded_modules[module_name] = module_instance
            
            # Use the module's name attribute if available, otherwise use filename
            module_key = getattr(module_instance, 'name', module_name)
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
        active_modules = [self.modules[name] for name in modules_list if name in self.modules]
        
        # Sort modules by order_before (default to 10 if not present)
        modules_sorted = sorted(
            active_modules, key=lambda m: getattr(m, "order_before", 10)
        )
        
        for m in modules_sorted:
            if hasattr(m, 'applies_before') and m.applies_before():
                if hasattr(m, 'process_prompt'):
                    prompt_data = m.process_prompt(prompt_data)
        
        return prompt_data
    
    def apply_after_modules(self, modules_list: List[str], response_data, prompt_data):
        """Apply modules that run after test generation."""
        active_modules = [self.modules[name] for name in modules_list if name in self.modules]
        
        # Sort modules by order_after (default to 10 if not present)
        modules_sorted = sorted(
            active_modules, key=lambda m: getattr(m, "order_after", 10)
        )
        
        for m in modules_sorted:
            if hasattr(m, 'applies_after') and m.applies_after():
                if hasattr(m, 'process_response'):
                    response_data = m.process_response(response_data, prompt_data)
        
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
        return response_data


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    # Insert underscore before each uppercase letter (except at start), then lowercase all
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


# Legacy functions for backward compatibility
<<<<<<< HEAD
def load_modules(module_names, loaded=None):
    """Legacy function for loading modules with dependency support."""
    if loaded is None:
        loaded = {}

    for name in module_names:
        if name in loaded:
            continue

        try:
            mod = importlib.import_module(f"modules.{name}")
            class_name = snake_to_camel(name)
            cls = getattr(mod, class_name)
            module = cls()
            loaded[name] = module

            # Recursively load dependencies
            if hasattr(module, "dependencies"):
                dependencies = (
                    module.dependencies()
                )  # should return list of module class types
                if dependencies:
                    dep_names = [
                        camel_to_snake(dep.__name__) for dep in dependencies
                    ]
                    print(
                        "loading dependencies for module:",
                        name,
                        "->",
                        dep_names,
                    )
                    load_modules(dep_names, loaded)

        except ImportError as e:
            print(
                "There are circular dependencies in the modules, please check the module dependencies."
            )
            print(f"Module '{name}' could not be imported: {e}")
            raise e
        except Exception as e:
            print(f"Failed to load module '{name}': {e}")

    return list(loaded.values())


def apply_before_modules(modules, prompt_data):
    """Legacy function for applying before modules with flexible ordering."""
    if COMMAND_ORDER:
        print("command order")
        modules_sorted = modules  # Keep command order
    else:
        print("sorting")
        # Try preprocessing_order first (development), fall back to order_before (feature)
        modules_sorted = sorted(
            modules,
            key=lambda m: getattr(
                m, "preprocessing_order", getattr(m, "order_before", 10)
            ),
        )

    for m in modules_sorted:
        if hasattr(m, "applies_before") and m.applies_before():
            if hasattr(m, "process_prompt"):
=======
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
        if hasattr(m, 'applies_before') and m.applies_before():
            if hasattr(m, 'process_prompt'):
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
                prompt_data = m.process_prompt(prompt_data)
    return prompt_data


def apply_after_modules(modules, response_data, prompt_data):
<<<<<<< HEAD
    """Legacy function for applying after modules with flexible ordering."""
    if COMMAND_ORDER:
        print("command order")
        modules_sorted = modules  # Keep order from command
    else:
        print("sorting")
        # Try postprocessing_order first (development), fall back to order_after (feature)
        modules_sorted = sorted(
            modules,
            key=lambda m: getattr(
                m, "postprocessing_order", getattr(m, "order_after", 10)
            ),
        )

    for m in modules_sorted:
        if hasattr(m, "applies_after") and m.applies_after():
            if hasattr(m, "process_response"):
=======
    """Legacy function for applying after modules."""
    # Sort modules by order_after (default to 0 if not present)
    modules_sorted = sorted(
        modules, key=lambda m: getattr(m, "order_after", 10)
    )
    for m in modules_sorted:
        if hasattr(m, 'applies_after') and m.applies_after():
            if hasattr(m, 'process_response'):
>>>>>>> 36a5455 (Final commit: Complete code coverage integration)
                response_data = m.process_response(response_data, prompt_data)
    return response_data
