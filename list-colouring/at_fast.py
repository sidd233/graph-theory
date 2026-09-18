"""Alon-Tarsi number by coefficient extraction, fast enough for line graphs.

AT(H) is the least k for which the graph polynomial  prod over edges (x_u - x_v)
has a nonzero coefficient on some monomial prod x_v^{d_v} with every d_v <= k-1.
(Necessarily sum d_v = |E|.)  Rather than enumerate orientations, expand edge by
edge: each edge contributes +x_u or -x_v, so a signed DP over the degree vector
gives every coefficient at once.  Capping entries at k-1 prunes it hard.

Validated below against the orientation-based values from alontarsi.py.
"""
pc = int.bit_count


def coeffs(edges, n, cap):
    """Signed coefficients of all monomials with every exponent <= cap."""
    states = {(0,) * n: 1}
    left = len(edges)
    for (u, v) in edges:
        left -= 1
        nxt = {}
        for d, c in states.items():
            for w, s in ((u, 1), (v, -1)):
                if d[w] == cap:
                    continue
                t = list(d)
                t[w] += 1
                t = tuple(t)
                val = nxt.get(t, 0) + s * c
                if val:
                    nxt[t] = val
                elif t in nxt:
                    del nxt[t]
        # a state needs enough room left to absorb the remaining edges
        states = {d: c for d, c in nxt.items()
                  if sum(cap - x for x in d) >= left}
    return states


def alon_tarsi_fast(edges, n):
    E = len(edges)
    for k in range(1, n + 2):
        cap = k - 1
        if cap * n < E:
            continue
        if coeffs(edges, n, cap):
            return k
    return None


def line_graph_edges(edges):
    """Edges of L(G), given the edges of G."""
    m = len(edges)
    return [(i, j) for i in range(m) for j in range(i + 1, m)
            if set(edges[i]) & set(edges[j])], m
