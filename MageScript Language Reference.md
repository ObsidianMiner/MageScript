# ✦ MageScript Language Specification & Reference (v4.0) ✦
> *"Speak the code as if you summon the arcane."*


## Overview

MageScript is a theatrical, speech-driven programming language built to compile into Python. It combines magical, spell-like phrases with programming logic, allowing users to write code through vocal incantations or stylized script.

---

## Syntax

### 1. Variable Declaration & Assignment

| Phrase                                   | Meaning                       | Python Equivalent          |
|------------------------------------------|------------------------------|---------------------------|
| `Let [name] be [value]`                   | Declare or assign variable   | `name = value`             |
| `Speak the name of [name] to be [value]` | Assign string value          | `name = "value"`           |

### 2. Reassignment

| Phrase                  | Operation           | Python Equivalent    |
|-------------------------|---------------------|---------------------|
| `Empower [name] by [value]` | Add to variable  | `name += value`      |
| `Drain [name] by [value]`   | Subtract          | `name -= value`      |
| `Transmute [name] with [value]` | Assign new value | `name = value`       |
| `Enfold [name] with the multiplicative power of [value]`   | Multiply          | `name -= value`      |
| `Divide the soul of [name] by the decree of [value]`   | Divide          | `name -= value`      |
| `Mark [name] with the remainder after striking by [value]`   | Modulo          | `name -= value`      |

### 3. Arithmetic

| Phrase                                | Meaning              | Python Equivalent |
|----------------------------------------|-----------------------|-------------------|
| `with the multiplicative power of`     | Multiply              | `*`               |
| `joined with`                          | Add                   | `+`               |
| `drained of`                           | Subtract              | `-`               |
| `striked by`                           | Divide                | `/`               |
| `modulo`                               | Modulo (remainder)    | `%`               |
| `to the power of`                      | Exponentiation        | `**`              |

> These phrases allow chaining complex expressions within natural, spoken-like sentences.

### 4. Lists & Arrays

| Phrase                            | Meaning                      | Python Equivalent     |
|-----------------------------------|------------------------------|----------------------|
| `Conjure an empty tome called [name]` | Create empty list       | `name = []`           |
| `Add [value] to the pages of [name]`  | Append element           | `name.append(value)`  |
| `Call forth the word [value] to the pages of [name]` | Append string    | `name.append("value")`|
| `Let [name] be the length of [list]`  | Get list length          | `name = len(list)`    |

### 5. Loops (Chants)

| Phrase                                           | Meaning            | Python Equivalent          |
|--------------------------------------------------|--------------------|---------------------------|
| `Chant upon [list], each soul called [item]`     | For loop over list | `for item in list:`        |
| `Sustain the chant while [condition] holds true` | While loop         | `while condition:`         |
| `scatter the chant to the winds of finality`         | break              | `break`                     |
| `pass over this soul in silence`                 | continue           | `continue`                |

### 6. Functions (Rituals)

| Phrase                                               | Meaning                    | Python Equivalent              |
|-----------------------------------------------------|-----------------------------|---------------------------------|
| `Inscribe ritual [name] with [param] and [param2]` | Define function              | `def name(param, param2):`       |
| `Invoke the ritual of [name], offering [arg] and [arg2]`      | Call function     | `name(args)`          |
| `summon [value] as the spirits from the ritual of [name] offering [arg] and [arg2]` | Call function with return | `value = name(args)` |
| `Return [value] to the aether`                       | Return statement           | `return value`                 |
| `Close the incantation`                              | End function block         | Dedent block                   |
| `Share [name] with the spirits`                      | Get Global Variable        | `global name`                   |

### 7. Conditionals (Fate)

| Phrase                                  | Meaning             | Python Equivalent          |
|-----------------------------------------|---------------------|---------------------------|
| `If fate whispers [condition]`           | if statement        | `if condition:`            |
| `Else if fate shifts [condition]`        | elif statement      | `elif condition:`          |
| `Else when all omens fail`               | else statement      | `else:`                    |
| `Let the omen pass`                      | End conditional block | Dedent block             |

#### Comparisons in conditions

| MageScript Phrase      | Python Equivalent |
|------------------------|-------------------|
| `wanes below [value]`  | `< [value]`       |
| `rises above [value]`  | `> [value]`       |
| `mirrors [value]`      | `== [value]`      |

---

### 8. Output & Input

