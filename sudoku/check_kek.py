p = [
    [6, 8, 5, 1, 3, 0, 0, 4, 7],
    [7, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 7, 6, 4, 0, 5, 0],
    [9, 0, 0, 0, 7, 0, 5, 0, 4],
    [8, 0, 1, 0, 0, 9, 0, 7, 2],
    [4, 0, 3, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 4, 2, 7, 3, 9, 0],
    [0, 4, 0, 9, 0, 0, 0, 6, 8],
    [1, 0, 7, 0, 0, 0, 4, 0, 0],
]
s = [
    [6, 8, 5, 1, 3, 2, 9, 4, 7],
    [7, 3, 4, 5, 9, 8, 2, 1, 6],
    [2, 1, 9, 7, 6, 4, 8, 5, 3],
    [9, 2, 6, 8, 7, 1, 5, 3, 4],
    [8, 5, 1, 3, 4, 9, 6, 7, 2],
    [4, 7, 3, 2, 5, 6, 1, 8, 9],
    [5, 6, 8, 4, 2, 7, 3, 9, 1],
    [3, 4, 2, 9, 1, 5, 7, 6, 8],
    [1, 9, 7, 6, 8, 3, 4, 2, 5],
]

n = 9
a = 1
b = 9
m = 3


def distinct(inp):
    x = 1
    prods = [inp[0]]
    for i in range(1, n):
        x *= i
        prods.append(prods[i - 1] * inp[i])

    x *= n
    assert prods[-1] == x

    for i in range(n):
        assert inrange(inp[i], a, b)

    return True


def bits4(inp):
    bits = []
    bitsum = 0
    for i in range(4):
        bits.append((inp >> i) & 1)
        assert bits[i] * (bits[i] - 1) == 0
        bitsum = bitsum + 2**i * bits[i]
    assert bitsum == inp
    return True


def inrange(inp, a, b):
    assert bits4(inp - a)
    assert bits4(inp + (15 - b))
    return True


def Sudoku(puzzle, solution, n, m):
    for i in range(n):
        for j in range(n):
            assert puzzle[i][j] * (puzzle[i][j] - solution[i][j]) == 0

    for i in range(n):
        assert distinct([solution[i][j] for j in range(n)])
        assert distinct([solution[j][i] for j in range(n)])
#        assert distinct([solution[(i // m) * m + (j // m)][(i % m) * m + j % m] for j in range(n)])
#        print([solution[(i // m) * m + (j // m)][(i % m) * m + j % m] for j in range(n)])
   
    print()
    for k in range(3):
        for z in range(3):
            tmp = []
            for i in range(3):
                for j in range(3):
                    tmp.append(solution[k * 3 + j][z * 3 + i])
            assert distinct(tmp)
#            print(tmp)
    return True


print(Sudoku(p, s, n, m))
for i in s:
    print(i)
