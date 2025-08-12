import subprocess
from parser.patterns import PATTERNS
from parser.handlers import Handlers
from parser.parser import MageScriptParser
import os
import sys

class MageScriptInterpreter:
    def interpret(self, scriptPath, write = True):
        with open(scriptPath) as spellFile:
            spellFileContents = spellFile.read()
        parser = MageScriptParser()
        python_code = parser.parse(spellFileContents)
        if write:
            spellPYName = scriptPath + ".py"
            with open(spellPYName, "w") as f:
                f.write(python_code)
        return python_code
        
    def run_python_code(self, spellPYName, shouldPrint = True, enviorment: str = None):
        original_cwd = os.getcwd()
        spell_dir = os.path.dirname(os.path.abspath(spellPYName))
        try:
            os.chdir(spell_dir)
            if enviorment:
                result = subprocess.run(["python3", enviorment, spellPYName], input="close\n", capture_output=True, text=True)
            else:
                result = subprocess.run(["python3", spellPYName])
            if shouldPrint:
                print(result.stdout)
        except ValueError:
            print(ValueError)
        finally:
            os.chdir(original_cwd)
        if shouldPrint and result.stderr:
            print(result.stderr)
        return result.stdout, result.stderr, result.returncode

def main():
    spellName = None
    if(len(sys.argv) == 2):
        spellName = sys.argv[1]
    else:
        spellName = input("Spell Name: ")
    
    if not spellName.endswith(".spell"):
        spellName += ".spell"
    if not os.path.exists(spellName):
        print(f"The spell: {spellName} could not be found.")
        return
    interpreter = MageScriptInterpreter()
    
    python_code = interpreter.interpret(spellName, True)
    #print("Generated Python code:\n")
    #print(python_code)


    interpreter.run_python_code(spellName + ".py", False)

if __name__ == "__main__":
    main()