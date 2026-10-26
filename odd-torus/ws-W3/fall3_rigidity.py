"""Test: is every fall 3-colouring f of C_b x C_c 'line-shift' type, i.e.
f(y, z) = e*y + g(z) (mod 3) or f(y, z) = e*z + g(y) (mod 3), e = +-1?
Enumerates all fall 3-colourings by SAT with blocking clauses (fixing f(0,0) = 0 to cut the
colour-permutation symmetry is NOT done, all colourings are counted).

Run: python fall3_rigidity.py b,c [b,c ...]
"""
import sys

from pysat.solvers import Cadical153

from common import torus
from fall3 import fall3  # noqa: F401


def clauses(b, c):
    verts, idx, adj = torus((b, c))
    var = lambda v, k: 3 * v + k + 1
    cls = []
    for v in range(len(verts)):
        cls.append([var(v, k) for k in range(3)])
        for k in range(3):
            for l in range(k + 1, 3):
                cls.append([-var(v, k), -var(v, l)])
            for w in adj[v]:
                if v < w:
                    cls.append([-var(v, k), -var(w, k)])
            for l in range(3):
                if l != k:
                    cls.append([-var(v, k)] + [var(w, l) for w in adj[v]])
    return verts, cls


def line_shift(f, b, c):
    for e in (1, -1):
        if all((f[(y + 1) % b][z] - f[y][z] - e) % 3 == 0 for y in range(b) for z in range(c)):
            return True
        if all((f[y][(z + 1) % c] - f[y][z] - e) % 3 == 0 for y in range(b) for z in range(c)):
            return True
    return False


for t in sys.argv[1:]:
    b, c = map(int, t.split(","))
    verts, cls = clauses(b, c)
    N = len(verts)
    tot = ok = 0
    with Cadical153(bootstrap_with=cls) as s:
        while s.solve():
            model = s.get_model()[: 3 * N]
            f = [[0] * c for _ in range(b)]
            for v in range(N):
                for k in range(3):
                    if model[3 * v + k] > 0:
                        y, z = verts[v]
                        f[y][z] = k
            tot += 1
            ok += line_shift(f, b, c)
            s.add_clause([-x for x in model if x > 0])
            if tot >= 100000:
                break
    print(f"C_{b} x C_{c}: fall 3-colourings={tot} line-shift type={ok}")
    sys.stdout.flush()
