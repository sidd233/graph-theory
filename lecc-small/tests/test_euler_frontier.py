"""euler_diff_frontier (verify_core.py) must equal alontarsi.euler_diff on every orientation tried.
Run: env/bin/python tests/test_euler_frontier.py"""
import os, random, sys, time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..")); sys.path.insert(0, os.path.join(here, "../../list-colouring"))
import networkx as nx
from alontarsi import euler_diff
from verify_core import euler_diff_frontier

rng = random.Random(1)
cases = nonzero = 0
for trial in range(600):
    n = rng.randint(2, 9)
    G = nx.gnp_random_graph(n, rng.uniform(0.2, 0.9), seed=rng.randint(0, 10**9))
    if rng.random() < 0.3:
        G = nx.line_graph(nx.random_regular_graph(3, 2 * rng.randint(2, 4), seed=trial))
        G = nx.convert_node_labels_to_integers(G); n = G.number_of_nodes()
    out = [0] * n
    for a, b in G.edges():
        if rng.random() < 0.5: a, b = b, a
        out[a] |= 1 << b
    x, y = euler_diff(out, n), euler_diff_frontier(out, n)
    assert x == y, (n, list(G.edges()), out, x, y)
    cases += 1; nonzero += x != 0
print(f"{cases} orientations agree ({nonzero} with EE != EO)")
