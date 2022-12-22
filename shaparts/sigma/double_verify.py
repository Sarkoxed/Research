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


def gen_python(inp, ar=1, br=2, cr=3):
    out = SmallSigma(inp, ar, br, cr)
    return out


def gen_r1cs(inp, out, constrs, map, nvars, p):
    vars = []
    j = 0
    for i in range(nvars):
        if "main.in" not in map[i]:
            vars.append(BitVec(f"var_{i}", 1))
        else:
            vars.append(inp[j])
            j += 1

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

    for i in range(nout):  # TODO change that to if "main,out" in ...
        s.add(vars[i + 1] != out[i])  # this might be changed to !=
    return s


constrs = json.load(open("constraints/constr.json"))
map = json.load(open("data/map.json"))["map"]

nvars = constrs["nVars"]
nout = constrs["nOutputs"]
ninp = constrs["nPrvInputs"]
p = int(constrs["prime"])

inp = [BitVec(f"f_{i}", 1) for i in range(ninp)]
out = gen_python(inp)
s = gen_r1cs(inp, out, constrs, map, nvars, p)

print(s.check())
# w = []
# i = 0
# if argv[1] == "1":
#    if s.check() == sat:
#        m = s.model()
#        for x in inp:
#            w.append(str(m[x]))
#        with open("twitness/witness.json", "wt") as f:
#            json.dump(w, f)
#        with open("data/calculated_input.json", "wt") as f:
#            json.dump([w[x] for x in range(len(w)) if "main.in" in map[x]], f)
#    else:
#        print("unsat")
# else:
#    while s.check() == sat:
#        m = s.model()
#        for x in inp:
#            w.append(str(m[x]))
#
#        print("".join(w))#len(w))
#        with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as f:
#            json.dump({"in": [w[x] for x in range(len(w)) if "main.in" in map[x]]}, f)
#
#        new = []
#        for x in inp:
#            new.append(x != m[x])
#        s.add(Or(new))
#        w = []
#        i += 1
#        if i > 20:
#            print("too much")
#            exit()
