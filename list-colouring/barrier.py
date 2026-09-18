"""Verification of the barrier results for the 2-kernel route to list colouring.

Everything here is about digon-free digraphs (orientations), because that is the
only regime in which the Bondy-Boppana-Siegel bound ch(G) <= Delta^+ + 1 says
anything: a digon makes both endpoints pay for the same edge.

Notation: a digraph on n vertices is a tuple `out` of n bitmasks, out[v] being
N^+(v).  Vertex sets are bitmasks too.
"""

from itertools import combinations
import random

pc = int.bit_count


def subsets(mask):
    """All submasks of `mask`, including 0 and mask itself."""
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def induced(out, W):
    return [out[v] & W if (W >> v) & 1 else 0 for v in range(len(out))]


def indeg_mask(out, n):
    inn = [0] * n
    for v in range(n):
        m = out[v]
        while m:
            b = m & -m
            inn[b.bit_length() - 1] |= 1 << v
            m ^= b
    return inn


def is_independent(out, K):
    m = K
    while m:
        b = m & -m
        v = b.bit_length() - 1
        if out[v] & K:
            return False
        m ^= b
    return True


def is_2kernel(out, W, K):
    """K is a 2-kernel of the subdigraph induced on W."""
    if not is_independent(out, K):
        return False
    rest = W & ~K
    m = rest
    while m:
        b = m & -m
        v = b.bit_length() - 1
        if pc(out[v] & K) < 2:
            return False
        m ^= b
    return True


def find_2kernel(out, W):
    for K in subsets(W):
        if is_2kernel(out, W, K):
            return K
    return None


def has_t_good_set(out, n, W, S, t):
    """Is there a t-good set for the current digraph D[W] and colour class S?

    K must be a nonempty independent subset of S such that every u in S\\K that
    is adjacent to K in D[W] has at least one out-arc into K when its ambient
    out-degree d^+_{D[W]}(u) is at most t, and at least two when it exceeds t.
    """
    o = induced(out, W)
    inn = indeg_mask(o, n)
    adj = [o[v] | inn[v] for v in range(n)]
    dout = [pc(o[v]) for v in range(n)]
    for K in subsets(S):
        if K == 0 or not is_independent(o, K):
            continue
        ok = True
        m = S & ~K
        while m:
            b = m & -m
            u = b.bit_length() - 1
            if adj[u] & K:
                need = 1 if dout[u] <= t else 2
                if pc(o[u] & K) < need:
                    ok = False
                    break
            m ^= b
        if ok:
            return True
    return False


def is_t_kernel_perfect(out, n, t):
    """Every current digraph D[W] and every colour class S admits a t-good set."""
    full = (1 << n) - 1
    for W in subsets(full):
        if W == 0:
            continue
        for S in subsets(W):
            if S == 0:
                continue
            if not has_t_good_set(out, n, W, S, t):
                return False
    return True


def max_outdeg(out):
    return max((pc(m) for m in out), default=0)


def all_orientations(n):
    """Every labelled digon-free digraph on n vertices, up to nothing."""
    pairs = list(combinations(range(n), 2))
    for code in range(3 ** len(pairs)):
        out = [0] * n
        c = code
        for (u, v) in pairs:
            d = c % 3
            c //= 3
            if d == 1:
                out[u] |= 1 << v
            elif d == 2:
                out[v] |= 1 << u
        yield out


def experiment_1(nmax=5):
    """Barrier: t-kernel-perfect forces Delta^+ <= t, so the threshold
    refinement of the kernel bound never improves on Delta^+ + 1."""
    print("E-B1  threshold barrier, exhaustive over labelled orientations")
    for n in range(2, nmax + 1):
        witnesses = 0
        total = 0
        for out in all_orientations(n):
            d = max_outdeg(out)
            if d == 0:
                continue
            total += 1
            for t in range(1, d):
                if is_t_kernel_perfect(out, n, t):
                    witnesses += 1
                    print("   COUNTEREXAMPLE", n, out, "t =", t, "Delta+ =", d)
                    break
        print(f"   n={n}: {total} orientations with an arc, "
              f"{witnesses} that are t-kernel-perfect for some t < Delta^+")


def experiment_2(nmax=6):
    """The single-arc obstruction, stated for plain 2-kernels."""
    print("E-B2  no orientation with an arc is hereditarily 2-kernelled")
    for n in range(2, nmax + 1):
        bad = 0
        total = 0
        for out in all_orientations(n):
            if max_outdeg(out) == 0:
                continue
            total += 1
            full = (1 << n) - 1
            if all(find_2kernel(out, W) is not None
                   for W in subsets(full) if W):
                bad += 1
        print(f"   n={n}: {total} orientations with an arc, "
              f"{bad} hereditarily 2-kernelled")
        if n >= 4:
            break


def peel(out, n):
    """Iterated 2-kernel removal.  Returns the number of 2-kernels peeled
    before the remainder is arcless, or None if it stalls."""
    W = (1 << n) - 1
    steps = 0
    while True:
        o = induced(out, W)
        if all(o[v] == 0 for v in range(n)):
            return steps
        K = None
        for cand in subsets(W):
            if cand and is_2kernel(out, W, cand):
                K = cand
                break
        if K is None:
            return None
        W &= ~K
        steps += 1


def experiment_3():
    """The chromatic-number theorem on the extremal 8-vertex oriented graph
    from the census (J = {0,1,2,3}, B = {4,5,6,7}, underlying K_{4,4})."""
    print("E-B3  iterated 2-kernel removal on the extremal j=4,t=4 digraph")
    arcs = [(0, 5), (0, 6), (1, 6), (1, 7), (2, 4), (2, 7), (3, 4), (3, 5),
            (4, 0), (4, 1), (5, 1), (5, 2), (6, 2), (6, 3), (7, 0), (7, 3)]
    n = 8
    out = [0] * n
    for (u, v) in arcs:
        out[u] |= 1 << v
    d = max_outdeg(out)
    steps = peel(out, n)
    print(f"   Delta^+ = {d}, peeling steps = {steps}, "
          f"bound = ceil(Delta^+/2)+1 = {-(-d // 2) + 1}, "
          f"chi(K_4,4) = 2")


def experiment_4(trials=40000, seed=20260910):
    """Does iterated 2-kernel removal ever succeed with Delta^+ >= 3?"""
    print("E-B4  search for peelable orientations with Delta^+ >= 3")
    rng = random.Random(seed)
    best = None
    hits = 0
    for _ in range(trials):
        n = rng.randint(8, 13)
        p = rng.choice([0.35, 0.45, 0.55])
        out = [0] * n
        for u, v in combinations(range(n), 2):
            r = rng.random()
            if r < p / 2:
                out[u] |= 1 << v
            elif r < p:
                out[v] |= 1 << u
        d = max_outdeg(out)
        if d < 3:
            continue
        s = peel(out, n)
        if s is not None:
            hits += 1
            if best is None or d > best[0]:
                best = (d, s, n, list(out))
    print(f"   {hits} peelable orientations found with Delta^+ >= 3")
    if best:
        d, s, n, out = best
        print(f"   best: n={n}, Delta^+={d}, steps={s}, "
              f"bound={-(-d // 2) + 1}")


if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
