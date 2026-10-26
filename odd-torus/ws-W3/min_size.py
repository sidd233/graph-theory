"""Minimum size of a 2-d kernel (= independent 2-domination number i_2) and the
2-domination number gamma_2 of C_m x C_n, 3 <= m <= n <= nmax, by exact MILP (HiGHS via
scipy.optimize.milp). Also the maximum size of a 2-d kernel.

Compared with the closed forms that follow from the classification theorem (REPORT.md):
    d = gcd(m, n) >= 2:  min |S| = m n ceil(d/3) / d,  max |S| = m n floor(d/2) / d.

Run: python min_size.py nmax
"""
import sys
from math import gcd, ceil

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

from common import torus, is_2d_kernel


def solve(adj, independent, sense=1):
    N = len(adj)
    rows, lo, hi = [], [], []
    for v, nb in enumerate(adj):
        # 2-domination: 2 x_v + sum_{w in N(v)} x_w >= 2
        r = np.zeros(N)
        r[v] += 2
        for w in nb:
            r[w] += 1
        rows.append(r); lo.append(2); hi.append(np.inf)
        if independent:
            for w in nb:
                if v < w:
                    r = np.zeros(N); r[v] = 1; r[w] = 1
                    rows.append(r); lo.append(-np.inf); hi.append(1)
    A = np.array(rows)
    res = milp(c=sense * np.ones(N), constraints=LinearConstraint(A, lo, hi),
               integrality=np.ones(N), bounds=Bounds(0, 1),
               options={"time_limit": 600})
    if res.status == 2 or res.x is None:   # infeasible
        return None, res.status
    S = [v for v in range(N) if res.x[v] > 0.5]
    return S, res.status


def main():
    nmax = int(sys.argv[1])
    print("m n gcd | gamma2(status) | i2=min 2-d kernel (status) formula | "
          "max 2-d kernel formula")
    bad = 0
    for m in range(3, nmax + 1):
        for n in range(m, nmax + 1):
            verts, idx, adj = torus((m, n))
            d = gcd(m, n)
            g, sg = solve(adj, False)
            i2, si = solve(adj, True)
            mx, sm = solve(adj, True, sense=-1)
            if i2 is not None:
                assert is_2d_kernel(adj, i2) and is_2d_kernel(adj, mx)
            fmin = m * n * ceil(d / 3) // d if d > 1 else None
            fmax = m * n * (d // 2) // d if d > 1 else None
            gi = len(i2) if i2 is not None else None
            gm = len(mx) if mx is not None else None
            bad += (gi != fmin) or (gm != fmax) or sg != 0 or (i2 is not None and si != 0)
            print(f"{m} {n} {d} | {len(g)}({sg}) | {gi}({si}) {fmin} | {gm} {fmax}")
            sys.stdout.flush()
    print(f"status 0 = proven optimal by HiGHS; disagreements or non-optimal: {bad}")


if __name__ == "__main__":
    main()
