from z3 import BitVec, Or, And, sat, unsat, Solver, Distinct
from sys import argv

n = 9
m = 3
inp = [[BitVec(f"f_{i}_{j}", 5) for j in range(n)] for i in range(n)]
init = [[6, 8, 5, 1, 3, 0, 0, 4, 7], [7, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 7, 6, 4, 0, 5, 0], [9, 0, 0, 0, 7, 0, 5, 0, 4], [8, 0, 1, 0, 0, 9, 0, 7, 2], [4, 0, 3, 0, 0, 6, 0, 0, 0], [0, 0, 0, 4, 2, 7, 3, 9, 0], [0, 4, 0, 9, 0, 0, 0, 6, 8], [1, 0, 7, 0, 0, 0, 4, 0, 0]]

s = Solver()
s.add([And(x >= 1, x <= n) for r in inp for x in r])
s.add(And([Distinct([inp[i][j] for j in range(n)]) for i in range(n)]))
s.add(And([Distinct([inp[i][j] for i in range(n)]) for j in range(n)]))
s.add(And([Distinct([inp[i // m * m + j // m][(i % m) * m + j % m] for j in range(n)]) for i in range(n)]))
for r, rp in zip(inp, init):
    for i, j in zip(r, rp):
        if j != 0:
            s.add(i == j)

#print(s)

w = []
i = 0
print("__________________________________________________________")
print("Найденные Входные сигналы:")
print(s.check())

if argv[1] == "1":
    if s.check() == sat:
        m = s.model()
        ans = []
        for y in inp:
            tmp = []
            for x in y:
                tmp.append(int(str(m[x])))
                #print(m[x], end=" ")
            ans.append(tmp)
        print(ans)
    else:
        print("unsat")
else:
    while s.check() == sat:
        m = s.model()
        for y in inp:
            for x in y:
                print(m[x], end=" ")
            print()

        new = []
        for y in inp:
            for x in y:
                new.append(x != m[x])
        s.add(Or(new))
        w = []
        i += 1
        if i > 20:
            print("too much")
            exit()
