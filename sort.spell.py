essences = []
essences.append("fire")
essences.append("shadow")
essences.append("light")
essences.append("water")
essences.append("fire")
essences.append("stone")
chosen = []
fire = "fire"
water = "water"
for e in essences:
    if e == fire:
        chosen.append(e)
    elif e == water:
        chosen.append(e)
for e in chosen:
    print(e)