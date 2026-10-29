"""Decide whether a graph H is k-choosable, by a CEGAR loop of two SAT solvers.

Used for the positive LECC attempt on Schauz's open graphs (PLAN.md, "Next action" 1):
H = L(G), and H is k-choosable iff ch'(G) <= k.

The search is justified as follows.
  (P) Precheck. If every H - v is k-choosable (shown via a nonzero Alon-Tarsi coefficient with
      all exponents <= k-1), then any bad k-list assignment L of H is CRITICAL: no colour c in
      L(v) is missing from every neighbour's list. Otherwise, colour H - v from L, then give v
      the colour c.
  (B) Palette. Under (P), each colour lies in at least 2 lists, so at most n*k/2 colours occur.
      Without (P), at most n*k.
  (S) Symmetry. Colour names are irrelevant. Relabel colours in order of first appearance along
      the vertex order v_0, v_1, ..., breaking ties within a vertex arbitrarily. Then colour c
      appearing at v_i forces colour c-1 to appear at some v_j with j <= i. Every list
      assignment has such a relabelling.
  (L) Lists of size exactly k. A bad assignment with larger lists shrinks to a bad one with
      size-k lists.
Outer SAT: variables m[v][c], "c in L(v)", constrained by (L), (S) and, if (P) holds, the
criticality clauses. Each L-colouring phi found so far is excluded by the clause
OR_v not m[v][phi(v)]. Inner SAT: is the proposed L colourable? If yes, add up to K_DIVERSE
distinct colourings as exclusions and repeat. If no, L is a bad assignment and is verified
independently. If the outer problem becomes UNSAT, H is k-choosable.

  (R) Reducible colour classes (option --reduce). Let A = A(c) be the set of vertices whose
      list contains c, and let I be an independent subset of A. Colour I with c and delete c
      from the other lists in A. If H - I has a nonzero Alon-Tarsi coefficient with exponents
      <= |L'(w)| - 1 (that is, <= k-2 on A - I and <= k-1 elsewhere), then L is colourable,
      whatever the other lists are. So in a bad L no colour class A satisfies
      I ⊆ A ⊆ I ∪ Z(t) for such a witness, where Z(t) = {w : t_w <= k-2} for a nonzero
      monomial t of H - I with exponents <= k-1. Each witness becomes one clause per colour.

Run: env/bin/python choosability.py <graph6 of G> <k> [--line] [--reduce] [--log FILE]
     (--line: work on H = L(G); otherwise H = G)
"""
import argparse
import itertools
import sys
import time

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153, Minisat22

sys.path.insert(0, "../list-colouring")
from at_fast import coeffs  # noqa: E402

K_DIVERSE = 8


def precheck(H, k):
    """True iff every H - v has a nonzero Alon-Tarsi coefficient with exponents <= k-1."""
    n = H.number_of_nodes()
    for v in range(n):
        keep = [u for u in range(n) if u != v]
        idx = {u: j for j, u in enumerate(keep)}
        sub = [(idx[a], idx[b]) for a, b in H.edges() if v not in (a, b)]
        if not coeffs(sub, n - 1, k - 1):
            return False
    return True


def colourings(H, L, limit):
    """Up to `limit` proper colourings of H from lists L (dict v -> list of colours)."""
    pool = IDPool()
    cl = []
    for v in H:
        lits = [pool.id((v, c)) for c in L[v]]
        cl += CardEnc.equals(lits=lits, bound=1, vpool=pool, encoding=EncType.pairwise).clauses
    for u, v in H.edges():
        for c in set(L[u]) & set(L[v]):
            cl.append([-pool.id((u, c)), -pool.id((v, c))])
    out = []
    with Minisat22(bootstrap_with=cl) as s:
        while len(out) < limit and s.solve():
            model = set(l for l in s.get_model() if l > 0)
            phi = {v: c for v in H for c in L[v] if pool.id((v, c)) in model}
            out.append(phi)
            s.add_clause([-pool.id((v, phi[v])) for v in H])
    return out


def independent_sets(H):
    n = H.number_of_nodes()
    adj = [set(H[v]) for v in range(n)]
    out = []

    def rec(i, cur, forb):
        if i == n:
            if cur:
                out.append(tuple(cur))
            return
        rec(i + 1, cur, forb)
        if i not in forb:
            rec(i + 1, cur + [i], forb | adj[i])

    rec(0, [], set())
    return out


