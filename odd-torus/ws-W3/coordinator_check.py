# Written by the coordinating session as an independent check of the W3 count formula (own SAT encoding).
# Run: ../env/bin/python coordinator_check.py
# Independent check of W3 claims: enumerate 2-d kernels of C_m x C_n with pysat (own encoding).
import sys
from math import gcd
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
def count(m, n, cap=10**6):
    pool = IDPool(); x = lambda r, c: pool.id((r % m, c % n))
    s = Cadical153()
    for r in range(m):
        for c in range(n):
            nb = [x(r+1, c), x(r-1, c), x(r, c+1), x(r, c-1)]
            for y in nb: s.add_clause([-x(r, c), -y])
            # outside => at least 2 of the 4 neighbours in S: every 3 of them contain one
            for skip in range(4):
                s.add_clause([x(r, c)] + [nb[k] for k in range(4) if k != skip])
    V = [x(r, c) for r in range(m) for c in range(n)]
    k = 0
    while s.solve():
        mod = set(l for l in s.get_model() if l > 0)
        s.add_clause([-v if v in mod else v for v in V]); k += 1
        if k >= cap: break
    return k
P = [3, 0, 2]
for i in range(3, 20): P.append(P[i-2] + P[i-3])
bad = 0
for m in range(3, 11):
    for n in range(m, 13):
        d = gcd(m, n); pred = 0 if d == 1 else 2*P[d] - (2 if d % 2 == 0 else 0)
        k = count(m, n)
        bad += k != pred
        if (m, n) in [(3,6),(3,9),(5,10),(6,9),(6,6),(8,8),(9,9)] or k != pred:
            print(f"C{m} x C{n}: {k} 2-d kernels, W3 formula {pred}")
print("disagreements:", bad)
