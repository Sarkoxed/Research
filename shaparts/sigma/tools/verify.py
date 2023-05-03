from z3 import BitVec, Solver, sat, Or
import json
from sys import argv

def find_all_solutions(s, map, vars, bound):
    w = []
    i = 0
    print("___________________________________________")
    print("Найденные input:")
    if argv[1] == "--1":
        if s.check() == sat:
            m = s.model()
            for x in vars:
                w.append(str(m[x]))
            print("".join([w[i] for i in range(len(w)) if "main.in" in map[i]]))  # len(w))
            with open("twitness/witness.json", "wt") as f:
                json.dump(w, f)
            with open("data/calculated_input.json", "wt") as f:
                json.dump([w[x] for x in range(len(w)) if "main.in" in map[x]], f)
        else:
            print("unsat")

    elif argv[1] == "--all":
        while s.check() == sat:
            m = s.model()
            for x in vars:
                w.append(str(m[x]))

            print("".join([w[i] for i in range(len(w)) if "main.in" in map[i]]))  # len(w))
            with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as f:
                json.dump(
                    {"in": [w[x] for x in range(len(w)) if "main.in" in map[x]]}, f
                )

            new = []
            for x in vars:
                new.append(x != m[x])
            s.add(Or(new))
            w = []
            i += 1
            if i > bound:
                print("too much")
                exit()
    else:
        print("unknown option")


def verify(bound=20, flag=True):
    constrs = json.load(open("constraints/constr.json"))
    witness = json.load(open("witness/witness.json"))
    map = json.load(open("data/map.json"))["map"]
    
    nvars = constrs["nVars"]
    nout = constrs["nOutputs"]
    ninp = constrs["nPrvInputs"]

    p = int(constrs["prime"])

    out = [int(x) for x in witness[: 1 + nout]] # out[0] = 1
    vars = [BitVec(f"r1cs_var_{i}", 1) for i in range(nvars)]

    s = Solver()
    for i in range(nout + 1):  # 1 included
        s.add(vars[i] == out[i])

    for constr in constrs["constraints"]:
        abc = []
        for i in range(3):
            t = 0
            for varn, var in constr[i].items():
                n = int(varn)
                v = int(var)
                if v > p // 2:
                    v = v - p  # TODO track the optimizations
                t += vars[n] * v
            abc.append(t)
        a, b, c = abc
        s.add(a * b - c == 0)

    if flag:
        find_all_solutions(s, map, vars, bound)
    else:
        return (s, vars)


if __name__ == "__main__":
    verify()
