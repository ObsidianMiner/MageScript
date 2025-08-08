# MageScript
A dumb programing language where you have to speak eveything outloud like a wizard casting a spell.

### The voice has not been added yet but here are the current features:
- Interpret .spell files to .py and automaticly run it.
- Installs python automaticly if not already installed.
- Use interpret command in powershell to interpret, and run .spell files. Otherwise simply run interpret.py

## Example .spell file:
```pickle.spell
#Prints all pickles in the list of pickles.
Conjure an empty tome called pickles
call upon the phrase spicy pickles to the pages of pickles
call upon the phrase smoky pickles to the pages of pickles
call upon the phrase who even am I to the pages of pickles

chant upon the pickles each soul called pickle
    reveal the truth of pickle
    Complete the chant

So it is written
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
