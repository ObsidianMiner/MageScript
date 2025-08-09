import re
import subprocess
from parser.patterns import PATTERNS
from parser.handlers import Handlers
from parser.parser import MageScriptParser

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