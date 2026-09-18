"""Kernel-perfectness via the Borodin, Kostochka and Woodall characterisation.

BKW (Discrete Math. 191 (1998) 45-49): an orientation of a line graph is kernel-perfect
iff every clique has a kernel and every directed odd cycle has a chord or pseudochord.

For SIMPLE G the line graph is simple, so an edge of L(G) carries only one direction and
pseudochords cannot occur.  A directed odd cycle with no chord is an INDUCED directed odd
cycle.  So the test reduces to:

    no induced directed odd cycle,  and  every clique has a kernel (= a sink).

The naive test asks every one of the 2^m induced subdigraphs for a kernel, costing another
2^m per subset.  This one costs O(m) per subset, so it is about m-squared times faster.
"""
pc = int.bit_count


def induced_directed_cycle(out, adj, S):
    """Is the subdigraph induced on S exactly a directed cycle?  Returns its length or 0."""
    verts = []
    m = S
    while m:
        b = m & -m
        verts.append(b.bit_length() - 1)
        m ^= b
    t = len(verts)
    if t < 3:
        return 0
    for v in verts:                       # a directed cycle: in and out degree 1 each
        if pc(out[v] & S) != 1:
            return 0
        if pc(adj[v] & S) != 2:           # induced: exactly two neighbours in S
            return 0
    # connected?  follow the out-arcs from one vertex and count
    start = verts[0]
    seen, cur = 1, start
    for _ in range(t):
        cur = (out[cur] & S).bit_length() - 1
        if cur == start:
            break
        seen += 1
    else:
        return 0
    return t if seen == t else 0


def kernel_perfect_bkw(out, adj, m):
    full = (1 << m) - 1
    for S in range(1, 1 << m):
        if pc(S) < 3:
            continue
        t = induced_directed_cycle(out, adj, S)
        if t and t % 2 == 1:
            return False                  # induced directed odd cycle: no kernel
    # cliques: a clique needs a sink.  Stars are transitive by construction of M, so it is
    # enough to check every clique of the orientation directly.
    for S in range(1, 1 << m):
        ok = True
        v = S
        while v:
            b = v & -v
            x = b.bit_length() - 1
            if (adj[x] & S) != (S & ~b):
                ok = False
                break
            v ^= b
        if not ok:
            continue                      # not a clique
        if not any(not (out[y] & S) for y in range(m) if (S >> y) & 1):
            return False                  # clique with no sink
    return True
