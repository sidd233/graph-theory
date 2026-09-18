"""Broad hunt: does the refinement ever beat the plain kernel method on orientations?"""
from fractions import Fraction
from oriented import orientations, survives
from best_bound import degeneracy
import random
pc = int.bit_count
GRID = sorted({Fraction(a, b) for b in range(2, 10) for a in range(1, b + 1)})

rng = random.Random(20260911)
wins = 0; tested = 0
for n in [5, 6]:
    for _ in range(120):
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        p = rng.choice([0.35, 0.45, 0.55, 0.7])
        adj = [0] * n; E = 0
        for u, v in pairs:
            if rng.random() < p:
                adj[u] |= 1 << v; adj[v] |= 1 << u; E += 1
        if E == 0 or E > 10:
            continue
        tested += 1
        ors = list(orientations(adj, n))
        ker = min((d + 1 for out, d in ors if survives(out, n, 1, 1)), default=None)
        if ker is None:
            continue
        best = None
        for out, d in ors:
            for lam in GRID:
                val = -((-lam.numerator * d) // lam.denominator) + 1
                if val >= ker:
                    continue
                if survives(out, n, lam.numerator, lam.denominator):
                    best = val if best is None else min(best, val)
        if best is not None:
            wins += 1
            print(f"  WIN n={n} adj={adj} kernel={ker} method={best}")
    print(f"n={n}: {tested} graphs tested, {wins} wins so far")
print(f"\ntested {tested} random graphs over ALL orientations and all lam: {wins} wins")
