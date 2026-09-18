"""Alon-Tarsi: the algebraic cousin of the kernel method, with no hereditary condition.

Theorem (Alon, Tarsi 1992).  Let D be an orientation of G.  Call a set A of arcs
EULERIAN if every vertex has equal in-degree and out-degree inside A (isolated
vertices allowed).  Let EE and EO count the Eulerian arc sets of even and odd size.
If EE != EO then G is L-colourable whenever |L(v)| >= d+(v) + 1.

    AT(G) = min { Delta+(D) + 1 : D an orientation with EE(D) != EO(D) }
    ch(G) <= AT(G)

Every kernel-perfect orientation has EE != EO, so AT is at least as strong as the
kernel method, and it asks nothing about induced subgraphs, so none of the four
obstructions in 00-04 applies to it.

EE - EO is computed by a signed DP over arcs, tracking each vertex's out-minus-in
imbalance and reading off the all-zero state.
"""
from itertools import combinations
pc = int.bit_count


def euler_diff(out, n):
    """EE(D) - EO(D), by signed DP over the arcs."""
    arcs = [(u, v) for u in range(n) for v in range(n) if (out[u] >> v) & 1]
    states = {(0,) * n: 1}
    for (u, v) in arcs:
        nxt = {}
        for st, c in states.items():
            nxt[st] = nxt.get(st, 0) + c                      # arc excluded
            t = list(st)
            t[u] += 1
            t[v] -= 1
            t = tuple(t)
            nxt[t] = nxt.get(t, 0) - c                        # arc included, sign flips
        states = {k: val for k, val in nxt.items() if val}
    return states.get((0,) * n, 0)


def orientations_by_outdeg(adj, n):
    """All orientations, grouped by Delta+, ascending."""
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if (adj[u] >> v) & 1]
    buckets = {}
    for code in range(1 << len(edges)):
        out = [0] * n
        for i, (u, v) in enumerate(edges):
            if (code >> i) & 1:
                out[u] |= 1 << v
            else:
                out[v] |= 1 << u
        d = max((pc(x) for x in out), default=0)
        buckets.setdefault(d, []).append(out)
    return buckets


def alon_tarsi(adj, n):
    """AT(G), searching orientations thinnest first."""
    buckets = orientations_by_outdeg(adj, n)
    for d in sorted(buckets):
        for out in buckets[d]:
            if euler_diff(out, n) != 0:
                return d + 1, out
    return None, None


def min_outdeg(adj, n):
    """Hakimi: the thinnest possible orientation, and the floor for every method here."""
    best = 0
    for W in range(1, 1 << n):
        e = sum(pc(adj[v] & W) for v in range(n) if (W >> v) & 1) // 2
        best = max(best, -(-e // pc(W)))
    return best
