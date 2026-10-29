"""Check the 3D theorem: 2-d kernels of C_3 x C_b x C_c (Cartesian) versus fall 3-colourings.

Claim tested. For b, c >= 3,
  sigma(C_3 [] C_b [] C_c) = F(b, c)
    = 2 chi(c) [3 | b] + 2 chi(b) [3 | c] - 12 [3 | b and 3 | c],   chi(k) = 2^k + 2 (-1)^k,
and every 2-d kernel meets each triangle fibre {(x, y, z) : x in Z_3} in exactly one vertex.
All 2-d kernels are enumerated by SAT and each is re-checked against the definition.
Usage: python threed_check.py BMAX
"""
import sys
from itertools import combinations

from pysat.solvers import Cadical153


def chi(k):
    return 2 ** k + 2 * (-1) ** k


def formula(b, c):
    return (2 * chi(c) * (b % 3 == 0) + 2 * chi(b) * (c % 3 == 0)
            - 12 * (b % 3 == 0 and c % 3 == 0))


def graph(b, c):
    V = [(x, y, z) for x in range(3) for y in range(b) for z in range(c)]
    idx = {v: k for k, v in enumerate(V)}
    nb = []
    for x, y, z in V:
        N = [idx[((x + 1) % 3, y, z)], idx[((x + 2) % 3, y, z)],
             idx[(x, (y + 1) % b, z)], idx[(x, (y - 1) % b, z)],
             idx[(x, y, (z + 1) % c)], idx[(x, y, (z - 1) % c)]]
        assert len(set(N)) == 6
        nb.append(N)
    return V, nb


def is_2d_kernel(nb, S):
    for v, N in enumerate(nb):
        k = sum(u in S for u in N)
        if (v in S and k > 0) or (v not in S and k < 2):
            return False
    return True


def kernels(nb):
    s = Cadical153()
    var = lambda v: v + 1
    for v, N in enumerate(nb):
        for u in N:
            if u > v:
                s.add_clause([-var(v), -var(u)])
        # v outside => at least 2 of its 6 neighbours inside <=> no 5 neighbours all outside
        for T in combinations(N, len(N) - 1):
            s.add_clause([var(v)] + [var(u) for u in T])
    while s.solve():
        m = s.get_model()[:len(nb)]
        yield {v for v in range(len(nb)) if m[v] > 0}
        s.add_clause([-l for l in m])
    s.delete()


def main():
    bmax = int(sys.argv[1])
    bad = 0
    for b in range(3, bmax + 1):
        for c in range(b, bmax + 1):
            V, nb = graph(b, c)
            count, ok_def, ok_fibre = 0, True, True
            for S in kernels(nb):
                count += 1
                ok_def &= is_2d_kernel(nb, S)
                for y in range(b):
                    for z in range(c):
                        if sum(V[v][1:] == (y, z) for v in S) != 1:
                            ok_fibre = False
            want = formula(b, c)
            agree = count == want and ok_def and ok_fibre
            bad += not agree
            print(f"C3 x C{b} x C{c}: kernels={count} formula={want} "
                  f"definition_ok={ok_def} one_per_fibre={ok_fibre}"
                  + ("" if agree else "   <-- DISAGREES"), flush=True)
    print(f"disagreements: {bad}")


if __name__ == "__main__":
    main()
