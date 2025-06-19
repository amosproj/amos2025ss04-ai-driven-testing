import os
import ast
import uuid
from pathlib import Path
from modules.base import ModuleBase
from schemas import PromptData, ResponseData
import graphviz


class ShowControlFlow(ModuleBase):
    """Module that visualizes control flow from code and saves it as an image."""

    def __init__(self):
        self.visualizer = ControlFlowVisualizer()

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        """Process source code in the prompt and create a control flow visualization."""
        source_code = prompt_data.input.source_code
        if source_code and source_code.strip():
            # Generate visualization
            image_path, dot_path = self.visualizer.visualize_code(source_code)
            if image_path:
                # Store the image path in the prompt data
                prompt_data.prompt_code_path = image_path
                print(
                    f"Control flow visualization for prompt saved to: {image_path}"
                )
                print(f"DOT file saved to: {dot_path}")

        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """Process output code in the response and create a control flow visualization."""
        output_code = response_data.output.code
        if output_code and output_code.strip():
            # Generate visualization
            image_path, dot_path = self.visualizer.visualize_code(output_code)
            if image_path:
                # Store the image path in the response data
                response_data.output.output_code_path = image_path
                print(
                    f"Control flow visualization for response saved to: {image_path}"
                )
                print(f"DOT file saved to: {dot_path}")

        return response_data


