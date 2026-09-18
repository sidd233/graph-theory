"""Decisive test of the colour-choice route (B1).

The method stalls at a current graph W exactly when every vertex of W sits in
some bad colour class, since the adversary can then build lists out of bad classes
only.  So the method SUCCEEDS on G iff every induced subgraph of G has a safe vertex.
This is a far weaker demand than the hereditary 2-kernel condition, which the
single-edge argument killed outright.
"""
from itertools import combinations, permutations
from parity import safe_vertices, subsets, good_K
pc = int.bit_count


def survives(adj, n):
    """Does every nonempty induced subgraph have a safe vertex?"""
    for W in range(1, 1 << n):
        if not safe_vertices(adj, W):
            return False, W
    return True, None


def props(adj, n):
    tri = any((adj[u] >> v) & 1 and adj[u] & adj[v] for u in range(n) for v in range(n) if u < v)
    col = [-1] * n
    bip = True
    for s in range(n):
        if col[s] >= 0: continue
        col[s] = 0; st = [s]
        while st:
            v = st.pop(); m = adj[v]
            while m:
                b = m & -m; u = b.bit_length() - 1
                if col[u] < 0: col[u] = 1 - col[v]; st.append(u)
                elif col[u] == col[v]: bip = False
                m ^= b
    return tri, bip


for n in range(1, 7):
    pairs = list(combinations(range(n), 2))
    seen = set(); tot = 0; surv = 0
    surv_tri = surv_bip = tot_tri = tot_bip = 0
    for code in range(1 << len(pairs)):
        adj = [0] * n
        for i, (u, v) in enumerate(pairs):
            if (code >> i) & 1:
                adj[u] |= 1 << v; adj[v] |= 1 << u
        key = min(tuple(sorted((sum(((adj[p[u]] >> p[v]) & 1) << (u * n + v)
                    for u in range(n) for v in range(u + 1, n)),) for p in permutations(range(n)))))
        if key in seen: continue
        seen.add(key); tot += 1
        tri, bip = props(adj, n)
        if not tri: tot_tri += 1
        if bip: tot_bip += 1
        ok, _ = survives(adj, n)
        if ok:
            surv += 1
            if not tri: surv_tri += 1
            if bip: surv_bip += 1
    print(f"n={n}: {surv}/{tot} graphs have a safe vertex in every induced subgraph"
          f"   | triangle-free {surv_tri}/{tot_tri}   | bipartite {surv_bip}/{tot_bip}")
