"""Which graphs can the 2-kernel bound possibly cover?

Target bound: chi(G) <= ceil(D/2) + 1 where D = min over orientations of Delta^+.
Hakimi: min Delta^+ = max over vertex subsets W of ceil(|E(G[W])|/|W|).
Anything violating this is FORBIDDEN from any class the 2-kernel route can serve.
Compare with the kernel bound chi <= D + 1 for calibration.
"""
from itertools import combinations
pc = int.bit_count

def min_maxoutdeg(adj, n):
    best = 0
    for W in range(1, 1 << n):
        e = sum(pc(adj[v] & W) for v in range(n) if (W >> v) & 1) // 2
        k = -(-e // pc(W))
        best = max(best, k)
    return best

def chrom(adj, n):
    # independent sets, then minimum cover by independent sets via IDS over subsets
    full = (1 << n) - 1
    indep = []
    for S in range(1 << n):
        ok = True
        m = S
        while m:
            b = m & -m
            if adj[b.bit_length()-1] & S:
                ok = False; break
            m ^= b
        if ok and S:
            indep.append(S)
    INF = 99
    dp = [INF] * (1 << n)
    dp[0] = 0
    for S in range(1 << n):
        if dp[S] == INF: continue
        rest = full & ~S
        if not rest: continue
        low = rest & -rest          # fix lowest uncovered vertex
        for I in indep:
            if I & low and not (I & S):
                if dp[S | I] > dp[S] + 1:
                    dp[S | I] = dp[S] + 1
    return dp[full]

def canon(adj, n):
    from itertools import permutations
    best = None
    for p in permutations(range(n)):
        bits = 0
        for u in range(n):
            for v in range(u+1, n):
                if (adj[p[u]] >> p[v]) & 1:
                    bits |= 1 << (u * n + v)
        if best is None or bits < best: best = bits
    return best

for n in range(2, 7):
    pairs = list(combinations(range(n), 2))
    seen, viol_k, viol_2k = set(), {}, {}
    for code in range(1 << len(pairs)):
        adj = [0]*n
        for i, (u, v) in enumerate(pairs):
            if (code >> i) & 1:
                adj[u] |= 1 << v; adj[v] |= 1 << u
        c = canon(adj, n)
        if c in seen: continue
        seen.add(c)
        D = min_maxoutdeg(adj, n)
        x = chrom(adj, n)
        if x > D + 1:            viol_k[c]  = (x, D)
        if x > -(-D // 2) + 1:   viol_2k[c] = (x, D, adj[:])
    print(f"n={n}: {len(seen)} graphs | violate kernel bound chi<=D+1: {len(viol_k)}"
          f" | violate 2-kernel bound chi<=ceil(D/2)+1: {len(viol_2k)}")
    if n <= 4:
        for c, (x, D, adj) in viol_2k.items():
            print(f"      chi={x} D={D} adj={adj}")
