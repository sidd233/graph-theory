"""Column transfer digraph for 2-d kernels of C_m x C_n, for fixed m and all n.

Columns are indexed by j in Z_n; column j is a copy of C_m on rows Z_m. A 2-d kernel S is
recorded column by column as X_j = {r : (r, j) in S}, a subset of Z_m (a bitmask).

States: pairs (A, B) of subsets of Z_m with A, B independent in C_m and A, B disjoint.
Arcs:   (A, B) -> (B, C) iff C is independent in C_m, B and C are disjoint, and every row
        r not in B has at least 2 S-neighbours among (r-1, B), (r+1, B), (r, A), (r, C).

For n >= 3, closed walks of length n correspond one to one with 2-d kernels of C_m x C_n
(proof in REPORT.md). The script

  * builds the digraph (virtual state id = pos(A) * L + pos(B), L = number of independent
    sets of C_m),
  * computes strongly connected components (scipy, Tarjan-type),
  * for every nontrivial SCC (size >= 2 or a self-loop) computes its period d (gcd of
    level(u) + 1 - level(v) over arcs u -> v inside the SCC, levels from a BFS),
  * tests the "shift property": every arc (A, B) -> (B, C) inside a nontrivial SCC has
    B = A + s and C = B + s (rotation of Z_m by s) for one s in {+1, -1}.

Run: python transfer.py m_min m_max
"""
import sys
import time
from math import gcd

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def independent_masks(m):
    full = (1 << m) - 1
    out = []
    for x in range(1 << m):
        rot = ((x << 1) | (x >> (m - 1))) & full
        if x & rot == 0:
            out.append(x)
    return np.array(out, dtype=np.int64)


def rotate(x, s, m):
    """Rotate subset x of Z_m by s (r -> r + s)."""
    full = (1 << m) - 1
    s %= m
    return ((x << s) | (x >> (m - s))) & full


def build(m):
    full = (1 << m) - 1
    I = independent_masks(m)
    L = len(I)
    pos = -np.ones(1 << m, dtype=np.int64)
    pos[I] = np.arange(L)
    src, dst = [], []
    for b in range(L):
        B = int(I[b])
        up = rotate(B, 1, m)    # r in up  iff r-1 in B
        dn = rotate(B, -1, m)   # r in dn  iff r+1 in B
        nonB = full & ~B
        Z0 = nonB & ~up & ~dn               # no horizontal (in-column) S-neighbour
        Z1 = nonB & (up ^ dn)               # exactly one in-column S-neighbour
        cand = I[((I & B) == 0) & ((I & Z0) == Z0)]
        if len(cand) == 0:
            continue
        AC = cand[:, None] | cand[None, :]
        ok = (AC & Z1) == Z1
        ia, ic = np.nonzero(ok)
        src.append(pos[cand[ia]] * L + b)
        dst.append(b * L + pos[cand[ic]])
    src = np.concatenate(src) if src else np.zeros(0, dtype=np.int64)
    dst = np.concatenate(dst) if dst else np.zeros(0, dtype=np.int64)
    return I, L, src, dst


