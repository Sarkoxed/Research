import json
from random import choice

st = '10'

n = 32
a, b, c = [], [], []

for i in range(n):
    a.append(choice(st))
    b.append(choice(st))
    c.append(choice(st))

with open("input.json", "wt") as f:
    json.dump({"a": a, "b": b, "c": c}, f)
    
