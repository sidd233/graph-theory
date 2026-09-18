"""The ceiling on what Alon-Tarsi can ever prove.

The Combinatorial Nullstellensatz behind Alon-Tarsi works with the graph polynomial
prod over edges of (x_u - x_v), whose degree is |E|.  It needs a nonzero coefficient
of prod x_v^{t_v} with SUM t_v = |E|, and then gives L-colourability for
|L(v)| >= t_v + 1.  Since the t_v sum to |E|, the largest of them is at least
|E|/n.  So no bound below

        ceil(|E| / n) + 1 ,  roughly (average degree)/2 + 1,

is reachable by this route, whatever we do.  Halving BELOW that is impossible for
Alon-Tarsi exactly as it was for kernels.  Check how tight AT actually gets.
"""
from alontarsi import alon_tarsi, min_outdeg
from best_bound import degeneracy, mk
pc = int.bit_count

def report(name, adj, n):
    E = sum(pc(a) for a in adj) // 2
    at, _ = alon_tarsi(adj, n)
    mo = min_outdeg(adj, n)
    floor = -(-E // n) + 1
    dg = degeneracy(adj, n) + 1
    tag = "AT hits the Hakimi floor" if at == mo + 1 else "AT above the floor"
    print(f"  {name:12s} |E|={E:2d}  degen+1={dg:2d}  minD+ +1={mo+1:2d}  "
          f"AT={at:2d}  abs.floor={floor:2d}   {tag}")

tests = [
    ("C_4",    mk(4, [(i,(i+1)%4) for i in range(4)])),
    ("C_5",    mk(5, [(i,(i+1)%5) for i in range(5)])),
    ("K_4",    mk(4, [(i,j) for i in range(4) for j in range(i+1,4)])),
    ("K_5",    mk(5, [(i,j) for i in range(5) for j in range(i+1,5)])),
    ("K_2,3",  mk(5, [(i,2+j) for i in range(2) for j in range(3)])),
    ("K_3,3",  mk(6, [(i,3+j) for i in range(3) for j in range(3)])),
    ("prism",  mk(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])),
    ("C_6",    mk(6, [(i,(i+1)%6) for i in range(6)])),
    ("P_6",    mk(6, [(i,i+1) for i in range(5)])),
    ("K_1,5",  mk(6, [(0,i) for i in range(1,6)])),
    ("octahedron", mk(6, [(i,j) for i in range(6) for j in range(i+1,6)
                          if j - i != 3])),
]
for name, (adj, n) in tests:
    report(name, adj, n)
