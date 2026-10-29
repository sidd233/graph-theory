"""Test the grid-quotient form of the W3 theorem on tensor products and circulants.

Claim tested. Let G = Z^2 / L be a simple 4-regular quotient of the square grid, i.e. L avoids
(1,0), (0,1), (2,0), (0,2), (1,1), (1,-1) up to sign. Put d_+ = gcd{y - x : (x, y) in L} and
d_- = gcd{y + x : (x, y) in L}. Then the number of 2-d kernels of G is
    P(d_+) + P(d_-) - 2 [d_+ and d_- both even],    P = Perrin, P(1) = 0.
For C_m x C_n (Cartesian) this is 2 P(d) - 2 [d even] with d = gcd(m, n).

Families checked here by SAT enumeration of all 2-d kernels:
  tensor  : C_m x C_n (tensor product), 3 <= m <= n, m n <= MAXV. Each component is a grid
            quotient; the formula works out to
              m, n odd          : P(m) + P(n)
              m odd, n even     : P(2m) + P(n) - 2
              m, n even         : (P(m) + P(n) - 2)^2      (two isomorphic components)
  circ    : circulant C_N(a, b), connected, simple, 4-regular, N <= NMAX. Here
            d_+ = gcd(N, a + b), d_- = gcd(N, a - b).
Usage: python grid_quotient_check.py MAXV NMAX
"""
import sys
from itertools import combinations
from math import gcd

from pysat.solvers import Cadical153


def perrin(k):
    P = [3, 0, 2]
    while len(P) <= k:
        P.append(P[-2] + P[-3])
    return P[k]


def count_2d_kernels(nbrs):
    """nbrs: list of neighbour lists (simple graph). Enumerate all 2-d kernels by SAT."""
    var = lambda v: v + 1
    s = Cadical153()
    for v, N in enumerate(nbrs):
        for u in N:
            if u > v:
                s.add_clause([-var(v), -var(u)])
        # outside vertex has >= 2 neighbours inside  <=>  no 3 neighbours all outside (deg 4)
        assert len(N) == 4
        for T in combinations(N, 3):
            s.add_clause([var(v)] + [var(u) for u in T])
    count = 0
    while s.solve():
        model = s.get_model()
        count += 1
        s.add_clause([-l for l in model[:len(nbrs)]])
    s.delete()
    return count


def tensor(m, n):
    V = [(i, j) for i in range(m) for j in range(n)]
    idx = {v: k for k, v in enumerate(V)}
    return [[idx[((i + a) % m, (j + b) % n)] for a in (1, -1) for b in (1, -1)] for i, j in V]


def tensor_formula(m, n):
    if m % 2 and n % 2:
        return perrin(m) + perrin(n)
    if m % 2 == 0 and n % 2 == 0:
        return (perrin(m) + perrin(n) - 2) ** 2
    if m % 2 == 0:
        m, n = n, m
    return perrin(2 * m) + perrin(n) - 2


def circulant(N, a, b):
    return [[(v + s) % N for s in (a, -a, b, -b)] for v in range(N)]


def circ_ok(N, a, b):
    bad = {0}
    return (gcd(gcd(a, b), N) == 1 and a % N not in bad and b % N not in bad
            and (2 * a) % N not in bad and (2 * b) % N not in bad
            and (a + b) % N not in bad and (a - b) % N not in bad)


def circ_formula(N, a, b):
    dp, dm = gcd(N, a + b), gcd(N, abs(a - b))
    return perrin(dp) + perrin(dm) - (2 if dp % 2 == 0 and dm % 2 == 0 else 0)


def main():
    maxv, nmax = int(sys.argv[1]), int(sys.argv[2])
    bad = 0
    cases = 0
    for m in range(3, maxv + 1):
        for n in range(m, maxv // m + 1):
            got, want = count_2d_kernels(tensor(m, n)), tensor_formula(m, n)
            cases += 1
            flag = "" if got == want else "   <-- DISAGREES"
            bad += got != want
            print(f"tensor C{m} x C{n}: count={got} formula={want}{flag}", flush=True)
    print(f"tensor: {cases} cases, disagreements: {bad}\n", flush=True)
    bad2 = cases2 = 0
    for N in range(5, nmax + 1):
        for a in range(1, N // 2 + 1):
            for b in range(a + 1, N // 2 + 1):
                if not circ_ok(N, a, b):
                    continue
                got, want = count_2d_kernels(circulant(N, a, b)), circ_formula(N, a, b)
                cases2 += 1
                bad2 += got != want
                if got != want or got > 0:
                    flag = "" if got == want else "   <-- DISAGREES"
                    print(f"circulant C{N}({a},{b}): count={got} formula={want}{flag}", flush=True)
    print(f"circulant: {cases2} cases (zero-count agreements not printed), disagreements: {bad2}")


if __name__ == "__main__":
    main()
