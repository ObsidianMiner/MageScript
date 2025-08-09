import re

class Handlers:
    def __init__(self, parser):
        self.parser = parser
        self.indent = parser.indent
        self.py_lines = parser.python_lines

    # === Handlers ===
    def parse_let(self, name, value):
        py_line = f"{name} = {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

        
    def parse_let_string(self, name, value):
        py_line = f"{name} = \"{self.expr_clean(value)}\""
        self.py_lines.append(self.indent() + py_line)

    def parse_empower(self, name, value):
        py_line = f"{name} += {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

    def parse_drain(self, name, value):
        py_line = f"{name} -= {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

    def parse_transmute(self, name, value):
        py_line = f"{name} = {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

    def parse_print(self, value):
        py_line = f"print({self.expr_clean(value)})"
        self.py_lines.append(self.indent() + py_line)

    def parse_print_string(self, message):
        # Escape quotes properly
        safe_message = message.replace('"', '\\"')
        py_line = f'print("{safe_message}")'
        self.py_lines.append(self.indent() + py_line)

    def parse_return(self, value):
        py_line = f"return {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

    def parse_global(self, value):
        py_line = f"global {self.expr_clean(value)}"
        self.py_lines.append(self.indent() + py_line)

    def parse_function_call(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and')) if params else ""
        py_line = f"{name}({params_clean})"
        self.py_lines.append(self.indent() + py_line)

    def parse_join_strings(self, name, args):
        args = args or ""
        parts = [part.strip() for part in args.split('and') if part.strip()]
        joined = " + ".join(f"str({part})" for part in parts)
        self.py_lines.append(self.indent() + f"{name} = {joined}")

    def parse_cast_string(self, name, value):
        py_line = f"{name} = str({self.expr_clean(value)})"
        self.py_lines.append(self.indent() + py_line)

    def parse_function_def(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and')) if params else ""
        self.py_lines.append(self.indent() + f"def {name}({params_clean}):")
        self.parser.indent_level += 1
        self.parser.block_stack.append('function')

    def parse_list_conjure(self, name):
        py_line = f"{name} = []"
        self.py_lines.append(self.indent() + py_line)

    def parse_list_add(self, value, name):
        py_line = f"{name}.append({self.expr_clean(value)})"
        self.py_lines.append(self.indent() + py_line)
    
    def parse_list_add_string(self, value, name):
        py_line = f"{name}.append(\"{self.expr_clean(value)}\")"
        self.py_lines.append(self.indent() + py_line)

    def parse_length(self, var_name, list_name):
        py_line = f"{var_name} = len({list_name})"
        self.py_lines.append(self.indent() + py_line)

    def parse_if(self, condition):
        self.py_lines.append(self.indent() + f"if {self.condition_clean(condition)}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('if')

    def parse_elif(self, condition):
        if not self.parser.block_stack or self.parser.block_stack[-1] != 'if':
            raise SyntaxError("elif without preceding if")
        self.parser.indent_level -= 1
        self.py_lines.append(self.indent() + f"elif {self.condition_clean(condition)}:")
        self.parser.indent_level += 1

    def parse_else(self):
        if not self.parser.block_stack or self.parser.block_stack[-1] != 'if':
            raise SyntaxError("else without preceding if")
        self.parser.indent_level -= 1
        self.py_lines.append(self.indent() + "else:")
        self.parser.indent_level += 1

    def parse_for(self, iterable, item):
        self.py_lines.append(self.indent() + f"for {item} in {self.expr_clean(iterable)}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('loop')

    def parse_while(self, condition):
        self.py_lines.append(self.indent() + f"while {self.condition_clean(condition)}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('loop')

    # === New block close handlers ===
    def parse_close_function(self):
        self.close_block('function')

    def parse_close_if(self):
        self.close_block('if')

    def parse_close_loop(self):
        self.close_block('loop')

    def parse_close_any(self):
        # Close the most recent block regardless of type
        if self.parser.block_stack:
            block = self.parser.block_stack.pop()
            self.parser.indent_level = max(0, self.parser.indent_level - 1)
        else:
            # No open blocks to close; optionally warn or ignore
            pass

    def close_block(self, block_type):
        if not self.parser.block_stack:
            raise SyntaxError(f"Attempted to close a {block_type} block but no blocks are open")
        if self.parser.block_stack[-1] != block_type:
            raise SyntaxError(f"Attempted to close a {block_type} block but current open block is {self.parser.block_stack[-1]}")
        self.parser.block_stack.pop()
        self.parser.indent_level = max(0, self.parser.indent_level - 1)


    def parse_end(self, *args):
        self.parser.ended = True

    # Helpers for cleaning expressions and conditions
    def expr_clean(self, expr):
        # Replace mage comparisons
        expr = expr.lower()
        # Replace mage comparisons to Python
        expr = expr.replace(" wanes below ", " < ")
        expr = expr.replace(" rises above ", " > ")
        expr = expr.replace(" mirrors ", " == ")
        # Remove filler words, e.g., "the", "of", "by", "to", etc. (optional, can expand)
        #filler_words = ["the", "of", "by", "to", "from", "with", "and", "a", "an", "on", "in", "upon", "each", "called", "as"]
        #pattern = r"\b(" + "|".join(filler_words) + r")\b"
        #expr = re.sub(pattern, "", expr)
        return expr.strip()

    def condition_clean(self, cond):
        # Similar cleaning to expr_clean but keep logical connectors intact
        cond = cond.lower()
        cond = cond.replace(" wanes below ", " < ")
        cond = cond.replace(" rises above ", " > ")
        cond = cond.replace(" mirrors ", " == ")
        # You can add support for 'and', 'or' here if needed
        # Remove filler words except logical connectors
        filler_words = ["the", "of", "by", "to", "from", "with", "a", "an", "on", "in", "upon", "each", "called", "as"]
        pattern = r"\b(" + "|".join(filler_words) + r")\b"
        cond = re.sub(pattern, "", cond)
        return cond.strip()