class ControlFlowVisualizer:
    """Helper class to visualize control flow from Python code as GraphViz diagrams."""

    def __init__(self):
        self.output_dir = Path("outputs/control_flow")
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def _parse_code_to_blocks(self, code_str):
        """Parse Python code and build control flow blocks using AST."""
        try:
            # Parse the code into an AST
            tree = ast.parse(code_str)

            # Dictionary to store blocks of code
            blocks = {}
            edges = []

            # Dictionary to track function definitions for recursive calls
            function_blocks = {}

            # Counter for block IDs
            block_counter = 1

            # Add ENTRY and EXIT nodes
            entry_id = "ENTRY"
            exit_id = "EXIT"
            blocks[entry_id] = {"statements": ["ENTRY"], "type": "entry"}
            blocks[exit_id] = {"statements": ["EXIT"], "type": "exit"}

            # Helper function to get a string representation of an AST node
            def get_node_code(node):
                if isinstance(node, ast.Compare):
                    left = get_node_code(node.left)
                    ops = []
                    rights = []
                    for op, right in zip(node.ops, node.comparators):
                        if isinstance(op, ast.Eq):
                            ops.append("==")
                        elif isinstance(op, ast.NotEq):
                            ops.append("!=")
                        elif isinstance(op, ast.Lt):
                            ops.append("<")
                        elif isinstance(op, ast.LtE):
                            ops.append("<=")
                        elif isinstance(op, ast.Gt):
                            ops.append(">")
                        elif isinstance(op, ast.GtE):
                            ops.append(">=")
                        else:
                            ops.append(str(type(op).__name__))

                        rights.append(get_node_code(right))

                    return " ".join(
                        [left]
                        + [f"{op} {right}" for op, right in zip(ops, rights)]
                    )

                elif isinstance(node, ast.BinOp):
                    left = get_node_code(node.left)
                    right = get_node_code(node.right)

                    if isinstance(node.op, ast.Add):
                        op = "+"
                    elif isinstance(node.op, ast.Sub):
                        op = "-"
                    elif isinstance(node.op, ast.Mult):
                        op = "*"
                    elif isinstance(node.op, ast.Div):
                        op = "/"
                    else:
                        op = str(type(node.op).__name__)

                    return f"{left} {op} {right}"

                elif isinstance(node, ast.Attribute):
                    # Properly render attribute access (obj.attr)
                    value = get_node_code(node.value)
                    return f"{value}.{node.attr}"

                elif isinstance(node, ast.Name):
                    return node.id

                elif isinstance(node, ast.Constant):
                    return str(node.value)

                elif isinstance(node, ast.Call):
                    func_name = get_node_code(node.func)
                    args = []
                    for arg in node.args:
                        args.append(get_node_code(arg))
                    return f"{func_name}({', '.join(args)})"

                elif isinstance(node, ast.Subscript):
                    # Handle subscript access (e.g., self.visited[node], arr[i])
                    value = get_node_code(node.value)
                    slice_val = get_node_code(node.slice)
                    return f"{value}[{slice_val}]"

                elif isinstance(node, ast.List):
                    # Handle list literals
                    elts = []
                    for elt in node.elts:
                        elts.append(get_node_code(elt))
                    return f"[{', '.join(elts)}]"

                elif isinstance(node, ast.UnaryOp):
                    # Handle unary operations like 'not', '-', '+'
                    operand = get_node_code(node.operand)
                    if isinstance(node.op, ast.Not):
                        return f"not {operand}"
                    elif isinstance(node.op, ast.UAdd):
                        return f"+{operand}"
                    elif isinstance(node.op, ast.USub):
                        return f"-{operand}"
                    else:
                        return f"{type(node.op).__name__} {operand}"

                else:
                    return str(type(node).__name__)

            # Helper function to create a new block
            def create_block(block_type="basic", statements=None):
                nonlocal block_counter
                block_id = f"B{block_counter}"
                block_counter += 1
                # Initialize with empty list if statements is None, otherwise use provided statements
                block_statements = statements if statements is not None else []
                blocks[block_id] = {
                    "statements": block_statements,
                    "type": block_type,
                }
                return block_id

            # Helper function to add an edge between blocks
            def add_edge(from_block, to_block, label=None):
                edge = {"from": from_block, "to": to_block}
                if label:
                    edge["label"] = label
                if edge not in edges:
                    edges.append(edge)

            # Process functions separately to create better graph structure
            functions = {}
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    functions[node.name] = node

            # Helper function to analyze control flow in AST
            def process_node(node, block_id):
                # Store function entry blocks to allow visualization of recursive calls
                if isinstance(node, ast.FunctionDef):
                    # Create a block for the function definition
                    func_name = node.name
                    args = [arg.arg for arg in node.args.args]
                    arg_str = ", ".join(args)
                    func_block_id = create_block(
                        "function", [f"def {func_name}({arg_str}):"]
                    )

                    # Store function block ID for detecting recursive calls
                    function_blocks[func_name] = func_block_id

                    # Connect current block to the function block
                    add_edge(block_id, func_block_id)

                    # Process function body
                    current_block_id = func_block_id
                    for stmt in node.body:
                        current_block_id = process_node(stmt, current_block_id)

                    return current_block_id

                elif isinstance(node, ast.If):
                    # Extract the condition code
                    condition_code = get_node_code(node.test)

                    # Add the condition to the current block
                    blocks[block_id]["statements"].append(
                        f"if {condition_code}:"
                    )
                    condition_block_id = block_id

                    # Create if branch block
                    if_body_block_id = create_block("if-body")
                    add_edge(condition_block_id, if_body_block_id, "True")

                    # Process if body
                    if_end_block_id = if_body_block_id
                    for stmt in node.body:
                        if_end_block_id = process_node(stmt, if_end_block_id)

                    # Create after-if block for the merge point
                    after_if_block_id = create_block("after-if")

                    # Connect end of if branch to after-if
                    add_edge(if_end_block_id, after_if_block_id)

                    # Handle else/elif branch
                    if node.orelse:
                        if len(node.orelse) == 1 and isinstance(
                            node.orelse[0], ast.If
                        ):
                            # This is an elif - recursively process it
                            elif_end_block_id = process_node(
                                node.orelse[0], condition_block_id
                            )
                            # Connect the elif end to our after-if block
                            add_edge(elif_end_block_id, after_if_block_id)
                        else:
                            # This is an else branch
                            else_body_block_id = create_block("else-body")
                            add_edge(
                                condition_block_id, else_body_block_id, "False"
                            )

                            # Process else body
                            else_end_block_id = else_body_block_id
                            for stmt in node.orelse:
                                else_end_block_id = process_node(
                                    stmt, else_end_block_id
                                )

                            # Connect end of else branch to after-if
                            add_edge(else_end_block_id, after_if_block_id)
                    else:
                        # No else branch, connect condition directly to after-if for False case
                        add_edge(
                            condition_block_id, after_if_block_id, "False"
                        )

                    return after_if_block_id

                elif isinstance(node, ast.For) or isinstance(node, ast.While):
                    # Determine loop type
                    loop_type = "for" if isinstance(node, ast.For) else "while"

                    # Extract loop details for better visualization
                    if isinstance(node, ast.For):
                        target = get_node_code(node.target)
                        iter_expr = get_node_code(node.iter)
                        loop_condition = f"{target} in {iter_expr}"
                    else:  # While loop
                        loop_condition = get_node_code(node.test)

                    # Create loop header block
                    loop_header_id = create_block(f"{loop_type}-header")
                    if loop_type == "for":
                        blocks[loop_header_id]["statements"].append(
                            f"for {loop_condition}:"
                        )
                    else:
                        blocks[loop_header_id]["statements"].append(
                            f"while {loop_condition}:"
                        )

                    # Connect current block to loop header
                    add_edge(block_id, loop_header_id)

                    # Create loop body block
                    loop_body_id = create_block(f"{loop_type}-body")

                    # Connect loop header to loop body
                    add_edge(loop_header_id, loop_body_id, f"{loop_condition}")

                    # Process loop body and track continue/break statements
                    body_end_block_id = loop_body_id
                    continue_blocks = []
                    break_blocks = []

                    for stmt in node.body:
                        stmt_end_block_id = process_node(
                            stmt, body_end_block_id
                        )

                        # Check if this statement ends with continue or break
                        if stmt_end_block_id in blocks:
                            if (
                                blocks[stmt_end_block_id].get("type")
                                == "continue"
                            ):
                                continue_blocks.append(stmt_end_block_id)
                                # Continue blocks should connect back to loop header
                                add_edge(
                                    stmt_end_block_id,
                                    loop_header_id,
                                    "continue",
                                )
                            elif (
                                blocks[stmt_end_block_id].get("type")
                                == "break"
                            ):
                                break_blocks.append(stmt_end_block_id)
                                # Break blocks will be connected to after-loop later

                        body_end_block_id = stmt_end_block_id

                    # Create after-loop block
                    after_loop_id = create_block(f"after-{loop_type}")

                    # Connect loop header to after-loop (exit condition)
                    if loop_type == "for":
                        exit_condition = "end of iteration"
                    else:
                        exit_condition = f"not ({loop_condition})"
                    add_edge(loop_header_id, after_loop_id, exit_condition)

                    # Connect normal loop end back to header (if no continue/break)
                    if not continue_blocks and not break_blocks:
                        add_edge(body_end_block_id, loop_header_id, "continue")

                    # Connect break blocks to after-loop
                    for break_block in break_blocks:
                        add_edge(break_block, after_loop_id, "break")

                    return after_loop_id

                elif isinstance(node, ast.Try):
                    # Create try block
                    try_block_id = create_block("try")
                    blocks[try_block_id]["statements"].append("try:")

                    # Connect current block to try block
                    add_edge(block_id, try_block_id)

                    # Process try body
                    try_end_block_id = try_block_id
                    for stmt in node.body:
                        try_end_block_id = process_node(stmt, try_end_block_id)

                    # Create after-try block
                    after_try_id = create_block("after-try")

                    # Connect end of try block to after-try block
                    add_edge(try_end_block_id, after_try_id)

                    # Process except handlers
                    for handler in node.handlers:
                        except_block_id = create_block("except")
                        except_type = (
                            handler.type.id
                            if handler.type and hasattr(handler.type, "id")
                            else "Exception"
                        )
                        blocks[except_block_id]["statements"].append(
                            f"except {except_type}:"
                        )

                        # Connect try block to except block
                        add_edge(
                            try_block_id,
                            except_block_id,
                            f"Exception: {except_type}",
                        )

                        # Process except body
                        except_end_block_id = except_block_id
                        for stmt in handler.body:
                            except_end_block_id = process_node(
                                stmt, except_end_block_id
                            )

                        # Connect end of except block to after-try block
                        add_edge(except_end_block_id, after_try_id)

                    return after_try_id

                elif isinstance(node, ast.Return):
                    # Create return block
                    return_block_id = create_block("return")
                    if node.value:
                        return_value = get_node_code(node.value)
                        blocks[return_block_id]["statements"].append(
                            f"return {return_value}"
                        )

                        # Check if the return value involves a function call
                        if isinstance(node.value, ast.Call):
                            # Check if it's a call to a function we know about
                            if isinstance(node.value.func, ast.Name):
                                func_name = node.value.func.id
                                if func_name in function_blocks:
                                    # Add edge from this block to the function's entry block
                                    add_edge(
                                        return_block_id,
                                        function_blocks[func_name],
                                        "function call",
                                    )

                        # Check if there's a binary operation with function calls
                        elif isinstance(node.value, ast.BinOp):
                            # Check both sides of the operation for function calls
                            for operand in [node.value.left, node.value.right]:
                                if isinstance(
                                    operand, ast.Call
                                ) and isinstance(operand.func, ast.Name):
                                    func_name = operand.func.id
                                    if func_name in function_blocks:
                                        add_edge(
                                            return_block_id,
                                            function_blocks[func_name],
                                            "function call",
                                        )
                    else:
                        blocks[return_block_id]["statements"].append("return")

                    # Connect current block to return block
                    add_edge(block_id, return_block_id)

                    # Connect return to EXIT
                    add_edge(return_block_id, exit_id)

                    return return_block_id

                elif isinstance(node, ast.Expr):
                    # Handle expressions (often function calls)
                    if hasattr(node, "value") and isinstance(
                        node.value, ast.Call
                    ):
                        # Special handling for function calls
                        call_code = get_node_code(node.value)
                        blocks[block_id]["statements"].append(f"{call_code}")

                        # Check if this is a recursive call
                        if isinstance(node.value.func, ast.Name):
                            func_name = node.value.func.id
                            # If function name is in our tracked functions, add edge for recursive call
                            if func_name in function_blocks:
                                # Add edge from current block to function entry
                                add_edge(
                                    block_id,
                                    function_blocks[func_name],
                                    "recursive call",
                                )
                    else:
                        # Try to get more informative representation
                        expr_code = (
                            get_node_code(node.value)
                            if hasattr(node, "value")
                            else "expression"
                        )
                        blocks[block_id]["statements"].append(f"{expr_code}")

                    return block_id

                elif isinstance(node, ast.Continue):
                    # Handle continue statement
                    continue_block_id = create_block("continue")
                    blocks[continue_block_id]["statements"].append("continue")

                    # Connect current block to continue block
                    add_edge(block_id, continue_block_id)

                    # Continue block should connect back to loop header
                    # This will be handled by the loop processing logic
                    return continue_block_id

                elif isinstance(node, ast.Break):
                    # Handle break statement
                    break_block_id = create_block("break")
                    blocks[break_block_id]["statements"].append("break")

                    # Connect current block to break block
                    add_edge(block_id, break_block_id)

                    # Break block should connect to after-loop
                    # This will be handled by the loop processing logic
                    return break_block_id

                elif isinstance(node, ast.Assign):
                    # Handle variable assignments
                    try:
                        targets = []
                        for target in node.targets:
                            targets.append(get_node_code(target))

                        value = get_node_code(node.value)
                        assignment = f"{', '.join(targets)} = {value}"
                        blocks[block_id]["statements"].append(assignment)
                    except Exception:
                        blocks[block_id]["statements"].append("assignment")

                    return block_id

                else:
                    # For other statement types, try to get a more descriptive representation
                    try:
                        node_desc = type(node).__name__
                        # Add any available attributes that might be informative
                        if hasattr(node, "id"):
                            node_desc = f"{node_desc}: {node.id}"
                        elif hasattr(node, "name"):
                            node_desc = f"{node_desc}: {node.name}"

                        blocks[block_id]["statements"].append(node_desc)
                    except Exception:
                        # Fallback to just the type name
                        node_type = type(node).__name__
                        blocks[block_id]["statements"].append(node_type)

                    return block_id

            # Process each function as a separate graph
            for name, func_node in functions.items():
                # Create a block for the function header
                func_block_id = create_block(
                    "function-entry", [f"def {name}(...):"]
                )
                # Connect ENTRY to the function
                add_edge(entry_id, func_block_id)

                # Process function body statements sequentially
                current_block_id = func_block_id
                for i, stmt in enumerate(func_node.body):
                    # For simple statements at the beginning, add them to current block
                    if (
                        current_block_id == func_block_id
                        and isinstance(stmt, (ast.Assign, ast.Expr))
                        and not (
                            isinstance(stmt, ast.Expr)
                            and isinstance(stmt.value, ast.Call)
                        )
                    ):
                        # Add simple statements to function entry block
                        if isinstance(stmt, ast.Assign):
                            try:
                                targets = []
                                for target in stmt.targets:
                                    targets.append(get_node_code(target))
                                value = get_node_code(stmt.value)
                                assignment = f"{', '.join(targets)} = {value}"
                                blocks[current_block_id]["statements"].append(
                                    assignment
                                )
                            except Exception:
                                blocks[current_block_id]["statements"].append(
                                    "assignment"
                                )
                        elif isinstance(stmt, ast.Expr):
                            try:
                                expr_code = get_node_code(stmt.value)
                                blocks[current_block_id]["statements"].append(
                                    expr_code
                                )
                            except Exception:
                                blocks[current_block_id]["statements"].append(
                                    "expression"
                                )
                    else:
                        # For control structures or function calls, process them and continue the flow
                        current_block_id = process_node(stmt, current_block_id)

                # Connect to EXIT if not already connected (no return stmt)
                if not any(
                    edge["from"] == current_block_id and edge["to"] == exit_id
                    for edge in edges
                ):
                    add_edge(current_block_id, exit_id)

            # Process any non-function top-level nodes
            non_func_nodes = [
                node
                for node in tree.body
                if not isinstance(node, ast.FunctionDef)
            ]

            if non_func_nodes:
                first_block_id = create_block("module-body")
                add_edge(entry_id, first_block_id)

                current_block_id = first_block_id
                for node in non_func_nodes:
                    current_block_id = process_node(node, current_block_id)

                # Connect to EXIT
                if not any(
                    edge["from"] == current_block_id and edge["to"] == exit_id
                    for edge in edges
                ):
                    add_edge(current_block_id, exit_id)

            # Handle empty program
            if not functions and not non_func_nodes:
                add_edge(entry_id, exit_id, "Empty program")

            return blocks, edges

        except Exception as e:
            # Create basic error blocks
            blocks = {
                "ENTRY": {"statements": ["ENTRY"], "type": "entry"},
                "ERROR": {
                    "statements": [f"Error parsing code: {str(e)}"],
                    "type": "error",
                },
                "EXIT": {"statements": ["EXIT"], "type": "exit"},
            }
            edges = [
                {"from": "ENTRY", "to": "ERROR"},
                {"from": "ERROR", "to": "EXIT"},
            ]
            return blocks, edges

    def _create_graphviz_graph(self, blocks, edges):
        """Create a Graphviz graph from blocks and edges."""
        # Create a directed graph
        dot = graphviz.Digraph(comment="Control Flow Graph")
        dot.attr(rankdir="TB", size="10,8")
        dot.attr(
            "node", shape="box", style="rounded,filled", fillcolor="lightblue"
        )

        # Filter out empty blocks (except ENTRY and EXIT)
        non_empty_blocks = {}
        for block_id, block_data in blocks.items():
            if block_id in ("ENTRY", "EXIT") or (
                block_data["statements"] and len(block_data["statements"]) > 0
            ):
                non_empty_blocks[block_id] = block_data

        # Add nodes to the graph
        for block_id, block_data in non_empty_blocks.items():
            if block_id in ("ENTRY", "EXIT"):
                # Special formatting for ENTRY and EXIT nodes
                dot.node(
                    block_id, block_id, shape="oval", fillcolor="lightgreen"
                )
            else:
                # Format the statements with newlines
                label = (
                    f"{block_id}\\n"
                    + "\\l".join(block_data["statements"])
                    + "\\l"
                )
                dot.node(block_id, label)

        # Add edges to the graph
        for edge in edges:
            from_node = edge["from"]
            to_node = edge["to"]

            # Skip edges to/from empty blocks
            if (
                from_node not in non_empty_blocks
                or to_node not in non_empty_blocks
            ):
                continue

            if "label" in edge:
                dot.edge(from_node, to_node, label=edge["label"])
            else:
                dot.edge(from_node, to_node)

        return dot

    def visualize_code(self, code_str):
        """Generate a control flow diagram from Python code and save it to a file."""
        try:
            # Generate unique filenames with timestamp
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            output_path = (
                self.output_dir / f"control_flow_{timestamp}_{unique_id}"
            )

            print("Generating control flow visualization for code...")

            # Parse code to blocks
            blocks, edges = self._parse_code_to_blocks(code_str)
            print(
                f"Parsed code into {len(blocks)} blocks and {len(edges)} edges"
            )

            # Create Graphviz graph
            dot = self._create_graphviz_graph(blocks, edges)

            # Save as SVG and DOT
            svg_path = str(output_path) + ".svg"
            dot_path = str(output_path) + ".dot"

            # Render the graph
            dot.render(str(output_path), format="svg", cleanup=True)

            # Also save the DOT source
            with open(dot_path, "w") as f:
                f.write(dot.source)

            print("Successfully generated SVG file")
            return svg_path, dot_path

        except Exception as e:
            import traceback

            print(f"Error generating control flow visualization: {e}")
            traceback.print_exc()
            return None, None
