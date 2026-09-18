"""The same machinery, on orientations, where the kernel method actually has power.

D is a digon-free orientation of G.  A vertex u loses the colour when ANY neighbour
in K is coloured, but only pays out-degree for its out-neighbours in K.  So with
a = |N+(u) cap K| and f(d) = ceil(lam*d) + 1, a vertex u in S\\K adjacent to K needs

        f(d+(u)) - f(d+(u) - a) >= 1

which forces a >= 1 (ordinary kernel-perfectness) and then asks for more when
d+(u) sits at a bad degree.  Out-degrees are taken in D[W].  The bound proved is
f(Delta+(D)), so a small Delta+ is what buys the gain over degeneracy.
"""
from itertools import combinations
pc = int.bit_count


def subsets(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def induced_out(out, W, n):
    return [out[v] & W if (W >> v) & 1 else 0 for v in range(n)]


def undirected(out, n):
    adj = [0] * n
    for v in range(n):
        m = out[v]
        while m:
            b = m & -m
            u = b.bit_length() - 1
            adj[v] |= b
            adj[u] |= 1 << v
            m ^= b
    return adj


def class_good(o, adj, S, fv, dout):
    for K in subsets(S):
        if K == 0:
            continue
        m, ok = K, True
        while m:                                        # independent in G
            b = m & -m
            if adj[b.bit_length() - 1] & K:
                ok = False
                break
            m ^= b
        if not ok:
            continue
        m = S & ~K
        while m:
            b = m & -m
            u = b.bit_length() - 1
            if adj[u] & K:                              # only touched vertices pay
                a = pc(o[u] & K)
                if fv[dout[u]] - fv[dout[u] - a] < 1:
                    ok = False
                    break
            m ^= b
        if ok:
            return True
    return False


def W_ok(out, n, W, fv):
    o = induced_out(out, W, n)
    adj = undirected(o, n)
    dout = [pc(o[v]) for v in range(n)]
    cand = W
    verts = [v for v in range(n) if (W >> v) & 1]
    for u in verts:                                     # cheap pass: 2-element classes
        for v in verts:
            if v <= u:
                continue
            S = (1 << u) | (1 << v)
            if not class_good(o, adj, S, fv, dout):
                cand &= ~S
                if cand == 0:
                    return False
    for v in verts:                                     # full check on what is left
        if not (cand >> v) & 1:
            continue
        b = 1 << v
        if all(class_good(o, adj, b | T, fv, dout) for T in subsets(W & ~b)):
            return True
    return False


def survives(out, n, p, q):
    fv = [-((-p * d) // q) + 1 for d in range(n + 1)]
    return all(W_ok(out, n, W, fv) for W in range(1, 1 << n))


def orientations(adj, n, maxout=None):
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if (adj[u] >> v) & 1]
    for code in range(1 << len(edges)):
        out = [0] * n
        for i, (u, v) in enumerate(edges):
            if (code >> i) & 1:
                out[u] |= 1 << v
            else:
                out[v] |= 1 << u
        d = max((pc(x) for x in out), default=0)
        if maxout is None or d <= maxout:
            yield out, d
