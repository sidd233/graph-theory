"""The exact condition, with parity.

Invariant carried by the induction: |L(v)| >= f(d(v)) with f(d) = ceil(d/2) + 1.
A vertex u with a = |N(u) cap K| neighbours in the coloured set K loses one colour
and a edges, so it stays safe iff f(d) - f(d-a) >= 1.

    a = 0            ->  loses nothing at all, fine
    a >= 2           ->  f drops by at least 1, fine
    a = 1, d odd     ->  f(d) - f(d-1) = 1, FINE
    a = 1, d even    ->  f(d) - f(d-1) = 0, the only bad case

So one neighbour in K is acceptable whenever the vertex currently has odd degree.
This roughly doubles the supply of usable colour classes, and it was missing from
the plain 2-kernel framing.  Degrees are taken in the whole current graph, not in
the colour class.
"""
pc = int.bit_count


def subsets(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def good_K(adj, W, S):
    """A parity-good K for colour class S inside current graph W, or None."""
    deg = {v: pc(adj[v] & W) for v in range(len(adj)) if (W >> v) & 1}
    for K in subsets(S):
        if K == 0:
            continue
        ok, m = True, K
        while m:                                        # independent?
            b = m & -m
            if adj[b.bit_length() - 1] & K:
                ok = False
                break
            m ^= b
        if not ok:
            continue
        m = S & ~K
        while m:
            b = m & -m
            u = b.bit_length() - 1
            a = pc(adj[u] & K)
            if a == 1 and deg[u] % 2 == 0:
                ok = False
                break
            m ^= b
        if ok:
            return K
    return None


def safe_vertices(adj, W):
    """v is SAFE in W if EVERY colour class containing v is parity-good.
    A safe vertex means the adversary cannot hide: any colour in its list works."""
    out = []
    m = W
    while m:
        b = m & -m
        v = b.bit_length() - 1
        m ^= b
        rest = W & ~b
        if all(good_K(adj, W, b | T) is not None for T in subsets(rest)):
            out.append(v)
    return out