def analyse(m, verbose=True):
    t0 = time.time()
    I, L, src, dst = build(m)
    # compress virtual ids to the states that touch an arc
    vid, inv = np.unique(np.concatenate([src, dst]), return_inverse=True)
    nstates_with_arcs = len(vid)
    N = len(vid)
    src, dst = inv[:len(src)], inv[len(src):]
    G = csr_matrix((np.ones(len(src), dtype=np.int8), (src, dst)), shape=(N, N))
    ncomp, lab = connected_components(G, directed=True, connection="strong")
    sizes = np.bincount(lab, minlength=ncomp)
    selfloop = src == dst
    loopcomp = set(lab[src[selfloop]].tolist())
    intra = lab[src] == lab[dst]
    nontriv = [c for c in range(ncomp) if sizes[c] >= 2 or c in loopcomp]
    nontriv_set = np.zeros(ncomp, dtype=bool)
    nontriv_set[nontriv] = True
    keep = intra & nontriv_set[lab[src]]
    s2, d2 = src[keep], dst[keep]
    # shift property on arcs inside nontrivial SCCs
    A = I[vid[s2] // L]
    B = I[vid[s2] % L]
    C = I[vid[d2] % L]
    shift_ok = np.zeros(len(s2), dtype=bool)
    for s in (1, -1):
        rA = np.array([rotate(int(x), s, m) for x in A], dtype=np.int64) if len(A) else A
        rB = np.array([rotate(int(x), s, m) for x in B], dtype=np.int64) if len(B) else B
        shift_ok |= (rA == B) & (rB == C)
    # periods by BFS levels inside each nontrivial SCC
    Gi = csr_matrix((np.ones(len(s2), dtype=np.int8), (s2, d2)), shape=(N, N))
    periods = {}
    for c in nontriv:
        nodes = np.nonzero(lab == c)[0]
        root = int(nodes[0])
        level = {root: 0}
        frontier = [root]
        g = 0
        while frontier:
            nxt = []
            for u in frontier:
                for v in Gi.indices[Gi.indptr[u]:Gi.indptr[u + 1]]:
                    v = int(v)
                    if v not in level:
                        level[v] = level[u] + 1
                        nxt.append(v)
                    else:
                        g = gcd(g, level[u] + 1 - level[v])
            frontier = nxt
        assert len(level) == len(nodes)
        # include arcs into already-levelled nodes from the same frontier pass
        for u in nodes:
            u = int(u)
            for v in Gi.indices[Gi.indptr[u]:Gi.indptr[u + 1]]:
                g = gcd(g, level[u] + 1 - level[int(v)])
        periods[c] = abs(g)
    res = {
        "m": m,
        "L": L,
        "arcs": len(src),
        "states_touched": nstates_with_arcs,
        "nontrivial_sccs": len(nontriv),
        "scc_sizes": sorted(int(sizes[c]) for c in nontriv),
        "periods": sorted(periods[c] for c in nontriv),
        "states_on_cycles": int(sum(sizes[c] for c in nontriv)),
        "arcs_in_sccs": int(len(s2)),
        "shift_property": bool(shift_ok.all()),
        "time": time.time() - t0,
    }
    # all periods must share a factor with m for non-existence when gcd(m, n) = 1
    res["all_periods_share_factor_with_m"] = all(gcd(p, m) > 1 for p in periods.values())
    # each SCC: size equals period? (then it is a simple cycle)
    res["every_scc_is_simple_cycle"] = all(
        sizes[c] == periods[c] and int(np.sum(lab[s2] == c)) == sizes[c] for c in nontriv)
    # the column patterns that occur on cycles, grouped by rotation period
    res["_lab"], res["_nontriv"], res["_I"], res["_L"], res["_vid"] = lab, nontriv, I, L, vid
    return res


def rot_period(x, m):
    for t in range(1, m + 1):
        if m % t == 0 and rotate(x, t, m) == x:
            return t


def exact_n_set(res, nmax=60):
    """Closed-walk lengths n <= nmax: union over SCCs of multiples of the period, valid when
    every SCC is a simple cycle (then the closed walks in it have length exactly k * size)."""
    assert res["every_scc_is_simple_cycle"]
    ps = sorted(set(res["periods"]))
    return ps, [n for n in range(1, nmax + 1) if any(n % p == 0 for p in ps)]


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for m in range(lo, hi + 1):
        r = analyse(m)
        ps, ns = exact_n_set(r) if r["every_scc_is_simple_cycle"] else (None, None)
        # patterns: first column of each nontrivial SCC's states; check they are maximal
        # independent sets of C_m (independent dominating)
        I, L, lab, vid = r["_I"], r["_L"], r["_lab"], r["_vid"]
        full = (1 << m) - 1
        patterns = set()
        for c in r["_nontriv"]:
            for v in np.nonzero(lab == c)[0]:
                patterns.add(int(I[vid[v] // L]))
        mis = [x for x in I.tolist()
               if (x | rotate(x, 1, m) | rotate(x, -1, m)) == full]
        print(f"m={m}: L={r['L']} arcs={r['arcs']} states_touched={r['states_touched']} "
              f"nontrivial_SCCs={r['nontrivial_sccs']} states_on_cycles={r['states_on_cycles']} "
              f"arcs_in_SCCs={r['arcs_in_sccs']} time={r['time']:.1f}s")
        print(f"   SCC sizes={r['scc_sizes']}")
        print(f"   SCC periods={r['periods']}")
        print(f"   shift_property={r['shift_property']} every_SCC_simple_cycle="
              f"{r['every_scc_is_simple_cycle']} all_periods_share_factor_with_m="
              f"{r['all_periods_share_factor_with_m']}")
        print(f"   column patterns on cycles = maximal independent sets of C_m with rotation "
              f"period >= 2: {patterns == set(x for x in mis if rot_period(x, m) >= 2)} "
              f"(#patterns={len(patterns)}, #MIS(C_m)={len(mis)})")
        print(f"   distinct periods={ps}; n<=60 with a closed walk: {ns}")
        print(f"   check: that set == {{n<=60 : gcd(m,n)>1}}: "
              f"{ns == [n for n in range(1, 61) if gcd(m, n) > 1]}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
