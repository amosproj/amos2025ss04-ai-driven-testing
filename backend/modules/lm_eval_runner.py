import subprocess
import json
from pathlib import Path
from datetime import datetime
from modules.base import ModuleBase
import os
from schemas import PromptData, ResponseData


class LmEvalRunner(ModuleBase):

    pre_processing_order = 10
    post_processing_order = 10

    def __init__(self):
        self.output_dir = Path("outputs/human_eval")

    def applies_before(self):
        return False

    def applies_after(self):
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        model_id = prompt_data.model.id

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_path = self.output_dir / f"result_{timestamp}.json"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        command = [
            "lm_eval",
            "--model",
            "hf",
            "--model_args",
            "pretrained=microsoft/phi-1_5,device=cpu",  # <---- small model for testing, adapt hf-id here to try out different models
            "--tasks",
            "humaneval",
            "--limit",
            "1",  # <--- for now only passing 1 task, butdlete this for the whole set
            "--batch_size",
            "1",
            "--output_path",
            str(output_path),
            "--confirm_run_unsafe_code",
            "--write_out",
        ]

        env = os.environ.copy()
        env["HF_ALLOW_CODE_EVAL"] = "1"
        print("")
        print("")
        print(f"[HumanEval] Running benchmark for {model_id}...")
        try:
            subprocess.run(command, check=True, env=env)
            print("[HumanEval] Benchmark finished.")

            if output_path.exists():
                with open(output_path, "r") as f:
                    eval_data = json.load(f)
                result = eval_data["results"]["human_eval"]
                score = result.get("pass@1", "N/A")
                print(f"[HumanEval] pass@1 = {score}")

                response_data.output.lm_eval = result

                # Also save to metrics.json if you want
                metrics_out = {
                    "model": model_id,
                    "task": "humaneval",
                    "pass@1": score,
                    "raw": result,
                }
                with open(self.output_dir / "metrics.json", "w") as f:
                    json.dump(metrics_out, f, indent=2)

        except subprocess.CalledProcessError as e:
            print(f"[HumanEval] Benchmark failed: {e}")
            response_data.output.lm_eval = {"error": str(e)}

        return response_data
