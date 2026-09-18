"""The tight system, on regular class-1 graphs, K_6 being the smallest open case.

By the star lemma a kernel-perfect orientation of L(G) is a linear order at each
vertex of G.  Write M(u,v) for the number of edges at u that uv points to, so each
row of M is a bijection onto {0,...,d_u - 1} and d+(uv) = M(u,v) + M(v,u).

For G that is Delta-regular and class 1 the budget is exactly consumed, forcing

    M(u,v) + M(v,u) = s,   s = Delta - 1,   every row a permutation of 0..s.

A triangle uvw of G becomes a triangle of L(G).  With p = M(i,j), q = M(j,k),
r = M(i,k) it comes out CYCLIC, hence kernelless, exactly when

    (p + q < s and r > p and r > q)   or   (p + q > s and r < p and r < q).

So: is there an M with no cyclic triangle?  If not, Lemma 1 cannot prove the
conjecture for that G, whatever else is true.
"""
import sys
from itertools import combinations


def search(n, adjlist, s, want_all=False):
    """M(u,v) for each ordered pair; returns solutions with no cyclic triangle."""
    verts = range(n)
    tri = [(a, b, c) for a, b, c in combinations(verts, 3)
           if b in adjlist[a] and c in adjlist[b] and c in adjlist[a]]
    M = [[None] * n for _ in verts]
    edges = [(u, v) for u in verts for v in adjlist[u] if u < v]
    tri_at = {e: [] for e in edges}
    for (a, b, c) in tri:
        last = max((a, b), (b, c), (a, c), key=edges.index)
        tri_at[last].append((a, b, c))

    def cyclic(a, b, c):
        p, q, r = M[a][b], M[b][c], M[a][c]
        if None in (p, q, r):
            return False
        return ((p + q < s and r > p and r > q) or
                (p + q > s and r < p and r < q))

    sols = []

    def go(t):
        if t == len(edges):
            sols.append([row[:] for row in M])
            return not want_all
        u, v = edges[t]
        for val in range(s + 1):
            if val in (M[u][w] for w in adjlist[u] if M[u][w] is not None):
                continue
            other = s - val
            if other in (M[v][w] for w in adjlist[v] if M[v][w] is not None):
                continue
            M[u][v], M[v][u] = val, other
            if not any(cyclic(*x) for x in tri_at[(u, v)]):
                if go(t + 1):
                    return True
            M[u][v] = M[v][u] = None
        return False

    go(0)
    return sols


def complete(n):
    return [[v for v in range(n) if v != u] for u in range(n)]


for n in [4, 6, 8]:
    s = n - 2                                   # Delta = n-1, chi' = n-1, s = Delta-1
    sols = search(n, complete(n), s)
    print(f"K_{n}: Delta={n-1} chi'={n-1} s={s}  "
          f"{'solution with no cyclic triangle EXISTS' if sols else 'NO solution: Lemma 1 cannot prove K_' + str(n)}")
    if sols:
        print("      witness M =", sols[0])
