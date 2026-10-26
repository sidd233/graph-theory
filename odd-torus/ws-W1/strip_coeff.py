"""Exact strip coefficients c_S for H_m = C_3 x P_m via the Lason / Karasev-Petrov formula.

Graph: vertices (r, c), r in Z_3, c = 1..m. Column edge (r,c)-(r+1,c) contributes
x_{r,c} - x_{r+1,c}; row edge (r,c)-(r,c+1) contributes x_{r,c} - x_{r,c+1}.
End multiset S: 3 vertices from columns 1 and m, multiplicity mu_S(v) <= 2.
t_v = 2 - mu_S(v), c_S = [prod x_v^{t_v}] P_{H_m}.

Method A: c_S = [prod x_v^2](P * prod x_v^{mu(v)}), formula with every A_v = {1, w, w^2}:
  N_v(a) = 3/a, so c_S = sum_phi P(phi) prod_v phi(v)^{1 + mu(v)} / 3^{3m}.
Method B: formula applied directly with |A_v| = t_v + 1, A_v a subset of the cube roots
  (2-subset for t_v = 1, singleton for t_v = 0), subsets chosen pseudo-randomly per vertex.
Both: transfer over columns, open ends, exact arithmetic in Q(omega) (zomega.Z).
"""
import itertools
import random
import sys
from fractions import Fraction
from zomega import Z, wpow

ALL = (0, 1, 2)  # exponents j of omega^j


def end_vertices(m):
    return [(r, 1) for r in range(3)] + [(r, m) for r in range(3)]


def end_multisets(m):
    """All mu: end vertices -> {0,1,2} with total 3. Returned as dict v -> mu (nonzero only)."""
    ev = end_vertices(m)
    out = []
    for mus in itertools.product(range(3), repeat=6):
        if sum(mus) == 3:
            out.append({v: k for v, k in zip(ev, mus) if k})
    return out


def ks(m, mu):
    k = sum(c for (r, col), c in mu.items() if col == m)
    s = sum(c * r for (r, col), c in mu.items()) % 3
    return k, s


def diff(i, j):
    return wpow(i) - wpow(j)


def transfer(m, sets, vweight):
    """sets[(r,c)] = tuple of exponents allowed at (r,c); vweight(v, j) = weight of colour w^j at v.
    Returns sum over phi in prod A_v of P(phi) * prod_v vweight(v, phi(v))."""
    vec = None
    prev_states = None
    for c in range(1, m + 1):
        states = list(itertools.product(*[sets[(r, c)] for r in range(3)]))
        colw = {}
        for st in states:
            w = Z(1)
            for r in range(3):
                w = w * diff(st[r], st[(r + 1) % 3]) * vweight((r, c), st[r])
            colw[st] = w
        if vec is None:
            vec = colw
        else:
            new = {}
            for st in states:
                if colw[st].iszero():
                    continue
                acc = Z(0)
                for ps, val in vec.items():
                    if val.iszero():
                        continue
                    f = Z(1)
                    for r in range(3):
                        f = f * diff(ps[r], st[r])
                        if f.iszero():
                            break
                    if not f.iszero():
                        acc = acc + val * f
                new[st] = acc * colw[st]
            vec = new
    tot = Z(0)
    for v in vec.values():
        tot = tot + v
    return tot


def coeff_A(m, mu):
    sets = {(r, c): ALL for r in range(3) for c in range(1, m + 1)}
    # weight phi(v)^{1+mu(v)} / 3
    def vw(v, j):
        return wpow(j * (1 + mu.get(v, 0))) * Z(Fraction(1, 3))
    return transfer(m, sets, vw)


def coeff_B(m, mu, rng):
    sets = {}
    for r in range(3):
        for c in range(1, m + 1):
            t = 2 - mu.get((r, c), 0)
            sets[(r, c)] = tuple(sorted(rng.sample(ALL, t + 1)))

    def vw(v, j):
        n = Z(1)
        for b in sets[v]:
            if b != j:
                n = n * diff(j, b)
        return n.inv()
    return transfer(m, sets, vw), sets


def as_int(z):
    assert z.b == 0, f"non-rational coefficient {z}"
    assert z.a.denominator == 1, f"non-integer coefficient {z}"
    return int(z.a)


def main():
    m_lo, m_hi = int(sys.argv[1]), int(sys.argv[2])
    nB = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    rng = random.Random(20261026)
    print(f"# strip coefficients c_S, H_m = C3 x P_m, m = {m_lo}..{m_hi}; method A and {nB} runs of method B")
    print("# columns: m k s mu(as r,c:mult ...) c_S")
    nmismatch = 0
    for m in range(m_lo, m_hi + 1):
        for mu in end_multisets(m):
            k, s = ks(m, mu)
            a = coeff_A(m, mu)
            ia = as_int(a)
            for _ in range(nB):
                b, sets = coeff_B(m, mu, rng)
                if not (b == a):
                    nmismatch += 1
                    print(f"MISMATCH m={m} mu={mu} A={a} B={b} sets={sets}")
            key = " ".join(f"{r},{c}:{x}" for (r, c), x in sorted(mu.items(), key=lambda t: (t[0][1], t[0][0])))
            print(f"{m} {k} {s} [{key}] {ia}")
        sys.stdout.flush()
    print(f"# method A vs method B mismatches: {nmismatch}")


if __name__ == "__main__":
    main()
