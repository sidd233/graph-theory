"""Phase 4: empirical cross-check of the odd-ring lemma, plus regressions against notes 11/12.

For every rank system satisfying (1) permutation and (2) r_u(v) + r_v(u) = k-1 on small regular
graphs, "no odd ring" must agree with brute-force kernel-perfectness of the orientation of
L(G). Then: K_{3,3} admits a system (Galvin), K_4 / prism / K_6 admit none (notes 11 and 12).
Run from lecc-small/: env/bin/python tests/test_lemma.py
"""
import os
import sys
import time

import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kernel_sat import solve  # noqa: E402
from verify_cert import kernel_perfect_bruteforce, odd_cycles_dfs  # noqa: E402


def rank_systems(G):
    k = next(iter(dict(G.degree()).values()))
    E = sorted(tuple(sorted(e)) for e in G.edges())
    used = {v: set() for v in G}
    r = {}

    def rec(i):
        if i == len(E):
            yield dict(r)
            return
        u, v = E[i]
        for a in range(k):
            b = k - 1 - a
            if a in used[u] or b in used[v]:
                continue
            used[u].add(a); used[v].add(b); r[(u, v)] = a; r[(v, u)] = b
            yield from rec(i + 1)
            used[u].discard(a); used[v].discard(b)

    yield from rec(0)


def has_odd_ring(G, r):
    n = G.number_of_nodes()
    adj = [sorted(G[v]) for v in range(n)]
    for cyc in odd_cycles_dfs(adj, n):
        m = len(cyc)
        for seq in (cyc, cyc[::-1]):
            if all(r[(seq[i], seq[(i + 1) % m])] < r[(seq[i], seq[i - 1])] for i in range(m)):
                return True
    return False


def cross_check(name, G, limit=None):
    G = nx.convert_node_labels_to_integers(G)
    E = [tuple(e) for e in G.edges()]
    n_sys = agree = kp = 0
    t = time.time()
    for r in rank_systems(G):
        n_sys += 1
        ring = has_odd_ring(G, r)
        brute = kernel_perfect_bruteforce(E, r)
        assert brute == (not ring), f"{name}: lemma disagrees with brute force on {r}"
        agree += 1
        kp += brute
        if limit and n_sys >= limit:
            break
    print(f"  {name:10s} systems={n_sys:6d}  kernel-perfect={kp:5d}  all agree  "
          f"({time.time() - t:.1f}s)")


def main():
    print("cross-check: no odd ring <=> brute-force kernel-perfect")
    cross_check("K4", nx.complete_graph(4))
    cross_check("prism", nx.circular_ladder_graph(3))
    cross_check("K33", nx.complete_bipartite_graph(3, 3))
    cross_check("Q3", nx.hypercube_graph(3))
    cross_check("K222", nx.complete_multipartite_graph(2, 2, 2))
    cross_check("C5xK2", nx.circular_ladder_graph(5), limit=300)
    print("regressions (SAT solver):")
    for name, G, want in [("K33", nx.complete_bipartite_graph(3, 3), True),
                          ("K4", nx.complete_graph(4), False),
                          ("prism", nx.circular_ladder_graph(3), False),
                          ("K6", nx.complete_graph(6), False),
                          ("K44", nx.complete_bipartite_graph(4, 4), True)]:
        sat = solve(nx.convert_node_labels_to_integers(G))[0]
        assert sat == want, f"{name}: expected {want}, got {sat}"
        print(f"  {name:6s} {'SAT' if sat else 'UNSAT'} as expected")
    sat, r, _, _ = solve(nx.convert_node_labels_to_integers(nx.circular_ladder_graph(5)))
    print(f"  C5xK2  {'SAT' if sat else 'UNSAT'}  (undecided in note 11; settled here)")


def random_cross_check(trials_per_graph=400, seed=1):
    """Both directions of the lemma on NON-bipartite graphs, with arbitrary linear orders at
    each vertex (no sum condition), so that kernel-perfect systems with odd cycles occur."""
    import random
    rnd = random.Random(seed)
    graphs = {"C5": nx.cycle_graph(5), "K4": nx.complete_graph(4), "W5": nx.wheel_graph(6),
              "C5+chord": nx.Graph([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]),
              "K4-e+tail": nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]),
              "prism": nx.circular_ladder_graph(3), "C7": nx.cycle_graph(7),
              "bowtie": nx.Graph([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]),
              "rand10": nx.gnm_random_graph(8, 12, seed=3)}
    print("random cross-check (arbitrary orders, non-bipartite graphs):")
    for name, G in graphs.items():
        G = nx.convert_node_labels_to_integers(G)
        E = [tuple(e) for e in G.edges()]
        kp = 0
        for _ in range(trials_per_graph):
            r = {}
            for u in G:
                nb = list(G[u]); rnd.shuffle(nb)
                for i, v in enumerate(nb):
                    r[(u, v)] = i
            ring = has_odd_ring(G, r)
            brute = kernel_perfect_bruteforce(E, r)
            assert brute == (not ring), f"{name}: lemma disagrees on {r}"
            kp += brute
        print(f"  {name:10s} trials={trials_per_graph}  kernel-perfect={kp:4d}  "
              f"non-kernel-perfect={trials_per_graph - kp:4d}  all agree")


if __name__ == "__main__":
    main()
    random_cross_check()
