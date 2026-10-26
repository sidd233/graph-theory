"""Existence of 2-d kernels in C_a x C_b x C_c, 3 <= a <= b <= c <= cmax, by SAT.

Symmetry breaking: the graph is vertex-transitive and a 2-d kernel is nonempty, so we may
assume (0,0,0) is in S (unit clause). Each model is re-checked by the definition.
For SAT cases we also record whether the found kernel is 'layered linear': S equals
{x : (e1 x1 + e2 x2 + e3 x3) mod d in K} for d = gcd(a,b,c), signs e_i = +-1 (this is
just a description of the model, not used for the existence answer).

Run: python torus3d.py cmax  > torus3d.txt
"""
import itertools
import sys
import time
from math import gcd

from pysat.solvers import Cadical153

from common import torus, is_2d_kernel, kernel_clauses


def main():
    cmax = int(sys.argv[1])
    rows = []
    for a, b, c in itertools.combinations_with_replacement(range(3, cmax + 1), 3):
        verts, idx, adj = torus((a, b, c))
        t0 = time.time()
        with Cadical153(bootstrap_with=kernel_clauses(adj) + [[idx[(0, 0, 0)] + 1]]) as s:
            sat = s.solve()
            model = s.get_model() if sat else None
        dt = time.time() - t0
        g = gcd(gcd(a, b), c)
        pg = (gcd(a, b), gcd(a, c), gcd(b, c))
        size = None
        if sat:
            S = [v - 1 for v in model if v > 0]
            assert is_2d_kernel(adj, S)
            size = len(S)
        rows.append((a, b, c, sat))
        print(f"{a} {b} {c} | gcd3={g} pairwise_gcds={pg} | kernel={'YES' if sat else 'no'}"
              f" size={size} | {dt:.2f}s")
        sys.stdout.flush()
    agree = all(sat == (gcd(gcd(a, b), c) > 1) for a, b, c, sat in rows)
    print(f"existence == (gcd(a,b,c) > 1) on all {len(rows)} triples: {agree}")
    for a, b, c, sat in rows:
        if sat != (gcd(gcd(a, b), c) > 1):
            print("  exception:", a, b, c, sat)


if __name__ == "__main__":
    main()
