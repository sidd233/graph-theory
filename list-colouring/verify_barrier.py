"""Check the exact condition the kernel induction needs, at strength 2.

(star)  K nonempty, independent, K subset of S, and every u in S\K that is
        ADJACENT to K (in- or out-arc) has at least 2 out-arcs into K.

(star) is strictly weaker than "K is a 2-kernel of D[S]": vertices with no
neighbour in K are excused, because they lose no colour.
"""
from itertools import product

pc = int.bit_count

def subsets(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask

def induced(out, W, n):
    return [out[v] & W if (W >> v) & 1 else 0 for v in range(n)]

def indeg(o, n):
    inn = [0]*n
    for v in range(n):
        m = o[v]
        while m:
            b = m & -m
            inn[b.bit_length()-1] |= 1 << v
            m ^= b
    return inn

def independent(o, K):
    m = K
    while m:
        b = m & -m
        if o[b.bit_length()-1] & K:
            return False
        m ^= b
    return True

def star_good(out, n, W, S):
    o = induced(out, W, n)
    inn = indeg(o, n)
    adj = [o[v] | inn[v] for v in range(n)]
    for K in subsets(S):
        if K == 0 or not independent(o, K):
            continue
        ok = True
        m = S & ~K
        while m:
            b = m & -m
            u = b.bit_length()-1
            if adj[u] & K and pc(o[u] & K) < 2:
                ok = False
                break
            m ^= b
        if ok:
            return K
    return None

def first_failure(out, n):
    """Smallest (|S|, W, S) with no (star)-good set, or None."""
    full = (1 << n) - 1
    best = None
    for W in subsets(full):
        if W == 0:
            continue
        for S in subsets(W):
            if S == 0:
                continue
            if star_good(out, n, W, S) is None:
                if best is None or pc(S) < best[0]:
                    best = (pc(S), W, S)
    return best

def all_digraphs(n, digons=True):
    pairs = [(u, v) for u in range(n) for v in range(u+1, n)]
    states = 4 if digons else 3
    for code in product(range(states), repeat=len(pairs)):
        out = [0]*n
        for (u, v), d in zip(pairs, code):
            if d in (1, 3): out[u] |= 1 << v
            if d in (2, 3): out[v] |= 1 << u
        yield out

for n in range(2, 5):
    survivors, witness_sizes, total = 0, {}, 0
    for out in all_digraphs(n):
        if all(m == 0 for m in out):
            continue
        total += 1
        f = first_failure(out, n)
        if f is None:
            survivors += 1
            print("   SURVIVOR", out)
        else:
            witness_sizes[f[0]] = witness_sizes.get(f[0], 0) + 1
    print(f"n={n}: {total} digraphs with an arc; {survivors} satisfy (star) for all (W,S);"
          f" smallest failing |S| histogram = {witness_sizes}")
