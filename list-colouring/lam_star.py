"""For each graph, the BEST bound the method can certify.

lam* = the smallest lam for which the graph survives.  The bound proved is then
ceil(lam* * Delta) + 1.  lam* = 1 means the method proves nothing beyond greedy.
The question that matters: does lam* creep up to 1 as Delta grows?
"""
from fractions import Fraction
from fast import survives
pc = int.bit_count

GRID = sorted({Fraction(a, b) for b in range(2, 9) for a in range(1, b + 1)})

def lam_star(adj, n):
    for lam in GRID:
        if survives(adj, n, lam.numerator, lam.denominator):
            return lam
    return None

def mk(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v; adj[v] |= 1 << u
    return adj, n

def report(name, adj, n):
    D = max((pc(a) for a in adj), default=0)
    L = lam_star(adj, n)
    if L is None:
        print(f"  {name:22s} Delta={D:2d}   lam* = none (fails even at lam=1)")
        return
    proved = -((-L.numerator * D) // L.denominator) + 1
    gain = "GAIN" if proved < D + 1 else "no gain"
    print(f"  {name:22s} Delta={D:2d}   lam* = {str(L):>4s}   "
          f"proves ch <= {proved:2d}  (greedy {D+1:2d})   {gain}")

print("stars (a tree, high degree):")
for m in range(2, 10):
    report(f"K_1,{m}", *mk(m + 1, [(0, i) for i in range(1, m + 1)]))

print("\ncycles:")
for m in [3, 4, 5, 6, 7, 8, 9]:
    report(f"C_{m}", *mk(m, [(i, (i + 1) % m) for i in range(m)]))

print("\ncomplete graphs:")
for m in range(2, 8):
    report(f"K_{m}", *mk(m, [(i, j) for i in range(m) for j in range(i + 1, m)]))

print("\ncomplete bipartite:")
for a, b in [(2,2),(2,3),(3,3),(2,4),(3,4),(4,4),(2,6),(3,5)]:
    report(f"K_{a},{b}", *mk(a + b, [(i, a + j) for i in range(a) for j in range(b)]))

print("\ntrees with larger degree:")
report("double star 3-3", *mk(8, [(0,1)] + [(0,2+i) for i in range(3)] + [(1,5+i) for i in range(3)]))
report("spider legs-2 x4", *mk(9, [(0,1+2*i) for i in range(4)] + [(1+2*i,2+2*i) for i in range(4)]))
report("caterpillar", *mk(9, [(0,1),(1,2),(2,3),(0,4),(0,5),(1,6),(2,7),(3,8)]))
