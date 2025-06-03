import ast
import tokenize
from io import StringIO

class CCCCalculator(ast.NodeVisitor):
    """
    Calculates the CCC (Cognitive Code Complexity) for a given Python file
    based on the provided rules.

    The calculation is performed by traversing the Abstract Syntax Tree (AST)
    of the Python code and applying weights for various code structures.

    Interpretations made for specific rules due to Python's dynamic nature
    or rule ambiguities:
    - S_k (Size of executable statement): Approximated by counting significant
      AST nodes (names, constants, operators, calls, attributes, subscripts)
      within the statement.
    - W_i (Inheritance Level): Interpreted as the nesting depth of class
      definitions (e.g., top-level class = 0, nested class = 1).
    - W_n (Nesting): Interpreted as the nesting depth of control flow
      structures (if, for, while, try) for the current statement.
    - W_ad (Array Declarations): Interpreted as the creation of list, tuple,
      set, or dict literals. W_a (weight of array) is set to 1. S_ad (size
      of array dimension) is the number of elements/items.
    - W_cc (Compound Conditions): Each 'and' or 'or' operator within a
      conditional expression adds the W_c value of its enclosing control
      structure.
    - W_io (Input/Output Statements): Counts calls to 'input', 'print',
      and common file methods (open, read, write, close).
    """

    def __init__(self):
        self.total_ccc = 0
        self.current_nesting_level = 0
        self.class_nesting_level = 0
        self.function_stack = [] # To track current function for recursion detection
        self.function_recursion_counts = {} # {func_name: {call_name: count}}
        self.results = [] # Stores complexity details for each function/method

        # Common I/O functions/methods to look for
        self.io_functions = {'input', 'print', 'open'}
        self.io_methods = {'read', 'write', 'close'}

        # Weights for S_k approximation (significant nodes)
        self.sk_node_weights = {
            ast.Name: 1,
            ast.Constant: 1,
            ast.JoinedStr: 1,
            ast.FormattedValue: 1,
            ast.List: 1,
            ast.Tuple: 1,
            ast.Set: 1,
            ast.Dict: 1,
            ast.BinOp: 1,
            ast.UnaryOp: 1,
            ast.Compare: 1,
            ast.BoolOp: 1,
            ast.Call: 1,
            ast.Attribute: 1,
            ast.Subscript: 1,
        }

    def _get_sk_value(self, node):
        """
        Approximates S_k (size of executable statement) by counting significant
        nodes within the given AST node.
        """
        count = 0
        for child_node in ast.walk(node):
            if type(child_node) in self.sk_node_weights:
                count += self.sk_node_weights[type(child_node)]
            elif isinstance(child_node, (ast.List, ast.Tuple, ast.Set)):
                count += len(child_node.elts) # Count elements in literals
            elif isinstance(child_node, ast.Dict):
                count += len(child_node.keys) # Count key-value pairs
            #else:
                #count += 1
        return max(1, count) # Ensure S_k is at least 1

    def _calculate_statement_ccc(self, node, Wc_val=0):
        """
        Calculates the CCC for a single statement based on its context.
        """
        Sk = self._get_sk_value(node)
        Wc = Wc_val # Type of Control Structures
        Wi = self.class_nesting_level # Inheritance Level
        Wn = self.current_nesting_level # Nesting level of control structures

        # Base complexity for the statement
        statement_ccc = Sk * (Wc + Wi + Wn)

        # Additional weights (W_tc, W_rc, W_cc, W_ad, W_io) are handled
        # by specific visit methods and added to the total_ccc directly.
        # This formula structure is a bit unusual for a sum over k,
        # but I'll apply the additional weights as they are encountered
        # and add them to the running total.

        return statement_ccc

    def visit_FunctionDef(self, node):
        """Handle function definitions."""
        self.function_stack.append(node.name)
        self.function_recursion_counts[node.name] = {} # Reset recursion count for this function
        # Functions themselves don't add to CCC directly, but their body statements do.
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        """Handle async function definitions (similar to regular functions)."""
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        """Handle class definitions for W_n (inheritance level)."""
        self.class_nesting_level += 1
        self.generic_visit(node)
        self.class_nesting_level -= 1

    def visit_If(self, node):
        """Handle if/elif/else statements (W_c=1, W_i for nesting)."""
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=1)
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

    def visit_For(self, node):
        """Handle for loops (W_c=2, W_i for nesting)."""
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=2)
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

    def visit_While(self, node):
        """Handle while loops (W_c=2, W_i for nesting)."""
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=2)
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

    def visit_Try(self, node):
        """Handle try-except-finally blocks (W_tc, W_i for nesting)."""
        self.total_ccc += 1 # +1 for try
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

        # Handle except handlers (catch blocks)
        for handler in node.handlers:
            self.total_ccc += 1 # +1 for each catch (except)
            self.current_nesting_level += 1
            self.visit(handler) # Visit the handler node
            self.current_nesting_level -= 1

        # Handle finally block
        if node.finalbody:
            self.current_nesting_level += 1
            for stmt in node.finalbody:
                self.visit(stmt)
            self.current_nesting_level -= 1

    def visit_Match(self, node):
        """Handle match/case statements (W_c=n for n cases, W_i for nesting)."""
        Wc_val = len(node.cases) # n for switch statement with n cases
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=Wc_val)
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

    def visit_Break(self, node):
        """Handle break statements (considered a flow break, add to Sk * (Wc + Wn + Wi))."""
        # Break is a flow break, so it contributes to Wc. Let's assign Wc=1 for simplicity.
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=1)
        self.generic_visit(node)

    def visit_Continue(self, node):
        """Handle continue statements (considered a flow break, add to Sk * (Wc + Wn + Wi))."""
        # Continue is a flow break, so it contributes to Wc. Let's assign Wc=1 for simplicity.
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=1)
        self.generic_visit(node)

    def visit_Call(self, node):
        """Handle function calls for recursion and I/O."""
        current_func_name = self.function_stack[-1] if self.function_stack else None

        # Check for recursion (W_rc)
        if isinstance(node.func, ast.Name) and node.func.id == current_func_name:
            # This is a recursive call to the current function
            self.function_recursion_counts[current_func_name][node.func.id] = \
                self.function_recursion_counts[current_func_name].get(node.func.id, 0) + 1
            if self.function_recursion_counts[current_func_name][node.func.id] == 1:
                self.total_ccc += 1 # +1 for first recursive call
            else:
                self.total_ccc += 2 # +2 for each additional recursive call

        # Check for I/O statements (W_io)
        if isinstance(node.func, ast.Name) and node.func.id in self.io_functions:
            self.total_ccc += 1 # +1 for each input/output statement
        elif isinstance(node.func, ast.Attribute) and node.func.attr in self.io_methods:
            # Check if it's a method call on a file object (heuristic)
            # This is a simplification; a more robust check would involve type inference
            self.total_ccc += 1 # +1 for each input/output statement

        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Handle compound conditions (W_cc)."""
        # W_cc: for 'and' and 'or' the equal weight as the control structure they appear in.
        # This means if a BoolOp is inside an If (Wc=1), the BoolOp adds another 1.
        # This is a bit ambiguous, so I'll interpret it as adding the Wc of the
        # *enclosing* control structure for each 'and'/'or' operator.
        # We need to find the nearest enclosing control structure.
        # This is tricky with a simple visitor. I'll make a simplification:
        # if a BoolOp is encountered, and we are inside a control structure,
        # add the Wc value of a typical control structure (e.g., 1 for if/else).
        # This assumes the BoolOp is part of a conditional.
        if self.current_nesting_level > 0: # If we are inside any control structure
            # Assign a Wc value for the compound condition itself.
            # The rule says "equal weight as the control structure they appear in".
            # Let's use 1 (like an if statement) for each 'and'/'or' operator.
            self.total_ccc += len(node.values) - 1 # Number of operators (e.g., a and b and c has 2 'and's)
        self.generic_visit(node)

    def visit_List(self, node):
        """Handle list literals for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, len(node.elts))
        self.generic_visit(node)

    def visit_Tuple(self, node):
        """Handle tuple literals for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, len(node.elts))
        self.generic_visit(node)

    def visit_Set(self, node):
        """Handle set literals for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, len(node.elts))
        self.generic_visit(node)

    def visit_Dict(self, node):
        """Handle dict literals for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, len(node.keys))
        self.generic_visit(node)

    def visit_ListComp(self, node):
        """Handle list comprehensions for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, 1) # Treat as 1 dimension/size for comprehension
        self.generic_visit(node)

    def visit_SetComp(self, node):
        """Handle set comprehensions for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, 1)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        """Handle dict comprehensions for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, 1)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        """Handle generator expressions for W_ad (Array Declarations)."""
        self._handle_array_declaration(node, 1)
        self.generic_visit(node)

    def _handle_array_declaration(self, node, size_ad):
        """Helper for W_ad calculation."""
        Wa = 1 # Weight of array (default constant)
        self.total_ccc += Wa * size_ad

    def calculate_ccc(self, code_string):
        """
        Parses the code string and calculates its CCC.
        """
        self.total_ccc = 0
        self.current_nesting_level = 0
        self.class_nesting_level = 0
        self.function_stack = []
        self.function_recursion_counts = {}
        self.results = []

        tree = ast.parse(code_string)
        self.visit(tree)
        return self.total_ccc

