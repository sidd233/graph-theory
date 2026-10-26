"""Method 2 (independent of the coefficient formula): expand P_{H_m} = prod over oriented edges
(x_u - x_v) directly with integer dict polynomials, discarding every monomial with an exponent > 2
(valid: multiplication only raises exponents, and every target monomial has all exponents <= 2).
Then read off c_S = [prod x_v^{2 - mu_S(v)}] P for every end multiset S.
Also, for m = 2, recompute with sympy as a second independent expansion.
Output lines: m k s [mu] c_S (same format as strip_coeff.py)."""
import itertools
import sys


def edges(m):
    E = []
    for c in range(1, m + 1):
        for r in range(3):
            E.append(((r, c), ((r + 1) % 3, c)))
        if c < m:
            for r in range(3):
                E.append(((r, c), (r, c + 1)))
    return E


def expand(m):
    idx = {(r, c): (c - 1) * 3 + r for c in range(1, m + 1) for r in range(3)}
    pw = [3 ** i for i in range(3 * m)]
    poly = {0: 1}
    for u, v in edges(m):
        iu, iv = idx[u], idx[v]
        new = {}
        for mono, co in poly.items():
            du = (mono // pw[iu]) % 3
            dv = (mono // pw[iv]) % 3
            if du < 2:
                k = mono + pw[iu]
                new[k] = new.get(k, 0) + co
            if dv < 2:
                k = mono + pw[iv]
                new[k] = new.get(k, 0) - co
        poly = {k: c for k, c in new.items() if c}
    return poly, idx, pw


def end_multisets(m):
    ev = [(r, 1) for r in range(3)] + [(r, m) for r in range(3)]
    for mus in itertools.product(range(3), repeat=6):
        if sum(mus) == 3:
            yield {v: k for v, k in zip(ev, mus) if k}


def main():
    ms = [int(x) for x in sys.argv[1].split(",")]
    for m in ms:
        poly, idx, pw = expand(m)
        print(f"# m={m}: {len(edges(m))} edges, {len(poly)} surviving monomials")
        if m == 2:
            import sympy as sp
            xs = {v: sp.Symbol(f"x_{v[0]}_{v[1]}") for v in idx}
            P = sp.Poly(sp.Mul(*[xs[u] - xs[v] for u, v in edges(m)]), *xs.values())
        for mu in end_multisets(m):
            mono = sum((2 - mu.get(v, 0)) * pw[i] for v, i in idx.items())
            c = poly.get(mono, 0)
            k = sum(x for (r, col), x in mu.items() if col == m)
            s = sum(x * r for (r, col), x in mu.items()) % 3
            if m == 2:
                cs = P.coeff_monomial(sp.Mul(*[xs[v] ** (2 - mu.get(v, 0)) for v in idx]))
                assert int(cs) == c, (mu, cs, c)
            key = " ".join(f"{r},{col}:{x}" for (r, col), x in sorted(mu.items(), key=lambda t: (t[0][1], t[0][0])))
            print(f"{m} {k} {s} [{key}] {c}")
        if m == 2:
            print("# m=2: sympy expansion agrees with dict expansion on all 50 S")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
