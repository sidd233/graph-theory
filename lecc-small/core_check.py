"""choosability.py --reduce, with an unsat core over the (R) witnesses, saved as a certificate.

Same search as choosability.search(reduce=True), with one change: each (R) witness w gets a
selector literal s_w, its clauses become (not s_w) OR clause, and every solve runs under the
assumptions s_w. When the outer problem is UNSAT, get_core() names the witnesses the refutation
used. The answer "choosable" depends only on:
  (P) the precheck facts, (L), (S), (C) as in choosability.py;
  the blocked colourings (each a proper colouring, so each exclusion clause is sound);
  the core witnesses.
All three are written to data/cores/<graph>.json, and verify_core.py re-checks them
independently. The witness monomial t is stored with each witness so the checker needs no
coefficient expansion.

Run: env/bin/python core_check.py [workers] [time_limit]  (all open cubic graphs, k = 3)
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

sys.path.insert(0, "../list-colouring")
from at_fast import coeffs  # noqa: E402

from choosability import K_DIVERSE, colourings, independent_sets  # noqa: E402


def precheck_monomials(H, k):
    """For each v, one exponent vector t of H - v (indexed by the kept vertices) with nonzero
    coefficient and exponents <= k-1, or None if some H - v has none."""
    n = H.number_of_nodes()
    out = []
    for v in range(n):
        keep = [u for u in range(n) if u != v]
        idx = {u: j for j, u in enumerate(keep)}
        sub = [(idx[a], idx[b]) for a, b in H.edges() if v not in (a, b)]
        T = coeffs(sub, n - 1, k - 1)
        if not T:
            return None
        out.append([int(x) for x in min(T)])
    return out


def witnesses_with_monomials(H, k):
    """Like choosability.reducible_witnesses, but each witness also carries a monomial t of
    H - I (indexed by the kept vertices) with Z(t) = U - I."""
    n = H.number_of_nodes()
    wit = []
    for I in independent_sets(H):
        Iset = set(I)
        keep = [u for u in range(n) if u not in Iset]
        idx = {u: j for j, u in enumerate(keep)}
        sub = [(idx[a], idx[b]) for a, b in H.edges() if a not in Iset and b not in Iset]
        Zs = {}
        for t in coeffs(sub, len(keep), k - 1):
            Zs.setdefault(frozenset(keep[j] for j, x in enumerate(t) if x <= k - 2), t)
        for Z, t in Zs.items():
            if not any(Z < W for W in Zs):
                wit.append((sorted(Iset), sorted(Iset | Z), [int(x) for x in t]))
    return wit


def core_search(H, k, time_limit=None, log=print):
    n = H.number_of_nodes()
    t0 = time.time()
    pre = precheck_monomials(H, k)
    assert pre is not None, "precheck fails; this script assumes (P)"
    p = (n * k) // 2
    pool = IDPool()
    m = {(v, c): pool.id(("m", v, c)) for v in range(n) for c in range(p)}
    clauses = []
    for v in range(n):  # (L)
        clauses += CardEnc.equals(lits=[m[v, c] for c in range(p)], bound=k, vpool=pool,
                                  encoding=EncType.seqcounter).clauses
    for i in range(n):  # (S)
        for c in range(1, p):
            clauses.append([-m[i, c]] + [m[j, c - 1] for j in range(i + 1)])
    for v in range(n):  # (C)
        for c in range(p):
            clauses.append([-m[v, c]] + [m[w, c] for w in H[v]])
    wit = witnesses_with_monomials(H, k)
    sel = [pool.id(("s", i)) for i in range(len(wit))]
    for i, (I, U, _) in enumerate(wit):  # (R), guarded by selectors
        Uset = set(U)
        for c in range(p):
            clauses.append([-sel[i]] + [-m[v, c] for v in I]
                           + [m[w, c] for w in range(n) if w not in Uset])
    log(f"n={n} k={k} palette={p} witnesses={len(wit)}")
    blocked = []
    it = 0
    with Cadical153(bootstrap_with=clauses) as outer:
        while True:
            if time_limit and time.time() - t0 > time_limit:
                log(f"TIMEOUT after {it} iterations")
                return None
            if not outer.solve(assumptions=sel):
                core = outer.get_core() or []
                pos = {s: i for i, s in enumerate(sel)}
                used = sorted(pos[s] for s in core if s in pos)
                log(f"CHOOSABLE after {it} iterations, {len(blocked)} colourings blocked, "
                    f"core {len(used)} of {len(wit)} witnesses, {time.time() - t0:.1f}s")
                return {"n": n, "k": k, "palette": p, "precheck": pre,
                        "witnesses": [wit[i] for i in used], "witnesses_total": len(wit),
                        "blocked": blocked, "seconds": round(time.time() - t0, 1)}
            model = set(l for l in outer.get_model() if l > 0)
            L = {v: [c for c in range(p) if m[v, c] in model] for v in range(n)}
            phis = colourings(H, L, K_DIVERSE)
            it += 1
            assert phis, f"bad assignment found: {L}"
            for phi in phis:
                outer.add_clause([-m[v, phi[v]] for v in range(n)])
                blocked.append([phi[v] for v in range(n)])


def job(arg):
    g6, limit = arg
    G = nx.from_graph6_bytes(g6.encode())
    k = max(d for _, d in G.degree())
    H = nx.convert_node_labels_to_integers(nx.line_graph(G))
    msgs = []
    cert = core_search(H, k, limit, msgs.append)
    safe = g6.replace("/", "_").replace("\\", "_")
    if cert is not None:
        cert["graph6"] = g6
        with open(os.path.join("data/cores", safe + ".json"), "w") as f:
            json.dump(cert, f)
    return g6, msgs


if __name__ == "__main__":
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    os.makedirs("data/cores", exist_ok=True)
    graphs = []
    for fn in ("data/uncovered_N8.g6", "data/uncovered_N10.g6"):
        for line in open(fn):
            g6 = line.strip()
            if g6 and max(d for _, d in nx.from_graph6_bytes(g6.encode()).degree()) == 3:
                graphs.append(g6)
    with Pool(workers) as pool:
        for g6, msgs in pool.imap_unordered(job, [(g, limit) for g in graphs]):
            print(g6, "|", " / ".join(msgs), flush=True)
