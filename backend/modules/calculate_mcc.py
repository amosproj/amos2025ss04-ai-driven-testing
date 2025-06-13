from .base import ModuleBase
from mccabe import PathGraphingAstVisitor
import os
from schemas import PromptData, ResponseData
import sys
import ast


class CalculateMcc(ModuleBase):
    """Berechnet die McCabe Complexity (MCC) für Python-Code mittels AST-Analyse."""

    order_before = 5
    order_after = 5

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        prompt_path = prompt_data.prompt_code_path
        if prompt_path and os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = prompt_data.input.source_code

        try:
            mcc = get_code_complexity_sum(prompt, filename="stdin")
            print("Calculated MCC:", mcc)
        except Exception as e:
            print(f"Could not calculate MCC for prompt: {e}")
            mcc = None

        prompt_data.mcc_complexity = mcc
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        response_path = response_data.output.output_code_path
        if response_path and os.path.exists(response_path):
            with open(response_path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            code = getattr(response_data.output, "code", None) or getattr(
                response_data.output, "markdown", ""
            )

        try:
            mcc = get_code_complexity_sum(code, filename="stdin")
            print("Calculated MCC:", mcc)
        except Exception as e:
            print(f"Could not calculate MCC for response: {e}")
            mcc = None

        response_data.output.mcc_complexity = mcc
        return response_data


def get_code_complexity_sum(code, filename="stdin"):
    try:
        tree = compile(code, filename, "exec", ast.PyCF_ONLY_AST)
    except SyntaxError:
        e = sys.exc_info()[1]
        sys.stderr.write("Unable to parse %s: %s\n" % (filename, e))
        return 0

    visitor = PathGraphingAstVisitor()
    visitor.preorder(tree, visitor)
    total_complexity = 0
    for graph in visitor.graphs.values():
        total_complexity += graph.complexity()
    return total_complexity
