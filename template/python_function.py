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


f = SmallSigma
ar, br, cr = 17, 19, 10
params = [ar, br, cr]
