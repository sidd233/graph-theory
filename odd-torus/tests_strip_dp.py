"""Cross-check strip_dp.find_kernelless against the C checker on random orientations of T(3, n)."""
import random
import sys

from kpc import find_kernelless as c_find
import strip_dp

random.seed(7)
trials = 0
for n in range(3, 10):
    for t in range(60 if n <= 7 else 15):
        orient = {}
        def arc(u, v):
            key = (min(u, v), max(u, v))
            if key not in orient:
                orient[key] = random.random() < 0.5
            return orient[key] == (u < v)
        cells = strip_dp.find_kernelless(n, arc)
        out = [0] * (3 * n)
        for i in range(3):
            for j in range(n):
                for (a, b) in (((i + 1) % 3, j), ((i + 2) % 3, j), (i, (j + 1) % n), (i, (j - 1) % n)):
                    if arc((i, j), (a, b)):
                        out[i * n + j] |= 1 << (a * n + b)
        S = c_find(out)
        assert (cells is None) == (S == 0), (n, cells, S)
        if cells is not None:  # the DP's witness must really be kernel-less
            mask = sum(1 << (i * n + j) for i, j in cells)
            from kpc import has_kernel
            assert not has_kernel(out, mask), (n, cells)
        trials += 1
print("ok", trials, "trials")

# Acyclic orientations are kernel-perfect (Richardson / sink peeling): the DP must say so.
for n in range(3, 14):
    for t in range(10):
        rank = {(i, j): random.random() for i in range(3) for j in range(n)}
        arc = lambda u, v: rank[u] < rank[v]
        assert strip_dp.find_kernelless(n, arc) is None, n
print("acyclic ok")
