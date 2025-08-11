import subprocess
from parser.patterns import PATTERNS
from parser.handlers import Handlers
from parser.parser import MageScriptParser
import os
import sys

class MageScriptInterpreter:
    def interpret(self, scriptPath, write):
        with open(scriptPath) as spellFile:
            spellFileContents = spellFile.read()
        parser = MageScriptParser()
        python_code = parser.parse(spellFileContents)
        if write:
            spellPYName = scriptPath + ".py"
            with open(spellPYName, "w") as f:
                f.write(python_code)
        return python_code
        
    def run_python_code(self, spellPYName):
        original_cwd = os.getcwd()
        spell_dir = os.path.dirname(os.path.abspath(spellPYName))
        try:
            os.chdir(spell_dir)
            result = subprocess.run(["python3", spellPYName], capture_output=True, text=True)
        finally:
            os.chdir(original_cwd)
        return result.stdout, result.stderr, result.returncode

if __name__ == "__main__":
    spellName = None
    if(len(sys.argv) == 2):
        spellName = sys.argv[1]
    else:
        spellName = input("Spell Name: ")
    
    
    interpreter = MageScriptInterpreter()
    
    python_code = interpreter.interpret(spellName, True)
    #print("Generated Python code:\n")
    #print(python_code)


    interpreter.run_python_code(spellName + ".py")
    