from z3 import BitVec, Solver, sat, Or
import json
from sys import argv


constrs = json.load(open("constraints/constr.json"))
witness = json.load(open("witness/witness.json"))
map = json.load(open("data/map.json"))["map"]

nvars = constrs["nVars"]
nout = constrs["nOutputs"]
ninp = constrs["nPrvInputs"]

p = int(constrs["prime"])

out = [int(x) for x in witness[1 : 1 + nout]]
# print(out)

vars = [BitVec(f"var_{i}", 1) for i in range(nvars)]

s = Solver()
s.add(vars[0] == 1)

for constr in constrs["constraints"]:
    abc = []
    for i in range(3):
        t = 0
        for varn, var in constr[i].items():
            n = int(varn)
            v = int(var)
            if v > p // 2:
                v = v - p
            t += vars[n] * v
        abc.append(t)
    a, b, c = abc
    s.add(a * b - c == 0)

for i in range(nout):
    s.add(vars[i + 1] == out[i])

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

        print("".join(w))#len(w))
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
