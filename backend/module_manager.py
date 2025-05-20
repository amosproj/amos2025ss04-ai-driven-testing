import importlib


def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def load_modules(module_names):
    modules = []
    for name in module_names:
        try:
            mod = importlib.import_module(f"modules.{name}")
            class_name = snake_to_camel(name)
            cls = getattr(mod, class_name)
            modules.append(cls())
        except Exception as e:
            print(f"Failed to load module '{name}': {e}")
    return modules


def apply_before_modules(modules, prompt_data):
    for m in modules:
        if m.applies_before():
            prompt_data = m.process_prompt(prompt_data)
    return prompt_data


def apply_after_modules(modules, response_data, prompt_data):
    for m in modules:
        if m.applies_after():
            response_data = m.process_response(response_data, prompt_data)
    return response_data
