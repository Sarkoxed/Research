from z3 import BitVec, Solver, sat, Or, Int
import json
from sys import argv


def decomp(r, p):
    lins = []
    while r.children() != []:
        tmp = r.children()
        r = tmp[0]
        lins.append(tmp[1])

    exp = 0
    for x in lins:
        a, b = x.arg(0), int(str(x.arg(1)))
        b = (b * 8) % p

        if b > p // 2:
            b = b - p

        exp += a * b
    return exp


constrs = json.load(open("constraints/constr.json"))
witness = json.load(open("witness/witness.json"))
map = json.load(open("data/map.json"))["map"]

nvars = constrs["nVars"]
nout = constrs["nOutputs"]
ninp = constrs["nPrvInputs"]
p = int(constrs["prime"])
inp = [int(x) for x in witness[1 : 1 + 81]]

vars = [Int(f"var_{i}") for i in range(nvars)]
s = Solver()

s.add(vars[0] == 1)
for i in range(1, 82):
    s.add(vars[i] == inp[i - 1])

for constr in constrs["constraints"]:
    abc = []
    flag = False
    for i in range(3):
        t = 0
        for varn, var in constr[i].items():
            n = int(varn)
            v = int(var)
            if v > p // 2:  # handling - signs
                v = v - p

            t += vars[n] * v

            if (
                v == 10944121435919637611123202872628637544274182200208017171849102093287904247808
            ):
                flag = True

        abc.append(t)

    a, b, c = abc
    if flag:
        a, b = decomp(a, p), decomp(b, p) # handling 8*
#        print(a, b)
    s.add(a * b - c == 0)

w = []
i = 0
print("__________________________________________________________")
print("Найденные witness:")
if argv[1] == "1":
    if s.check() == sat:
        m = s.model()
        for x in vars:
            w.append(str(m[x]))
        with open("twitness/witness.json", "wt") as f:
            json.dump(w, f)
        with open("data/calculated_input.json", "wt") as f:
            json.dump([w[x] for x in range(len(w)) if "main.in" in map[x]], f)
    else:
        print("unsat")
else:
    while s.check() == sat:
        m = s.model()
        for x in vars:
            w.append(str(m[x]))

        print("".join(w))  # len(w))
        with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as f:
            json.dump({"in": [w[x] for x in range(len(w)) if "main.in" in map[x]]}, f)

        new = []
        for x in vars:
            new.append(x != m[x])
        s.add(Or(new))
        w = []
        i += 1
        if i > 20:
            print("too much")
            exit()
