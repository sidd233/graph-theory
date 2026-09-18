"""Does L(G) have a kernel-perfect orientation with Delta+ <= cap?

Brute force over 2^|E(L(G))| dies immediately past six edges.  Backtracking with
two prunes gets much further:

  * out-degree cap, enforced as arcs are assigned;
  * no directed triangle, which is necessary because a directed triangle has no
    kernel (chapter 33 says exactly this about the subgraph on {a, c, e}).

Only complete assignments surviving both go to the full kernel-perfectness test.
"""
from itertools import combinations
pc = int.bit_count


def has_kernel(out, adj, S):
    K = S
    while True:
        ok, m = True, K
        while m:
            b = m & -m
            if adj[b.bit_length() - 1] & K:
                ok = False; break
            m ^= b
        if ok:
            m = S & ~K
            while m:
                b = m & -m
                if not (out[b.bit_length() - 1] & K):
                    ok = False; break
                m ^= b
            if ok:
                return True
        if K == 0:
            return False
        K = (K - 1) & S


def kernel_perfect(out, adj, m):
    return all(has_kernel(out, adj, S) for S in range(1, 1 << m))


def find(adj, m, cap):
    """A kernel-perfect orientation with Delta+ <= cap, or None."""
    pairs = [(i, j) for i in range(m) for j in range(i + 1, m) if (adj[i] >> j) & 1]
    if len(pairs) > m * cap:
        return None                                   # counting: impossible
    tri = [(a, b, c) for a, b, c in combinations(range(m), 3)
           if (adj[a] >> b) & 1 and (adj[b] >> c) & 1 and (adj[a] >> c) & 1]
    # triangles become checkable once their last edge is assigned
    pos = {e: t for t, e in enumerate(pairs)}
    fire = [[] for _ in pairs]
    for (a, b, c) in tri:
        last = max(pos[(a, b)], pos[(b, c)], pos[(a, c)])
        fire[last].append((a, b, c))
    out = [0] * m
    deg = [0] * m

    def cyclic(a, b, c):
        return (((out[a] >> b) & 1 and (out[b] >> c) & 1 and (out[c] >> a) & 1) or
                ((out[a] >> c) & 1 and (out[c] >> b) & 1 and (out[b] >> a) & 1))

    def go(t, left):
        if t == len(pairs):
            return kernel_perfect(out, adj, m)
        if sum(cap - d for d in deg) < left:
            return False
        i, j = pairs[t]
        for u, v in ((i, j), (j, i)):
            if deg[u] == cap:
                continue
            out[u] |= 1 << v; deg[u] += 1
            if not any(cyclic(*x) for x in fire[t]):
                if go(t + 1, left - 1):
                    return True
            out[u] &= ~(1 << v); deg[u] -= 1
        return False

    return out[:] if go(0, len(pairs)) else None
