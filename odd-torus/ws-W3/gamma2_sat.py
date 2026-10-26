"""Independent cross-check of the MILP values in min_size_upto12.txt by SAT + cardinality
(pysat, sequential counter): gamma_2 = k iff '2-dominating with |D| <= k' is SAT and
'|D| <= k-1' is UNSAT; same for the min 2-d kernel (adds independence).

Run: python gamma2_sat.py nmax   (reads min_size_upto12.txt for the claimed values)
"""
import sys

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

from common import torus


def feasible(adj, k, independent):
    N = len(adj)
    pool = IDPool(start_from=N + 1)
    cls = []
    for v, nb in enumerate(adj):
        for w in nb:
            cls.append([v + 1] + [u + 1 for u in nb if u != w])
            if independent and v < w:
                cls.append([-(v + 1), -(w + 1)])
    card = CardEnc.atmost(lits=list(range(1, N + 1)), bound=k, vpool=pool,
                          encoding=EncType.seqcounter)
    with Cadical153(bootstrap_with=cls + card.clauses) as s:
        return s.solve()


def main():
    nmax = int(sys.argv[1])
    claimed = {}
    for line in open("min_size_upto12.txt"):
        p = line.split()
        if len(p) > 3 and p[0].isdigit():
            m, n = int(p[0]), int(p[1])
            g2 = int(p[4].split("(")[0])
            i2 = p[6].split("(")[0]
            claimed[(m, n)] = (g2, None if i2 == "None" else int(i2))
    bad = 0
    for (m, n), (g2, i2) in sorted(claimed.items()):
        if n > nmax:
            continue
        verts, idx, adj = torus((m, n))
        ok = feasible(adj, g2, False) and not feasible(adj, g2 - 1, False)
        if i2 is not None:
            ok &= feasible(adj, i2, True) and not feasible(adj, i2 - 1, True)
        bad += not ok
        print(f"m={m} n={n} gamma2={g2} i2={i2} SAT-confirmed={ok}")
        sys.stdout.flush()
    print(f"disagreements: {bad}")


if __name__ == "__main__":
    main()
