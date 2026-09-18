"""Can the KERNEL METHOD prove the line-graph conjecture for a given G?

Galvin's argument, stripped to what it needs (Lemma 1 of Chapter 33):
    if L(G) has a KERNEL-PERFECT orientation with Delta+ <= chi'(G) - 1,
    then ch'(G) = chi'(G) for that G.
Galvin built exactly such an orientation when G is bipartite, from a proper edge
colouring plus stable matchings.  The question here is definition-free: does such
an orientation EXIST, for small non-bipartite G?
"""
from itertools import combinations
pc = int.bit_count


def line_graph(edges, n):
    m = len(edges)
    adj = [0] * m
    for i in range(m):
        for j in range(i + 1, m):
            if set(edges[i]) & set(edges[j]):
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return adj, m


def chromatic_index(edges, n):
    """Smallest proper edge colouring, by brute force on the line graph."""
    adj, m = line_graph(edges, n)
    for k in range(1, m + 1):
        col = [-1] * m
        def go(i):
            if i == m:
                return True
            used = {col[j] for j in range(i) if (adj[i] >> j) & 1}
            for c in range(k):
                if c not in used:
                    col[i] = c
                    if go(i + 1):
                        return True
                    col[i] = -1
            return False
        if go(0):
            return k
    return None


def has_kernel(out, adj, S):
    """A kernel of the subdigraph induced on S: independent, and every vertex
    outside it has an arc INTO it."""
    K = S
    while True:
        ok = True
        m = K
        while m:
            b = m & -m
            if adj[b.bit_length() - 1] & K:
                ok = False
                break
            m ^= b
        if ok:
            m = S & ~K
            while m:
                b = m & -m
                if not (out[b.bit_length() - 1] & K):
                    ok = False
                    break
                m ^= b
            if ok:
                return True
        if K == 0:
            return False
        K = (K - 1) & S


def kernel_perfect(out, adj, m):
    return all(has_kernel(out, adj, S) for S in range(1, 1 << m))


def search(name, edges, n):
    adj, m = line_graph(edges, n)
    k = chromatic_index(edges, n)
    cap = k - 1
    pairs = [(i, j) for i in range(m) for j in range(i + 1, m) if (adj[i] >> j) & 1]
    found = None
    for code in range(1 << len(pairs)):
        out = [0] * m
        for t, (i, j) in enumerate(pairs):
            if (code >> t) & 1:
                out[i] |= 1 << j
            else:
                out[j] |= 1 << i
        if max(pc(x) for x in out) > cap:
            continue
        if kernel_perfect(out, adj, m):
            found = out
            break
    print(f"  {name:12s} |E(G)|={m:2d}  chi'={k}  need Delta+ <= {cap}  "
          f"{'KERNEL-PERFECT ORIENTATION EXISTS' if found else 'NONE EXISTS'}")
    return found


print("bipartite controls (Galvin's theorem covers these):")
search("C_4", [(0,1),(1,2),(2,3),(3,0)], 4)
search("path P_4", [(0,1),(1,2),(2,3)], 4)
search("K_2,3", [(i,2+j) for i in range(2) for j in range(3)], 5)
print("\nnon-bipartite, where Galvin's proof does not reach:")
search("C_5", [(i,(i+1)%5) for i in range(5)], 5)
search("triangle", [(0,1),(1,2),(2,0)], 3)
search("K_4", [(i,j) for i in range(4) for j in range(i+1,4)], 4)
