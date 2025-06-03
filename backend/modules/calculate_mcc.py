import sys
from radon.complexity import cc_visit
from radon.raw import analyze

def calculate_mccabe_complexity(filepath):
    """
    Calculates McCabe's Cyclomatic Complexity for a given Python file.

    Args:
        filepath (str): The path to the Python file.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary where keys are function/method names and values
                    are their cyclomatic complexity scores.
            - int: The total cyclomatic complexity for the file (sum of all scores).
            - str: An error message if the file cannot be read, otherwise None.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        return {}, 0, f"Error: File not found at '{filepath}'"
    except Exception as e:
        return {}, 0, f"Error reading file '{filepath}': {e}"

    complexities = {}
    total_complexity = 0

    try:
        # Use cc_visit to get complexity of blocks (functions, methods, classes)
        # It returns a list of Complexity objects
        for item in cc_visit(code):
            # The 'name' attribute holds the function/method/class name
            # The 'complexity' attribute holds the cyclomatic complexity score
            complexities[item.name] = item.complexity
            total_complexity += item.complexity
    except Exception as e:
        return {}, 0, f"Error calculating complexity for '{filepath}': {e}"

    return complexities, total_complexity, None

if __name__ == "__main__":

    python_file = "/home/olaf_van_huusen/amos2025ss04-ai-driven-testing/backend/mcc_test_file.py"
    
    print(f"Calculating McCabe's Cyclomatic Complexity for: {python_file}")
    
    function_complexities, total_cc, error_message = calculate_mccabe_complexity(python_file)

    if error_message:
        print(error_message)
    else:
        if function_complexities:
            print("\nComplexity per function/method/class:")
            for name, complexity in function_complexities.items():
                print(f"  {name}: {complexity}")
            print(f"\nTotal Cyclomatic Complexity for the file: {total_cc}")
        else:
            print("No functions, methods, or classes found to analyze for complexity.")
            print(f"\nTotal Cyclomatic Complexity for the file (likely 0 as no blocks found): {total_cc}")