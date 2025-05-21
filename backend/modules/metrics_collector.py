import json
from pathlib import Path
from datetime import datetime
from modules.base import ModuleBase


class MetricsCollector(ModuleBase):
    def __init__(self):
        self.loading_time = None
        self.generation_time = None
        self.latest_dir = None
        self.archive_dir = None

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        # Prepare folders
        model_name = prompt_data["model"]["name"]
        self.latest_dir, self.archive_dir = self.make_output_dirs(model_name)

        cleaned = self.clean_response_text(response_data["response"])

        # Save cleaned code
        self.write_to_outputs("generated_test.py", cleaned)

        # Check syntax
        syntax_valid = self.check_syntax_validity(
            self.latest_dir / "generated_test.py"
        )

        metrics = {
            "Model": prompt_data["model"]["name"],
            "Syntax Valid": syntax_valid,
            "Loading Time (s)": round(response_data.get("loading_time", 0), 2),
            "Generation Time (s)": round(
                response_data.get("final_time", 0), 2
            ),
        }

        self.write_to_outputs("metrics.json", json.dumps(metrics, indent=4))

        return response_data

    def make_output_dirs(self, model_name):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        archive_dir = (
            Path("outputs/archive")
            / f"{timestamp}_{model_name.lower().replace(' ', '_')}"
        )
        latest_dir = Path("outputs/latest")

        archive_dir.mkdir(parents=True, exist_ok=True)
        latest_dir.mkdir(parents=True, exist_ok=True)

        return latest_dir, archive_dir

    def write_to_outputs(self, filename, content: str):
        for directory in [self.latest_dir, self.archive_dir]:
            path = directory / filename
            if filename.endswith(".json"):
                path.write_text(content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    def clean_response_text(self, response_text):
        import_index = response_text.find("import")
        if import_index != -1:
            response_text = response_text[import_index:]

        response_text = response_text.replace("```python", "").replace(
            "```", ""
        )
        for marker in ["Explanation:", "# Explanation", "This script defines"]:
            if marker in response_text:
                response_text = response_text.split(marker)[0]

        return response_text.strip()

    def check_syntax_validity(self, file_path):
        try:
            with open(file_path, "r") as f:
                code = f.read()
            compile(code, str(file_path), "exec")
            return True
        except SyntaxError as e:
            print(f"[Metrics] Syntax Error: {e}")
            return False
