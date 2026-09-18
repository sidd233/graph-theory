"""Hunt for ANY graph where the method beats the free degeneracy bound.

To win, the method needs ceil(lam*Delta) + 1 < degen + 1, i.e. it must survive at
some lam with ceil(lam*Delta) <= degen - 1.  So only those lam need testing, which
prunes the search hard: for most graphs that means only very small lam, and small
lam are exactly the hardest to survive.
"""
from fractions import Fraction
from fast import survives
from best_bound import degeneracy, GRID
import random, sys
pc = int.bit_count

def wins(adj, n):
    D = max((pc(a) for a in adj), default=0)
    if D == 0:
        return None
    dg = degeneracy(adj, n)
    for lam in GRID:                       # ascending; first win is the best win
        if -((-lam.numerator * D) // lam.denominator) + 1 >= dg + 1:
            break                          # from here on the method cannot win
        if survives(adj, n, lam.numerator, lam.denominator):
            return (lam, D, dg + 1, -((-lam.numerator * D) // lam.denominator) + 1)
    return None

rng = random.Random(20260911)
found = []
tested = 0
for n in [6, 7, 8, 9]:
    for trial in range(400):
        p = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.75])
        adj = [0] * n
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < p:
                    adj[u] |= 1 << v; adj[v] |= 1 << u
        tested += 1
        w = wins(adj, n)
        if w:
            found.append((n, adj[:], w))
            print(f"  WINNER n={n} adj={adj} lam={w[0]} Delta={w[1]} "
                  f"degen+1={w[2]} method={w[3]}")
    print(f"n={n}: done, {len(found)} winners so far")

print(f"\ntested {tested} random graphs, {len(found)} beat the degeneracy bound")
