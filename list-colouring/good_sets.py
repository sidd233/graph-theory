"""Which colour classes can the 2-kernel step handle?

Working in the symmetric setting (an undirected graph G read as a digraph with
both arcs), the condition the induction needs on the colour class S is:

    there is a NONEMPTY INDEPENDENT K inside S such that no vertex of S \ K has
    EXACTLY ONE neighbour in K.

Zero neighbours is fine: such a vertex keeps the colour and loses nothing.
Two or more is fine: it pays for the lost colour with two lost edges.
Exactly one is the only bad case.  Call such a K a "2-or-0 set", and call the
graph GOOD if one exists, BAD otherwise.
"""
from itertools import combinations, permutations
pc = int.bit_count


def good_set(adj, n, S=None):
    """Return a 2-or-0 set of G[S], or None."""
    if S is None:
        S = (1 << n) - 1
    K = S
    while True:
        if K:
            ok = True
            m = K
            while m:                                   # K independent?
                b = m & -m
                if adj[b.bit_length() - 1] & K:
                    ok = False
                    break
                m ^= b
            if ok:
                m = S & ~K
                while m:                               # nobody sees exactly one
                    b = m & -m
                    if pc(adj[b.bit_length() - 1] & K) == 1:
                        ok = False
                        break
                    m ^= b
                if ok:
                    return K
        if K == 0:
            return None
        K = (K - 1) & S


def is_connected(adj, n):
    seen, stack = 1, [0]
    while stack:
        v = stack.pop()
        m = adj[v] & ~seen
        while m:
            b = m & -m
            seen |= b
            stack.append(b.bit_length() - 1)
            m ^= b
    return seen == (1 << n) - 1


def bipartite(adj, n):
    colour = [-1] * n
    for s in range(n):
        if colour[s] >= 0:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            v = stack.pop()
            m = adj[v]
            while m:
                b = m & -m
                u = b.bit_length() - 1
                if colour[u] < 0:
                    colour[u] = 1 - colour[v]
                    stack.append(u)
                elif colour[u] == colour[v]:
                    return None
                m ^= b
    return colour


def canon(adj, n):
    best = None
    for p in permutations(range(n)):
        bits = 0
        for u in range(n):
            for v in range(u + 1, n):
                if (adj[p[u]] >> p[v]) & 1:
                    bits |= 1 << (u * n + v)
        if best is None or bits < best:
            best = bits
    return best


def describe(adj, n):
    deg = sorted(pc(a) for a in adj)
    tri = any(adj[u] & adj[v] & ~0 for u in range(n) for v in range(n)
              if u < v and (adj[u] >> v) & 1)
    return f"deg={deg} bip={bipartite(adj,n) is not None} tri={tri}"


if __name__ == "__main__":
    print("connected BAD graphs (no 2-or-0 set), by order\n")
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        bad, seen_bad, total = [], set(), 0
        for code in range(1 << len(pairs)):
            adj = [0] * n
            for i, (u, v) in enumerate(pairs):
                if (code >> i) & 1:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            if not is_connected(adj, n):
                continue
            total += 1
            if good_set(adj, n) is None:
                c = canon(adj, n)
                if c not in seen_bad:
                    seen_bad.add(c)
                    bad.append(adj[:])
        print(f"n={n}: {len(seen_bad)} bad connected classes")
        for adj in bad:
            print(f"        {describe(adj, n)}  adj={adj}")
