#!/usr/bin/env python3
import os
import cli
import execution
import module_manager
import model_manager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Parse command-line arguments
    args = cli.parse_arguments()

    promp_data = cli.build_prompt_data(args)

    # Get model information
    model = model_manager.load_models()[args.model]
    print("using model:")
    print(model)

    # Load modules
    active_modules = module_manager.load_modules(args.modules)

    # load prompt text
    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    # Execute the flow
    execution.execute_prompt(
        model, active_modules, prompt_text, args.output_file
    )
