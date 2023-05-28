from z3 import BitVec, Or, And, sat, unsat, Solver
import json
from sys import argv

from tools.verify import verify as constrs_r1cs
from python_function import f as function, params


def verify(bound=20):
    constrs = json.load(open("constraints/constr.json"))
    map = json.load(open("data/map.json"))["map"]

    nvars = constrs["nVars"]
    nout = constrs["nOutputs"]
    nPubInputs = constrs["nPubInputs"]
    nPrvInputs = constrs["nPrvInputs"]

    print("Вычисляется cхема SmallSigma...")
    s, vars = constrs_r1cs(flag=False)
    
    inp = vars[1 + nout: 1 + nout + nPrvInputs] # TODO NOT PRESENT
    print("Вычисляется SmallSigma...")
    out_python = function(inp, *params)

    newconstrs = []
    for i in range(1, 1 + nout):
        newconstrs.append(vars[i] != out_python[i-1])
    s.add(Or(newconstrs))

    print("Проверяетcя эквивалентность...")
    res = s.check()
    if res == unsat:
        print("Программы эквивалентны.")
    else:
        print("Программы не эквивалентны. Возможные входные данные:")
        w = []
        i = 0
        if argv[1] == "--1":
            if s.check() == sat:
                m = s.model()
                for x in inp:
                    w.append(str(m[x]))
                with open("twitness/witness.json", "wt") as f:
                    json.dump(w, f)
                with open("data/calculated_input.json", "wt") as f:
                    json.dump([w[x] for x in range(len(w)) if "main.in" in map[x]], f)
            else:
                print("unsat")
        elif argv[1] == "--all":
            while s.check() == sat:
                m = s.model()
                for x in inp:
                    w.append(str(m[x]))
    
                print("".join(w))  # len(w))
                with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as f:
                    json.dump(
                        {"in": [w[x] for x in range(len(w)) if "main.in" in map[x]]}, f
                    )
    
                new = []
                for x in inp:
                    new.append(x != m[x])
                s.add(Or(new))
                w = []
                i += 1
                if i > bound:
                    print("too much")
                    break
        else:
            print("unknown option")

verify()
