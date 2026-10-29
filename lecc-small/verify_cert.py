"""Phase 6: independent checker for a kernel-orientation certificate.

Shares no code with kernel_sat.py. Given G (graph6) and ranks r_u(v), it checks:
  (a) ranks at each vertex are a permutation of 0..k-1;
  (b) r_u(v) + r_v(u) = k-1 on every edge, hence Delta+ = k-1 in L(G);
  (c) no odd ring, by its own depth-first enumeration of every odd cycle;
  (d) if |E| <= BRUTE_LIMIT: brute-force kernel-perfectness of the actual orientation of L(G),
      by testing every vertex subset of L(G) for a kernel (no use of the lemma at all).
Run: env/bin/python verify_cert.py data/certs/*.json
"""
import json
import sys

import networkx as nx

BRUTE_LIMIT = 21


def odd_cycles_dfs(adj, n):
    """Yield each odd simple cycle once (smallest vertex first, one direction)."""
    for s in range(n):
        stack = [(s, [s])]
        while stack:
            v, path = stack.pop()
            for w in adj[v]:
                if w == s and len(path) >= 3 and path[1] < path[-1] and len(path) % 2 == 1:
                    yield path
                elif w > s and w not in path:
                    stack.append((w, path + [w]))


def check(cert):
    G = nx.from_graph6_bytes(cert["graph6"].encode())
    k = cert["k"]
    n = G.number_of_nodes()
    r = {(u, v): a for u, v, a in cert["ranks"]}
    adj = [sorted(G[v]) for v in range(n)]
    # (a)
    for u in range(n):
        assert sorted(r[(u, v)] for v in adj[u]) == list(range(k)), f"not a permutation at {u}"
    # (b)
    for u, v in G.edges():
        assert r[(u, v)] + r[(v, u)] == k - 1, f"sum fails on {u}{v}"
    # (c)
    n_odd = 0
    for cyc in odd_cycles_dfs(adj, n):
        n_odd += 1
        m = len(cyc)
        for seq in (cyc, cyc[::-1]):
            ring = all(r[(seq[i], seq[(i + 1) % m])] < r[(seq[i], seq[i - 1])] for i in range(m))
            assert not ring, f"odd ring {seq}"
    # (d)
    brute = None
    E = [tuple(e) for e in G.edges()]
    if len(E) <= BRUTE_LIMIT:
        brute = kernel_perfect_bruteforce(E, r)
        assert brute, "brute force: orientation is NOT kernel-perfect"
    return n_odd, brute


def kernel_perfect_bruteforce(E, r):
    """Orientation of L(G): e -> f if e, f share vertex x and f is ranked above e at x."""
    m = len(E)
    out = [0] * m
    adjL = [0] * m
    for i, (a, b) in enumerate(E):
        for j, (c, d) in enumerate(E):
            if i == j:
                continue
            shared = {a, b} & {c, d}
            if shared:
                x = shared.pop()
                adjL[i] |= 1 << j
                ei = b if x == a else a
                fj = d if x == c else c
                if r[(x, fj)] < r[(x, ei)]:
                    out[i] |= 1 << j
    # every subset S must contain an independent K with every vertex of S-K pointing into K
    for S in range(1, 1 << m):
        if not has_kernel(S, out, adjL):
            return False
    return True


def has_kernel(S, out, adjL):
    # Kernels of D[S] by recursion on sinks first: a sink of D[S] must be in every kernel.
    K = 0
    rest = S
    changed = True
    while changed:
        changed = False
        m = rest
        while m:
            b = m & -m
            m ^= b
            i = b.bit_length() - 1
            if not (out[i] & rest):          # sink in D[rest]: must join K
                K |= b
                rest &= ~b
                # its in-neighbours are dominated; remove them
                m2 = rest
                while m2:
                    b2 = m2 & -m2
                    m2 ^= b2
                    j = b2.bit_length() - 1
                    if out[j] & b:
                        rest &= ~b2
                changed = True
                break
    if rest == 0:
        return True
    # remaining part is sink-free: exhaustive search for an independent dominating K' in rest,
    # with vertices already dominated by K free to stay out
    verts = []
    m = rest
    while m:
        b = m & -m
        m ^= b
        verts.append(b.bit_length() - 1)
    # also remove from 'rest' consideration vertices adjacent to K (cannot join K')
    cand = [v for v in verts if not (adjL[v] & K)]
    for mask in range(1 << len(cand)):
        Kp = 0
        for t, v in enumerate(cand):
            if (mask >> t) & 1:
                Kp |= 1 << v
        ok = True
        mm = Kp
        while mm and ok:
            b = mm & -mm
            mm ^= b
            if adjL[b.bit_length() - 1] & Kp:
                ok = False
        if not ok:
            continue
        KK = K | Kp
        for v in verts:
            if not ((KK >> v) & 1) and not (out[v] & KK):
                ok = False
                break
        if ok:
            return True
    return False


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        cert = json.load(open(fn))
        n_odd, brute = check(cert)
        print(f"{cert['graph6']}: OK  (odd cycles checked: {n_odd}; "
              f"brute-force kernel-perfect: {'yes' if brute else 'skipped'})")
