from z3 import BitVec, Solver, sat, Or
import json
from sys import argv


def find_all_solutions(s, map, vars, bound, ninp, nout):
    w = []
    i = 0
    print("___________________________________________")
    print("Найденные input:")
    if argv[1] == "--1":
        if s.check() == sat:
            m = s.model()
            for x in vars:
                w.append(str(m[x]))

            m_inp = "".join([w[i] for i in range(1 + nout, 1 + nout + ninp)])
            print(m_inp)
            with open("twitness/witness.json", "wt") as file:
                json.dump(w, file)
            with open("data/calculated_input.json", "wt") as file:
                json.dump([int(x) for x in m_inp], file)
        else:
            print("unsat")

    elif argv[1] == "--all":
        while s.check() == sat:
            m = s.model()
            print(m)
            print(len(m))
            for x in vars:
                w.append(str(m[x]))

            m_inp = "".join([w[i] for i in range(1 + nout, 1 + nout + ninp)])
            print(ninp)
            print(m_inp)
            with open(f"calculations/input{str(i).zfill(2)}.json", "wt") as file:
                json.dump({"in": [int(x) for x in m_inp]}, file)

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
    nOut = constrs["nOutputs"]
    nInp = constrs["nPrvInputs"]

    p = int(constrs["prime"])

    vars = [BitVec(f"r1cs_var_{i}", 1) for i in range(nvars)]

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
                    v = v - p  # TODO track the optimizations
                t += vars[n] * v
            abc.append(t)
        a, b, c = abc
        s.add(a * b - c == 0)

    if flag:
        out = [int(x) for x in witness[: 1 + nOut]]  # out[0] = 1
        for i in range(nOut + 1):  # 1 included
            s.add(vars[i] == out[i])

        find_all_solutions(s, map, vars, bound, nInp, nOut)
    else:
        return (s, vars)


def check_witness():
    constrs = json.load(open("constraints/constr.json"))
    witness = json.load(open("witness/witness.json"))
    p = int(constrs["prime"])

    assert int(witness[0]) == 1
    for constr in constrs["constraints"]:
        abc = []
        for i in range(3):
            t = 0
            for varn, var in constr[i].items():
                n = int(varn)
                v = int(var)
                if v > p // 2:
                    v = v - p  # TODO track the optimizations
                t += int(witness[n]) * v
            abc.append(t)
        a, b, c = abc
        assert a * b - c == 0


if __name__ == "__main__":
    check_witness()
    verify()
