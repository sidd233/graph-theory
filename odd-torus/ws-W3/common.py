"""Shared helpers for W3: 2-d kernels of Cartesian products of cycles.

A 2-d kernel of an undirected graph G is a set S that is independent and such that every
vertex outside S has at least 2 neighbours in S (an independent 2-dominating set).

Vertices of C_{d1} x ... x C_{dk} are tuples; we number them in mixed radix.
All cycle lengths are >= 3, so the product is a simple 2k-regular graph.
"""
import itertools

from pysat.solvers import Cadical153


def torus(dims):
    """Return (vertex list, index map, adjacency list) of C_{d1} x ... x C_{dk}."""
    for d in dims:
        assert d >= 3, "cycle lengths must be >= 3"
    verts = list(itertools.product(*[range(d) for d in dims]))
    idx = {v: i for i, v in enumerate(verts)}
    adj = []
    for v in verts:
        nb = []
        for k, d in enumerate(dims):
            for s in (1, -1):
                w = list(v)
                w[k] = (w[k] + s) % d
                nb.append(idx[tuple(w)])
        adj.append(nb)
    return verts, idx, adj


def is_2d_kernel(adj, S):
    """Direct check of the definition."""
    S = set(S)
    for v, nb in enumerate(adj):
        if v in S:
            if any(w in S for w in nb):
                return False
        else:
            if sum(1 for w in nb if w in S) < 2:
                return False
    return True


def kernel_clauses(adj):
    """CNF (variables 1..N) whose models are exactly the 2-d kernels.

    Independence: (-x_u or -x_w) per edge.
    2-domination of v: x_v or 'at least 2 of N(v)'. 'At least 2 of N(v)' holds iff every
    subset of N(v) of size |N(v)|-1 contains a true variable, so we add, for each w in N(v),
    the clause x_v or OR(N(v) minus w).
    """
    cls = []
    for v, nb in enumerate(adj):
        for w in nb:
            if v < w:
                cls.append([-(v + 1), -(w + 1)])
        for w in nb:
            cls.append([v + 1] + [u + 1 for u in nb if u != w])
    return cls


def sat_find(adj):
    """Return a 2-d kernel (list of vertex indices) or None, by SAT (CaDiCaL)."""
    with Cadical153(bootstrap_with=kernel_clauses(adj)) as s:
        if s.solve():
            return [v - 1 for v in s.get_model() if v > 0]
        return None
