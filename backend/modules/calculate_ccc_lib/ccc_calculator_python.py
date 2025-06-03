import ast
import warnings


class CCCCalculator(ast.NodeVisitor):
    """
    Calculates the CCC (Cognitive Code Complexity) for a given Python file.

    The calculation is performed by traversing the Abstract Syntax Tree (AST)
    of the Python code and calculating the complexity based on the rules provided at https://github.com/amosproj/amos2025ss04-ai-driven-testing/wiki/Code-Complexity
    """

    def __init__(self):
        self.total_ccc = 0
        self.current_nesting_level = 0
        self.class_nesting_level = 0
        self.function_stack = (
            []
        )  # To track current function for recursion detection
        self.function_recursion_counts = {}  # {func_name: {call_name: count}}
        self.results = []  # Stores complexity details for each function/method

        # Common I/O functions/methods to look for
        self.io_functions = {"input", "print", "open"}
        self.io_methods = {"read", "write", "close"}

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
                count += len(child_node.elts)  # Count elements in literals
            elif isinstance(child_node, ast.Dict):
                count += len(child_node.keys)  # Count key-value pairs
            # else:
            # count += 1
        return max(1, count)  # Ensure S_k is at least 1

    def _calculate_statement_ccc(self, node, Wc_val=0):
        """
        Calculates the CCC for a single statement based on its context.
        """
        Sk = self._get_sk_value(node)
        Wc = Wc_val  # Type of Control Structures
        Wi = self.class_nesting_level  # Inheritance Level
        Wn = self.current_nesting_level  # Nesting level of control structures

        # Base complexity for the statement
        statement_ccc = Sk * (Wc + Wi + Wn)

        return statement_ccc

    def visit_FunctionDef(self, node):
        """Handle function definitions."""
        self.function_stack.append(node.name)
        self.function_recursion_counts[node.name] = (
            {}
        )  # Reset recursion count for this function
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
        self.total_ccc += 1  # +1 for try
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

        # Handle except handlers (catch blocks)
        for handler in node.handlers:
            self.total_ccc += 1  # +1 for each catch (except)
            self.current_nesting_level += 1
            self.visit(handler)  # Visit the handler node
            self.current_nesting_level -= 1

        # Handle finally block
        if node.finalbody:
            self.current_nesting_level += 1
            for stmt in node.finalbody:
                self.visit(stmt)
            self.current_nesting_level -= 1

    def visit_Match(self, node):
        """Handle match/case statements (W_c=n for n cases, W_i for nesting)."""
        Wc_val = len(node.cases)  # n for switch statement with n cases
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=Wc_val)
        self.current_nesting_level += 1
        self.generic_visit(node)
        self.current_nesting_level -= 1

    def visit_Break(self, node):
        """Handle break statements (considered a flow break, add to Sk * (Wc + Wn + Wi))."""
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=1)
        self.generic_visit(node)

    def visit_Continue(self, node):
        """Handle continue statements (considered a flow break, add to Sk * (Wc + Wn + Wi))."""
        self.total_ccc += self._calculate_statement_ccc(node, Wc_val=1)
        self.generic_visit(node)

    def visit_Call(self, node):
        """Handle function calls for recursion and I/O."""
        current_func_name = (
            self.function_stack[-1] if self.function_stack else None
        )

        # Check for recursion (W_rc)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == current_func_name
        ):
            # This is a recursive call to the current function
            self.function_recursion_counts[current_func_name][node.func.id] = (
                self.function_recursion_counts[current_func_name].get(
                    node.func.id, 0
                )
                + 1
            )
            if (
                self.function_recursion_counts[current_func_name][node.func.id]
                == 1
            ):
                self.total_ccc += 1  # +1 for first recursive call
            else:
                self.total_ccc += 2  # +2 for each additional recursive call

        # Check for I/O statements (W_io)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in self.io_functions
        ):
            self.total_ccc += 1  # +1 for each input/output statement
        elif (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in self.io_methods
        ):
            self.total_ccc += 1  # +1 for each input/output statement

        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Handle compound conditions (W_cc)."""
        if (
            self.current_nesting_level > 0
        ):  # If we are inside any control structure
            self.total_ccc += (
                len(node.values) - 1
            )  # Number of operators (e.g., a and b and c has 2 'and's)
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
        self._handle_array_declaration(
            node, 1
        )  # Treat as 1 dimension/size for comprehension
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
        Wa = 1  # Weight of array (default constant)
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
        with open(filepath, "r", encoding="utf-8") as f:
            code_string = f.read()
        calculator = CCCCalculator()
        ccc_score = calculator.calculate_ccc(code_string)
        return ccc_score
    except FileNotFoundError:
        warnings.warn(f"File not found: {filepath}")
        return None
    except Exception as e:
        warnings.warn(f"Error processing file {filepath}: {e}")
        return None
