import unittest
import os
import io
import random

from Interpret import MageScriptInterpreter

from unittest.mock import patch


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPELLS_DIR = os.path.join(BASE_DIR, "spells")
RESULTS_DIR = os.path.join(BASE_DIR, "spellExpectations")

class TestAllSpells(unittest.TestCase):
    pass  # Tests are added dynamically

def generate_spell_test(spell_filename):
    def test(self):
        spell_path = os.path.join(SPELLS_DIR, spell_filename)
        expected_path = os.path.join(RESULTS_DIR, spell_filename + ".expected")

        # Run and capture output
        interpreter = MageScriptInterpreter()
        interpreter.interpret(spell_path, True) # Creates spell_path.py
        stdout, stderr, returnCode = interpreter.run_python_code(spell_path + ".py", False, os.path.abspath("testEnviorment.py"))

        # Check or create expected output
        if not os.path.exists(expected_path) or getattr(self, "update_snapshots", False):
            with open(expected_path, "w", encoding="utf-8") as f:
                f.write(stdout)
            print(f"[Snapshot created/updated] {expected_path}")
        else:
            with open(expected_path, "r", encoding="utf-8") as f:
                expected = f.read()
            self.assertMultiLineEqual(stdout, expected)
        
        self.assertEqual(stderr, "")
        self.assertEqual(returnCode, 0)
    return test

# Auto-generate test for each .spell file
for file in os.listdir(SPELLS_DIR):
    if file.endswith(".spell"):
        test_func = generate_spell_test(file)
        test_name = f"test_spell_{file.replace('.', '_')}"
        setattr(TestAllSpells, test_name, test_func)

if __name__ == "__main__":
    
    import sys
    update_snapshots = "--update" in sys.argv
    sys.argv = [arg for arg in sys.argv if arg != "--update"]

    TestAllSpells.update_snapshots = update_snapshots

    unittest.main()