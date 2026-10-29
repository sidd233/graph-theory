"""Exact kernel-perfectness test for orientations of T(3, n) = C_3 x C_n by a transfer matrix.

D is kernel-perfect iff every induced subdigraph D[S] has a kernel.  We scan the columns
j = 0, ..., n-1 (each column is a triangle).  For a fixed S, a kernel K meets each column in at
most one vertex.  A partial kernel up to column j is summarised by a profile (k_j, U_j): k_j is the
row of K in column j (or None), and U_j is the set of rows of column j whose vertex is in S \\ K and
is not yet absorbed (it can only be absorbed by its right neighbour).  To close the cycle we guess
g = k_{n-1} and remember k_0.  For each S the set F_j of feasible (g, k_0, profile) triples evolves
deterministically; the outer search explores all S column by column, keeping each distinct F once.
S is kernel-less iff no triple in the final F closes up.  Returns a kernel-less S or None.
"""
import sys

ROWS = (0, 1, 2)
KOPTS = (None, 0, 1, 2)


def make(n, arc):
    """arc(u, v) -> True iff u -> v, for adjacent vertices u = (i, j), v = (i', j')."""
    col = {}   # col[j][(i, i2)] : (i, j) -> (i2, j)
    rowR = {}  # rowR[j][i] : (i, j) -> (i, j+1)
    for j in range(n):
        col[j] = {(i, i2): arc((i, j), (i2, j)) for i in ROWS for i2 in ROWS if i != i2}
        rowR[j] = {i: arc((i, j), (i, (j + 1) % n)) for i in ROWS}
    return col, rowR


def first_column(Sj, g, k0, col, rowR, n):
    """Profile of column 0 given S_0, guessed k_{n-1} = g and chosen k_0 (or None if infeasible)."""
    if k0 is not None and k0 not in Sj:
        return None
    if g is not None and g == k0:
        return None  # (g, n-1) and (g, 0) adjacent, both in K
    U = []
    for i in Sj:
        if i == k0:
            continue
        ok = k0 is not None and col[0][(i, k0)]
        ok = ok or (g == i and not rowR[n - 1][i])  # (i,0) -> (i,n-1) iff not (i,n-1)->(i,0)
        if not ok:
            U.append(i)
    return (k0, frozenset(U))


def step(prof, Sn, jn, col, rowR):
    """All profiles of column jn reachable from profile prof of column jn-1, given S_{jn}."""
    kj, U = prof
    res = []
    for kn in KOPTS:
        if kn is not None and kn not in Sn:
            continue
        if kn is not None and kn == kj:
            continue
        # every unabsorbed vertex of the previous column must point to k_n in the same row
        if any(not (kn == i and rowR[jn - 1][i]) for i in U):
            continue
        Un = []
        for i in Sn:
            if i == kn:
                continue
            ok = kn is not None and col[jn][(i, kn)]
            ok = ok or (kj == i and not rowR[jn - 1][i])
            if not ok:
                Un.append(i)
        res.append((kn, frozenset(Un)))
    return res


def subsets(rows):
    return [tuple(i for i in rows if m >> i & 1) for m in range(8)]


def find_kernelless(n, arc):
    col, rowR = make(n, arc)
    S_opts = subsets(ROWS)
    # layer 0: F = set of (g, k0, profile)
    layer = {}
    for S0 in S_opts:
        F = set()
        for g in KOPTS:
            for k0 in KOPTS:
                p = first_column(S0, g, k0, col, rowR, n)
                if p is not None:
                    F.add((g, k0, p))
        F = frozenset(F)
        if F not in layer:
            layer[F] = (None, S0)
    history = [layer]
    for j in range(1, n):
        new = {}
        for F, _ in layer.items():
            for Sj in S_opts:
                G = set()
                for g, k0, p in F:
                    for q in step(p, Sj, j, col, rowR):
                        G.add((g, k0, q))
                G = frozenset(G)
                if G not in new:
                    new[G] = (F, Sj)
        layer = new
        history.append(layer)
        print(f"  column {j}: {len(layer)} distinct states", file=sys.stderr, flush=True)
    for F in layer:
        ok = False
        for g, k0, (kl, U) in F:
            if kl != g:
                continue
            if all(k0 == i and rowR[n - 1][i] for i in U):
                ok = True
                break
        if not ok:
            # reconstruct S
            S = []
            G = F
            for j in range(n - 1, -1, -1):
                prev, Sj = history[j][G]
                S.append(Sj)
                G = prev
            S.reverse()
            cells = [(i, j) for j, Sj in enumerate(S) for i in Sj]
            if cells:
                return cells
    return None


def galvin_arc(n):
    c = lambda v: (v[0] + v[1]) % 3

    def arc(u, v):
        if u[1] == v[1]:  # column edge: towards the smaller colour
            return c(u) > c(v)
        return c(u) < c(v)  # row edge: towards the larger colour
    return arc


if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        r = find_kernelless(n, galvin_arc(n))
        print(f"T(3,{n}) Galvin-type: " + ("KERNEL-PERFECT" if r is None else f"kernel-less S, |S|={len(r)}: {r}"),
              flush=True)
