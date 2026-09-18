from at_fast import alon_tarsi_fast, line_graph_edges
from alontarsi import alon_tarsi
from best_bound import mk

def E(adj, n):
    return [(u, v) for u in range(n) for v in range(u + 1, n) if (adj[u] >> v) & 1]

cases = [("C_4", mk(4, [(i,(i+1)%4) for i in range(4)])),
         ("C_5", mk(5, [(i,(i+1)%5) for i in range(5)])),
         ("K_4", mk(4, [(i,j) for i in range(4) for j in range(i+1,4)])),
         ("K_5", mk(5, [(i,j) for i in range(5) for j in range(i+1,5)])),
         ("K_2,3", mk(5, [(i,2+j) for i in range(2) for j in range(3)])),
         ("K_3,3", mk(6, [(i,3+j) for i in range(3) for j in range(3)])),
         ("prism", mk(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])),
         ("octahedron", mk(6, [(i,j) for i in range(6) for j in range(i+1,6) if j-i != 3]))]
print("validating the fast routine against the orientation-based one:")
ok = True
for name, (adj, n) in cases:
    a = alon_tarsi_fast(E(adj, n), n)
    b, _ = alon_tarsi(adj, n)
    flag = "ok" if a == b else "MISMATCH"
    if a != b: ok = False
    print(f"  {name:12s} fast={a}  orientations={b}   {flag}")
print("all agree" if ok else "DISAGREEMENT, do not trust the fast routine")
