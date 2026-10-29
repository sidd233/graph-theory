"""Independent re-check of every Alon-Tarsi fact used by choosability.py on a graph.

choosability.py gets coefficients from at_fast.coeffs, a signed expansion of the graph
polynomial. Here each one is re-derived from the combinatorial side of the Alon-Tarsi theorem:
the coefficient of prod x_v^{d_v} equals +-(EE(D) - EO(D)) for any orientation D with
out-degree sequence d. Its Eulerian subgraphs are counted by alontarsi.euler_diff, which shares
no code with at_fast. Checked:
  (P) for every v, H - v has SOME orientation with out-degrees <= k-1 and EE != EO;
  (R) for every witness (I, t), H - I has an orientation with out-degrees exactly t and
      EE != EO.
Run: env/bin/python verify_reduce.py 'GCY^B_' 3
"""
import sys

import networkx as nx

sys.path.insert(0, "../list-colouring")
from alontarsi import euler_diff  # noqa: E402
from at_fast import coeffs  # noqa: E402

from choosability import independent_sets  # noqa: E402


def orient_with_outdegrees(n, edges, d):
    """An orientation (list of out-bitmasks) with out-degree d[v], via max-flow; None if none."""
    F = nx.DiGraph()
    for i, (u, v) in enumerate(edges):
        F.add_edge("s", ("e", i), capacity=1)
        F.add_edge(("e", i), ("v", u), capacity=1)
        F.add_edge(("e", i), ("v", v), capacity=1)
    for v in range(n):
        F.add_edge(("v", v), "t", capacity=d[v])
    val, flow = nx.maximum_flow(F, "s", "t")
    if val != len(edges):
        return None
    out = [0] * n
    for i, (u, v) in enumerate(edges):
        if flow[("e", i)][("v", u)] == 1:   # edge i charged to u: arc u -> v
            out[u] |= 1 << v
        else:
            out[v] |= 1 << u
    return out


def sub(H, removed):
    keep = [u for u in H if u not in removed]
    idx = {u: j for j, u in enumerate(keep)}
    return keep, [(idx[a], idx[b]) for a, b in H.edges() if a not in removed and b not in removed]


def main(g6, k):
    H = nx.convert_node_labels_to_integers(nx.line_graph(nx.from_graph6_bytes(g6.encode())))
    n = H.number_of_nodes()
    # (P)
    for v in range(n):
        keep, E = sub(H, {v})
        T = coeffs(E, len(keep), k - 1)
        t = next(iter(T))
        D = orient_with_outdegrees(len(keep), E, t)
        assert D is not None and euler_diff(D, len(keep)) != 0, f"precheck fails at {v}"
    print(f"(P) all {n} vertex-deleted subgraphs: independent AT check passes")
    # (R)
    checked = 0
    for I in independent_sets(H):
        keep, E = sub(H, set(I))
        T = coeffs(E, len(keep), k - 1)
        Zs = {}
        for t in T:
            Z = frozenset(j for j, x in enumerate(t) if x <= k - 2)
            Zs.setdefault(Z, t)
        maximal = [Z for Z in Zs if not any(Z < W for W in Zs)]
        for Z in maximal:
            t = Zs[Z]
            D = orient_with_outdegrees(len(keep), E, t)
            assert D is not None, "no orientation with these out-degrees"
            assert euler_diff(D, len(keep)) != 0, f"witness fails: I={I} t={t}"
            checked += 1
    print(f"(R) {checked} reducibility witnesses: independent AT check passes")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
