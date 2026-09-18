"""Obstruction B, measured: does the remainder cancel the halving?

`PROBLEM.md` records a floor of roughly `mad/2 + 1` under this whole family of methods, never
independently re-derived, and notes that it decides whether the target is reachable at all.
Theorem 14.4 turns it into something measurable.

The best orientation has `Delta+(D) = D*(G) := max over subgraphs H of ceil(|E(H)|/|V(H)|)`,
which is about `mad/2` (Hakimi).  The ordinary kernel method therefore bottoms out at
`D* + 1`.  Theorem 14.4 gives the 2-d kernel method

    ch(G) <= ceil(Delta+(D)/2) + max(1, r(D)),

so the halving would push under `D* + 1` unless the remainder `r` grows to compensate.  The
floor claim is exactly the negation of the criterion in note `14`:

    FLOOR:  for every graph G,   min over orientations D of [ceil(Delta+(D)/2) + max(1, r(D))]
            is at least D*(G) + 1.

This script measures both sides.

Computing `r(D)`.  `r(D)` is the largest induced subdigraph of `D` admitting a stalling list
assignment.  Enumerating list assignments is unnecessary:

    Lemma.  `W` admits a stalling assignment iff the union of its **bad** sets is `V(W)`,
    where `S` is bad when no legitimate `K` (Definition 14.1) lies inside it.

    Proof.  If `(W, L)` is stalled then every colour class is bad, and every vertex lies in
    some class because every list is nonempty, so the bad sets cover.  Conversely, given bad
    sets covering `V(W)`, take one colour per bad set repeated `max_v f(d+(v))` times and let
    `L(v)` collect the colours of the bad sets containing `v`.  Every list is then long
    enough and every class is bad.  QED

Run: `python list-colouring/floor.py [max_n]`
"""

import sys
from itertools import combinations
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "list-colouring"))
sys.path.insert(0, str(_root / "census-tool"))

from three_hereditary import certificate, chromatic_number
from twokernel.core import Digraph, bits, popcount


def f_half(d):
    return -(-d // 2) + 1


def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & mask


def independent_subsets(D, mask):
    verts = list(bits(mask))
    for size in range(1, len(verts) + 1):
        for combo in combinations(verts, size):
            m, ok = 0, True
            for v in combo:
                if D.adj[v] & m:
                    ok = False
                    break
                m |= 1 << v
            if ok:
                yield m


def has_legitimate_move(W, S, f):
    for K in independent_subsets(W, S):
        good = True
        for u in bits(S & ~K):
            if not (W.adj[u] & K):
                continue
            d = popcount(W.out[u])
            if f(d) - f(d - popcount(W.out[u] & K)) < 1:
                good = False
                break
        if good:
            return True
    return False


def stalls(W, f):
    """True iff the bad sets of W cover V(W), i.e. some valid list assignment stalls."""
    covered = 0
    for S in submasks(W.full):
        if S == 0:
            continue
        if not has_legitimate_move(W, S, f):
            covered |= S
            if covered == W.full:
                return True
    return covered == W.full


def r_of(D, f=f_half):
    """Largest induced subdigraph of D admitting a stalling assignment; 0 if none."""
    best = 0
    for wmask in submasks(D.full):
        if popcount(wmask) <= best:
            continue
        if stalls(D.sub(wmask), f):
            best = popcount(wmask)
    return best


# ------------------------------------------------------------------------------------
# graphs, orientations, and the two sides of the claim
# ------------------------------------------------------------------------------------


def all_graphs_bf(n):
    slots = [(u, v) for u in range(n) for v in range(n) if u < v]
    seen, out = set(), []
    for m in range(1 << len(slots)):
        edges = [slots[i] for i in range(len(slots)) if m >> i & 1]
        G = Digraph.from_edges(n, edges)
        cert = certificate(G)
        if cert not in seen:
            seen.add(cert)
            out.append((G, edges))
    return out


def orientations(n, edges):
    for m in range(1 << len(edges)):
        arcs = [
            (v, u) if m >> i & 1 else (u, v) for i, (u, v) in enumerate(edges)
        ]
        yield Digraph.from_arcs(n, arcs)


def degeneracy(G):
    adj, alive, best = list(G.adj), G.full, 0
    for _ in range(G.n):
        v = min(bits(alive), key=lambda u: popcount(adj[u] & alive))
        best = max(best, popcount(adj[v] & alive))
        alive &= ~(1 << v)
    return best


def d_star(n, edges):
    """min over orientations of Delta+, which by Hakimi is max_H ceil(|E(H)|/|V(H)|)."""
    best = None
    for D in orientations(n, edges):
        dp = max((D.out_degree(v) for v in range(n)), default=0)
        if best is None or dp < best:
            best = dp
    return best if best is not None else 0


def best_halved_bound(n, edges):
    """min over orientations of ceil(Delta+/2) + max(1, r), and the r attaining it."""
    best, best_r, best_dp = None, None, None
    for D in orientations(n, edges):
        dp = max((D.out_degree(v) for v in range(n)), default=0)
        if best is not None and -(-dp // 2) + 1 >= best:
            continue  # even r = 0 cannot beat the incumbent
        r = r_of(D)
        val = -(-dp // 2) + max(1, r)
        if best is None or val < best:
            best, best_r, best_dp = val, r, dp
    return best, best_r, best_dp


def all_outdeg_odd_hereditarily(D):
    """Is the single-out-neighbour escape of 14.6 available throughout D?"""
    for wmask in submasks(D.full):
        if wmask == 0:
            continue
        W = D.sub(wmask)
        if any(popcount(W.out[v]) % 2 == 0 for v in range(W.n)):
            return False
    return True


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("FLOOR claim: min over orientations of ceil(Delta+/2) + max(1, r)  >=  D* + 1")
    print("f(d) = ceil(d/2) + 1\n")
    for n in range(2, max_n + 1):
        graphs = all_graphs_bf(n)
        violations, tight, ties = [], 0, 0
        for G, edges in graphs:
            if not edges:
                continue
            ds = d_star(n, edges)
            bound, r, dp = best_halved_bound(n, edges)
            if bound < ds + 1:
                violations.append((edges, bound, ds, r, dp))
            elif bound == ds + 1:
                tight += 1
            else:
                ties += 1
        print(f"n = {n}: {len(graphs)} graphs, {len(violations)} beat the floor, "
              f"{tight} meet it exactly, {ties} fall short of it")
        for edges, bound, ds, r, dp in violations[:5]:
            print(f"    VIOLATION edges={edges} bound={bound} < D*+1={ds+1} "
                  f"(r={r}, Delta+={dp})")

    print()
    print("Why the parity escape cannot carry an induction:")
    from stall_census import all_digraphs_bf as _ad
    for n in range(2, 6):
        pool = _ad(n)
        surv = sum(1 for D in pool if all_outdeg_odd_hereditarily(D))
        print(f"  n = {n}: of {len(pool):>4} digraphs, {surv} keep every out-degree odd "
              f"in every induced subdigraph")
    print("  If u -> v and d+(u) is odd, then in D - v it is even.  So the escape is")
    print("  a boundary effect, never a property an induction can rely on.")


if __name__ == "__main__":
    main()
