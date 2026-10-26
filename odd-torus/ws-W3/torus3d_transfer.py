"""Exact set of c for which C_a x C_b x C_c has a 2-d kernel, for small fixed (a, b).

Layer transfer digraph (the 3D analogue of transfer.py): a layer is the graph
L = C_a x C_b; states are pairs (A, B) of independent sets of L with A, B disjoint; arcs
(A, B) -> (B, C) iff C is independent, B and C are disjoint, and every v of L outside B
has [v in A] + [v in C] + |N_L(v) & B| >= 2. For c >= 3, closed walks of length c <->
2-d kernels of C_a x C_b x C_c (same proof as in 2D, with columns replaced by layers).

Exact closed-walk lengths: closed walks lie inside one strongly connected component (SCC).
For each nontrivial SCC with boolean adjacency matrix M we compute the boolean powers
M^1, M^2, ... until a repeat M^t = M^s (s < t) occurs. Since M^{t+1} = M^t M, the sequence
is then periodic from s on with period t - s, so the set {c : trace(M^c) > 0} is known
exactly for every c, from these finitely many powers. No bound such as Wielandt's is
needed: the repeat is detected, not assumed.

Run: python torus3d_transfer.py a b [a b ...]
"""
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from common import torus


def layer_independent_sets(a, b):
    verts, idx, adj = torus((a, b))
    N = len(verts)
    nbmask = [sum(1 << w for w in set(adj[v])) for v in range(N)]
    out = []

    def rec(v, mask, forbidden):
        if v == N:
            out.append(mask)
            return
        rec(v + 1, mask, forbidden)
        if not (forbidden >> v) & 1:
            rec(v + 1, mask | (1 << v), forbidden | nbmask[v])

    rec(0, 0, 0)
    return np.array(out, dtype=np.int64), nbmask, adj


def build(a, b):
    I, nbmask, adj = layer_independent_sets(a, b)
    N = a * b
    L = len(I)
    pos = {int(x): i for i, x in enumerate(I)}
    src, dst = [], []
    for bi in range(L):
        B = int(I[bi])
        Z0 = Z1 = 0
        for v in range(N):
            if (B >> v) & 1:
                continue
            k = sum((B >> w) & 1 for w in adj[v])
            if k == 0:
                Z0 |= 1 << v
            elif k == 1:
                Z1 |= 1 << v
        cand = I[((I & B) == 0) & ((I & Z0) == Z0)]
        if len(cand) == 0:
            continue
        ok = ((cand[:, None] | cand[None, :]) & Z1) == Z1
        ia, ic = np.nonzero(ok)
        pa = np.array([pos[int(x)] for x in cand], dtype=np.int64)
        src.append(pa[ia] * L + bi)
        dst.append(bi * L + pa[ic])
    src = np.concatenate(src)
    dst = np.concatenate(dst)
    return L, src, dst


def closed_walk_set(M):
    """Exact {c >= 1 : trace(M^c) > 0} as (finite list below s, periodic part)."""
    M = M.astype(np.float32)
    seen = {}
    P = M.copy()
    traces = []
    t = 1
    while True:
        key = np.packbits(P > 0).tobytes()
        if key in seen:
            s = seen[key]
            return traces, s, t - s   # traces[c-1] for c < t; periodic from s, period t-s
        seen[key] = t
        traces.append(bool(np.trace(P) > 0))
        P = np.minimum(P @ M, 1.0)
        t += 1


def analyse(a, b, cmax=60):
    t0 = time.time()
    L, src, dst = build(a, b)
    vid, inv = np.unique(np.concatenate([src, dst]), return_inverse=True)
    n = len(vid)
    s2, d2 = inv[:len(src)], inv[len(src):]
    G = csr_matrix((np.ones(len(s2), dtype=np.int8), (s2, d2)), shape=(n, n))
    nc, lab = connected_components(G, directed=True, connection="strong")
    sizes = np.bincount(lab)
    loops = set(lab[s2[s2 == d2]].tolist())
    nontriv = [c for c in range(nc) if sizes[c] >= 2 or c in loops]
    good = set()
    info = []
    for c in nontriv:
        nodes = np.nonzero(lab == c)[0]
        loc = -np.ones(n, dtype=np.int64)
        loc[nodes] = np.arange(len(nodes))
        mask = (lab[s2] == c) & (lab[d2] == c)
        M = np.zeros((len(nodes), len(nodes)), dtype=np.float32)
        M[loc[s2[mask]], loc[d2[mask]]] = 1
        traces, s, per = closed_walk_set(M)

        def has(cc):
            if cc <= len(traces):
                return traces[cc - 1]
            return traces[s - 1 + (cc - s) % per]

        info.append((len(nodes), int(mask.sum()), s, per))
        good |= {cc for cc in range(1, cmax + 1) if has(cc)}
    print(f"(a,b)=({a},{b}): independent layer sets={L} arcs={len(src)} "
          f"nontrivial SCCs={len(nontriv)} (size, arcs, preperiod start s, period) per SCC: "
          f"{sorted(info)[:12]}{' ...' if len(info) > 12 else ''}  time={time.time()-t0:.1f}s")
    cs = sorted(x for x in good if x >= 3)
    missing = [x for x in range(3, cmax + 1) if x not in good]
    print(f"   c in [3,{cmax}] with a 2-d kernel: {cs}")
    print(f"   c in [3,{cmax}] without: {missing}")
    sys.stdout.flush()
    return good


if __name__ == "__main__":
    args = list(map(int, sys.argv[1:]))
    for i in range(0, len(args), 2):
        analyse(args[i], args[i + 1])
