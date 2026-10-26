"""Independent verification of cuts produced by cegar2.py.

A cut is a list of literals over list assignments L:
  ("n", v, a)     true iff a not in L(v)
  ("y", w, X, t)  true iff |L(w) & X| >= t
Claim (for k-lists): every L with |L(v)| = k for all v that FALSIFIES the cut is colourable.

Proof of the claim given the checks below. Let S = {v : ("n", v, a) in cut}, phi(v) = a on S.
If L falsifies the cut then phi(v) in L(v) for v in S. Colour S by phi (phi is proper on S:
checked). For w outside S let X_w = phi(N(w) & S); w keeps at least |L(w) - X_w| =
k - |L(w) & X_w| colours. If w has a literal ("y", w, X_w, t), falsity gives |L(w) & X_w| <= t-1,
so w keeps >= k - t + 1 colours; otherwise w keeps >= k - |X_w|. Call this bound f(w). If
V - S is peelable for f (repeatedly remove a vertex with fewer than f(w) remaining neighbours),
colouring V - S in reverse removal order always succeeds. So L is colourable.
"""
from graphs import adjacency, peelable


def verify_cut(N, E, k, cut, adj=None):
    adj = adj or adjacency(N, E)
    phi, lit = {}, {}
    for x in cut:
        if x[0] == "n":
            _, v, a = x
            if v in phi:
                return False          # two colours fixed at one vertex: not a partial colouring
            phi[v] = a
        else:
            _, w, X, t = x
            if w in lit:
                return False
            lit[w] = (frozenset(X), t)
    if any(w in phi for w in lit):
        return False
    if any(phi[u] == phi[v] for u, v in E if u in phi and v in phi):
        return False
    D = [w for w in range(N) if w not in phi]
    f = {}
    for w in D:
        Xw = frozenset(phi[u] for u in adj[w] if u in phi)
        if w in lit:
            X, t = lit[w]
            if X != Xw or not (1 <= t <= len(X)):
                return False
            f[w] = k - t + 1
        else:
            f[w] = k - len(Xw)
    return peelable(D, f, adj)


def cut_holds(cut, L):
    """Truth value of the cut on the list assignment L."""
    for x in cut:
        if x[0] == "n":
            if x[2] not in L[x[1]]:
                return True
        else:
            if len(set(L[x[1]]) & set(x[2])) >= x[3]:
                return True
    return False
