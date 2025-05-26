import json
from pathlib import Path
from datetime import datetime
from modules.base import ModuleBase
from coverage import Coverage
import re



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

        cleaned_test = self.clean_code_block(response_data["response"], kind="test")
        cleaned_source = self.clean_code_block(prompt_data["prompt"], kind="code")

        self.write_to_outputs("generated_test.py", cleaned_test)
        self.write_to_outputs("source.py", cleaned_source)

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
        '''
        if syntax_valid:
            try:
                self.write_to_outputs("source.py", prompt_data["prompt"])
                coverage_percent = self.measure_coverage(
                    self.latest_dir / "generated_test.py",
                    self.latest_dir / "source.py"
                )
                metrics["Coverage (%)"] = coverage_percent

                mutation_score = self.run_mutation_testing(self.latest_dir / "source.py")
                if mutation_score is not None:
                    metrics["Mutation Score (%)"] = mutation_score
            except Exception as e:
                metrics["Error"] = f"Evaluation failed: {e}"
        else:
            metrics["Error"] = "Syntax error in generated test file"
        '''
        self.write_to_outputs("metrics.json", json.dumps(metrics, indent=4))

        return response_data

    def measure_coverage(self, test_file, source_file):
        cov = Coverage()
        cov.start()
        try:
            namespace = {}
            exec(open(source_file).read(), namespace)
            exec(open(test_file).read(), namespace)
        except Exception as e:
            print(f"[Coverage] Runtime Error: {e}")
            return 0.0
        finally:
            cov.stop()
            cov.save()

        _, _, covered, missing, _ = cov.analysis2(source_file)
        if covered + len(missing) == 0:
            return 0.0
        return round(covered / (covered + len(missing)) * 100, 2)

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
        print(f"writing ouputs to {self.latest_dir}")
        for directory in [self.latest_dir, self.archive_dir]:
            path = directory / filename
            if filename.endswith(".json"):
                path.write_text(content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    def clean_response_text2(self, response_text):
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

    def clean_response_text1(self, response_text: str) -> str:

        import_index = response_text.find("import")
        if import_index != -1:
            response_text = response_text[import_index:]

        # Remove Markdown code fences
        response_text = re.sub(r"```(?:python)?", "", response_text)
        response_text = response_text.replace("```", "")

        # Remove trailing explanations and narrative sections
        explanation_markers = [
            "Explanation:",
            "# Explanation",
            "# Example Output",
            "This script defines",
            "In this example",
            "The test suite includes",
        ]
        for marker in explanation_markers:
            if marker in response_text:
                response_text = response_text.split(marker)[0]

        # Optional: Remove standalone comments (that aren't in test code)
        lines = response_text.splitlines()
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Allow actual Python comments in tests, remove only narrative ones
            if stripped.startswith("#") and not stripped.startswith("# test"):
                continue
            cleaned_lines.append(line)

        response_text = "\n".join(cleaned_lines)

        # Optional: Remove trailing empty lines
        response_text = response_text.strip()

        print(response_text)
        return response_text

    def clean_code_block(self, raw_text: str, kind: str = "code") -> str:
        """
        Cleans raw LLM output or prompt text. Strips markdown, narration, and explanations.
        kind = "code" for source functions, "test" for generated test files
        """
        # Remove Markdown fences
        raw_text = re.sub(r"```(?:python)?", "", raw_text)
        raw_text = raw_text.replace("```", "")

        if kind == "test":
            stop_index = raw_text.find("unittest.main()")
            if stop_index != -1:
                # Include everything up to and including the unittest.main() line
                end = raw_text.find("\n", stop_index)
                raw_text = raw_text[:end if end != -1 else None]

        # Remove everything before the first def/class/import
        code_start = None
        lines = raw_text.splitlines()
        for idx, line in enumerate(lines):
            if line.strip().startswith(("def", "class", "import")):
                code_start = idx
                break
        if code_start is not None:
            lines = lines[code_start:]
        else:
            print(f"[Cleaner] No code start found in {kind}.")
            return ""

        # Remove trailing explanations
        explanation_markers = [
            "Explanation:",
            "# Explanation",
            "# Example Output",
            "This script defines",
            "In this example",
            "The test suite includes",
        ]
        cleaned_lines = []
        for line in lines:
            if any(marker in line for marker in explanation_markers):
                break
            if kind == "test" and line.strip().startswith("#") and "test" not in line.lower():
                continue
            cleaned_lines.append(line)

        code = "\n".join(cleaned_lines).strip()
        return code

    def check_syntax_validity(self, file_path):
        try:
            with open(file_path, "r") as f:
                code = f.read()
            compile(code, str(file_path), "exec")
            return True
        except SyntaxError as e:
            print(f"[Metrics] Syntax Error: {e}")
            return False
