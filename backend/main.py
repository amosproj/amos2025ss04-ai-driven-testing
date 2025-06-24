#!/usr/bin/env python3
"""Main script to run a single model test generation pipeline.

This script serves as the primary entry point for the command-line interface.
It orchestrates the entire process by:
1. Parsing command-line arguments using the `cli` module.
2. Loading the specified model and modules.
3. Building the initial prompt data structure.
4. Executing the prompt-response-refinement loop via the `execution` module.
"""

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

    # Print active modules (from the development branch)
    print("active modules:")
    for module in active_modules:
        print(f"- {module.__class__.__name__}")

    # Execute the flow, passing the new iterations argument (from your branch)
    execution.execute_prompt(
        active_modules=active_modules,
        prompt_data=prompt_data,
        output_file=args.output_file,
        iterations=args.iterations,
    )
