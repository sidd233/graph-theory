from parity import safe_vertices
pc = int.bit_count

def mk(n, edges):
    adj = [0]*n
    for u, v in edges:
        adj[u] |= 1 << v; adj[v] |= 1 << u
    return adj, n

def survives(adj, n):
    for W in range(1, 1 << n):
        if not safe_vertices(adj, W):
            return False, W
    return True, None

def show(name, adj, n):
    ok, W = survives(adj, n)
    D = max(pc(a) for a in adj) if any(adj) else 0
    bad = [v for v in range(n) if (W >> v) & 1] if W is not None else []
    print(f"  {name:26s} Delta={D}  bound=ceil(D/2)+1={-(-D//2)+1}  "
          f"{'SURVIVES' if ok else 'fails on induced ' + str(bad)}")

tests = [
    ("path P6",        mk(6, [(i, i+1) for i in range(5)])),
    ("star K_1,5",     mk(6, [(0, i) for i in range(1, 6)])),
    ("spider/tree",    mk(7, [(0,1),(0,2),(0,3),(1,4),(2,5),(3,6)])),
    ("binary tree 7",  mk(7, [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)])),
    ("cycle C4",       mk(4, [(0,1),(1,2),(2,3),(3,0)])),
    ("cycle C6",       mk(6, [(i,(i+1)%6) for i in range(6)])),
    ("cycle C8",       mk(8, [(i,(i+1)%8) for i in range(8)])),
    ("K_3,3",          mk(6, [(i, 3+j) for i in range(3) for j in range(3)])),
    ("K_2,3",          mk(5, [(i, 2+j) for i in range(2) for j in range(3)])),
    ("K_2,4",          mk(6, [(i, 2+j) for i in range(2) for j in range(4)])),
    ("K_1,3 plus leaf", mk(5, [(0,1),(0,2),(0,3),(3,4)])),
    ("cube Q3",        mk(8, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                              (0,4),(1,5),(2,6),(3,7)])),
    ("subdivided K_1,3", mk(7, [(0,1),(1,2),(0,3),(3,4),(0,5),(5,6)])),
]
for name, (adj, n) in tests:
    show(name, adj, n)
