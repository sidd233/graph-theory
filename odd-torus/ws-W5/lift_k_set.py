# Exact set of k for which the Latin-lift orientation of C3 x C_{3k} is NOT kernel-perfect,
# for each of the 12 Latin squares. Refines orch/prove_lift_final.py, which records only the
# parity of k. X_k = set of boolean products of k block generators (one block = 3 columns);
# the lift on C3 x C_{3k} is kernel-perfect iff no product in X_k has zero trace. X_{k+1} is a
# function of X_k, so the sequence X_1, X_2, ... is eventually periodic and the first repeat
# gives the exact answer for every k >= 1.
# Run: ../env/bin/python lift_k_set.py   (from odd-torus/ws-W5)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "orch"))
from automaton import mul, trace, subsets, trans
from latin_lift import latin_squares, column_arcs, row_arcs

def k_profile(L):
    Ms = [{U: trans(column_arcs(L[p]), row_arcs(L[(p - 1) % 3], L[p]), U) for U in subsets()} for p in range(3)]
    gens = frozenset(mul(mul(A, B), C) for A in Ms[0].values() for B in Ms[1].values() for C in Ms[2].values())
    seen = {}
    X = gens
    k = 1
    bad = []
    while X not in seen:
        seen[X] = k
        bad.append(any(not trace(P) for P in X))
        X = frozenset(mul(P, g) for P in X for g in gens)
        k += 1
    return bad, seen[X], k - seen[X]

def is_galvin_type(L):
    # Galvin-type orientation (old odd-torus/galvin_type.py): colour (i + j) mod 3, column edges
    # towards the smaller colour (so source S = colour 2, sink T = colour 0), row edges towards the
    # larger colour. Its column j has type pattern r -> {2: S, 1: M, 0: T}[(r + j) % 3].
    t = {2: 'S', 1: 'M', 0: 'T'}
    return all(L[j][r] == t[(r + j) % 3] for j in range(3) for r in range(3))

for i, L in enumerate(latin_squares()):
    bad, start, period = k_profile(L)
    badk = [k for k in range(1, len(bad) + 1) if bad[k - 1]]
    res = sorted(k % period for k in range(start, start + period) if bad[k - 1])
    tag = " (Galvin-type)" if is_galvin_type(L) else ""
    print(f"square #{i}{tag}: X_k periodic from k = {start}, period {period}; "
          f"bad k in 1..{len(bad)}: {badk}; for k >= {start}: bad iff k mod {period} in {res}")
