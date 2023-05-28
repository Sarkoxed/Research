from z3 import LShR

def BinSum(inps, n, ops, flag):
    nout = ((2**n - 1) * ops).bit_length()
    print(nout)

    lin = 0
    lout = 0

    e2 = 1
    print(n, ops, len(inps))
    for k in range(0, n):
        for j in range(0, ops):
            lin += inps[j][k] * e2
        e2 += e2

    e2 = 1
    out = []
    for k in range(0, nout):
        out.append((lin & (1 << k)) >> k)
        lout += out[k] * e2
        e2 += e2

    if flag:
        assert lout == lin

    return out


f = BinSum
params = [32, 4, False]