def get_ccc_for_file(filepath):
    """
    Reads a Python file and calculates its CCC.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code_string = f.read()
        calculator = CCCCalculator()
        ccc_score = calculator.calculate_ccc(code_string)
        return ccc_score
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Examples ---
if __name__ == "__main__":
    # Example 1: Simple Sequential Code
    code_1 = """
def greet(name):
    message = f"Hello, {name}!"
    print(message)
    return message
"""
    print(f"--- Example 1 (Simple Sequential) ---")
    calculator = CCCCalculator()
    ccc_score_1 = calculator.calculate_ccc(code_1)
    # Expected: S_k for each statement (e.g., 1 for assignment, 1 for print, 1 for return).
    # Wc=0, Wn=0, Wi=0. W_io for print.
    # Roughly: (1*0) + (1*0) + (1*0) + 1 (print) = 1
    # Let's trace more carefully:
    # message = f"Hello, {name}!" -> Sk=3 (message, name, "Hello, {}!") * (0+0+0) = 0
    # print(message) -> Sk=2 (print, message) * (0+0+0) + W_io=1 = 1
    # return message -> Sk=2 (return, message) * (0+0+0) = 0
    # Total based on my interpretation: 1 (for print)
    print(f"Code:\n{code_1}")
    print(f"CCC Score: {ccc_score_1}\n")

    # Example 2: Basic Conditional and Loop
    code_2 = """
