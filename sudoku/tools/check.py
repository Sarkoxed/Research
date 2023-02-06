from sys import argv
import json

a, b = 1, 33
x1 = json.load(open(argv[1]))[a:b]
x2 = json.load(open(argv[2]))[a:b]

if x1 == x2:
    print("Outputs are equal.")
else:
    print("".join(x1))
    print("".join(x2))
    print("Outputs are not equal.")
