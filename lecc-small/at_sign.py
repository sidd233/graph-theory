"""Alon-Tarsi census for line graphs of regular graphs (PLAN.md, Phase 2).

For a k-regular graph G on N vertices (N even), fix at each vertex v the reference order of its
edges by neighbour index. A proper k-edge-colouring c gives each v a permutation pi_v (position
-> colour). The coefficient of prod_e x_e^(k-1) in the graph polynomial of L(G) is a nonzero
constant times

    S(G) = sum over proper k-edge-colourings c of prod_v sgn(pi_v(c)),

(derivation in 01-at-sign.md), and S is invariant under permuting colours because N is even.
We fix the colours at vertex 0, which divides the sum by k!, and return

    (number of colourings with vertex 0 fixed, S restricted to those colourings).

Zero colourings means class 2. S = 0 with colourings present means zero-sum: the Alon-Tarsi
method with lists of size k says nothing about G.

Usage:  env/bin/python at_sign.py data/regular_N8.g6 > data/census_N8.csv
"""
import sys

import networkx as nx


def at_sign(G):
    G = nx.convert_node_labels_to_integers(G)
    N = G.number_of_nodes()
    degs = {d for _, d in G.degree()}
    assert len(degs) == 1, "graph must be regular"
    k = degs.pop()
    nbrs = [sorted(G[v]) for v in range(N)]
    pos = [{w: i for i, w in enumerate(nbrs[v])} for v in range(N)]
    # edges in lexicographic order; vertex 0's edges come first and are pre-coloured
    edges = sorted((min(u, v), max(u, v)) for u, v in G.edges())
    # at each vertex, the colours seen at each position (-1 = not yet coloured)
    col_at = [[-1] * k for _ in range(N)]
    used = [0] * N  # bitmask of colours used at each vertex

    def inv_parity(v, p, c):
        """Parity of inversions created at v by putting colour c at position p."""
        par = 0
        for q in range(k):
            cq = col_at[v][q]
            if cq >= 0 and ((q < p and cq > c) or (q > p and cq < c)):
                par ^= 1
        return par

    def put(u, v, c):
        par = inv_parity(u, pos[u][v], c) ^ inv_parity(v, pos[v][u], c)
        col_at[u][pos[u][v]] = c
        col_at[v][pos[v][u]] = c
        used[u] |= 1 << c
        used[v] |= 1 << c
        return par

    def take(u, v, c):
        col_at[u][pos[u][v]] = -1
        col_at[v][pos[v][u]] = -1
        used[u] &= ~(1 << c)
        used[v] &= ~(1 << c)

    parity0 = 0
    for i, w in enumerate(nbrs[0]):
        parity0 ^= put(0, w, i)
    rest = [e for e in edges if e[0] != 0]
    full = (1 << k) - 1
    count = 0
    total = 0

    def rec(i, parity):
        nonlocal count, total
        if i == len(rest):
            count += 1
            total += -1 if parity else 1
            return
        u, v = rest[i]
        free = full & ~used[u] & ~used[v]
        while free:
            b = free & -free
            free ^= b
            c = b.bit_length() - 1
            par = put(u, v, c)
            rec(i + 1, parity ^ par)
            take(u, v, c)

    rec(0, parity0)
    return k, count, total


def main(path):
    print("graph6,N,k,colourings_v0_fixed,S")
    with open(path) as f:
        for line in f:
            g6 = line.strip()
            if not g6:
                continue
            G = nx.from_graph6_bytes(g6.encode())
            k, cnt, S = at_sign(G)
            print(f"{g6},{G.number_of_nodes()},{k},{cnt},{S}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
