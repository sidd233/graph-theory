"""Why the symmetric setting was the wrong arena.

Working with G as an undirected graph means out-degree = degree, and that is exactly
the setting where the kernel method has NO power over greedy: it just says
ch <= Delta + 1.  The kernel method's whole point is to use an ORIENTATION, where
Hakimi gives min Delta^+ = max over subgraphs of ceil(|E(H)|/|V(H)|), which can be
about HALF the degeneracy.  That factor of two is the headroom I threw away.
"""
from best_bound import degeneracy, mk
pc = int.bit_count

def min_outdeg(adj, n):
    best = 0
    for W in range(1, 1 << n):
        e = sum(pc(adj[v] & W) for v in range(n) if (W >> v) & 1) // 2
        best = max(best, -(-e // pc(W)))
    return best

fams = [("star K_1,7", mk(8, [(0,i) for i in range(1,8)])),
        ("K_2,5",      mk(7, [(i,2+j) for i in range(2) for j in range(5)])),
        ("K_3,3",      mk(6, [(i,3+j) for i in range(3) for j in range(3)])),
        ("K_4,4",      mk(8, [(i,4+j) for i in range(4) for j in range(4)])),
        ("K_5,5",      mk(10,[(i,5+j) for i in range(5) for j in range(5)])),
        ("cube Q3",    mk(8, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                              (0,4),(1,5),(2,6),(3,7)])),
        ("C_8",        mk(8, [(i,(i+1)%8) for i in range(8)])),
        ("K_6",        mk(6, [(i,j) for i in range(6) for j in range(i+1,6)]))]

print(f"{'graph':14s} {'Delta':>6} {'degen+1':>8} {'minD+ +1':>9} {'2-kernel dream':>15}")
for name, (adj, n) in fams:
    D = max(pc(a) for a in adj)
    dg = degeneracy(adj, n) + 1
    mo = min_outdeg(adj, n)
    print(f"{name:14s} {D:>6} {dg:>8} {mo+1:>9} {-(-mo//2)+1:>15}")
