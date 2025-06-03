import re

class CCCEstimator:
    """
    A class to estimate Cognitive Complexity (CCC) of code files.
    Since it's not language-specific, it's quite bad.
    """

    def __init__(self):
        # Common control structure keywords across many languages
        self.control_keywords = {
            'if': 1, 'elif': 1, 'else': 1,
            'while': 2, 'for': 2, 'foreach': 2, 'loop': 2,
            'switch': 1, 'case': 1, 'default': 1, # switch/case structures
            'try': 1, 'catch': 1, 'except': 1, 'finally': 1, # exception handling
            'match': 1, # For languages like Python (3.10+) or Rust
            # Other potential control flow, might need context
            # 'return': 0, 'break': 0, 'continue': 0 # These typically don't add decision weight directly
        }
        # Common brace/scope delimiters
        self.open_braces = {'{', '(', '['}
        self.close_braces = {'}', ')', ']'}
        # Regex for common function/method definitions (highly simplified)
        # Using a more inclusive pattern for function names, allowing for different syntaxes
        self.function_def_pattern = re.compile(r'\b(?:func|function|def|public\s+static|private\s+static|void|int|string|bool|var|let|const|class\s+\w+\s*:\s*\w+|[a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', re.IGNORECASE)

        # Common input/output patterns
        self.io_patterns = [
            r'\bprint\s*\(', r'\bconsole\.log\s*\(', r'\bsystem\.out\.println\s*\(', r'\bstd::cout\b',
            r'\binput\s*\(', r'\bscanner\.next', r'\bstd::cin\b',
            r'\breadline\s*\(', r'\bread\s*\(', r'\bwrite\s*\(', r'\bopen\s*\(', r'\bclose\s*\(',
            r'\bfile\.read', r'\bfile\.write', r'\bfile\.close'
        ]


    def _get_generic_tokens(self, line):
        """
        Attempts to count tokens in a generic line using common delimiters and whitespace.
        This is a very rough tokenizer.
        """
        # Improved regex to capture words and common operators/punctuations.
        # It's important to not include newlines in the token set.
        # This regex tries to capture:
        # 1. Sequences of word characters (letters, numbers, underscore)
        # 2. Operators and common punctuation characters individually
        # 3. String literals (basic attempt: quoted sequences) - will need more robustness for escape chars
        tokens = re.findall(r'\b\w+\b|\S+', line) # Simpler, catches sequences of non-whitespace or word chars
        # Filter out comments that might be captured by the generic tokenization
        filtered_tokens = []
        for token in tokens:
            if token.startswith('//') or token.startswith('#') or token.startswith('/*'):
                # Stop processing the line for tokens if a comment starts
                break
            filtered_tokens.append(token)
        return len(filtered_tokens)

    def _calculate_Wc_general(self, line):
        """
        Calculates W_c (Type of Control Structures) for a given line based on common keywords.
        """
        line_lower = line.strip().lower()
        if not line_lower:
            return 0

        weight = 0
        for keyword, val in self.control_keywords.items():
            # Use word boundaries to avoid partial matches (e.g., 'for' in 'formula')
            if re.search(r'\b' + re.escape(keyword) + r'\b', line_lower):
                weight += val
        return weight

    def _get_indentation_level(self, line):
        """Returns the number of leading spaces for indentation."""
        return len(line) - len(line.lstrip(' '))

    def _get_brace_level_change(self, line):
        """Calculates net change in brace level within a line."""
        open_count = sum(line.count(b) for b in self.open_braces)
        close_count = sum(line.count(b) for b in self.close_braces)
        return open_count - close_count

    def _calculate_Wn_general(self, current_indentation, class_indentations, current_brace_level):
        """
        Calculates W_n (Inheritance Level of Statements) - very heuristic.
        Combines indentation and a simplified brace level.
        """
        # Prioritize deeper brace levels if available, otherwise rely on indentation
        if current_brace_level > 0:
            return current_brace_level

        if not class_indentations:
            return 0 # Not inside any class/type block

        deepest_class_level = -1
        for indent_level, _, _ in class_indentations: # Adjusted to unpack the tuple
            # Current line is "inside" this class's indentation
            if current_indentation > indent_level:
                deepest_class_level = max(deepest_class_level, indent_level)

        if deepest_class_level == -1:
            return 0 # Not inside a class or not deeper than any known class

        # A very rough level based on active class scopes
        level = 0
        for i, (indent, _, _) in enumerate(class_indentations): # Adjusted to unpack the tuple
            if current_indentation > indent:
                level = i + 1
        return level

    def _calculate_Wtc_general(self, line):
        """
        Calculates W_tc (Try-Catch Blocks) - simplified to common keywords.
        """
        weight = 0
        if re.search(r'\btry\b', line, re.IGNORECASE):
            weight += 1
        if re.search(r'\b(?:catch|except)\b', line, re.IGNORECASE):
            weight += 1
        return weight

    def _calculate_Wrc_general(self, line, method_name_stack):
        """
        Calculates W_rc (Recursive Calls) - very weak heuristic.
        Checks if the current active method's name appears in the line.
        """
        weight = 0
        if method_name_stack:
            current_method = method_name_stack[-1][0] # Get method name from stack
            # Check if the current method name is called within the line (case-insensitive)
            # This is a very weak heuristic for recursion
            if re.search(r'\b' + re.escape(current_method) + r'\s*\(', line, re.IGNORECASE):
                weight += 1
        return weight

    def _calculate_Wad_general(self, line):
        """
        Calculates W_ad (Array/Collection Declarations).
        Looks for common patterns like [], (), or some common list/array constructors.
        W_a := Weight of array (arbitrarily set to 1 for simplicity)
        S_ad := Size of array dimension (number of elements initially)
        """
        weight = 0
        W_a = 1 # Arbitrary weight for array declaration

        # Match common list/array/tuple initializations
        match_collection = re.search(r'=\s*(\[[^\]]*\]|\([^\)]*\)|new\s+\w+\[[^\]]*\])', line)
        if match_collection:
            content = match_collection.group(1)
            # Attempt to count elements by splitting by comma, ignoring empty content
            elements_str = content.strip('[]()').strip()
            if elements_str and elements_str != '*': # Avoid counting '*' as an element for 'new type[*]'
                elements_count = len(elements_str.split(','))
                # Heuristic: if only one element and no comma, it might not be a multi-element collection
                if elements_count == 1 and not (',' in elements_str or '[' in elements_str or '{' in elements_str):
                    if not (content.startswith('[') and content.endswith(']')) and \
                       not (content.startswith('(') and content.endswith(')')):
                        elements_count = 0 # Likely a single value or expression, not an array of size 1
            else:
                elements_count = 0 # Empty collection or direct size declaration

            weight = W_a * elements_count
        return weight

    def _calculate_Wcc_general(self, line, latest_control_weight):
        """
        Calculates W_cc (Compound Conditions).
        Assigns the weight of the control structure they appear in.
        """
        weight = 0
        if latest_control_weight > 0: # Only if inside a control structure
            # Common logical operators
            if ' && ' in line or ' || ' in line or ' and ' in line or ' or ' in line:
                # Count occurrences of any of these operators
                weight += (line.count(' && ') + line.count(' || ') +
                           line.count(' and ') + line.count(' or ')) * latest_control_weight
        return weight

    def _calculate_Wio_general(self, line):
        """
        Calculates W_io (Input/Output Statements).
        Looks for common I/O functions/keywords across various languages.
        """
        weight = 0
        for pattern in self.io_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                weight += 1
        return weight


    def calculate_ccc(self, file_path):
        """
        Calculates the estimated Cognitive Complexity for a given file
        and prints the CCC per line for debugging.
        """
        total_ccc = 0
        previous_indentation = 0
        current_control_weight = 0
        current_brace_level = 0 # Track brace nesting

        # To track inheritance levels (indentation, type_name, brace_level_at_declaration)
        # We try to recognize 'class', 'struct', 'interface', 'enum'
        class_indentations = []

        # To track current method for recursive calls heuristic (method_name, brace_level_at_declaration)
        method_name_stack = []

        print(f"\n--- Cognitive Complexity Guesstimate for '{file_path}' ---")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    stripped_line = line.strip()
                    # Skip comments and empty lines based on common prefixes
                    if not stripped_line or \
                       stripped_line.startswith('#') or \
                       stripped_line.startswith('//') or \
                       stripped_line.startswith('/*') or \
                       stripped_line.startswith('*'): # Handle multi-line comments
                        continue

                    current_indentation = self._get_indentation_level(line)
                    brace_level_change = self._get_brace_level_change(line)
                    current_brace_level += brace_level_change
                    # Ensure brace level doesn't go negative due to heuristic issues
                    current_brace_level = max(0, current_brace_level)

                    # --- Update Scope Tracking (Highly Heuristic) ---
                    # Type (Class/Struct/Interface/Enum) tracking
                    type_declaration_match = re.search(r'\b(?:class|struct|interface|enum)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', stripped_line, re.IGNORECASE)
                    if type_declaration_match:
                        type_name = type_declaration_match.group(1)
                        # Pop out types that are at a shallower or same indentation/brace level
                        while class_indentations and \
                              (class_indentations[-1][0] >= current_indentation or \
                               (current_brace_level > 0 and current_brace_level <= class_indentations[-1][2])): # New brace level check
                            class_indentations.pop()
                        class_indentations.append((current_indentation, type_name, current_brace_level))
                    else:
                        # If indentation or brace level decreases, pop out types that are no longer in scope
                        # This logic needs to be careful not to pop parent scopes too early.
                        # For brace-based languages, ending brace signifies scope exit.
                        # For indentation-based, it's a decrease in indent.
                        while class_indentations and \
                              (current_indentation < class_indentations[-1][0] or \
                               (current_brace_level < class_indentations[-1][2] and class_indentations[-1][2] > 0)):
                            class_indentations.pop()


                    # Method/Function tracking
                    method_name_match = self.function_def_pattern.search(stripped_line)
                    if method_name_match:
                        method_name = method_name_match.group(1)
                        # Pop out methods if indentation or brace level indicates exit
                        while method_name_stack and \
                              (current_indentation <= previous_indentation and \
                               (current_brace_level < method_name_stack[-1][1] if len(method_name_stack[-1]) > 1 else 0)):
                            method_name_stack.pop()
                        method_name_stack.append((method_name, current_brace_level)) # Store method name and its brace level
                    elif method_name_stack and \
                         (current_indentation <= previous_indentation or \
                          (current_brace_level < method_name_stack[-1][1] if len(method_name_stack[-1]) > 1 else 0)):
                        # Heuristic: if indentation or brace level goes back, assume we've exited the method
                        if method_name_stack:
                            method_name_stack.pop()


                    # --- CCC Calculation for the current line ---
                    ccc_line = 0

                    S_k = self._get_generic_tokens(line)
                    W_c = self._calculate_Wc_general(line)
                    current_control_weight = W_c # Update current control weight for compound conditions
                    W_n = self._calculate_Wn_general(current_indentation, class_indentations, current_brace_level)
                    W_tc = self._calculate_Wtc_general(line)
                    W_rc = self._calculate_Wrc_general(line, method_name_stack)
                    W_ad = self._calculate_Wad_general(line)
                    W_cc = self._calculate_Wcc_general(line, current_control_weight)
                    W_io = self._calculate_Wio_general(line)

                    multiplier = max(1, W_c + W_n)
                    ccc_line = (S_k * multiplier) + W_tc + W_rc + W_ad + W_cc + W_io

                    total_ccc += ccc_line
                    previous_indentation = current_indentation

                    # Print for debugging
                    # print(f"Line {line_num:4}: CCC = {ccc_line:5} | Indent: {current_indentation:2} | BraceL: {current_brace_level:2} | Tokens: {S_k:3} | Wc: {W_c:2} | Wn: {W_n:2} | Wtc: {W_tc:2} | Wrc: {W_rc:2} | Wad: {W_ad:2} | Wcc: {W_cc:2} | Wio: {W_io:2} | {stripped_line}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return -1
        return total_ccc