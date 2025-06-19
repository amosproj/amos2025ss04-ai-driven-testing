import os
import ast
import uuid
import subprocess
from pathlib import Path
from modules.base import ModuleBase
from schemas import PromptData, ResponseData
import networkx as nx
import matplotlib

matplotlib.use("Agg")


class ShowControlFlow(ModuleBase):
    """Module that visualizes control flow from code and saves it as an image."""

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
        """Parse Python code and build control flow blocks using AST.

        Each block represents a sequence of statements with a single entry and exit point.
        Control flow between blocks is represented as edges in the graph.
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code_str)

            # Dictionary to store blocks of code
            blocks = {}
            edges = []

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
                if isinstance(node, ast.FunctionDef):
                    # Create a block for the function definition
                    func_name = node.name
                    args = [arg.arg for arg in node.args.args]
                    arg_str = ", ".join(args)
                    func_block_id = create_block(
                        "function", [f"def {func_name}({arg_str}):"]
                    )

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
                    condition_block_id = block_id
                    blocks[condition_block_id]["statements"].append(
                        f"if {condition_code}:"
                    )

                    # Process if body - reuse current block if body is simple
                    if len(node.body) <= 1:
                        # For simple if statements, include the body in the same block
                        if_block_id = condition_block_id
                        if len(node.body) == 1:
                            # Add the single statement to the condition block
                            if_end_block_id = process_node(
                                node.body[0], if_block_id
                            )
                        else:
                            if_end_block_id = if_block_id
                    else:
                        # For more complex if statements, create a separate block
                        if_block_id = create_block("if-body")
                        # Connect condition to if branch with True label
                        add_edge(
                            condition_block_id,
                            if_block_id,
                            f"{condition_code}",
                        )

                        # Process if body
                        if_end_block_id = if_block_id
                        for stmt in node.body:
                            if_end_block_id = process_node(
                                stmt, if_end_block_id
                            )

                    # Create after-if block for the merge point
                    after_if_block_id = create_block("after-if")

                    # Connect end of if block to after-if block
                    if if_end_block_id != condition_block_id:
                        add_edge(if_end_block_id, after_if_block_id)

                    # Process else/elif body if it exists
                    if node.orelse:
                        if len(node.orelse) == 1 and isinstance(
                            node.orelse[0], ast.If
                        ):
                            # This is an elif branch
                            elif_node = node.orelse[0]
                            elif_condition = get_node_code(elif_node.test)

                            # Check if we can reuse the condition block
                            if condition_block_id == if_end_block_id:
                                # Add to the existing block
                                blocks[condition_block_id][
                                    "statements"
                                ].append(f"elif {elif_condition}:")
                                elif_block_id = condition_block_id
                            else:
                                # Create a new block
                                elif_block_id = create_block(
                                    "elif-condition",
                                    [f"elif {elif_condition}:"],
                                )
                                # Connect the condition to the elif with "False" label
                                add_edge(
                                    condition_block_id,
                                    elif_block_id,
                                    f"not {condition_code}",
                                )

                            # Process the elif (which is just another if)
                            else_end_block_id = process_node(
                                elif_node, elif_block_id
                            )

                            # Connect end of elif to after-if block
                            if else_end_block_id != condition_block_id:
                                add_edge(else_end_block_id, after_if_block_id)
                        else:
                            # This is a regular else branch
                            # Check if we can reuse the condition block
                            if condition_block_id == if_end_block_id:
                                # Add to the existing block
                                blocks[condition_block_id][
                                    "statements"
                                ].append("else:")
                                else_block_id = condition_block_id
                            else:
                                # Create a new block
                                else_block_id = create_block(
                                    "else-body", ["else:"]
                                )
                                # Connect condition to else branch with False label
                                add_edge(
                                    condition_block_id,
                                    else_block_id,
                                    f"not {condition_code}",
                                )

                            # Process else body
                            else_end_block_id = else_block_id
                            for stmt in node.orelse:
                                else_end_block_id = process_node(
                                    stmt, else_end_block_id
                                )

                            # Connect end of else to after-if block
                            if else_end_block_id != condition_block_id:
                                add_edge(else_end_block_id, after_if_block_id)
                    else:
                        # No else - connect condition directly to after-if with False label
                        add_edge(
                            condition_block_id,
                            after_if_block_id,
                            f"not {condition_code}",
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

                    # Process loop body
                    body_end_block_id = loop_body_id
                    for stmt in node.body:
                        body_end_block_id = process_node(
                            stmt, body_end_block_id
                        )

                    # Loop back from body to header
                    add_edge(body_end_block_id, loop_header_id, "continue")

                    # Create after-loop block
                    after_loop_id = create_block(f"after-{loop_type}")

                    # Connect loop header to after-loop (exit condition)
                    if loop_type == "for":
                        exit_condition = "end of iteration"
                    else:
                        exit_condition = f"not ({loop_condition})"
                    add_edge(loop_header_id, after_loop_id, exit_condition)

                    # Process else clause if it exists
                    if node.orelse:
                        else_block_id = create_block(f"{loop_type}-else")
                        # Connect loop header to else block - executed when loop completes normally
                        add_edge(loop_header_id, else_block_id, "no break")

                        else_end_block_id = else_block_id
                        for stmt in node.orelse:
                            else_end_block_id = process_node(
                                stmt, else_end_block_id
                            )

                        # Connect end of else block to after-loop
                        add_edge(else_end_block_id, after_loop_id)

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
                    else:
                        # Try to get more informative representation
                        expr_code = (
                            get_node_code(node.value)
                            if hasattr(node, "value")
                            else "expression"
                        )
                        blocks[block_id]["statements"].append(f"{expr_code}")

                    return block_id

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
                # Create a block for the function
                func_block_id = create_block(
                    "function-entry", [f"def {name}(...):"]
                )
                # Connect ENTRY to the function
                add_edge(entry_id, func_block_id)

                # Process function body
                current_block_id = func_block_id
                for stmt in func_node.body:
                    current_block_id = process_node(stmt, current_block_id)

                # Connect to EXIT if not already connected (no return stmt)
                if not any(
                    edge["from"] == current_block_id and edge["to"] == exit_id
                    for edge in edges
                ):
                    add_edge(current_block_id, exit_id)

            # Process any non-function top-level nodes
            first_block_id = None
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
        try:
            # Parse the code into an AST
            tree = ast.parse(code_str)

            # Create a directed graph
            graph = nx.DiGraph()

            # Track the current node and create an entry node
            current_node_id = 0
            entry_node_id = current_node_id
            graph.add_node(current_node_id, label="Entry")
            current_node_id += 1

            # Helper function to analyze control flow in AST
            def analyze_node(node, parent_id):
                nonlocal current_node_id

                if isinstance(node, ast.FunctionDef):
                    # Add function definition node
                    func_node_id = current_node_id
                    graph.add_node(
                        func_node_id, label=f"Function: {node.name}"
                    )
                    graph.add_edge(parent_id, func_node_id)
                    current_node_id += 1

                    # Process function body
                    last_node_id = func_node_id
                    for item in node.body:
                        last_node_id = analyze_node(item, last_node_id)

                    return last_node_id

                elif isinstance(node, ast.If):
                    # Add if statement node
                    if_node_id = current_node_id
                    graph.add_node(if_node_id, label="If")
                    graph.add_edge(parent_id, if_node_id)
                    current_node_id += 1

                    # Process if body
                    last_if_node_id = if_node_id
                    for item in node.body:
                        last_if_node_id = analyze_node(item, if_node_id)

                    # Process else body if it exists
                    last_else_node_id = if_node_id
                    for item in node.orelse:
                        last_else_node_id = analyze_node(item, if_node_id)

                    # Create a merge node if needed
                    if (
                        last_if_node_id != if_node_id
                        or last_else_node_id != if_node_id
                    ):
                        merge_node_id = current_node_id
                        graph.add_node(merge_node_id, label="Merge")
                        graph.add_edge(last_if_node_id, merge_node_id)
                        if node.orelse:
                            graph.add_edge(last_else_node_id, merge_node_id)
                        current_node_id += 1
                        return merge_node_id

                    return if_node_id

                elif isinstance(node, ast.For) or isinstance(node, ast.While):
                    # Add loop node
                    loop_type = "For" if isinstance(node, ast.For) else "While"
                    loop_node_id = current_node_id
                    graph.add_node(loop_node_id, label=loop_type)
                    graph.add_edge(parent_id, loop_node_id)
                    current_node_id += 1

                    # Process loop body
                    last_body_node_id = loop_node_id
                    for item in node.body:
                        last_body_node_id = analyze_node(
                            item, last_body_node_id
                        )

                    # Loop back
                    graph.add_edge(last_body_node_id, loop_node_id)

                    # Process else clause if it exists
                    after_loop_node_id = current_node_id
                    graph.add_node(
                        after_loop_node_id, label=f"After {loop_type}"
                    )
                    graph.add_edge(loop_node_id, after_loop_node_id)
                    current_node_id += 1

                    if node.orelse:
                        last_else_node_id = after_loop_node_id
                        for item in node.orelse:
                            last_else_node_id = analyze_node(
                                item, last_else_node_id
                            )
                        return last_else_node_id

                    return after_loop_node_id

                elif isinstance(node, ast.Try):
                    # Add try node
                    try_node_id = current_node_id
                    graph.add_node(try_node_id, label="Try")
                    graph.add_edge(parent_id, try_node_id)
                    current_node_id += 1

                    # Process try body
                    last_try_node_id = try_node_id
                    for item in node.body:
                        last_try_node_id = analyze_node(item, last_try_node_id)

                    # Process except handlers
                    except_node_ids = []
                    for handler in node.handlers:
                        except_node_id = current_node_id
                        except_type = (
                            handler.type.id
                            if handler.type and hasattr(handler.type, "id")
                            else "Exception"
                        )
                        graph.add_node(
                            except_node_id, label=f"Except: {except_type}"
                        )
                        graph.add_edge(try_node_id, except_node_id)
                        current_node_id += 1

                        last_except_node_id = except_node_id
                        for item in handler.body:
                            last_except_node_id = analyze_node(
                                item, last_except_node_id
                            )
                        except_node_ids.append(last_except_node_id)

                    # Create a merge node
                    merge_node_id = current_node_id
                    graph.add_node(merge_node_id, label="Merge")
                    graph.add_edge(last_try_node_id, merge_node_id)
                    for node_id in except_node_ids:
                        graph.add_edge(node_id, merge_node_id)
                    current_node_id += 1

                    return merge_node_id

                else:
                    # Add a generic statement node for other types
                    node_type = type(node).__name__
                    stmt_node_id = current_node_id
                    graph.add_node(stmt_node_id, label=node_type)
                    graph.add_edge(parent_id, stmt_node_id)
                    current_node_id += 1

                    return stmt_node_id

            # Start analysis from the module level
            for item in tree.body:
                analyze_node(item, entry_node_id)

            return graph
        except Exception as e:
            # Create a simple error graph
            graph = nx.DiGraph()
            graph.add_node(0, label=f"Error parsing code: {str(e)}")
            return graph

    def _generate_dot_code(self, blocks, edges):
        """Generate DOT code from the CFG blocks and edges."""
        dot_lines = ["digraph cfg {", "    Node [shape=box];"]

        # Filter out empty blocks (except ENTRY and EXIT)
        non_empty_blocks = {}
        for block_id, block_data in blocks.items():
            if block_id in ("ENTRY", "EXIT") or (
                block_data["statements"] and len(block_data["statements"]) > 0
            ):
                non_empty_blocks[block_id] = block_data

        # Redirect edges that point to empty blocks
        updated_edges = []
        empty_block_redirects = {}

        # First, identify empty blocks and create redirections
        for edge in edges:
            from_node = edge["from"]
            to_node = edge["to"]

            # Skip edges from or to empty blocks (but keep ENTRY and EXIT)
            if from_node not in non_empty_blocks and from_node not in (
                "ENTRY",
                "EXIT",
            ):
                if from_node not in empty_block_redirects:
                    # Find where this empty block should redirect to
                    next_blocks = [
                        e["to"] for e in edges if e["from"] == from_node
                    ]
                    if next_blocks:
                        empty_block_redirects[from_node] = next_blocks[0]

            if to_node not in non_empty_blocks and to_node not in (
                "ENTRY",
                "EXIT",
            ):
                if to_node not in empty_block_redirects:
                    # Find where this empty block should redirect to
                    next_blocks = [
                        e["to"] for e in edges if e["from"] == to_node
                    ]
                    if next_blocks:
                        empty_block_redirects[to_node] = next_blocks[0]

        # Now create the updated edges, skipping empty blocks
        for edge in edges:
            from_node = edge["from"]
            to_node = edge["to"]

            # Skip edges between empty blocks
            if (
                from_node not in non_empty_blocks
                and from_node not in ("ENTRY", "EXIT")
                and to_node not in non_empty_blocks
                and to_node not in ("ENTRY", "EXIT")
            ):
                continue

            # Redirect if needed
            if from_node not in non_empty_blocks and from_node not in (
                "ENTRY",
                "EXIT",
            ):
                from_node = empty_block_redirects.get(from_node, from_node)

            if to_node not in non_empty_blocks and to_node not in (
                "ENTRY",
                "EXIT",
            ):
                to_node = empty_block_redirects.get(to_node, to_node)

            # Add the edge (possibly redirected)
            new_edge = {"from": from_node, "to": to_node}
            if "label" in edge:
                new_edge["label"] = edge["label"]

            # Avoid duplicate edges after redirection
            if new_edge not in updated_edges:
                updated_edges.append(new_edge)

        # Add nodes
        for block_id, block_data in non_empty_blocks.items():
            if block_id not in ("ENTRY", "EXIT"):
                # Format the statements with newlines
                label = (
                    f"{block_id}\\n"
                    + "\\l".join(block_data["statements"])
                    + "\\l"
                )
                dot_lines.append(f'    {block_id} [label="{label}"];')
            else:
                # Special formatting for ENTRY and EXIT nodes
                dot_lines.append(
                    f'    {block_id} [label="{block_id}", shape=oval];'
                )

        # Add edges (now using the updated edges)
        for edge in updated_edges:
            from_node = edge["from"]
            to_node = edge["to"]
            if "label" in edge:
                dot_lines.append(
                    f'    {from_node}->{to_node} [label="{edge["label"]}"];'
                )
            else:
                dot_lines.append(f"    {from_node}->{to_node};")

        dot_lines.append("}")
        return "\n".join(dot_lines)

    def _generate_svg_from_dot(self, dot_code, output_path):
        """Generate an SVG file from DOT code using graphviz."""
        try:
            # Save DOT code to a temporary file
            dot_file_path = output_path.with_suffix(".dot")
            with open(dot_file_path, "w") as f:
                f.write(dot_code)

            # Run graphviz to generate SVG
            cmd = ["dot", "-Tsvg", str(dot_file_path), "-o", str(output_path)]

            # Try to run the command and handle errors
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                return True, dot_file_path
            except subprocess.CalledProcessError as e:
                print(f"Error running graphviz: {e}")
                print(f"Command output: {e.stdout.decode()}")
                print(f"Command error: {e.stderr.decode()}")

                # Try to generate PNG if SVG fails (fallback)
                try:
                    png_path = output_path.with_suffix(".png")
                    subprocess.run(
                        [
                            "dot",
                            "-Tpng",
                            str(dot_file_path),
                            "-o",
                            str(png_path),
                        ],
                        check=True,
                        capture_output=True,
                    )
                    return True, dot_file_path
                except Exception:
                    # If both fail, return the dot file only
                    return False, dot_file_path

        except Exception as e:
            print(f"Error generating SVG from DOT: {e}")
            return False, None

    def visualize_code(self, code_str):
        """Generate a control flow diagram from Python code and save it to a file."""
        try:
            # Generate unique filenames
            unique_id = uuid.uuid4().hex[:8]
            output_path = self.output_dir / f"control_flow_{unique_id}.svg"

            print("Generating control flow visualization for code...")

            # Parse code to blocks
            blocks, edges = self._parse_code_to_blocks(code_str)
            print(
                f"Parsed code into {len(blocks)} blocks and {len(edges)} edges"
            )

            # Generate DOT code
            dot_code = self._generate_dot_code(blocks, edges)
            print(f"Generated DOT code ({len(dot_code)} characters)")

            # Generate SVG from DOT code
            print(f"Generating SVG from DOT code to {output_path}")
            success, dot_file_path = self._generate_svg_from_dot(
                dot_code, output_path
            )

            if success:
                print("Successfully generated SVG file")
                return str(output_path), str(dot_file_path)
            elif dot_file_path:
                # Return the DOT file if SVG generation failed
                print("Failed to generate SVG, but DOT file was created")
                return None, str(dot_file_path)
            else:
                print("Failed to generate both SVG and DOT files")
                return None, None

        except Exception as e:
            import traceback

            print(f"Error generating control flow visualization: {e}")
            traceback.print_exc()
            return None, None
