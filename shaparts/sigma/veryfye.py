from z3 import BitVec, Or, And, sat, unsat, Solver
import json
from sys import argv


def SmallSigma(inp, ra, rb, rc):
    rota = RotR(32, ra, inp)
    rotb = RotR(32, rb, inp)
    shrc = ShR(32, rc, inp)

    s = xor3(rota, rotb, shrc, 32)
    return s


def xor3(a, b, c, n):
    mid = []
    for k in range(n):
        mid.append(b[k] ^ c[k] ^ a[k])
    return mid


def ShR(n, r, inp):
    out = []
    for i in range(n):
        if i + r >= n:
            out.append(0)
        else:
            out.append(inp[i + r])
    return out


def RotR(n, r, inp):
    out = []
    for i in range(n):
        out.append(inp[(i + r) % n])
    return out


constrs = json.load(open("constraints/constr.json"))
witness = json.load(open("witness/witness.json"))
nvars = constrs["nVars"]
nout = constrs["nOutputs"]
out0 = [int(x) for x in witness[1 : 1 + nout]]


inp = [BitVec(f"f_{i}", 1) for i in range(32)]
ar, br, cr = 1, 2, 3
out = SmallSigma(inp, ar, br, cr)

s = Solver()
for i in range(len(out)):
    s.add(out[i] == out0[i])

w = []
i = 0
print("__________________________________________________________")
print("Найденные Входные сигналы:")
if argv[1] == "1":
    if s.check() == sat:
        m = s.model()
        for x in inp:
            w.append(str(m[x]))
    #        with open("twitness/witness.json", "wt") as f:
    #            json.dump(w, f)
    #        with open("data/calculated_input.json", "wt") as f:
    #            json.dump([w[x] for x in range(len(w)) if "main.in" in map[x]], f)
    else:
        print("unsat")
else:
    while s.check() == sat:
        m = s.model()
        for x in inp:
            w.append(str(m[x]))

        print("".join(w))  # len(w))
        #        with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as f:
        #            json.dump({"in": [w[x] for x in range(len(w)) if "main.in" in map[x]]}, f)

        new = []
        for x in inp:
            new.append(x != m[x])
        s.add(Or(new))
        w = []
        i += 1
        if i > 20:
            print("too much")
            exit()
