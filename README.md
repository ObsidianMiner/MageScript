# MageScript  
A dumb programming language where you have to speak everything out loud like a wizard casting a spell.

### Voice input hasn't been added yet, but here are the current features:
- Interprets .spell files into .py and automatically runs them.  
- Automatically installs Python if it's not already installed.  
- Use the interpret command in PowerShell to interpret and run .spell files. Otherwise, simply run interpret.py.

## How to use

1. Run setup.bat
    - installs python, and "interpret" powershell command
2. If you are using vs code install the MageScript extension via vscodeExt/magescript-syntax/magescript-syntax-3.0.1.vsix
3. Check out reference spells, and MageScript Language Reference.md
    - I recommend popping up the language reference in a side window if you are using vs code.
4. Create a .spell file anywhere on your device, and run it by putting this into powershell:
```
    interpret <filename>.spell
```
## Example .spell file:
```pickle.spell
#Prints all pickles in the list of pickles.
Conjure an empty tome called pickles
call upon the phrase spicy pickles to the pages of pickles
call upon the phrase smoky pickles to the pages of pickles
call upon the phrase who even am I to the pages of pickles

chant upon pickles each soul called pickle
    reveal the truth of pickle
    Complete the chant

so it is written
```
This compiles to
```pickle.spell.py
pickles = []
pickles.append("spicy pickles")
pickles.append("smoky pickles")
pickles.append("who even am i")
for pickle in pickles:
    print(pickle)
```
