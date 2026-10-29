"""Independent check of a certificate written by core_check.py.

Shares no code with choosability.py or core_check.py. It checks:
  (P) for each v, the stored t is the out-degree sequence of some orientation of H - v, with
      every entry <= k-1 and EE != EO (so its coefficient is nonzero, Alon-Tarsi);
  (R) for each core witness (I, U, t): I is independent in H; t has entries <= k-1 and
      {w : t_w <= k-2} = U - I; t is the out-degree sequence of an orientation of H - I with
      EE != EO;
  (B) each blocked colouring uses colours < palette and is proper on H;
  (U) the CNF built here from (L), (S), (C), the core witnesses and the exclusions of the blocked
      colourings is UNSAT, by Glucose 4 (the search used CaDiCaL). The CNF is also written to
      data/cores/<graph>.cnf for a later DRAT check.
Run: env/bin/python verify_core.py data/cores/<graph>.json
"""
import json
import sys

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose4

sys.path.insert(0, "../list-colouring")
from alontarsi import euler_diff  # noqa: E402

from verify_reduce import orient_with_outdegrees, sub  # noqa: E402  (max-flow only)


def euler_diff_frontier(out, n):
    """EE(D) - EO(D), the same signed sum as alontarsi.euler_diff, but the arcs are processed
    vertex by vertex. Once every arc at a vertex has been decided, states where it is unbalanced
    are dropped and it leaves the state; states that cannot balance a vertex with its remaining
    arcs are dropped early. A state is the set of (vertex, nonzero imbalance) pairs."""
    arcs = [(u, v) for u in range(n) for v in range(n) if (out[u] >> v) & 1]
    rem = [0] * n
    for u, v in arcs:
        rem[u] += 1
        rem[v] += 1
    states = {(): 1}
    done = set()
    for x in range(n):
        for u, v in [a for a in arcs if x in a and not (set(a) & done)]:
            rem[u] -= 1
            rem[v] -= 1
            nxt = {}
            for st, c in states.items():
                nxt[st] = nxt.get(st, 0) + c
                d = dict(st)
                d[u] = d.get(u, 0) + 1
                d[v] = d.get(v, 0) - 1
                key = tuple(sorted((w, b) for w, b in d.items() if b))
                nxt[key] = nxt.get(key, 0) - c
            states = {st: c for st, c in nxt.items() if c and all(abs(b) <= rem[w] for w, b in st)}
        done.add(x)
    return states.get((), 0)


def at_nonzero(H, removed, t, k, diff=euler_diff_frontier):
    keep, E = sub(H, set(removed))
    assert len(t) == len(keep) and all(0 <= x <= k - 1 for x in t), "bad exponents"
    D = orient_with_outdegrees(len(keep), E, t)
    assert D is not None, "no orientation with these out-degrees"
    assert diff(D, len(keep)) != 0, "EE = EO"
    return keep


def main(path):
    c = json.load(open(path))
    G = nx.from_graph6_bytes(c["graph6"].encode())
    H = nx.convert_node_labels_to_integers(nx.line_graph(G))
    n, k, p = H.number_of_nodes(), c["k"], c["palette"]
    assert n == c["n"] and k == max(d for _, d in G.degree()) and p == (n * k) // 2
    for v in range(n):  # (P)
        at_nonzero(H, [v], c["precheck"][v], k)
    print(f"(P) {n} vertex-deleted subgraphs pass")
    for I, U, t in c["witnesses"]:  # (R)
        assert all(not H.has_edge(a, b) for a in I for b in I if a < b), "I not independent"
        keep = at_nonzero(H, I, t, k)
        assert {keep[j] for j, x in enumerate(t) if x <= k - 2} == set(U) - set(I)
    print(f"(R) {len(c['witnesses'])} core witnesses pass "
          f"(of {c['witnesses_total']} generated)")
    for phi in c["blocked"]:  # (B)
        assert len(phi) == n and all(0 <= x < p for x in phi)
        assert all(phi[a] != phi[b] for a, b in H.edges()), "blocked colouring not proper"
    print(f"(B) {len(c['blocked'])} blocked colourings are proper")
    pool = IDPool()
    x = lambda v, col: pool.id((v, col))  # noqa: E731
    cnf = CNF()
    for v in range(n):  # (L)
        cnf.extend(CardEnc.equals(lits=[x(v, col) for col in range(p)], bound=k, vpool=pool,
                                  encoding=EncType.totalizer).clauses)
    for i in range(n):  # (S)
        for col in range(1, p):
            cnf.append([-x(i, col)] + [x(j, col - 1) for j in range(i + 1)])
    for v in range(n):  # (C)
        for col in range(p):
            cnf.append([-x(v, col)] + [x(w, col) for w in H[v]])
    for I, U, _ in c["witnesses"]:  # (R)
        for col in range(p):
            cnf.append([-x(v, col) for v in I] + [x(w, col) for w in range(n) if w not in U])
    for phi in c["blocked"]:
        cnf.append([-x(v, phi[v]) for v in range(n)])
    cnf.to_file(path.replace(".json", ".cnf"))
    with Glucose4(bootstrap_with=cnf.clauses) as s:
        sat = s.solve()
    assert not sat, "CNF is satisfiable: certificate does not prove choosability"
    print(f"(U) CNF with {len(cnf.clauses)} clauses is UNSAT (Glucose 4)")
    print("CERTIFICATE OK")


if __name__ == "__main__":
    main(sys.argv[1])
