#!/usr/bin/env python
# filepath: /home/olaf_van_huusen/amos_version_3/amos2025ss04-ai-driven-testing-1/backend/test_control_flow.py

"""
Test script for the ShowControlFlow module.
This script demonstrates how the control flow visualization works.
"""

from modules.show_control_flow import ControlFlowVisualizer
import os

# Sample Python code with various control structures
SAMPLE_CODE = """
def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

if __name__ == "__main__":
    main()
"""


def main():
    try:
        # Make sure output directory exists
        os.makedirs("outputs/control_flow", exist_ok=True)
        print("Starting control flow visualization test...")

        # Initialize the control flow visualizer
        visualizer = ControlFlowVisualizer()
        print("Visualizer initialized.")

        print("Parsing code...")
        # Parse code to blocks to debug
        blocks, edges = visualizer._parse_code_to_blocks(SAMPLE_CODE)
        print(f"Parsed {len(blocks)} blocks and {len(edges)} edges.")

        # Print blocks for debugging
        print("\nBlocks:")
        for block_id, block_data in blocks.items():
            print(
                f"Block {block_id} ({block_data['type']}): {block_data['statements']}"
            )

        # Generate the visualization
        print("\nGenerating visualization...")
        svg_path, dot_path = visualizer.visualize_code(SAMPLE_CODE)

        if svg_path:
            print("Control flow visualization created successfully!")
            print(f"SVG saved to: {svg_path}")
            print(f"DOT file saved to: {dot_path}")

            # Print the DOT file content
            print("\nDOT file content:")
            with open(dot_path, "r") as f:
                print(f.read())
        elif dot_path:
            print(
                "Failed to create SVG visualization, but DOT file was created."
            )
            print(f"DOT file saved to: {dot_path}")

            # Print the DOT file content
            print("\nDOT file content:")
            with open(dot_path, "r") as f:
                print(f.read())
        else:
            print("Failed to create control flow visualization.")
    except Exception as e:
        import traceback

        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
