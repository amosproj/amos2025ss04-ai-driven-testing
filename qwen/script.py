"""Command execution utility for Ollama model management.

This module handles the execution of terminal commands for creating, running,
and removing Ollama models. It executes a sequence of commands in a specified
directory, captures their output, and provides status feedback during the process.
"""

import subprocess
from pathlib import Path

from specifications import model_name, script_directory


def execute_commands_in_directory(directory, commands):
    """
    Execute a list of terminal commands in a specified directory.

    Args:
        directory (str): Path to the directory where commands should be executed.
        commands (list): List of commands to execute.

    Returns:
        bool: True if all commands succeed, False otherwise.
    """
    try:
        # Convert string path to Path object for better handling
        target_dir = Path(directory)

        # Verify the directory exists
        if not target_dir.exists():
            raise FileNotFoundError(f"Directory {directory} does not exist")

        # Execute each command in sequence
        for cmd in commands:
            print(f"\n{'=' * 50}")
            print(f"Executing command: {cmd}")
            print(f"In directory: {target_dir}")
            print(f"{'=' * 50}\n")

            result = subprocess.run(
                cmd,
                cwd=str(target_dir),
                shell=True,
                capture_output=True,
                text=True,
            )

            # Print command output
            if result.stdout:
                print("Standard Output:")
                print(result.stdout)

            # Print error output if any
            if result.stderr:
                print("\nError Output:")
                print(result.stderr)

            # Check if command failed
            if result.returncode != 0:
                print(f"\nCommand failed with exit code {result.returncode}")
                return False

        return True

    except Exception as e:
        print(f"\nUnexpected error occurred: {str(e)}")
        return False


# List of commands to execute
commands_to_run = [
    "ollama create " + model_name + " -f ./modelfile",  # Create the model
    "python code_analysis_bot.py",  # Run the instructions to create the test
    "ollama rm " + model_name,  # remove model after use
]

# Execute the commands
success = execute_commands_in_directory(script_directory, commands_to_run)

print("\n" + "=" * 50)
print(f"Final Status: {'SUCCESS' if success else 'FAILED'}")
print("=" * 50)
