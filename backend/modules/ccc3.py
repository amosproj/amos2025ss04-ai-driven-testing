import re
import tokenize
from io import BytesIO

def get_tokens(line):
    """
    Counts tokens in a line. A simplified tokenizer.
    Considers operators, operands, methods/functions, and strings.
    """
    tokens = []
    try:
        # Use Python's built-in tokenize module for better accuracy
        # It expects bytes-like object
        for toknum, tokval, _, _, _ in tokenize.tokenize(BytesIO(line.encode('utf-8')).readline):
            # Ignore whitespace and comments
            if toknum not in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING, tokenize.NL, tokenize.COMMENT):
                tokens.append(tokval)
    except tokenize.TokenError:
        # Fallback for malformed lines if tokenize fails
        tokens = re.findall(r'\b\w+\b|[+\-*/%&|=!<>~^@]', line)
    return len(tokens)

def calculate_Wc(line):
    """
    Calculates W_c (Type of Control Structures) for a given line.
    """
    line = line.strip()
    if not line:
        return 0

    if re.match(r'^\s*(if|elif|else):', line):
        return 1
    elif re.match(r'^\s*(while|for)\s.*:', line):
        return 2
    elif re.match(r'^\s*match\s.*:', line): # Python 3.10+ structural pattern matching
        return 1 # Base for match
    elif re.match(r'^\s*case\s.*:', line):
        return 1 # Each case adds 1
    return 0

def calculate_Wn(current_indentation, class_indentations):
    """
    Calculates W_n (Inheritance Level of Statements).
    Requires tracking class indentations.
    """
    if not class_indentations:
        return 0 # Not inside any class
    
    # Find the deepest class indentation that the current line is within
    deepest_class_level = -1
    for indent_level, _ in class_indentations:
        if current_indentation > indent_level:
            deepest_class_level = max(deepest_class_level, indent_level)
    
    if deepest_class_level == -1:
        return 0 # Not inside a class or not deeper than any known class

    # Calculate Wn based on the level of nesting relative to the outermost class
    # For simplicity, we assume each deeper class adds to the inheritance level.
    # This is still a heuristic.
    level = 0
    for i, (indent, _) in enumerate(class_indentations):
        if current_indentation > indent:
            level = i + 1
    return level

def calculate_Wtc(line):
    """
    Calculates W_tc (Try-Catch Blocks).
    """
    weight = 0
    if 'try:' in line:
        weight += 1
    if 'except' in line:
        weight += 1
    return weight

def calculate_Wrc(line, method_name_stack):
    """
    Calculates W_rc (Recursive Calls).
    This is highly heuristic for line-by-line analysis.
    It checks if the current line (presumably inside a function) calls the current function.
    """
    weight = 0
    if method_name_stack:
        current_method = method_name_stack[-1]
        # Check if the current method name is called within the line
        # This is a very weak heuristic for recursion
        if re.search(r'\b' + re.escape(current_method) + r'\s*\(', line):
            # This logic for "additional recursive call" is hard without call tracking.
            # We'll just add 1 for any detected call.
            # A more robust solution would require analyzing the call graph.
            weight += 1
    return weight

def calculate_Wad(line):
    """
    Calculates W_ad (Array Declarations).
    For Python, this typically means list/tuple initializations.
    W_a := Weight of array (arbitrarily set to 1 for simplicity)
    S_ad := Size of array dimension (number of elements initially)
    """
    weight = 0
    # Match list or tuple declarations with initial elements
    match_list = re.search(r'=\s*\[(.*?)\]', line)
    match_tuple = re.search(r'=\s*\((.*?)\)', line)

    elements_count = 0
    if match_list:
        elements_str = match_list.group(1).strip()
        if elements_str:
            elements_count = len(elements_str.split(','))
    elif match_tuple:
        elements_str = match_tuple.group(1).strip()
        if elements_str:
            elements_count = len(elements_str.split(','))
            if elements_count == 1 and not elements_str.endswith(','): # Handle single-element tuple without comma
                 elements_count = 0 # It might be just an expression in parentheses
            elif elements_count == 0 and elements_str == "":
                elements_count = 0 # Empty tuple/list
            elif elements_count > 0 and not elements_str.strip(): # Handles cases like "(), []"
                elements_count = 0

    W_a = 1 # Arbitrary weight for array
    weight = W_a * elements_count
    return weight

