"""Cross-validation of choosability.py (the CEGAR search with --reduce).

1. Brute force on tiny graphs: enumerate EVERY k-list assignment over a palette of size n*k
   (up to relabelling of colours by first appearance) and test colourability directly. That
   gives ch-k-ness with no theory at all. Compare with search(reduce=True) and
   search(reduce=False).
2. Random graphs on 6 to 8 vertices with k = 2 and 3: compare reduce=True with reduce=False.
Run from lecc-small/: env/bin/python tests/test_choosability.py
"""
import itertools
import os
import random
import sys

import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from choosability import search  # noqa: E402


def canonical_assignments(n, k):
    """All k-list assignments on n vertices up to colour relabelling (first-appearance order)."""
    def rec(i, used, lists):
        if i == n:
            yield list(lists)
            return
        # colours 0..used-1 seen so far; may add new colours used, used+1, ...
        for new in range(0, k + 1):
            olds = k - new
            if olds > used:
                continue
            for old in itertools.combinations(range(used), olds):
                L = list(old) + list(range(used, used + new))
                lists.append(L)
                yield from rec(i + 1, used + new, lists)
                lists.pop()
    yield from rec(0, 0, [])


def colourable(H, L):
    n = H.number_of_nodes()
    for phi in itertools.product(*[L[v] for v in range(n)]):
        if all(phi[u] != phi[v] for u, v in H.edges()):
            return True
    return False


def brute_choosable(H, k):
    H = nx.convert_node_labels_to_integers(H)
    return all(colourable(H, L) for L in canonical_assignments(H.number_of_nodes(), k))


def run(H, k, reduce):
    res, _ = search(H, k, log=lambda s: None, reduce=reduce)
    return res == "choosable"


def main():
    rnd = random.Random(7)
    print("brute force vs search, tiny graphs:")
    n_ok = 0
    for trial in range(80):
        k = 2 if trial % 3 else 3
        n = rnd.randint(4, 6) if k == 2 else rnd.randint(4, 5)
        H = nx.gnp_random_graph(n, rnd.uniform(0.3, 0.9), seed=rnd.randint(0, 10**6))
        if H.number_of_edges() == 0:
            continue
        b = brute_choosable(H, k)
        r1, r0 = run(H, k, True), run(H, k, False)
        assert b == r1 == r0, f"MISMATCH n={n} edges={list(H.edges())} k={k}: brute={b} reduce={r1} plain={r0}"
        n_ok += 1
        print(f"    n={n} k={k} m={H.number_of_edges()} choosable={b}: agree", flush=True)
    print(f"  {n_ok} graphs, all agree")
    print("reduce vs plain, random graphs n=6..9:")
    stats = {True: 0, False: 0}
    for trial in range(120):
        n = rnd.randint(6, 9)
        H = nx.gnp_random_graph(n, rnd.uniform(0.3, 0.8), seed=rnd.randint(0, 10**6))
        if H.number_of_edges() == 0:
            continue
        k = rnd.choice([2, 3])
        r1, r0 = run(H, k, True), run(H, k, False)
        assert r1 == r0, f"MISMATCH n={n} edges={list(H.edges())} k={k}"
        stats[r1] += 1
    print(f"  all agree; choosable={stats[True]}, not choosable={stats[False]}")


if __name__ == "__main__":
    main()
