import re

class Handlers:
    def __init__(self, parser):
        self.parser = parser
        self.indent = parser.indent
        self.py_lines = parser.python_lines

    # ==========================
    # Variable Declarations & Assignment
    # ==========================
    def parse_let(self, name, value):
        self.py_lines.append(self.indent() + f"{name} = {self.expr_clean(value)}")

    def parse_let_string(self, name, value):
        self.py_lines.append(self.indent() + f"{name} = \"{self.expr_clean(value)}\"")

    def parse_transmute(self, name, value):
        self.py_lines.append(self.indent() + f"{name} = {self.expr_clean(value)}")

    def parse_global(self, value):
        self.py_lines.append(self.indent() + f"global {self.expr_clean(value)}")

    # ==========================
    # Reassignment & Math Operations
    # ==========================
    def parse_empower(self, name, value):
        self.py_lines.append(self.indent() + f"{name} += {self.expr_clean(value)}")

    def parse_drain(self, name, value):
        self.py_lines.append(self.indent() + f"{name} -= {self.expr_clean(value)}")

    def parse_divide(self, name, value):
        self.py_lines.append(self.indent() + f"{name} /= {self.expr_clean(value)}")

    def parse_multiply(self, name, value):
        self.py_lines.append(self.indent() + f"{name} *= {self.expr_clean(value)}")

    def parse_modulus(self, name, value):
        self.py_lines.append(self.indent() + f"{name} %= {self.expr_clean(value)}")

    # ==========================
    # Output & Input
    # ==========================
    def parse_print(self, value):
        self.py_lines.append(self.indent() + f"print({self.expr_clean(value)})")

    def parse_print_string(self, message):
        safe_message = message.replace('"', '\\"')
        self.py_lines.append(self.indent() + f'print("{safe_message}")')

    # ==========================
    # Loops & Flow Control
    # ==========================
    def parse_for(self, iterable, item):
        self.py_lines.append(self.indent() + f"for {item} in {self.expr_clean(iterable)}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('loop')

    def parse_while(self, condition):
        self.py_lines.append(self.indent() + f"while {self.condition_clean(condition)}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('loop')

    def parse_break(self):
        self.py_lines.append(self.indent() + "break")

    def parse_continue(self):
        self.py_lines.append(self.indent() + "continue")

    # ==========================
    # Conditionals
    # ==========================
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

    # ==========================
    # Functions (Rituals)
    # ==========================
    def parse_function_def(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and'))
        self.py_lines.append(self.indent() + f"def {name}({params_clean}):")
        self.parser.indent_level += 1
        self.parser.block_stack.append('function')

    def parse_function_call(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and'))
        self.py_lines.append(self.indent() + f"{name}({params_clean})")

    def parse_function_call_with_output(self, outputName, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and'))
        self.py_lines.append(self.indent() + f"{outputName} = {name}({params_clean})")

    def parse_return(self, value):
        self.py_lines.append(self.indent() + f"return {self.expr_clean(value)}")

    # ==========================
    # Lists & Arrays (Tomes)
    # ==========================
    def parse_list_conjure(self, name):
        self.py_lines.append(self.indent() + f"{name} = []")

    def parse_list_add(self, value, name):
        self.py_lines.append(self.indent() + f"{name}.append({self.expr_clean(value)})")

    def parse_list_add_string(self, value, name):
        self.py_lines.append(self.indent() + f"{name}.append(\"{self.expr_clean(value)}\")")

    def parse_length(self, var_name, list_name):
        self.py_lines.append(self.indent() + f"{var_name} = len({list_name})")

    # ==========================
    # Class (Scroll)
    # ==========================

    def parse_class_def(self, name):
        self.py_lines.append(self.indent() + f"class {name}:")
        self.parser.indent_level += 1
        self.parser.block_stack.append('class')
        
    def parse_inherited_class_def(self, name, parent_name):
        self.py_lines.append(self.indent() + f"class {name}({parent_name}):")
        self.parser.indent_level += 1
        self.parser.block_stack.append('class')
    
    def parse_constructor_def(self):
        # Add a constructor
        self.py_lines.append(self.indent() + "def __init__(self):")
        self.parser.indent_level += 1
    
    def parse_class_function_call(self, class_name, function_name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split('and'))
        self.py_lines.append(self.indent() + f"{class_name}.{function_name}({params_clean})")
    
    def parse_instantiate_class(self, instance_name, class_name):
        self.py_lines.append(self.indent() + f"{instance_name} = {class_name}()")

    # ==========================
    # File Operations
    # ==========================
    def parse_read_file(self, varName, path):
        file_var = varName + "filed"
        self.py_lines.append(self.indent() + f"{file_var} = open({path})")
        self.py_lines.append(self.indent() + f"{varName} = {file_var}.read()")

    def parse_write_file(self, path, name):
        self.py_lines.append(self.indent() + f"with open({path}, 'w') as f:")
        self.py_lines.append(self.indent() + f"    f.write({name})")

    def parse_append_file(self, path, name):
        self.py_lines.append(self.indent() + f"with open({path}, 'a') as f:")
        self.py_lines.append(self.indent() + f"    f.write({name})")

    def parse_delete_file(self, path):
        self.py_lines.append(self.indent() + f"import os\nos.remove({path})")

    # ==========================
    # String Operations
    # ==========================
    def parse_join_strings(self, name, args):
        parts = [part.strip() for part in (args or "").split('and') if part.strip()]
        joined = " + ".join(f"str({part})" for part in parts)
        self.py_lines.append(self.indent() + f"{name} = {joined}")

    def parse_cast_string(self, name, value):
        self.py_lines.append(self.indent() + f"{name} = str({self.expr_clean(value)})")

    # ==========================
    # Imports
    # ==========================
    def parse_import(self, module):
        self.py_lines.append(self.indent() + f"import {module}")

    def parse_import_from_module(self, function, module):
        self.py_lines.append(self.indent() + f"from {module} import {function}")

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