def calculate_Wcc(line, latest_control_weight):
    """
    Calculates W_cc (Compound Conditions).
    Assigns the weight of the control structure they appear in.
    """
    weight = 0
    if latest_control_weight > 0: # Only if inside a control structure
        if ' and ' in line or ' or ' in line:
            # For each occurrence of 'and' or 'or', add the control structure's weight.
            weight += (line.count(' and ') + line.count(' or ')) * latest_control_weight
    return weight

def calculate_Wio(line):
    """
    Calculates W_io (Input/Output Statements).
    Looks for common Python I/O functions.
    """
    weight = 0
    # Common input/output functions in Python
    io_patterns = ['input(', 'print(', 'open(', '.read(', '.write(', '.close(']
    for pattern in io_patterns:
        if pattern in line:
            weight += 1
    return weight

def get_indentation_level(line):
    """Returns the number of leading spaces for indentation."""
    return len(line) - len(line.lstrip(' '))

def calculate_ccc(file_path):
    """
    Calculates the CCC (Cognitive Complexity for Code) for a given Python file
    and prints the CCC per line for debugging.
    """
    total_ccc = 0
    previous_indentation = 0
    current_control_weight = 0
    
    # To track inheritance levels (indentation, class_name)
    class_indentations = [] 
    
    # To track current method for recursive calls heuristic
    method_name_stack = [] 

    print(f"\n--- CCC Calculation Details for '{file_path}' ---")
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'): # Skip empty lines and comments
                # print(f"Line {line_num}: (Skipped - Empty or Comment) CCC = 0")
                continue

            current_indentation = get_indentation_level(line)

            # Update inheritance level tracking
            if 'class ' in stripped_line and stripped_line.endswith(':'):
                class_name_match = re.search(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:(]', stripped_line)
                if class_name_match:
                    class_name = class_name_match.group(1)
                    # Pop out classes that are at a shallower or same indentation level
                    while class_indentations and class_indentations[-1][0] >= current_indentation:
                        class_indentations.pop()
                    class_indentations.append((current_indentation, class_name))
            else:
                # If indentation decreases, pop out classes that are no longer in scope
                while class_indentations and class_indentations[-1][0] >= current_indentation:
                    class_indentations.pop()

            # Update method name stack tracking for recursive calls
            if 'def ' in stripped_line and stripped_line.endswith(':'):
                method_name_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', stripped_line)
                if method_name_match:
                    method_name = method_name_match.group(1)
                    # Pop out methods that are at a shallower or same indentation level
                    while method_name_stack and get_indentation_level(line) <= previous_indentation and not any(cls[0] == current_indentation for cls in class_indentations if 'class' in line): # This is a crude way to handle scope
                        method_name_stack.pop() # Pop functions if indentation goes back. Needs refinement.
                    method_name_stack.append(method_name)
            elif method_name_stack and current_indentation <= previous_indentation and not any(cls[0] == current_indentation for cls in class_indentations if 'class' in line):
                 # Heuristic: if indentation goes back, assume we've exited the method
                 if method_name_stack:
                     method_name_stack.pop() # Pop current method

            # CCC calculation for the current line
            ccc_line = 0

            S_k = get_tokens(line)
            W_c = calculate_Wc(line)
            current_control_weight = W_c # Update current control weight for compound conditions
            W_n = calculate_Wn(current_indentation, class_indentations)
            W_tc = calculate_Wtc(line)
            W_rc = calculate_Wrc(line, method_name_stack)
            W_ad = calculate_Wad(line)
            W_cc = calculate_Wcc(line, current_control_weight)
            W_io = calculate_Wio(line)
            
            # CCC_line = S_k * (W_c + W_n) + W_tc + W_rc + W_ad + W_cc + W_io
            ccc_line = (S_k * (W_c + W_n)) + W_tc + W_rc + W_ad + W_cc + W_io

            total_ccc += ccc_line
            previous_indentation = current_indentation
            
            print(f"Line {line_num}: CCC = {ccc_line} | {stripped_line.strip()}")

    print(f"--- End of CCC Calculation Details ---")
    return total_ccc

# Example Usage:
if __name__ == "__main__":
    # Create a dummy Python file for testing
    dummy_code = """
import os

class BaseClass:
    def __init__(self, data):
        self.data = data

    def process(self, value):
        # Sequential statement
        result = value * 2
        print(f"Processing data: {result}") # I/O statement

class DerivedClass(BaseClass):
    def __init__(self, data, config):
        super().__init__(data)
        self.config = config

    def complex_logic(self, num_iterations, input_list):
        if num_iterations > 0 and self.data > 10: # Decision-making, compound condition
            for i in range(num_iterations): # Decision-making (for loop)
                try: # Try-catch block
                    if i % 2 == 0:
                        self.data += i
                    else:
                        self.data -= i
                    my_array = [1, 2, 3, 4, 5] # Array declaration
                    if self.recursive_call(num_iterations - 1): # Recursive call (heuristic)
                         print("Recursion happened!") # I/O
                except ValueError as e: # Try-catch block
                    print(f"Error: {e}") # I/O statement
                finally:
                    pass
            while self.data < 100: # Decision-making (while loop)
                self.data += 1
        elif self.data == 0:
            pass # Sequential statement
        else:
            print("Another branch") # I/O statement
        return self.data

    def recursive_call(self, n):
        if n <= 0:
            return False
        return self.recursive_call(n - 1) # Additional recursive call of the same method
        
def main():
    b_obj = BaseClass(5)
    b_obj.process(10)

    d_obj = DerivedClass(15, {"mode": "test"})
    final_data = d_obj.complex_logic(3, [1,2,3])
    print(f"Final data: {final_data}") # I/O

if __name__ == "__main__":
    main()
"""
    
    file_name = "test_code.py"
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(dummy_code)

    ccc_score = calculate_ccc(file_name)
    print(f"\nTotal CCC for '{file_name}': {ccc_score}")

    # You can also test with an empty file or a simple file
    with open("empty_file.py", "w") as f:
        f.write("")
    ccc_score_empty = calculate_ccc("empty_file.py")
    print(f"\nTotal CCC for 'empty_file.py': {ccc_score_empty}")

    simple_code = """
class ComplexityExample:

    @staticmethod
    def main():
        x = 10
        y = 20
        a = 5

        if (x > y) and (x > a):
            for i in range(5):
                print(f"Loop iteration: {i + 1}")
                try:
                    result = x // y
                    print("Result: ", result)
                except ZeroDivisionError:
                    print("Error: Division by zero")
        else:
            sum_ = x + y
            print("Sum = ", sum_)

            nums = [1, 2, 3, 4, 5]
            factorial = ComplexityExample.calculate_factorial(5)
            print("Factorial of 5: ", factorial)

            if sum_ > 15:
                print("Sum is greater than 15")
            else:
                print("Sum is not greater than 15")

    @staticmethod
    def calculate_factorial(n):
        if n <= 1:
            return 1
        else:
            return n * ComplexityExample.calculate_factorial(n - 1)
"""
    with open("simple_code.py", "w") as f:
        f.write(simple_code)
    ccc_score_simple = calculate_ccc("simple_code.py")
    print(f"\nTotal CCC for 'simple_code.py': {ccc_score_simple}")