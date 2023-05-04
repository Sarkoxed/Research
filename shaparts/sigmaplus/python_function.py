from z3 import LShR

def SigmaPlus(inp, flag):
    in2, in7, in15, in16 = [inp[i: i + 32] for i in range(0, len(inp), 32)]
    params_sigma1 = [17, 19, 10]
    params_sigma0 = [7, 18, 3]

    out1 = SmallSigma(in2, *params_sigma1)
    print(out1)
    out0 = SmallSigma(in15, *params_sigma0)
    print(out0)

    sum = BinSum([out1, in7, out0, in16], 32, 4, flag)
    print(sum)
    return sum[:32]


def BinSum(inps, n, ops, flag):
    nout = ((2**n - 1) * ops).bit_length()

    lin = 0
    lout = 0

    e2 = 1
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


def SmallSigma(inp, ra, rb, rc):
    rota = RotR(32, ra, inp)
    rotb = RotR(32, rb, inp)
    shrc = ShR(32, rc, inp)

    s = xor3(rota, rotb, shrc, 32)
    return s


def BigSigma(inp, ra, rb, rc):
    rota = RotR(32, ra, inp)
    rotb = RotR(32, rb, inp)
    rotc = RotR(32, rc, inp)

    s = xor3(rota, rotb, rotc, 32)
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


f = SigmaPlus
params = [False]
