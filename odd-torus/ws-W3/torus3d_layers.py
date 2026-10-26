"""Explain the 3D table by 'layered' 2-d kernels, and test whether every 2-d kernel is layered.

Layered construction. Fix an axis, say the third. If every layer x3 = const of S is a 2-d
kernel of C_a x C_b, and consecutive layers are disjoint, then S is a 2-d kernel of
C_a x C_b x C_c: independence inside a layer and between layers holds, and a vertex outside
S already has 2 S-neighbours inside its own layer. So a layered kernel exists iff the
'disjointness graph' D(a, b) (vertices: 2-d kernels of C_a x C_b; edges: disjoint pairs)
has a closed walk of length c. The 2-d kernels of C_a x C_b are known exactly by the 2D
classification theorem (diagonal sets), and they are recomputed here by SAT enumeration as
a check.

Parts:
  predict cmax : for 3 <= a <= b <= c <= cmax compute 'layered kernel exists along some
                 axis' and compare with the SAT column of torus3d_upto9.txt.
  layered list : enumerate ALL 2-d kernels of the given triples by SAT and report how
                 many are layered along at least one axis.
"""
import itertools
import sys
from math import gcd

import numpy as np
from pysat.solvers import Cadical153

from common import torus, is_2d_kernel, kernel_clauses


def kernels_2d(a, b):
    """All 2-d kernels of C_a x C_b as frozensets of (r, c), by SAT enumeration."""
    verts, idx, adj = torus((a, b))
    out = []
    with Cadical153(bootstrap_with=kernel_clauses(adj)) as s:
        while s.solve():
            model = s.get_model()[: a * b]
            out.append(frozenset(verts[v - 1] for v in model if v > 0))
            s.add_clause([-v for v in model])
    return out


def closed_walk_lengths(Ks, cmax):
    k = len(Ks)
    if k == 0:
        return set()
    A = np.zeros((k, k), dtype=np.int64)
    for i in range(k):
        for j in range(k):
            if not (Ks[i] & Ks[j]):
                A[i, j] = 1
    out = set()
    P = np.eye(k, dtype=np.int64)
    for c in range(1, cmax + 1):
        P = np.minimum(P @ A, 1)
        if np.trace(P) > 0:
            out.add(c)
    return out


def predict(cmax):
    CW = {}
    for a in range(3, cmax + 1):
        for b in range(a, cmax + 1):
            CW[(a, b)] = closed_walk_lengths(kernels_2d(a, b), cmax)
    sat = {}
    for line in open("torus3d_upto9.txt"):
        p = line.split()
        if len(p) > 4 and p[0].isdigit():
            sat[(int(p[0]), int(p[1]), int(p[2]))] = "YES" in line
    bad = 0
    print("closed-walk lengths <= cmax of the disjointness graph D(a,b) of 2-d kernels:")
    for (a, b), s in sorted(CW.items()):
        if s:
            print(f"   D({a},{b}): |kernels|={len(kernels_2d(a, b))} lengths={sorted(s)}")
    for a, b, c in itertools.combinations_with_replacement(range(3, cmax + 1), 3):
        pred = (c in CW[(a, b)]) or (b in CW[(a, c)]) or (a in CW[(b, c)])
        s = sat.get((a, b, c))
        bad += pred != s
        flag = "" if pred == s else "   <-- DIFFERS"
        print(f"{a} {b} {c}: layered_prediction={pred} SAT={s}{flag}")
    print(f"triples where layered prediction != SAT: {bad}")


def layered_along(S, dims, axis):
    other = [i for i in range(3) if i != axis]
    a, b = dims[other[0]], dims[other[1]]
    _, idx2, adj2 = torus((a, b))
    for t in range(dims[axis]):
        layer = [idx2[(x[other[0]], x[other[1]])] for x in S if x[axis] == t]
        if not is_2d_kernel(adj2, layer):
            return False
    return True


def layered_list(triples):
    for dims in triples:
        verts, idx, adj = torus(dims)
        N = len(verts)
        tot = lay = 0
        with Cadical153(bootstrap_with=kernel_clauses(adj)) as s:
            while s.solve():
                model = s.get_model()[:N]
                S = [verts[v - 1] for v in model if v > 0]
                tot += 1
                lay += any(layered_along(S, dims, ax) for ax in range(3))
                s.add_clause([-v for v in model])
                if tot >= 200000:
                    break
        print(f"{dims}: 2-d kernels enumerated={tot} layered along some axis={lay}")
        sys.stdout.flush()


if __name__ == "__main__":
    if sys.argv[1] == "predict":
        predict(int(sys.argv[2]))
    else:
        layered_list([tuple(map(int, t.split(","))) for t in sys.argv[2:]])
