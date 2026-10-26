# W4: exact minimal polynomial and certified spectral data of the undamaged transfer matrix T (m = 5).
#
# Exact facts checked here (all integer / Z[omega] arithmetic):
#   (E1) char poly of the 60x60 integer realification of T is x^12 q1^4 q2^4, with
#        q1 = x^4 + 10x^2 + 5, q2 = x^8 + 35x^6 + 110x^4 + 100x^2 + 25.
#   (E2) T * q1(T) * q2(T) = 0 exactly, and q1(T) q2(T) != 0.
#   (E3) q1*q2 is squarefree with nonzero constant term, so mu(x) = x q1 q2 has simple roots:
#        T is diagonalisable, T = sum_z z P_z over the 13 roots z of x q1 q2 (P_z may be 0 a priori).
#   (E4) q1, q2 have only purely imaginary roots (sign changes of q(-y) evaluated at rationals).
# Certified (arb/acb ball arithmetic):
#   roots isolated by acb_poly.roots; dominant modulus attained by exactly two roots +-i*l1;
#   projectors P_z = prod_{z' != z} (T - z')/(z - z') as acb_mat balls (Lagrange interpolation,
#   valid because of (E2),(E3)).
import sys
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')
import flint
from flint import acb, arb, acb_mat, acb_poly, fmpz_poly, fmpq
from tmlib import build, ZWMat, identity

Q1 = [5, 0, 10, 0, 1]                      # low -> high
Q2 = [25, 0, 100, 0, 110, 0, 35, 0, 1]


def realify(A):
    n = A.nrows()
    M = flint.fmpz_mat(2 * n, 2 * n)
    for i in range(n):
        for j in range(n):
            a0, a1 = A.A0[i, j], A.A1[i, j]
            M[i, j] = a0; M[i, j + n] = -a1; M[i + n, j] = a1; M[i + n, j + n] = a0 - a1
    return M


def poly_of(T, coeffs_low_high):
    n = T.nrows()
    I = identity(n)
    R = ZWMat(flint.fmpz_mat(n, n), flint.fmpz_mat(n, n), 1)
    for c in reversed(coeffs_low_high):
        R = R @ T
        R = ZWMat(R.A0 + I.A0 * c, R.A1, 1)
    return R


def is_zero(A):
    return A.A0.is_zero() and A.A1.is_zero()


def exact_checks(B, log=print):
    T = B['T']
    assert T.den == 1
    q1, q2 = fmpz_poly(Q1), fmpz_poly(Q2)
    x = fmpz_poly([0, 1])
    g = realify(T).charpoly()
    E1 = (g == x ** 12 * q1 ** 4 * q2 ** 4)
    log(f"(E1) charpoly(realified T) == x^12 q1^4 q2^4 : {E1}")
    Q = poly_of(T, Q1) @ poly_of(T, Q2)
    E2a = is_zero(T @ Q)
    E2b = not is_zero(Q)
    log(f"(E2) T q1(T) q2(T) == 0 : {E2a};  q1(T) q2(T) != 0 : {E2b}")
    qq = q1 * q2
    E3 = (qq.gcd(qq.derivative()) == 1) and qq[0] != 0
    log(f"(E3) q1 q2 squarefree and q1 q2 (0) != 0 : {E3}")
    # (E4): roots in y = x^2 are negative reals: count sign changes of q(y) at rational points
    def ev(c, y):
        return sum(fmpq(c[2 * k]) * y ** k for k in range(len(c) // 2 + 1))
    pts1 = [fmpq(0), fmpq(-1), fmpq(-20)]                 # y^2+10y+5: +,-,+  -> 2 neg roots
    pts2 = [fmpq(0), fmpq(-1, 2), fmpq(-3, 2), fmpq(-3), fmpq(-40)]
    s1 = [ev(Q1, y) > 0 for y in pts1]
    s2 = [ev(Q2, y) > 0 for y in pts2]
    ch1 = sum(s1[k] != s1[k + 1] for k in range(len(s1) - 1))
    ch2 = sum(s2[k] != s2[k + 1] for k in range(len(s2) - 1))
    E4 = (ch1 == 2 and ch2 == 4)
    log(f"(E4) q1(y=x^2) has {ch1} sign changes on negative reals (deg 2), q2 has {ch2} (deg 4): all roots purely imaginary : {E4}")
    assert E1 and E2a and E2b and E3 and E4
    return True


def certified_spectrum(B, prec=300, log=print):
    flint.ctx.prec = prec
    qq = fmpz_poly(Q1) * fmpz_poly(Q2)
    roots = acb_poly([acb(int(c)) for c in qq.coeffs()]).roots(tol=arb(2) ** (-(prec - 40)))
    assert len(roots) == 12
    mods = [r.abs_upper() for r in roots]
    lows = [r.abs_lower() for r in roots]
    order = sorted(range(12), key=lambda k: -float(roots[k].abs_upper()))
    # dominant: the two roots with largest modulus; certify strict separation
    dom = order[:2]
    rest = order[2:]
    L = min(lows[k] for k in dom)
    U = max(mods[k] for k in rest)
    assert L > U, "dominance not certified"
    # the two dominant roots are negatives of each other (+-i l1) and purely imaginary
    z1, z2 = roots[dom[0]], roots[dom[1]]
    assert (z1 + z2).contains(0)
    if z1.imag < 0:
        z1, z2 = z2, z1
    roots_sorted = [z1, z2] + [roots[k] for k in rest]
    # exact purity: replace each root ball by i * (real ball) using (E4): real part is exactly 0
    roots_sorted = [acb(0, r.imag) for r in roots_sorted]
    rho = z1.imag
    log(f"dominant root nu = i*l1, l1 in {rho.str(30, radius=True)}")
    log(f"|other roots| <= {U.str(20, radius=True)};  ratio r = max|other|/l1 <= {(U / L).upper().str(20)}")
    return roots_sorted


def projectors(B, roots, prec=300):
    """P_z for z in [0] + roots, as acb_mat; uses mu = x q1 q2 with simple roots."""
    flint.ctx.prec = prec
    T = B['T'].to_acb()
    n = T.nrows()
    I = acb_mat(n, n)
    for k in range(n):
        I[k, k] = 1
    Z = [acb(0)] + list(roots)
    P = []
    for a, z in enumerate(Z):
        M = I
        for b, z2 in enumerate(Z):
            if a == b:
                continue
            M = M * ((T - I * z2) * (1 / (z - z2)))
        P.append(M)
    return Z, P


def check_projectors(B, Z, P, log=print):
    T = B['T'].to_acb()
    n = T.nrows()
    S = P[0]
    TS = P[0] * Z[0]
    for z, M in zip(Z[1:], P[1:]):
        S = S + M
        TS = TS + M * z
    I = acb_mat(n, n)
    for k in range(n):
        I[k, k] = 1
    ok1 = all((S - I)[i, j].contains(0) for i in range(n) for j in range(n))
    ok2 = all((TS - T)[i, j].contains(0) for i in range(n) for j in range(n))
    ranks = [round(float(M.trace().real)) for M in P]
    log(f"projector sanity: sum P_z contains I: {ok1}; sum z P_z contains T: {ok2}; traces (ranks) of P_z, z=0 first: {ranks}")
    return ranks


if __name__ == '__main__':
    B = build(5)
    exact_checks(B)
    roots = certified_spectrum(B)
    Z, P = projectors(B, roots)
    check_projectors(B, Z, P)
    for z in Z:
        print("  root", z.str(12))
