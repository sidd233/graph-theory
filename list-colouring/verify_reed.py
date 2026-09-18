"""Calibrate the target. In the symmetric (undirected) setting d^+ = d, so the
2-kernel accounting would give chi <= ceil(Delta/2) + 1.  Compare that with
Reed's form ceil((Delta + 1 + omega)/2), which has extra slack of about omega/2.
"""
from itertools import combinations, permutations
import sys
sys.path.insert(0, '.')
from check_target import chrom, canon
pc = int.bit_count

def omega(adj, n):
    best = 0
    for S in range(1 << n):
        ok = True; m = S
        while m:
            b = m & -m; v = b.bit_length()-1
            if (adj[v] | b) & S != S: ok = False; break
            m ^= b
        if ok: best = max(best, pc(S))
    return best

for n in range(2, 8):
    pairs = list(combinations(range(n), 2))
    seen = set(); bad_half = 0; bad_reed = []
    for code in range(1 << len(pairs)):
        adj = [0]*n
        for i, (u, v) in enumerate(pairs):
            if (code >> i) & 1:
                adj[u] |= 1 << v; adj[v] |= 1 << u
        c = canon(adj, n)
        if c in seen: continue
        seen.add(c)
        D = max(pc(a) for a in adj); x = chrom(adj, n); w = omega(adj, n)
        if x > -(-D // 2) + 1: bad_half += 1
        if x > -(-(D + 1 + w) // 2): bad_reed.append((x, D, w, adj[:]))
    print(f"n={n}: {len(seen)} graphs | violate chi<=ceil(D/2)+1: {bad_half}"
          f" | violate Reed ceil((D+1+w)/2): {len(bad_reed)}")
    if n == 7: break
