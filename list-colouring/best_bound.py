"""The honest benchmark.

The method is only worth anything if it beats the bounds you get for free:
  greedy       ch <= Delta + 1
  degeneracy   ch <= degen + 1,  degen = max over subgraphs of the min degree
Survival is NOT monotone in lam (the bad-degree sets for different lam are not
nested), so take the best bound over every lam that survives, not the first.
"""
from fractions import Fraction
from fast import survives
pc = int.bit_count

GRID = sorted({Fraction(a, b) for b in range(2, 10) for a in range(1, b + 1)})


def degeneracy(adj, n):
    W, best = (1 << n) - 1, 0
    for _ in range(n):
        if W == 0:
            break
        v = min((x for x in range(n) if (W >> x) & 1), key=lambda x: pc(adj[x] & W))
        best = max(best, pc(adj[v] & W))
        W &= ~(1 << v)
    return best


def best_method_bound(adj, n):
    D = max((pc(a) for a in adj), default=0)
    best, arg = D + 1, None
    for lam in GRID:
        if survives(adj, n, lam.numerator, lam.denominator):
            b = -((-lam.numerator * D) // lam.denominator) + 1
            if b < best:
                best, arg = b, lam
    return best, arg, D


def mk(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v; adj[v] |= 1 << u
    return adj, n


def report(name, adj, n):
    b, lam, D = best_method_bound(adj, n)
    dg = degeneracy(adj, n) + 1
    verdict = "BEATS BOTH" if b < min(D + 1, dg) else ("ties degen" if b == dg else "loses")
    print(f"  {name:20s} Delta={D:2d}  greedy={D+1:2d}  degen+1={dg:2d}  "
          f"method={b:2d} (lam={str(lam) if lam else '-':>4s})   {verdict}")


print("families with growing Delta:")
for m in range(3, 10):
    report(f"star K_1,{m}", *mk(m + 1, [(0, i) for i in range(1, m + 1)]))
print()
for m in [3, 4, 5, 6, 7]:
    report(f"K_2,{m}", *mk(2 + m, [(i, 2 + j) for i in range(2) for j in range(m)]))
print()
for m in [3, 4, 5]:
    report(f"K_{m},{m}", *mk(2 * m, [(i, m + j) for i in range(m) for j in range(m)]))
print()
for m in [4, 6, 8, 9]:
    report(f"cycle C_{m}", *mk(m, [(i, (i + 1) % m) for i in range(m)]))
print()
report("cube Q3", *mk(8, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                          (0,4),(1,5),(2,6),(3,7)]))
report("Petersen-ish 8", *mk(8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(0,3),(4,7)]))
report("double star 4-4", *mk(10, [(0,1)] + [(0,2+i) for i in range(4)] + [(1,6+i) for i in range(4)]))
