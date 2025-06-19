from pathlib import Path
from modules.base import ModuleBase
from schemas import PromptData, ResponseData
from py2cfg import CFGBuilder as py2cfgCFGBuilder
from staticfg import CFGBuilder as staticfgCFGBuilder
import tempfile
import warnings
from datetime import datetime


class ShowControlFlow(ModuleBase):
    """Module that visualizes control flow from code and saves it as an image."""

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        """Processes the input source code to generate a control flow image for it."""
        source_code = prompt_data.input.source_code
        if not source_code:
            warnings.warn(
                "No source code provided for control flow visualization."
            )

        # Output path is timestamped with current time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(
            f"outputs/control_flow/control_flow_input_{current_time}"
        )
        try:
            # Create control flow image from the source code
            self.create_control_flow_image(source_code, output_path)
            # Store the path to the control flow image in the prompt data
            prompt_data.control_flow_image = str(output_path)
            print(f"Control flow image created successfully: {output_path}")
        except Exception as e:
            warnings.warn(f"Failed to create control flow image: {e}")
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """Processes the extracted response code to generate a control flow image for the output code."""
        code = response_data.output.code
        if code:

            # Output path is timestamped with current time
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(
                f"outputs/control_flow/control_flow_output_{current_time}"
            )

            try:
                # Create control flow image from the response code
                self.create_control_flow_image(code, output_path)
                # Store the path to the control flow image in the response data
                response_data.output.control_flow_image = str(output_path)
                print(
                    f"Control flow image created successfully: {output_path}"
                )
            except Exception as e:
                warnings.warn(f"Failed to create control flow image: {e}")
        else:
            warnings.warn(
                "No code in response to visualize control flow. Module text_converter is required!"
            )
        return response_data

    def create_control_flow_image_colorful(
        self, source_code: str, output_path: Path
    ):
        """Generates a control flow image from the source code."""
        # Create a temporary file to store the source code
        code_path = self.create_temporary_file(source_code)
        # Use py2cfg to build the control flow graph (more colors but less readable)
        cfg = py2cfgCFGBuilder().build_from_file("cfg", code_path)
        # save the control flow graph as an SVG image
        cfg.build_visual(output_path, format="svg", show=False)
        # Clean up the temporary file
        Path(code_path).unlink(missing_ok=True)
        return output_path

    def create_control_flow_image(self, source_code: str, output_path: Path):
        """Generates a control flow image from the source code."""
        # Create a temporary file to store the source code
        code_path = self.create_temporary_file(source_code)
        # Use staticfg to build the control flow graph (more readable)
        cfg = staticfgCFGBuilder().build_from_file("cfg", code_path)
        # save the control flow graph as an SVG image
        cfg.build_visual(output_path, format="svg", show=False)
        # Clean up the temporary file
        Path(code_path).unlink(missing_ok=True)
        return output_path

    def create_temporary_file(self, code: str) -> Path:
        """Creates a temporary file with the source code."""
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".py"
        ) as temp_file:
            temp_file.write(code.encode("utf-8"))
            return Path(temp_file.name)
