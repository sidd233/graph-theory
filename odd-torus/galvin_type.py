"""Galvin-type orientation of the toroidal grid T(m, n), 3 | m and 3 | n.

Colour c(i, j) = (i + j) mod 3, a proper 3-colouring in which every vertex sees both other colours
among its two column neighbours and among its two row neighbours.  Orient column edges
(i, j) -- (i+1, j) towards the smaller colour and row edges (i, j) -- (i, j+1) towards the larger
colour.  Then every vertex has out-degree exactly 2 (c(v) in its column, 2 - c(v) in its row).
For m = n = 3 this is Galvin's orientation of K_3 x K_3 = L(K_{3,3}).

Searches for a smallest kernel-less induced subdigraph, up to --max vertices (default: all).

Run: python3 galvin_type.py m n [--max K]
"""
import argparse
import time

from kpc import find_kernelless, find_kernelless128


def galvin_type(m, n):
    idx = lambda i, j: (i % m) * n + (j % n)
    c = lambda i, j: (i + j) % 3
    out = [0] * (m * n)
    for i in range(m):
        for j in range(n):
            # column edge to (i+1, j): towards the smaller colour
            a, b = (idx(i, j), idx(i + 1, j)) if c(i, j) > c(i + 1, j) else (idx(i + 1, j), idx(i, j))
            out[a] |= 1 << b
            # row edge to (i, j+1): towards the larger colour
            a, b = (idx(i, j), idx(i, j + 1)) if c(i, j) < c(i, j + 1) else (idx(i, j + 1), idx(i, j))
            out[a] |= 1 << b
    assert all(bin(o).count("1") == 2 for o in out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("n", type=int)
    ap.add_argument("--max", type=int, default=None)
    a = ap.parse_args()
    assert a.m % 3 == 0 and a.n % 3 == 0
    out = galvin_type(a.m, a.n)
    t = time.time()
    f = (find_kernelless if a.m * a.n <= 63 else find_kernelless128)(out, a.max)
    cells = sorted((v // a.n, v % a.n) for v in range(a.m * a.n) if f >> v & 1)
    lim = "all sizes" if a.max is None else f"sizes <= {a.max}"
    if f:
        print(f"T({a.m},{a.n}): kernel-less set of size {len(cells)}: {cells}  [{time.time() - t:.1f}s]")
    else:
        print(f"T({a.m},{a.n}): no kernel-less induced subdigraph ({lim})  [{time.time() - t:.1f}s]")


if __name__ == "__main__":
    main()
