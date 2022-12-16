from z3 import BitVec, Solver, sat
import json


constrs = json.load(open("constraints/constr.json"))
witness = json.load(open("witness/witness.json"))


nvars = constrs["nVars"]
nout = constrs["nOutputs"]
ninp = constrs["nPrvInputs"]

p = int(constrs["prime"])

out = [int(x) for x in witness[1: 1 + nout]]
print(out)

vars = [BitVec(f"var_{i}", 1) for i in range(nvars)]

s = Solver()
s.add(vars[0] == 1)

for constr in constrs["constraints"]:
#    print(constr)
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
#    print(a)
#    print(b)
#    print(c)
    s.add(a * b - c == 0)

for i in range(nout):
    s.add(vars[i + 1] == out[i])

w = []
if s.check() == sat:
    m = s.model()
    for x in vars:
        w.append(str(m[x]))

    with open("calculated_witness.json", "wt") as f:
        json.dump(w, f)
else:
    print("unsat")
