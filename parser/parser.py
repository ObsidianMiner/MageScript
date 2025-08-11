# parser/magescript_parser.py

import re
from parser.patterns import PATTERNS
from parser.handlers import Handlers
from parser.preproc import MageScriptPreprocessor

class MageScriptParser:
    def __init__(self):
        
        self.indent_level = 0
        self.python_lines = []
        self.ended = False
        self.block_stack = []
        self.handlers = Handlers(self)

        self.patterns = []
        for regex, handler_name in PATTERNS:
            handler_func = getattr(self.handlers, handler_name, None)
            if handler_func is None:
                raise ValueError(f"Handler {handler_name} not found in handlers.py")
            self.patterns.append((regex, handler_func))

    def indent(self):
        return "    " * self.indent_level

    def parse(self, mage_script):
        

        self.python_lines = []
        self.indent_level = 0
        self.ended = False
        self.block_stack = []

        lines = MageScriptPreprocessor(mage_script.strip().split('\n')).spellLines

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
                raise SyntaxError(f"Unknown or unsupported statement at line {lineno}: '{line}'")

            if self.ended:
                break

        while self.block_stack:
            self.block_stack.pop()
            self.indent_level = max(0, self.indent_level - 1)

        self.python_lines = self.handlers.py_lines
        return "\n".join(self.python_lines)