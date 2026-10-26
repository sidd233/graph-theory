# W4: exact closed form and exact non-vanishing of the dominant amplitudes.
#
# Let y = nu^2 = -l1^2 (real, ~ -31.62), the root of F(y) = y^4 + 35y^3 + 110y^2 + 100y + 25 (q2(x) = F(x^2)).
# mu(x) = x q1(x) q2(x) = (x^2 - y) g(x) with g(x) = x q1(x) (F(x^2) - F(y))/(x^2 - y)  in Q[y][x], g odd.
# Spectral projectors onto the dominant pair (Lagrange):
#   Q_e = P_nu + P_{-nu} = T g(T) / (nu g(nu)),   Q_o = P_nu - P_{-nu} = g(T) / g(nu),
#   g(nu) = nu Q1(y) F'(y),   Q1(y) = y^2 + 10y + 5.
# Hence, with c(a,b) = tr(X T^a D_i T^b) and g(x) = sum_k g_k(y) x^k:
#   B(e,e) = sum g_k g_l c(k+1,l+1) / (y^2 Q1^2 F'^2)
#   B(e,o) = sum g_k g_l c(k+1,l)   / (nu y Q1^2 F'^2)
#   B(o,e) = sum g_k g_l c(k,l+1)   / (nu y Q1^2 F'^2)
#   B(o,o) = sum g_k g_l c(k,l)     / (y Q1^2 F'^2)
# Every c(.,.) that occurs has the parity of a torus coefficient (g is odd), so it is a rational integer
# (checked). The numerator r(y) is reduced mod F to degree < 4 with rational coefficients.
# Non-vanishing: F is irreducible over Q (checked), so r(nu^2) != 0 iff r != 0 as a polynomial.
import sys
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')
import sympy as sp
import flint
from fractions import Fraction as Fr
from tmlib import build, powers

y, x = sp.symbols('y x')
Fy = y**4 + 35*y**3 + 110*y**2 + 100*y + 25
Q1y = y**2 + 10*y + 5
out = []


def log(s):
    print(s, flush=True); out.append(s)


fz = flint.fmpz_poly([25, 100, 110, 35, 1])
fac = fz.factor()
log(f"F(y) = {Fy}; factorisation over Q (flint): {fac}")
assert len(fac[1]) == 1 and fac[1][0][1] == 1 and fac[1][0][0].degree() == 4
q1x = x**4 + 10*x**2 + 5
g = sp.expand(x * q1x * sp.cancel((Fy.subs(y, x**2) - Fy) / (x**2 - y)))
gp = sp.Poly(g, x)
gk = {k: sp.expand(gp.coeff_monomial(x**k)) for k in range(gp.degree() + 1)}
assert all(gk[k] == 0 for k in gk if k % 2 == 0)
# sanity: (x^2 - y) g(x) == x q1 q2 mod F(y)
chk = sp.Poly(sp.expand((x**2 - y) * g - x * q1x * Fy.subs(y, x**2)), x)
assert all(sp.rem(c, Fy, y) == 0 for c in chk.all_coeffs())
log(f"g(x) has degree {gp.degree()} in x, odd; (x^2-y) g(x) = x q1(x) q2(x) mod F(y): verified")

B = build(5)
dg = gp.degree()
Tp = powers(B['T'], dg + 1)
Fp = sp.diff(Fy, y)
den_common = sp.expand(y * Q1y**2 * Fp**2)

def red(expr):
    return sp.Poly(sp.rem(sp.expand(expr), Fy, y), y)

results = {}
cases = [('col', i) for i in range(5)] + [('row', i) for i in range(1, 5)]
for et, i in cases:
    X = B['G'] if et == 'col' else B['H']
    C = {}
    for a in range(dg + 2):
        XA = X @ Tp[a] @ B['D'][i]
        for b in range(dg + 2):
            C[(a, b)] = (XA @ Tp[b]).trace()
    combos = [('e', 'o'), ('o', 'e')] if et == 'col' else [('e', 'e'), ('o', 'o')]
    for p, q in combos:
        num = 0
        for k in gk:
            if gk[k] == 0:
                continue
            for l in gk:
                if gk[l] == 0:
                    continue
                cv = C[(k + (p == 'e'), l + (q == 'e'))]
                assert cv[1] == 0 and cv[0].denominator == 1, "non-integer c"
                num += gk[k] * gk[l] * int(cv[0])
        # amplitude = num / (den_common * extra), extra = y (ee), nu (eo/oe), 1 (oo)
        # we report  beta = num / den_common  reduced in Q[y]/F  (exact), and the amplitude:
        #   B(e,e) = beta / y,  B(e,o) = B(o,e) = beta / nu,  B(o,o) = beta
        inv = sp.invert(den_common, Fy, y)
        beta = red(num * inv)
        nz = not beta.is_zero
        results[(et, i, p, q)] = beta
        yv = sp.nroots(Fy, n=40)
        yv = min(yv, key=lambda r: sp.re(r))      # nu^2 = most negative root
        bval = sp.N(beta.as_expr().subs(y, yv), 25)
        if (p, q) == ('e', 'e'):
            amp = f"B = beta/y = {sp.N(bval/yv, 20)}"
        elif (p, q) == ('o', 'o'):
            amp = f"B = beta = {sp.N(bval, 20)}"
        else:
            amp = f"B = beta/nu = {sp.N(-bval/sp.sqrt(-yv), 20)}*i  (nu = i*sqrt(-y))"
        log(f"{et} i={i} B({p},{q}): beta(y) mod F = {beta.as_expr()} ; nonzero polynomial: {nz} ; numerically {amp}")
        assert nz
log("all dominant amplitudes are nonzero elements of Q(nu): PROVED exactly (F irreducible over Q, beta != 0 mod F)")
open('/home/sid/work/gt/odd-torus/ws-W4/dominant_exact_output.txt', 'w').write("\n".join(out) + "\n")
