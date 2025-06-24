import importlib
import re


ORDER = True


def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def camel_to_snake(name: str) -> str:
    # Insert underscore before each uppercase letter (except at start), then lowercase all
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


def load_modules(module_names, loaded=None):
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
            dependencies = (
                module.dependencies()
            )  # should return list of module class types
            if dependencies:
                dep_names = [
                    camel_to_snake(dep.__name__) for dep in dependencies
                ]
                print(
                    "loading dependencies for module:", name, "->", dep_names
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
    # Sort modules by preprocessing_order (default to 10 if not present)
    if ORDER:
        print("sorting")
        modules_sorted = sorted(
            modules, key=lambda m: getattr(m, "preprocessing_order", 10)
        )
    else:
        print("not sorting")
        modules_sorted = modules  # Keep original order

    for m in modules_sorted:
        if m.applies_before():
            prompt_data = m.process_prompt(prompt_data)
    return prompt_data


def apply_after_modules(modules, response_data, prompt_data):
    # Sort modules by postprocessing_order (default to 10 if not present)
    if ORDER:
        print("sorting")
        modules_sorted = sorted(
            modules, key=lambda m: getattr(m, "postprocessing_order", 10)
        )
    else:
        print("not sorting")
        modules_sorted = modules  # Keep original order
    for m in modules_sorted:
        if m.applies_after():
            response_data = m.process_response(response_data, prompt_data)
    return response_data