def check_number(num):
    if num > 0: # Wc=1, Wi=0
        for i in range(num): # Wc=2, Wi=1
            if i % 2 == 0: # Wc=1, Wi=2
                print(f"{i} is even") # W_io=1
            else:
                print(f"{i} is odd") # W_io=1
    elif num == 0: # Wc=1, Wi=0
        print("Zero") # W_io=1
    else:
        print("Negative") # W_io=1
"""
    print(f"--- Example 2 (Conditional and Loop) ---")
    calculator = CCCCalculator()
    ccc_score_2 = calculator.calculate_ccc(code_2)
    # Let's manually trace based on the rules and interpretations:
    # 1. if num > 0:
    #    Sk (if) approx 3 (num, >, 0)
    #    Wc=1, Wn=0, Wi=0
    #    Contribution: Sk * (1+0+0) = 3
    #    Current nesting level = 1

    # 2. for i in range(num):
    #    Sk (for) approx 3 (i, range, num)
    #    Wc=2, Wn=0, Wi=1
    #    Contribution: Sk * (2+0+1) = 3 * 3 = 9
    #    Current nesting level = 2

    # 3. if i % 2 == 0: (inside for)
    #    Sk (if) approx 4 (i, %, 2, ==, 0)
    #    Wc=1, Wn=0, Wi=2
    #    Contribution: Sk * (1+0+2) = 4 * 3 = 12
    #    Current nesting level = 3

    # 4. print(f"{i} is even") (inside inner if)
    #    Sk (print) approx 2 (print, i)
    #    Wc=0, Wn=0, Wi=3
    #    Contribution: Sk * (0+0+3) = 2 * 3 = 6
    #    W_io = +1
    #    Total for this line: 6 + 1 = 7

    # 5. print(f"{i} is odd") (inside else of inner if)
    #    Sk (print) approx 2 (print, i)
    #    Wc=0, Wn=0, Wi=3
    #    Contribution: Sk * (0+0+3) = 2 * 3 = 6
    #    W_io = +1
    #    Total for this line: 6 + 1 = 7

    # 6. elif num == 0: (top-level elif)
    #    Sk (elif) approx 3 (num, ==, 0)
    #    Wc=1, Wn=0, Wi=0
    #    Contribution: Sk * (1+0+0) = 3
    #    Current nesting level = 1 (after first if block, but before this elif)

    # 7. print("Zero") (inside elif)
    #    Sk (print) approx 1 (print)
    #    Wc=0, Wn=0, Wi=1
    #    Contribution: Sk * (0+0+1) = 1
    #    W_io = +1
    #    Total for this line: 1 + 1 = 2

    # 8. else: (top-level else)
    #    Sk (else) approx 0 (no specific nodes, just block)
    #    Wc=0, Wn=0, Wi=0 (context of the else block is top level)
    #    Contribution: 0 (else itself doesn't add base Sk, but its body does)
    #    Current nesting level = 1

    # 9. print("Negative") (inside else)
    #    Sk (print) approx 1 (print)
    #    Wc=0, Wn=0, Wi=1
    #    Contribution: Sk * (0+0+1) = 1
    #    W_io = +1
    #    Total for this line: 1 + 1 = 2

    # Summing up contributions:
    # 3 (if) + 9 (for) + 12 (inner if) + 7 (print even) + 7 (print odd) + 3 (elif) + 2 (print zero) + 2 (print negative)
    # = 45 (This is a rough manual estimate, actual will depend on precise Sk and AST traversal)

    print(f"Code:\n{code_2}")
    print(f"CCC Score: {ccc_score_2}\n")


    # Example 3: Class with Inheritance-like nesting, Try-Except, Recursion, Compound Condition, Array Decl
    code_3 = """
