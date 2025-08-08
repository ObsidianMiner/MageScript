import re
import subprocess

class MageScriptParser:
    def __init__(self):
        self.patterns = [

            # LENGTH MUST COME BEFORE LET
            # Length: Let (\w+) be the length of (\w+)
            (re.compile(r"let (.+) be the length of (\w+)", re.IGNORECASE), self.parse_length),

            # Variable declaration: Let [name] be [value]
            (re.compile(r"let\s+(\w+)\s+be\s+(.+)", re.IGNORECASE), self.parse_let),
            (re.compile(r"speak the name of\s+(\w+)\s+to be\s+(.+)", re.IGNORECASE), self.parse_let_string),

            # Empower (add): Empower [name] by [value]
            (re.compile(r"empower\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), self.parse_empower),

            # Drain (subtract): Drain [name] by [value]
            (re.compile(r"drain\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), self.parse_drain),

            # Transmute (assign): Transmute [name] with [value]
            (re.compile(r"transmute\s+(\w+)\s+with\s+(.+)", re.IGNORECASE), self.parse_transmute),

            # Print: Reveal the truth of [value]
            (re.compile(r"reveal the truth of (.+)", re.IGNORECASE), self.parse_print),

            # Print string literal: Let the spell echo: "message"
            (re.compile(r'let the spell echo:\s*"(.*)"', re.IGNORECASE), self.parse_print_string),

            #------------------
            # Functions
            #------------------

            # Function definition: Inscribe ritual [name] with [parameters]
            (re.compile(r"inscribe ritual (\w+)(?: with (.+))?", re.IGNORECASE), self.parse_function_def),

            # Return statement: Return [value] to the aether
            (re.compile(r"return (.+) to the aether", re.IGNORECASE), self.parse_return),

            # Function call: Invoke the ritual of [name], offering [arguments]
            (re.compile(r"invoke the ritual of (\w+)(?:,? offering (.+))?", re.IGNORECASE), self.parse_function_call),

            #------------------
            # Conditional
            #------------------

            # If condition: If fate whispers: (.+)
            (re.compile(r"if fate whispers (.+)", re.IGNORECASE), self.parse_if),

            # Else if: Else if fate shifts: (.+)
            (re.compile(r"else if fate shifts (.+)", re.IGNORECASE), self.parse_elif),

            # Else: Else, when all omens fail:
            (re.compile(r"else, when all omens fail", re.IGNORECASE), self.parse_else),

            #------------------
            # Loops
            #------------------
            # For loop: Chant upon (.+), each soul called (\w+)
            (re.compile(r"chant upon (.+) each soul called (\w+)", re.IGNORECASE), self.parse_for),

            # While loop: Sustain the chant while (.+) holds true
            (re.compile(r"sustain the chant while (.+) holds true", re.IGNORECASE), self.parse_while),

            
            #------------------
            # Lists
            #------------------

            # List conjure: Conjure an empty tome called (\w+)
            (re.compile(r"conjure an empty tome called (\w+)", re.IGNORECASE), self.parse_list_conjure),

            # List add: Add (.+) to the pages of (\w+)
            (re.compile(r"add (.+) to the pages of (\w+)", re.IGNORECASE), self.parse_list_add),
            (re.compile(r"call forth the word (.+) to the pages of (\w+)", re.IGNORECASE), self.parse_list_add_string),
            (re.compile(r"call upon the phrase (.+) to the pages of (\w+)", re.IGNORECASE), self.parse_list_add_string),
            (re.compile(r"invoke the sacred phrase (.+) to the pages of (\w+)", re.IGNORECASE), self.parse_list_add_string),

            #--------------------
            # BLCOK CLOSING
            #--------------------

            # Block closing phrases (multiple, general)
            (re.compile(r"close the incantation", re.IGNORECASE), self.parse_close_function),
            (re.compile(r"let the omen pass", re.IGNORECASE), self.parse_close_if),
            (re.compile(r"complete the chant", re.IGNORECASE), self.parse_close_loop),
            (re.compile(r"seal the spell", re.IGNORECASE), self.parse_close_any),

            # End spell - triggers compile
            (re.compile(r"(so it is written|the spell is complete|thus concludes the incantation|let it be done)\.?$", re.IGNORECASE), self.parse_end),

        ]
        # Internal state
        self.indent_level = 0
        self.python_lines = []
        self.ended = False

        # Stack to track open blocks: 'function', 'if', 'loop' (for/while)
        self.block_stack = []

    def indent(self):
        return "    " * self.indent_level

    def parse(self, mage_script):
        self.python_lines = []
        self.indent_level = 0
        self.ended = False
        self.block_stack = []

        lines = mage_script.strip().split('\n')

        for lineno, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line[0] == '#':
                continue

            matched = False
            for pattern, handler in self.patterns:
                match = pattern.fullmatch(line)
                if match:
                    try:
                        handler(*match.groups())
                    except Exception as e:
                        raise SyntaxError(f"Error parsing line {lineno}: '{line}'\n{str(e)}")
                    matched = True
                    break

            if not matched:
                # Ignore filler words but if nothing matched, it's unknown
                # You can tweak this to allow more words ignored or make this a warning
                raise SyntaxError(f"Unknown or unsupported statement at line {lineno}: '{line}'")

            if self.ended:
                break
        # If blocks remain open at end of script, optionally warn or auto-close
        while self.block_stack:
            block = self.block_stack.pop()
            self.indent_level = max(0, self.indent_level - 1)
            # Optionally: self.python_lines.append(f"# Warning: auto-closed {block} block")
        
        return "\n".join(self.python_lines)

    # === Handlers ===
    def parse_let(self, name, value):
        py_line = f"{name} = {self.expr_clean(value)}"
        self.python_lines.append(self.indent() + py_line)

        
    def parse_let_string(self, name, value):
        py_line = f"{name} = \"{self.expr_clean(value)}\""
        self.python_lines.append(self.indent() + py_line)

    def parse_empower(self, name, value):
        py_line = f"{name} += {self.expr_clean(value)}"
        self.python_lines.append(self.indent() + py_line)

    def parse_drain(self, name, value):
        py_line = f"{name} -= {self.expr_clean(value)}"
        self.python_lines.append(self.indent() + py_line)

    def parse_transmute(self, name, value):
        py_line = f"{name} = {self.expr_clean(value)}"
        self.python_lines.append(self.indent() + py_line)

    def parse_print(self, value):
        py_line = f"print({self.expr_clean(value)})"
        self.python_lines.append(self.indent() + py_line)

    def parse_print_string(self, message):
        # Escape quotes properly
        safe_message = message.replace('"', '\\"')
        py_line = f'print("{safe_message}")'
        self.python_lines.append(self.indent() + py_line)

    def parse_function_def(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split(',')) if params else ""
        py_line = f"def {name}({params_clean}):"
        self.python_lines.append(self.indent() + py_line)
        self.indent_level += 1

    def parse_return(self, value):
        py_line = f"return {self.expr_clean(value)}"
        self.python_lines.append(self.indent() + py_line)

    def parse_function_call(self, name, args):
        args = args or ""
        args_clean = ", ".join(arg.strip() for arg in args.split(',')) if args else ""
        py_line = f"{name}({args_clean})"
        self.python_lines.append(self.indent() + py_line)

    def parse_list_conjure(self, name):
        py_line = f"{name} = []"
        self.python_lines.append(self.indent() + py_line)

    def parse_list_add(self, value, name):
        py_line = f"{name}.append({self.expr_clean(value)})"
        self.python_lines.append(self.indent() + py_line)
    
    def parse_list_add_string(self, value, name):
        py_line = f"{name}.append(\"{self.expr_clean(value)}\")"
        self.python_lines.append(self.indent() + py_line)

    def parse_length(self, var_name, list_name):
        py_line = f"{var_name} = len({list_name})"
        self.python_lines.append(self.indent() + py_line)

    def parse_function_def(self, name, params):
        params = params or ""
        params_clean = ", ".join(p.strip() for p in params.split(',')) if params else ""
        self.python_lines.append(self.indent() + f"def {name}({params_clean}):")
        self.indent_level += 1
        self.block_stack.append('function')

    def parse_if(self, condition):
        self.python_lines.append(self.indent() + f"if {self.condition_clean(condition)}:")
        self.indent_level += 1
        self.block_stack.append('if')

    def parse_elif(self, condition):
        if not self.block_stack or self.block_stack[-1] != 'if':
            raise SyntaxError("elif without preceding if")
        self.indent_level -= 1
        self.python_lines.append(self.indent() + f"elif {self.condition_clean(condition)}:")
        self.indent_level += 1

    def parse_else(self):
        if not self.block_stack or self.block_stack[-1] != 'if':
            raise SyntaxError("else without preceding if")
        self.indent_level -= 1
        self.python_lines.append(self.indent() + "else:")
        self.indent_level += 1

    def parse_for(self, iterable, item):
        self.python_lines.append(self.indent() + f"for {item} in {self.expr_clean(iterable)}:")
        self.indent_level += 1
        self.block_stack.append('loop')

    def parse_while(self, condition):
        self.python_lines.append(self.indent() + f"while {self.condition_clean(condition)}:")
        self.indent_level += 1
        self.block_stack.append('loop')

    # === New block close handlers ===
    def parse_close_function(self):
        self.close_block('function')

    def parse_close_if(self):
        self.close_block('if')

    def parse_close_loop(self):
        self.close_block('loop')

    def parse_close_any(self):
        # Close the most recent block regardless of type
        if self.block_stack:
            block = self.block_stack.pop()
            self.indent_level = max(0, self.indent_level - 1)
        else:
            # No open blocks to close; optionally warn or ignore
            pass

    def close_block(self, block_type):
        if not self.block_stack:
            raise SyntaxError(f"Attempted to close a {block_type} block but no blocks are open")
        if self.block_stack[-1] != block_type:
            raise SyntaxError(f"Attempted to close a {block_type} block but current open block is {self.block_stack[-1]}")
        self.block_stack.pop()
        self.indent_level = max(0, self.indent_level - 1)


    def parse_end(self, *args):
        self.ended = True

    # Helpers for cleaning expressions and conditions
    def expr_clean(self, expr):
        # Replace mage comparisons
        expr = expr.lower()
        # Replace mage comparisons to Python
        expr = expr.replace(" wanes below ", " < ")
        expr = expr.replace(" rises above ", " > ")
        expr = expr.replace(" mirrors ", " == ")
        # Remove filler words, e.g., "the", "of", "by", "to", etc. (optional, can expand)
        filler_words = ["the", "of", "by", "to", "from", "with", "and", "a", "an", "on", "in", "upon", "each", "called", "as"]
        pattern = r"\b(" + "|".join(filler_words) + r")\b"
        expr = re.sub(pattern, "", expr)
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


if __name__ == "__main__":
    spellName = input("Spell Name: ")
    spellFile = open(spellName)
    sample_script = spellFile.read()

    parser = MageScriptParser()
    python_code = parser.parse(sample_script)
    #print("Generated Python code:\n")
    #print(python_code)

    spellPYName = spellName + ".py"

    with open(spellPYName, "w") as f:
        f.write(python_code)

    subprocess.run(["python3", spellPYName])