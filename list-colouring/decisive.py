"""THE decisive question.

lam = 1 is exactly the classical kernel method: a vertex adjacent to K needs one
out-arc into K, which is kernel-perfectness, and the bound is Delta+ + 1.
lam < 1 is our refinement, the 2-kernel family of ideas.

So compare, over ALL orientations:
    kernel bound  = min over orientations surviving at lam=1 of Delta+ + 1
    method bound  = min over orientations and ALL lam of ceil(lam*Delta+) + 1
If the method never comes in below the kernel bound, the refinement adds nothing
and the whole 2-kernel programme is redundant.  A worse orientation with a better
lam is the only way it can win, so all orientations are searched, not just the
thin ones.
"""
from fractions import Fraction
from oriented import orientations, survives
from best_bound import degeneracy, mk
pc = int.bit_count
GRID = sorted({Fraction(a, b) for b in range(2, 10) for a in range(1, b + 1)})

def compare(adj, n):
    ker, meth, witness = None, None, None
    for out, d in orientations(adj, n):
        if survives(out, n, 1, 1):
            if ker is None or d + 1 < ker:
                ker = d + 1
        for lam in GRID:
            val = -((-lam.numerator * d) // lam.denominator) + 1
            if meth is not None and val >= meth:
                continue
            if survives(out, n, lam.numerator, lam.denominator):
                meth, witness = val, (lam, d)
    return ker, meth, witness

tests = [
    ("C_4",     mk(4, [(i,(i+1)%4) for i in range(4)])),
    ("C_5",     mk(5, [(i,(i+1)%5) for i in range(5)])),
    ("C_6",     mk(6, [(i,(i+1)%6) for i in range(6)])),
    ("K_4",     mk(4, [(i,j) for i in range(4) for j in range(i+1,4)])),
    ("K_2,3",   mk(5, [(i,2+j) for i in range(2) for j in range(3)])),
    ("K_2,4",   mk(6, [(i,2+j) for i in range(2) for j in range(4)])),
    ("K_3,3",   mk(6, [(i,3+j) for i in range(3) for j in range(3)])),
    ("prism",   mk(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])),
    ("P_6",     mk(6, [(i,i+1) for i in range(5)])),
    ("K_1,5",   mk(6, [(0,i) for i in range(1,6)])),
    ("bull",    mk(5, [(0,1),(1,2),(2,0),(0,3),(1,4)])),
    ("K_5",     mk(5, [(i,j) for i in range(5) for j in range(i+1,5)])),
    ("L(K_2,3)",mk(6, [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)])),
]
print(f"{'graph':10s} {'degen+1':>8} {'kernel bd':>10} {'method bd':>10}  {'lam used':>9}  verdict")
for name, (adj, n) in tests:
    k, m, w = compare(adj, n)
    if m is None:
        print(f"{name:10s} {degeneracy(adj,n)+1:>8} {'-':>10} {'-':>10}  {'-':>9}  nothing survives")
        continue
    v = ("REFINEMENT WINS" if k is None or m < k
         else "refinement adds nothing")
    print(f"{name:10s} {degeneracy(adj,n)+1:>8} {str(k):>10} {m:>10}  {str(w[0]):>9}  {v}")
