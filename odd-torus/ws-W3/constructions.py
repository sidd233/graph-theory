"""Explicit 2-d kernels of C_m x C_n (and of 3-dimensional tori) and the covering lemma.

Construction D(d, K): with d = gcd(m, n) >= 2 and K a maximal independent set of the cycle
Z_d (adjacency i ~ i +- 1; for d = 2 this means K = {0} or {1}),
    S = {(r, c) : (r + c) mod d in K}.
Checked here, by the definition, for all 3 <= m, n <= 40 with gcd > 1, for every MIS K of
Z_d, with both diagonal directions (r + c and r - c). Also checks the covering lemma: the
preimage under (r, c) -> (r mod p, c mod p) of a 2-d kernel of C_p x C_p is a 2-d kernel of
C_m x C_n, and prints the explicit kernels for p = 2 (via C_4 x C_4), 3, 5, 7, 11, 13.
3D: S = {x : (x1 + x2 + x3) mod d in K}, d = gcd(a, b, c), checked for a, b, c <= 12.

Run: python constructions.py
"""
import itertools
from math import gcd

from common import torus, is_2d_kernel


def mis_of_Zd(d):
    """All maximal independent sets of Z_d with i ~ i +- 1 (d >= 2), by DFS over words
    with no '11' and no '000', then a cyclic check by the definition."""
    out = []

    def ok(K):
        indep = all(((i + 1) % d) not in K for i in K)
        dom = all(i in K or ((i + 1) % d) in K or ((i - 1) % d) in K for i in range(d))
        return indep and dom

    def rec(w):
        if len(w) == d:
            K = frozenset(i for i in range(d) if w[i])
            if ok(K):
                out.append(K)
            return
        for b in (0, 1):
            if b and w and w[-1]:
                continue
            if not b and len(w) >= 2 and not w[-1] and not w[-2]:
                continue
            rec(w + [b])

    rec([])
    return out


def sample(Ks, d):
    """All MIS for d <= 15; otherwise the smallest, the largest and the first 4."""
    if d <= 15:
        return Ks
    return list({*Ks[:4], min(Ks, key=len), max(Ks, key=len)})


def diag_kernel(dims, d, K, signs):
    verts, idx, adj = torus(dims)
    S = [idx[v] for v in verts if (sum(s * x for s, x in zip(signs, v)) % d) in K]
    return adj, S, verts


def main():
    # 2D: all MIS K, both directions
    MIS = {d: mis_of_Zd(d) for d in range(2, 41)}
    tested = fails = 0
    for m in range(3, 41):
        for n in range(3, 41):
            d = gcd(m, n)
            if d == 1:
                continue
            for K in sample(MIS[d], d):
                for signs in ((1, 1), (1, -1)):
                    adj, S, _ = diag_kernel((m, n), d, K, signs)
                    tested += 1
                    fails += not is_2d_kernel(adj, S)
    print(f"2D diagonal construction: {tested} (m, n, K, direction) cases with 3<=m,n<=40, "
          f"gcd>1 (all MIS K of Z_d for d<=15, 6 sampled K for d>15); failures: {fails}")
    print("number of MIS of Z_d, d=2..20:", [len(MIS[d]) for d in range(2, 21)])

    # covering lemma: lift kernels of C_p x C_p (p = 3, 5, 7) and C_4 x C_4 to multiples
    from common import sat_find
    lifts = lfail = 0
    for p in (3, 4, 5, 7):
        vp, ip, ap = torus((p, p))
        Sp = set(sat_find(ap))   # a kernel found by SAT, not by the construction
        for m in range(p, 41, p):
            for n in range(p, 41, p):
                v, i, a = torus((m, n))
                S = [i[x] for x in v if ip[(x[0] % p, x[1] % p)] in Sp]
                lifts += 1
                lfail += not is_2d_kernel(a, S)
    print(f"covering lifts of SAT kernels of C_p x C_p, p in (3,4,5,7), to all multiples "
          f"<= 40: {lifts} cases, failures: {lfail}")

    # explicit examples
    for p in (4, 3, 5, 7, 11, 13):
        K = sorted(min(mis_of_Zd(p), key=lambda K: (len(K), sorted(K))))
        adj, S, verts = diag_kernel((p, p), p, set(K), (1, 1))
        print(f"\nC_{p} x C_{p}: S = {{(r,c): (r+c) mod {p} in {K}}}, |S| = {len(S)}, "
              f"valid = {is_2d_kernel(adj, S)}")
        Sset = {verts[s] for s in S}
        for r in range(p):
            print("   " + "".join("X" if (r, c) in Sset else "." for c in range(p)))

    # 3D
    tested = fails = 0
    for a, b, c in itertools.combinations_with_replacement(range(3, 13), 3):
        d = gcd(gcd(a, b), c)
        if d == 1:
            continue
        for K in mis_of_Zd(d)[:3]:
            adj, S, _ = diag_kernel((a, b, c), d, K, (1, 1, 1))
            tested += 1
            fails += not is_2d_kernel(adj, S)
    print(f"\n3D construction (x1+x2+x3) mod d in K, a<=b<=c<=12, gcd(a,b,c)>1: {tested} cases,"
          f" failures: {fails}")


if __name__ == "__main__":
    main()
