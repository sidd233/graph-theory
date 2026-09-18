from fractions import Fraction
from oriented import orientations, survives
from best_bound import degeneracy, mk
pc = int.bit_count

GRID = sorted({Fraction(a, b) for b in range(2, 10) for a in range(1, b + 1)})

def min_outdeg(adj, n):
    best = 0
    for W in range(1, 1 << n):
        e = sum(pc(adj[v] & W) for v in range(n) if (W >> v) & 1) // 2
        best = max(best, -(-e // pc(W)))
    return best

def best(adj, n, slack=1):
    """Best bound over orientations with small Delta+ and over lam."""
    mo = min_outdeg(adj, n)
    dg = degeneracy(adj, n) + 1
    b, arg = None, None
    for out, d in orientations(adj, n, maxout=mo + slack):
        for lam in GRID:
            val = -((-lam.numerator * d) // lam.denominator) + 1
            if b is not None and val >= b:
                continue
            if survives(out, n, lam.numerator, lam.denominator):
                b, arg = val, (lam, d)
    return b, arg, dg, mo

tests = [
    ("C_4",    mk(4, [(i,(i+1)%4) for i in range(4)])),
    ("C_5",    mk(5, [(i,(i+1)%5) for i in range(5)])),
    ("C_6",    mk(6, [(i,(i+1)%6) for i in range(6)])),
    ("K_4",    mk(4, [(i,j) for i in range(4) for j in range(i+1,4)])),
    ("K_2,3",  mk(5, [(i,2+j) for i in range(2) for j in range(3)])),
    ("K_2,4",  mk(6, [(i,2+j) for i in range(2) for j in range(4)])),
    ("K_3,3",  mk(6, [(i,3+j) for i in range(3) for j in range(3)])),
    ("tree P6",mk(6, [(i,i+1) for i in range(5)])),
    ("K_1,5",  mk(6, [(0,i) for i in range(1,6)])),
    ("prism",  mk(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])),
]
print(f"{'graph':10s} {'degen+1':>8} {'minD+':>6} {'kernel bd':>10} {'best method':>12}  verdict")
for name, (adj, n) in tests:
    b, arg, dg, mo = best(adj, n)
    kb = mo + 1
    v = "BEATS degeneracy" if b is not None and b < dg else "no gain"
    got = f"{b} (lam={arg[0]}, D+={arg[1]})" if b else "none survives"
    print(f"{name:10s} {dg:>8} {mo:>6} {kb:>10} {got:>12}  {v}")
