"""choosability.py --reduce with (R) added lazily, for degree 4 and up (note 04, "Why degree 4
and up stalls").

All (R) witnesses (I, U, t) are generated as before, but kept in memory, indexed by I. When the
outer solver proposes L, each colour class A = A(c) of L is looked up: every independent I ⊆ A
with a witness (I, U) such that A ⊆ U shows L is colourable, and the witness's clauses (one per
colour) are added. Only if no class is reducible does the inner solver look for colourings.
Soundness is that of choosability.py: every clause added is a valid (R) witness or the exclusion
of a proper colouring. The witnesses and colourings used are saved in the same certificate
format as core_check.py, so verify_core.py checks them.

Run: env/bin/python lazy_choos.py <file with one graph6 per line> <line number> [time_limit]
     (graph6 strings are read from a file because they contain backticks)
"""
import json
import os
import sys
import time

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

from choosability import K_DIVERSE, colourings
from core_check import precheck_monomials, witnesses_with_monomials


def subsets_independent(A, adj):
    """All nonempty independent subsets of the vertex list A."""
    out = []

    def rec(i, cur, forb):
        if i == len(A):
            if cur:
                out.append(cur)
            return
        rec(i + 1, cur, forb)
        if not (forb >> A[i]) & 1:
            rec(i + 1, cur | (1 << A[i]), forb | adj[A[i]])

    rec(0, 0, 0)
    return out


def lazy_search(H, k, time_limit=None, log=print):
    n = H.number_of_nodes()
    t0 = time.time()
    pre = precheck_monomials(H, k)
    assert pre is not None, "precheck fails; this script assumes (P)"
    log(f"n={n} k={k} precheck ok {time.time() - t0:.0f}s")
    wit = witnesses_with_monomials(H, k)
    by_I = {}
    for w in wit:
        by_I.setdefault(sum(1 << v for v in w[0]), []).append((sum(1 << v for v in w[1]), w))
    log(f"witnesses={len(wit)} generated {time.time() - t0:.0f}s")
    adj = [sum(1 << u for u in H[v]) for v in range(n)]
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
    used, used_keys, blocked = [], set(), []
    it = 0
    with Cadical153(bootstrap_with=clauses) as outer:
        while True:
            if time_limit and time.time() - t0 > time_limit:
                log(f"TIMEOUT after {it} iterations, {len(used)} witnesses, "
                    f"{len(blocked)} colourings")
                return None
            if not outer.solve():
                log(f"CHOOSABLE after {it} iterations, {len(used)} witnesses used, "
                    f"{len(blocked)} colourings blocked, {time.time() - t0:.1f}s")
                return {"n": n, "k": k, "palette": p, "precheck": pre, "witnesses": used,
                        "witnesses_total": len(wit), "blocked": blocked,
                        "seconds": round(time.time() - t0, 1)}
            model = set(l for l in outer.get_model() if l > 0)
            L = {v: [c for c in range(p) if m[v, c] in model] for v in range(n)}
            it += 1
            added = 0
            for c in range(p):
                A = [v for v in range(n) if c in L[v]]
                Amask = sum(1 << v for v in A)
                for Imask in subsets_independent(A, adj):
                    hit = next((w for U, w in by_I.get(Imask, ()) if Amask & ~U == 0), None)
                    if hit is None:
                        continue
                    key = (tuple(hit[0]), tuple(hit[1]))
                    if key not in used_keys:
                        used_keys.add(key)
                        used.append(hit)
                        Uset = set(hit[1])
                        for c2 in range(p):
                            outer.add_clause([-m[v, c2] for v in hit[0]]
                                             + [m[w, c2] for w in range(n) if w not in Uset])
                        added += 1
                    break
            if not added:
                phis = colourings(H, L, K_DIVERSE)
                assert phis, f"BAD ASSIGNMENT (verify before believing!): {L}"
                for phi in phis:
                    outer.add_clause([-m[v, phi[v]] for v in range(n)])
                    blocked.append([phi[v] for v in range(n)])
            if it % 200 == 0:
                log(f"  it={it} witnesses={len(used)} blocked={len(blocked)} "
                    f"t={time.time() - t0:.0f}s")


def main():
    g6 = [l.strip() for l in open(sys.argv[1]) if l.strip()][int(sys.argv[2])]
    limit = float(sys.argv[3]) if len(sys.argv) > 3 else None
    G = nx.from_graph6_bytes(g6.encode())
    k = max(d for _, d in G.degree())
    H = nx.convert_node_labels_to_integers(nx.line_graph(G))
    print(f"graph {g6} N={G.number_of_nodes()} k={k}", flush=True)
    cert = lazy_search(H, k, limit, lambda s: print(s, flush=True))
    if cert is not None:
        cert["graph6"] = g6
        os.makedirs("data/lazy", exist_ok=True)
        safe = g6.replace("/", "_").replace("\\", "_")
        with open(os.path.join("data/lazy", safe + ".json"), "w") as f:
            json.dump(cert, f)


if __name__ == "__main__":
    main()
