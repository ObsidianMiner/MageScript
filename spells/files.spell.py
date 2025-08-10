itselffiled = open("files.spell")
itself = itselffiled.read()
print(itself)
with open("files.spell", 'a') as f:
    f.write(itself)