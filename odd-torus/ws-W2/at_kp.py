"""Alon-Tarsi coefficients of subgraphs of C_m x C_n, exactly mod a prime p.

coef(m, n, Edel, t) = [prod_v x_v^{t_v}] prod_{edges u->v kept} (x_u - x_v)  (mod p),
computed by the Karasev-Petrov / Lason coefficient formula with A_v = {0, 1, ..., t_v} in F_p:
    [x^t] Q = sum_{phi in prod A_v} Q(phi) / prod_v N_v(phi_v),  N_v(a) = prod_{b in A_v, b != a}(a-b),
valid over any field when deg Q <= sum t_v (here deg Q = |E kept| = sum t_v). The sum factorises
over the columns of the torus into a trace of a product of transfer matrices.

A NONZERO value mod p proves the integer coefficient is nonzero, hence (Combinatorial
Nullstellensatz) the graph is colourable from any lists with |L(v)| >= t_v + 1. A zero mod p
proves nothing on its own (we use two primes for the sanity check that the full odd torus gives 0).

Checks run by main() (output at_kp.txt):
  (a) sanity: full torus, t = 2 everywhere: 0 for odd x odd (Li-Shao-Petrov-Gordeev), nonzero
      for odd x even;
  (b) hypothesis of (C): G - v has a nonzero coefficient with all t <= 2 (so G - v is
      3-choosable); vertex-transitivity means one v suffices;
  (c) hypothesis of (O): G - e has a nonzero coefficient with t <= 2 (one vertex w with t_w = 1),
      for a row edge and a column edge (all edges of each type are equivalent under rotations).
"""
import itertools
import sys

import numpy as np

PRIMES = (33554393, 33554383)   # primes < 2^25: products < 2^50, sums of <= 243 terms < 2^58


def coef(m, n, Edel, t, p):
    """t: dict vertex -> exponent (missing = 2); Edel: set of deleted edges (min,max)."""
    idx = lambda r, c: r * n + c
    keep = lambda a, b: (min(a, b), max(a, b)) not in Edel
    inv = lambda x: pow(int(x) % p, p - 2, p)
    cols = []
    for c in range(n):
        vs = [idx(r, c) for r in range(m)]
        rng = [range(t.get(v, 2) + 1) for v in vs]
        states = list(itertools.product(*rng))
        w = []
        for s in states:
            val = 1
            for r in range(m):          # vertical edges (r,c)-(r+1,c)
                a, b = vs[r], vs[(r + 1) % m]
                if m == 2 and r == 1:
                    continue
                if keep(a, b):
                    val = val * (s[r] - s[(r + 1) % m]) % p
            for r in range(m):          # 1 / N_v
                tv = t.get(vs[r], 2)
                Nv = 1
                for b in range(tv + 1):
                    if b != s[r]:
                        Nv *= (s[r] - b)
                val = val * inv(Nv) % p
            w.append(val % p)
        cols.append((vs, states, np.array(w, dtype=np.int64)))
    M = None
    for c in range(n):
        vs, st, w = cols[c]
        vs2, st2, _ = cols[(c + 1) % n]
        T = np.ones((len(st), len(st2)), dtype=np.int64)
        for r in range(m):
            if keep(vs[r], vs2[r]):
                d = (np.array([s[r] for s in st])[:, None] - np.array([s[r] for s in st2])[None, :])
                T = (T * (d % p)) % p
        T = (w[:, None] * T) % p
        M = T if M is None else (M @ T) % p
    return int(np.trace(M) % p)


def main():
    out = open("at_kp.txt", "w")

    def log(s):
        print(s, flush=True)
        out.write(s + "\n")

    cases = [(3, 3), (3, 4), (3, 5), (3, 7), (5, 5), (4, 5), (5, 7)]
    if len(sys.argv) > 1:
        cases = [tuple(map(int, a.split("x"))) for a in sys.argv[1:]]
    for m, n in cases:
        N = m * n
        full = [coef(m, n, set(), {}, p) for p in PRIMES]
        log(f"C{m}xC{n}: (a) full torus coefficient of prod x^2 mod p1,p2 = {full}")
        # (b) G - v, v = (0,0): delete its 4 edges, t_v = 0, two more vertices get t = 1
        v = 0
        nb = [(1 % m) * n, (m - 1) * n, 1 % n, n - 1]
        Edel = {(min(v, u), max(v, u)) for u in nb}
        found = None
        for w1, w2 in itertools.combinations(range(1, N), 2):
            t = {v: 0, w1: 1, w2: 1}
            val = coef(m, n, Edel, t, PRIMES[0])
            if val:
                found = (w1, w2, val)
                break
        log(f"C{m}xC{n}: (b) G-v, v=(0,0): first nonzero monomial with t_w1=t_w2=1: "
            f"{'NONE FOUND' if not found else f'w1={divmod(found[0], n)} w2={divmod(found[1], n)} coef mod p = {found[2]}'}")
        # (c) G - e for a row edge and a column edge at (0,0)
        for name, e in (("row", (0, 1 % n)), ("column", (0, (1 % m) * n))):
            e = (min(e), max(e))
            nz = [w for w in range(N) if coef(m, n, {e}, {w: 1}, PRIMES[0])]
            log(f"C{m}xC{n}: (c) G-e, {name} edge (0,0)-{divmod(e[1], n)}: {len(nz)} of {N} "
                f"vertices w give a nonzero coefficient of x_w prod x^2"
                f"{'' if not nz else '; e.g. w=' + str(divmod(nz[0], n))}")


if __name__ == "__main__":
    main()
