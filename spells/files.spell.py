files = "files.spell"
itselffiled = open(files)
itself = itselffiled.read()
print(itself)
with open(files, 'a') as f:
    f.write(itself)