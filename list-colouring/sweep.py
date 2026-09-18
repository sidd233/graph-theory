"""How far can the bound be pushed before the method collapses?

Target the bound  ch <= ceil(lam * Delta) + 1  for a rational lam in (0, 1].
  lam = 1   is the ordinary greedy / kernel bound, always available.
  lam = 1/2 is the 2-kernel dream.
A vertex u with a neighbours in the coloured set K is safe iff
  f(d) - f(d - a) >= 1   where f(d) = ceil(lam*d) + 1.
Sweep lam and see which graphs still work, to find where the method dies.
"""
from itertools import combinations, permutations
from fractions import Fraction
import sys
pc = int.bit_count

def subsets(mask):
    s = mask
    while True:
        yield s
        if s == 0: break
        s = (s - 1) & mask

def make_f(lam):
    return lambda d: -((-lam.numerator * d) // lam.denominator) + 1

def good(adj, W, S, f):
    deg = [pc(adj[v] & W) for v in range(len(adj))]
    for K in subsets(S):
        if K == 0: continue
        ok, m = True, K
        while m:
            b = m & -m
            if adj[b.bit_length()-1] & K: ok = False; break
            m ^= b
        if not ok: continue
        m = S & ~K
        while m:
            b = m & -m; u = b.bit_length()-1
            a = pc(adj[u] & K)
            if a and f(deg[u]) - f(deg[u]-a) < 1: ok = False; break
            m ^= b
        if ok: return True
    return False

def has_safe(adj, W, f):
    m = W
    while m:
        b = m & -m; m ^= b
        if all(good(adj, W, b | T, f) for T in subsets(W & ~b)):
            return True
    return False

def survives(adj, n, f):
    return all(has_safe(adj, W, f) for W in range(1, 1 << n))

def classes(n):
    pairs = list(combinations(range(n), 2)); seen = set()
    for code in range(1 << len(pairs)):
        adj = [0]*n
        for i, (u, v) in enumerate(pairs):
            if (code >> i) & 1: adj[u] |= 1 << v; adj[v] |= 1 << u
        key = min(sum(((adj[p[u]] >> p[v]) & 1) << (u*n+v)
                  for u in range(n) for v in range(u+1, n)) for p in permutations(range(n)))
        if key in seen: continue
        seen.add(key); yield adj

def acyclic(adj, n):
    seen = 0
    for s in range(n):
        if (seen >> s) & 1: continue
        stack = [(s, -1)]; seen |= 1 << s; cnt = 1; edges = 0
        comp = 1 << s
        while stack:
            v, p = stack.pop()
            m = adj[v]
            while m:
                b = m & -m; u = b.bit_length()-1; m ^= b
                edges += 1
                if not (seen >> u) & 1:
                    seen |= b; comp |= b; cnt += 1; stack.append((u, v))
        if edges // 2 != cnt - 1: return False
    return True

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    pool = list(classes(n))
    forests = sum(1 for a in pool if acyclic(a, n))
    print(f"n={n}: {len(pool)} graphs, {forests} forests\n")
    print(f"{'lambda':>8} {'bound at Delta':>16} {'survive':>9} {'= forests?':>11}")
    for lam in [Fraction(1), Fraction(9,10), Fraction(5,6), Fraction(4,5), Fraction(3,4),
                Fraction(2,3), Fraction(3,5), Fraction(1,2)]:
        f = make_f(lam)
        s = [a for a in pool if survives(a, n, f)]
        allf = all(acyclic(a, n) for a in s)
        print(f"{str(lam):>8} {'ceil('+str(lam)+'D)+1':>16} {len(s):>9} "
              f"{('yes' if len(s)==forests and allf else 'no'):>11}")
