element = "water"
progress = 0
fire = "fire"
water = "water"
lighting = "lighting"
while not element == fire:
    if element == water:
        progress += 1
        if progress == 20:
            element = "lighting"
            progress = 0
    if element == lighting:
        progress += 1
        if progress == 20:
            element = fire
    print(progress)
    print(element)