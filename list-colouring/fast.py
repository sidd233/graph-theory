"""Faster exact test, using two facts that prune almost everything.

Write f(d) = ceil(lam*d) + 1.  Call a degree d BAD if f(d) - f(d-1) = 0, i.e. a
vertex of that degree cannot afford to lose a colour for only one edge.  For
lam = (q-1)/q the bad degrees are exactly the multiples of q, so bad degrees have
density 1 - lam.

Prune 1.  If the current graph W has no vertex of bad degree, every colour class
is good (take K = one vertex), so W is fine.  No search needed.

Prune 2.  A colour class S is good as soon as some u in S has all of its
S-neighbours of good degree, since K = {u} then works.  So a BAD S must have
every one of its vertices adjacent, inside S, to a bad-degree vertex of S.
That is a heavy restriction and kills the vast majority of subsets at once.

A graph survives iff every induced subgraph has a safe vertex, where v is safe
iff no bad S contains v.
"""
pc = int.bit_count


def subsets(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def bad_degrees(p, q, n):
    """d is bad iff ceil(p*d/q) == ceil(p*(d-1)/q)."""
    f = [-((-p * d) // q) + 1 for d in range(n + 1)]
    return [d > 0 and f[d] == f[d - 1] for d in range(n + 1)]


def class_is_good(adj, S, badv, fv):
    """Is there a usable K inside colour class S?  badv = bitmask of bad-degree
    vertices, fv[d] = f(d)."""
    for K in subsets(S):
        if K == 0:
            continue
        m, ok = K, True
        while m:                                     # independent
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
            if a == 1 and (badv >> u) & 1:
                ok = False
                break
            m ^= b
        if ok:
            return True
    return False


def W_ok(adj, W, isbad, fv):
    """Does the current graph W contain a safe vertex?"""
    deg = {}
    badv = 0
    m = W
    while m:
        b = m & -m
        v = b.bit_length() - 1
        d = pc(adj[v] & W)
        deg[v] = d
        if isbad[d]:
            badv |= b
        m ^= b
    if badv == 0:
        return True                                   # prune 1
    unsafe = 0
    for S in subsets(W):
        if S == 0 or (S & ~unsafe) == 0:
            continue                                  # adds nothing new
        dominated = True                              # prune 2
        m = S
        while m:
            b = m & -m
            if not (adj[b.bit_length() - 1] & S & badv):
                dominated = False
                break
            m ^= b
        if not dominated:
            continue
        if not class_is_good(adj, S, badv, fv):
            unsafe |= S
            if unsafe == W:
                return False
    return unsafe != W


def survives(adj, n, p, q):
    isbad = bad_degrees(p, q, n)
    fv = [-((-p * d) // q) + 1 for d in range(n + 1)]
    for W in range(1, 1 << n):
        if not W_ok(adj, W, isbad, fv):
            return False
    return True