class BaseProcessor: # Wn=0
    def __init__(self, data):
        self.data = data
        self.processed_list = [] # W_ad for list literal

    def process(self):
        pass

class AdvancedProcessor(BaseProcessor): # Wn=1 (nested within conceptual hierarchy)
    def __init__(self, data):
        super().__init__(data)

    def recursive_sum(self, n): # Wn=1 for statements inside this method
        if n <= 0: # Wc=1, Wi=0
            return 0
        else:
            # Compound condition: n > 0 and n % 2 == 0
            if n > 0 and n % 2 == 0: # Wc=1, Wi=1, Wcc for 'and'
                try: # W_tc=1, Wi=2
                    result = n + self.recursive_sum(n - 1) # W_rc=1 (first recursion)
                    return result
                except Exception as e: # W_tc=1, Wi=3
                    print(f"Error: {e}") # W_io=1
                    return 0
            return n + self.recursive_sum(n - 1) # W_rc=2 (additional recursion)

def main():
    my_data = [1, 2, 3] # W_ad for list literal
    processor = AdvancedProcessor(my_data)
    total = processor.recursive_sum(5)
    print(f"Total sum: {total}") # W_io=1
"""
    print(f"--- Example 3 (Complex Scenario) ---")
    calculator = CCCCalculator()
    ccc_score_3 = calculator.calculate_ccc(code_3)
    print(f"Code:\n{code_3}")
    print(f"CCC Score: {ccc_score_3}\n")

    # Example 4: Match/Case (Python 3.10+)
    code_4 = """
def get_status_message(status_code):
    match status_code: # Wc=n (number of cases)
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown Status"
"""
    print(f"--- Example 4 (Match/Case) ---")
    calculator = CCCCalculator()
    ccc_score_4 = calculator.calculate_ccc(code_4)
    # Expected: Wc = 4 (for 4 cases) * Sk + ...
    print(f"Code:\n{code_4}")
    print(f"CCC Score: {ccc_score_4}\n")
    code_5 = """
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
    print(f"--- Example 5 (from Paper) ---")
    calculator = CCCCalculator()
    ccc_score_5 = calculator.calculate_ccc(code_5)
    # Expected: 255
    print(f"Code:\n{code_5}")
    print(f"CCC Score: {ccc_score_5}\n")
