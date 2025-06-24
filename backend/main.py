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

    # Get model information
    model = model_manager.load_models()[args.model]
    print("using model:")
    print(model)

    prompt_data = cli.build_prompt_data(args, model)

    # Load modules
    active_modules = module_manager.load_modules(args.modules)
    # Save type of ordering for modules
    module_manager.ORDER = args.order

    print("active modules:")
    for module in active_modules:
        print(f" - {module.__class__.__name__}")

    # Execute the flow
    execution.execute_prompt(active_modules, prompt_data, args.output_file)