def reducible_witnesses(H, k):
    """Pairs (I, U): any colour class A with I ⊆ A ⊆ U is reducible (see (R))."""
    n = H.number_of_nodes()
    wit = []
    for I in independent_sets(H):
        Iset = set(I)
        keep = [u for u in range(n) if u not in Iset]
        idx = {u: j for j, u in enumerate(keep)}
        sub = [(idx[a], idx[b]) for a, b in H.edges() if a not in Iset and b not in Iset]
        T = coeffs(sub, len(keep), k - 1)
        Zs = {frozenset(keep[j] for j, x in enumerate(t) if x <= k - 2) for t in T}
        for Z in Zs:
            if not any(Z < W for W in Zs):
                wit.append((Iset, Iset | Z))
    return wit


def search(H, k, log=print, time_limit=None, reduce=False, sym=True):
    H = nx.convert_node_labels_to_integers(H)
    n = H.number_of_nodes()
    t0 = time.time()
    crit = precheck(H, k)
    p = (n * k) // 2 if crit else n * k
    log(f"n={n} k={k} precheck(all H-v k-choosable)={crit} palette={p}")
    pool = IDPool()
    m = {(v, c): pool.id(("m", v, c)) for v in range(n) for c in range(p)}
    clauses = []
    for v in range(n):  # (L)
        clauses += CardEnc.equals(lits=[m[v, c] for c in range(p)], bound=k, vpool=pool,
                                  encoding=EncType.seqcounter).clauses
    for i in (range(n) if sym else []):  # (S)
        for c in range(1, p):
            clauses.append([-m[i, c]] + [m[j, c - 1] for j in range(i + 1)])
    if crit:  # (P)
        for v in range(n):
            for c in range(p):
                clauses.append([-m[v, c]] + [m[w, c] for w in H[v]])
    if reduce:  # (R)
        wit = reducible_witnesses(H, k)
        for c in range(p):
            for I, U in wit:
                clauses.append([-m[v, c] for v in I] + [m[w, c] for w in range(n) if w not in U])
        log(f"reducible-class witnesses: {len(wit)} ({len(wit) * p} clauses)")
    it = blocked = 0
    with Cadical153(bootstrap_with=clauses) as outer:
        while True:
            if time_limit and time.time() - t0 > time_limit:
                log(f"TIMEOUT after {it} iterations, {blocked} colourings blocked")
                return "timeout", None
            if not outer.solve():
                log(f"CHOOSABLE: outer UNSAT after {it} iterations, {blocked} colourings "
                    f"blocked, {time.time() - t0:.1f}s")
                return "choosable", None
            model = set(l for l in outer.get_model() if l > 0)
            L = {v: [c for c in range(p) if m[v, c] in model] for v in range(n)}
            phis = colourings(H, L, K_DIVERSE)
            it += 1
            if not phis:
                log(f"BAD ASSIGNMENT found after {it} iterations: {L}")
                return "bad", L
            for phi in phis:
                outer.add_clause([-m[v, phi[v]] for v in range(n)])
                blocked += 1
            if it % 1000 == 0:
                log(f"  it={it} blocked={blocked} t={time.time() - t0:.0f}s")


def verify_bad(H, L):
    """Independent exhaustive check that H has no proper colouring from L."""
    H = nx.convert_node_labels_to_integers(H)
    for phi in itertools.product(*[L[v] for v in range(H.number_of_nodes())]):
        if all(phi[u] != phi[v] for u, v in H.edges()):
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("g6")
    ap.add_argument("k", type=int)
    ap.add_argument("--line", action="store_true")
    ap.add_argument("--log")
    ap.add_argument("--time-limit", type=float)
    ap.add_argument("--reduce", action="store_true")
    ap.add_argument("--no-sym", action="store_true", help="drop (S); for cross-checking only")
    a = ap.parse_args()
    G = nx.from_graph6_bytes(a.g6.encode())
    H = nx.line_graph(G) if a.line else G
    f = open(a.log, "a") if a.log else None

    def log(s):
        print(s, flush=True)
        if f:
            f.write(s + "\n"); f.flush()

    res, L = search(H, a.k, log, a.time_limit, a.reduce, not a.no_sym)
    if res == "bad":
        log(f"independent verification of bad assignment: {verify_bad(H, L)}")


if __name__ == "__main__":
    main()
