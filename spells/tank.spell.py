percent = 50
def filling(amount):
    while amount > 0:
        global percent
        p = str(percent)
        amount -= 1
        percent += 1
        symbol = "%"
        message = str(percent) + str(symbol)
        print(message)
def draining(amount):
    while amount > 0:
        global percent
        p = str(percent)
        amount -= 1
        percent -= 1
        symbol = "%"
        message = str(percent) + str(symbol)
        print(message)
filling(5)
draining(55)