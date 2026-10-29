"""Cross-check the C kernel code against brute force on random digraphs."""
import random
from kpc import find_kernelless, has_kernel


def brute_has_kernel(out, S):
    K = S
    while True:
        ok = all(not (out[v] & K) for v in range(len(out)) if K >> v & 1)
        if ok:
            ok = all(out[v] & K for v in range(len(out)) if (S & ~K) >> v & 1)
        if ok:
            return True
        if K == 0:
            return False
        K = (K - 1) & S


random.seed(1)
for trial in range(3000):
    n = random.randint(1, 9)
    p = random.random()
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                r = random.random()
                if r < 0.45:
                    out[i] |= 1 << j
                elif r < 0.9:
                    out[j] |= 1 << i
                else:
                    out[i] |= 1 << j
                    out[j] |= 1 << i
    full = (1 << n) - 1
    for S in range(1, full + 1):
        assert has_kernel(out, S) == brute_has_kernel(out, S), (out, S)
    bad = [S for S in range(1, full + 1) if not brute_has_kernel(out, S)]
    f = find_kernelless(out)
    if not bad:
        assert f == 0
    else:
        m = min(bin(S).count("1") for S in bad)
        assert f and not brute_has_kernel(out, f) and bin(f).count("1") == m, (out, f, m)
print("ok")
