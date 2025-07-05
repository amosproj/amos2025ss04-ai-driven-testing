#!/usr/bin/env python3
"""Main entry point for AI-Driven Testing CLI."""
import os
import cli
import execution
import module_manager
import model_manager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Parse command-line arguments
    args = cli.parse_arguments()

    # Validate export arguments
    cli.validate_export_args(args)

    # Get model information
    model = model_manager.load_models()[args.model]
    print("using model:")
    print(model)

    prompt_data = cli.build_prompt_data(args, model)

    # Load modules
    active_modules = module_manager.load_modules(args.modules)
    # Save type of ordering for modules
    module_manager.COMMAND_ORDER = args.order

    print("active modules:")
    for module in active_modules:
        print(f" - {module.__class__.__name__}")

    # Execute the flow
    response_content = execution.execute_prompt(
        active_modules, prompt_data, args.output_file
    )

    # Handle export if requested
    if response_content and (args.export_format or args.export_all):
        cli.handle_export(args, response_content, args.output_file)
