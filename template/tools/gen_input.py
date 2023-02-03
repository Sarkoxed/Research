import json
from random import choice

st = '10'

n = 32
a = []

for i in range(n):
    a.append(choice(st))

with open("data/input.json", "wt") as f:
    json.dump({"in": a}, f)
