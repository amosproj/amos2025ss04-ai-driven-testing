import subprocess
from pathlib import Path
from typing import Union
import black
from modules.base import ModuleBase
from schemas import PromptData, ResponseData
from modules.text_converter import (
    fix_indent,
    add_pass_to_empty_functions,
)


class PruneDuplicateTests(ModuleBase):
    """Executes the generated prompt and response code (typically unittests)."""

    postprocessing_order = 30

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        print("Pruning duplicate tests and asserts:")

        # Read the response code from extracted/response.py
        response_path = (
            response_data.output.output_code_path or "extracted/response.py"
        )
        response_path = Path(response_path).resolve()

        # Check if there are duplicate test functions by comparing their names
        # They start with "dev test_"
        if not response_path.exists():
            return response_data

        with open(response_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Find all test function definitions
        test_functions = []
        for line in code.splitlines():
            line = line.strip()
            if line.startswith("def test_"):
                test_functions.append(line)

        print(f"Original number of tests found: {len(test_functions)}")

        # Identify duplicate test functions
        duplicate_tests = set()
        seen = set()
        for test in test_functions:
            if test in seen:
                duplicate_tests.add(test)
            seen.add(test)

        print(
            f"After pruning duplicates: {len(test_functions) - len(duplicate_tests)} tests remaining"
        )

        # Check for duplicate asserts
        lines = code.splitlines()
        processed_lines = []
        seen_asserts = set()
        duplicate_asserts = set()

        original_assert_count = sum(
            1 for line in lines if "assert" in line.strip()
        )
        print(
            f"\nOriginal number of assert statements: {original_assert_count}"
        )

        for line in lines:
            stripped_line = line.strip()
            if "assert" in stripped_line:
                if stripped_line in seen_asserts:
                    duplicate_asserts.add(stripped_line)
                seen_asserts.add(stripped_line)
            processed_lines.append(line)

        final_assert_count = len(seen_asserts)
        print(
            f"After pruning duplicates: {final_assert_count} assert statements remaining"
        )

        # Combine the processed lines back into code
        processed_code = "\n".join(processed_lines)

        # Format the code using Black
        try:
            formatted_code = black.format_str(
                processed_code, mode=black.Mode()
            )
        except Exception:
            formatted_code = fix_indent(processed_code)
        formatted_code = add_pass_to_empty_functions(formatted_code)
        try:
            formatted_code = black.format_str(
                formatted_code, mode=black.Mode()
            )
        except Exception:
            formatted_code = (
                formatted_code  # fallback to fixed code if Black fails again
            )

        # Override the original response (in the file and in the response_data)
        # with the pruned and formatted response code
        if formatted_code != code:
            response_data.output.code = formatted_code
            response_data.output.output_code_path = str(response_path)
            with open(response_path, "w", encoding="utf-8") as f:
                f.write(formatted_code)
            print(
                f"Processed and formatted response code from {response_path}"
            )

        return response_data