| Phrase                                   | Meaning         | Python Equivalent       |
|------------------------------------------|-----------------|-------------------------|
| `Reveal the truth of [value]`            | Print variable  | `print(value)`          |
| `Let the spell echo [message]`        | Print string    | `print("message")`      |
| `Whisper to the void [message]`        | Print string    | `print("message")`       |
| `ask the stars for [value] saying [prompt]`            | Input prompt    | `value = input("prompt")`|
| `seek the ether for [value] with the words [prompt]`            | Input prompt    | `value = input("prompt")`|

---

### 9. Block Closures & Spell Endings

| Phrase                        | Meaning                  |
|-------------------------------|--------------------------|
| `Close the incantation`       | Close function block     |
| `Let the omen pass`           | Close conditional block  |
| `Complete the chant`          | Close loop block         |
| `Seal the spell`              | Close any open block     |
| `Vanish the beast`            | Close class block        |
| `So it is written.`           | End spell & compile      |
| `The spell is complete.`      | End spell & compile      |
| `Thus concludes the incantation.` | End spell & compile  |
| `Let it be done.`             | End spell & compile      |

### 10. String Creation & Type Conversion

| Phrase                                   | Meaning         | Python Equivalent       |
|------------------------------------------|-----------------|-------------------------|
| `Conjure the phrase [name] using [parts...]`| Join elements as string  | `name = "a" + str(b) + "c"`          |
| `Let [name] be the spelltext of [value]"`        | Cast to a string    | `name = str(value)`      |

### 11. Filesystem
| Phrase                                                                | Meaning                     | Python Equivalent                           |
|-------------------------------------------------------------------------------------|-----------------------------|---------------------------------------------|
| `Unseal the scroll [varname] from [filename]`                                       | Read file into variable     | `varname = open(filename).read()`           |
| `By quill of eternity let the tome of [filename] be born etched in [varname] and sealed in flame` | Write contents to file       | `open(filename, 'w').write(content)`        |
| `Extend the infinite scroll of [filename] with [varName] that its verses may never cease` | Append contents to file      | `open(filename, 'a').write(content)`        |
| `Purge the chronicle of [filename] from the vault of aeons that even the gods forget it once was` | Delete a file               | `os.remove(filename)`                       |
reading line by line, checking if a file or directory exists, as well as creating directories is coming soon...

### 12. Classes (Abominations)

| Phrase                                                     | Meaning                      | Python Equivalent                          |
|------------------------------------------------------------|------------------------------|--------------------------------------------|
| `Proclaim a(n) [type] abomination`       | Define a class                | `class ClassName:`                          |
| `Fuel the abomination with [param] and [param2]`            | Define the constructor (__init__) with parameters | `def __init__(self, param, param2):`         |
| `Birth an abomination of [ClassName] named [instanceName] fueled with [args]` | Instantiate an object of a class with arguments | `instanceName = ClassName(args)`              |
| `The beast`       | Referencing itself                | `self`                          |
---

## Code Structure & Parsing Notes

- Indentation is managed via block stack.
- Block openers increase indentation; closers decrease it.
- Error handling for mismatched block closures.
- Functions are called rituals; variables are named magically.
- Everything in mage script is lowercase except for strings.
- You don't create string litterals via quotes ("), instead you use speak the name of
- The language is meant to be spoken out loud so make sure to not include things that cannot be spoken as words.

## Example Reference Spells

```spell
let power be 42
let name be "eldrin"
let max_power be 100

reveal the truth of name
reveal the truth of "initiating spell test..."

if fate whispers power wanes below 50
    reveal the truth of "power is below half."
else when all omens fail
    reveal the truth of "power is strong."
let the omen pass

conjure an empty tome called energies
add 10 to the pages of energies
add 20 to the pages of energies
add 30 to the pages of energies

let count be the length of energies
reveal the truth of count

chant upon energies each soul called e
    reveal the truth of e
complete the chant

let i be 0
sustain the chant while i wanes below 3 holds true
    reveal the truth of i
    empower i by 1
complete the chant

inscribe ritual greet with person
    let message be "greetings, " + person
    reveal the truth of message
    return message to the aether
close the incantation

invoke the ritual of greet offering "traveler"
invoke the ritual of greet offering "s"

seal the spell
so it is written.
```

> If you made it to the bottom trying to figure out how to use this, you must be going insane by now.