# W4: generic-m version of the dominance proof (used for m = 7, and re-run for m = 5 as a cross-check of prove_m5.py).
#
# Differences from prove_m5.py: no hard-coded polynomials, possible nilpotent part x^k, and the amplitudes are
# computed from the EXACT moment matrix  C[k,l] = c(k,l) = tr(X T^k D_i T^l)  (k,l < d + K) instead of from
# ball projector matrices:  P_z = p_z(T),  p_z(x) = mu(x)/((x-z) mu'(z)) = sum_k u_k(z) x^k / mu'(z), so
#   A_{z z'}   = tr(X P_z D P_z') = u(z)^T C u(z') / (mu'(z) mu'(z'))
#   beta_z(b)  = tr(P_z D T^b X)  = sum_k u_k(z) C[k,b] / mu'(z)
#   gamma_z(a) = tr(P_z X T^a D)  = sum_k u_k(z) C[a,k] / mu'(z)
# Expansion valid for exponents >= k (k = multiplicity of x in mu, checked exactly).
# Usage: python prove_gen.py m
import sys, time
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')
import flint
import sympy as sp
from flint import acb, arb, acb_mat, acb_poly, fmpz_poly
from tmlib import build, powers, ZWMat, identity
from spectral import realify, is_zero

m = int(sys.argv[1])
PREC = int(sys.argv[2]) if len(sys.argv) > 2 else 400
KMAX = 40
out = []


def log(s=""):
    print(s, flush=True); out.append(s)


def poly_at(T, coeffs_low_high):
    n = T.nrows()
    I = identity(n)
    R = ZWMat(flint.fmpz_mat(n, n), flint.fmpz_mat(n, n), 1)
    for c in reversed(coeffs_low_high):
        R = R @ T
        R = ZWMat(R.A0 + I.A0 * int(c), R.A1, 1)
    return R


t0 = time.time()
B = build(m)
T = B['T']; ns = T.nrows()
assert T.den == 1
g = realify(T).charpoly()
fac = g.factor()
xp = fmpz_poly([0, 1])
irr = [(p, e) for p, e in fac[1] if p != xp]
log(f"m={m}: {ns} column states, {len(B['Se'])} damaged-column states")
log(f"charpoly of realified T = " + " * ".join(f"({p})^{e}" for p, e in fac[1]))
q = fmpz_poly([1])
for p, e in irr:
    q = q * p
assert q.gcd(q.derivative()) == 1 and q[0] != 0
# purely imaginary roots: every factor is h(x^2) with h having only negative real roots (Sturm count, exact)
ys = sp.symbols('y')
for p, e in irr:
    cs = [int(c) for c in p.coeffs()]
    assert all(cs[j] == 0 for j in range(1, len(cs), 2)), "factor not even"
    h = sp.Poly(sum(cs[2 * j] * ys ** j for j in range(len(cs) // 2 + 1)), ys)
    assert h.count_roots(-sp.oo, 0) == h.degree() and h.eval(0) != 0
log("every nonzero factor is h(x^2) with all roots of h real negative (exact Sturm count): nonzero eigenvalues are +-i*l, l > 0")
Qt = poly_at(T, [int(c) for c in q.coeffs()])
assert not is_zero(Qt)
k = 0
M = Qt
while not is_zero(M):
    M = T @ M; k += 1
    assert k <= 20
log(f"exact: T^{k} q(T) = 0 and T^{k-1} q(T) != 0, q = product of the distinct nonzero irreducible factors (deg {q.degree()}), squarefree")
mu = xp ** k * q
d = mu.degree()
mu_c = [int(c) for c in mu.coeffs()]          # low -> high

flint.ctx.prec = PREC
roots = acb_poly([acb(c) for c in q.coeffs()]).roots(tol=arb(2) ** (-(PREC - 60)))
roots = sorted(roots, key=lambda z: -float(z.abs_upper()))
nu = roots[0] if roots[0].imag > 0 else roots[1]
assert (roots[0] + roots[1]).contains(0)
L1 = min(roots[0].abs_lower(), roots[1].abs_lower())
U2 = max(z.abs_upper() for z in roots[2:])
assert L1 > U2
rest = [z for z in roots if not (z.overlaps(nu) or z.overlaps(-nu))]
assert len(rest) == len(roots) - 2
Zs = [nu, -nu] + rest
l1 = nu.imag
r_ratio = U2 / L1
log(f"certified: dominant pair +-i*l1, l1 in {l1.str(25, radius=True)} (l1^2 = {(l1*l1).str(20)}); all other |z| <= {U2.str(20)}; r = {r_ratio.upper().str(15)}")
t = [arb(1), arb(1)] + [(abs(z) / l1).upper() for z in rest]
nz = len(Zs)


def uvec(z):
    # mu(x)/(x - z) = sum_k x^k * sum_{j>k} mu_j z^{j-k-1}
    u = []
    for kk in range(d):
        s = acb(0)
        for j in range(d, kk, -1):
            s = s * z + mu_c[j]
        u.append(s)
    dmu = acb(0)
    for j in range(d, 0, -1):
        dmu = dmu * z + j * mu_c[j]
    return u, dmu


U = [uvec(z) for z in Zs]
Lmax = d + KMAX
Tp = powers(T, Lmax)
log(f"built T^0..T^{Lmax} exactly ({time.time()-t0:.1f}s)")
wacb = acb(-0.5) + acb(0, 1) * arb(3).sqrt() / 2


def moment_matrix(X, Di):
    """exact C[a,b] = tr(X T^a D T^b), a,b <= Lmax, returned as dict of (Fraction,Fraction) and acb_mat"""
    n2 = ns * ns
    V0 = flint.fmpz_mat(n2, Lmax + 1); V1 = flint.fmpz_mat(n2, Lmax + 1)
    for b in range(Lmax + 1):
        for p in range(ns):
            for qq in range(ns):
                V0[p * ns + qq, b] = Tp[b].A0[qq, p]; V1[p * ns + qq, b] = Tp[b].A1[qq, p]
    U0 = flint.fmpz_mat(Lmax + 1, n2); U1 = flint.fmpz_mat(Lmax + 1, n2)
    for a in range(Lmax + 1):
        Mx = X @ Tp[a] @ Di
        for p in range(ns):
            for qq in range(ns):
                U0[a, p * ns + qq] = Mx.A0[p, qq]; U1[a, p * ns + qq] = Mx.A1[p, qq]
    P0 = U0 * V0; Q0 = U1 * V1
    C0 = P0 - Q0; C1 = U0 * V1 + U1 * V0 - Q0
    den = X.den * Di.den
    Cacb = acb_mat(Lmax + 1, Lmax + 1)
    for a in range(Lmax + 1):
        for b in range(Lmax + 1):
            Cacb[a, b] = (acb(int(C0[a, b])) + acb(int(C1[a, b])) * wacb) / den
    return C0, C1, den, Cacb


Vm = [acb_mat(d, 1, [U[z][0][kk] / U[z][1] for kk in range(d)]) for z in range(nz)]   # u(z)/mu'(z)
cases = [('col', i) for i in range(m)] + [('row', i) for i in range(1, m)]
summary = []
for et, i in cases:
    X = B['G'] if et == 'col' else B['H']
    par_sum = 1 if et == 'col' else 0
    nfun = (lambda a, b: a + b + 2) if et == 'col' else (lambda a, b: a + b + 1)
    C0, C1, den, Cacb = moment_matrix(X, B['D'][i])
    log(f"\n=== m={m} edge {et}, w row i={i} ===  ({time.time()-t0:.1f}s)")
    # integrality check of the genuine coefficients (n >= 3)
    for a in range(Lmax + 1):
        for b in range(Lmax + 1 - a):
            if (a + b) % 2 == par_sum and nfun(a, b) >= 3:
                assert int(C1[a, b]) == 0 and int(C0[a, b]) % den == 0
    Csub = acb_mat(d, d, [Cacb[a, b] for a in range(d) for b in range(d)])
    VT = [Vv.transpose() for Vv in Vm]
    A = [[(VT[z] * Csub * Vm[zz])[0, 0] for zz in range(nz)] for z in range(nz)]
    # validation against exact values for k <= a,b, n <= 25 (expansion needs exponents >= k)
    nval = 0
    for a in range(max(k, 1), 24):
        for b in range(max(k, 1), 24):
            if (a + b) % 2 != par_sum or nfun(a, b) > 25:
                continue
            spv = sum((A[z][zz] * Zs[z] ** a * Zs[zz] ** b for z in range(nz) for zz in range(nz)), acb(0))
            if not ((spv - Cacb[a, b]).contains(0) and spv.rad() < 1e-6):
                log(f"VALIDATION FAILED at (a,b)=({a},{b}): expansion {spv.str(20, radius=True)} exact {Cacb[a, b].str(20, radius=True)}")
                sys.exit(1)
            nval += 1
    log(f"  validation: double expansion encloses the exact c(a,b) for {nval} pairs (n <= 25)")
    Bd = {}
    for p in (0, 1):
        qq = (par_sum - p) % 2
        s = A[0][0] + (-1) ** qq * A[0][1] + (-1) ** p * A[1][0] + (-1) ** (p + qq) * A[1][1]
        Bd[(p, qq)] = s
        assert not s.contains(0)
        log(f"  dominant amplitude B(a={p}, b={qq} mod 2) = {s.str(15, radius=True)}")
    K = None
    for KK in range(max(k, 1), KMAX + 1):
        err = arb(0)
        for z in range(nz):
            for zz in range(nz):
                if z < 2 and zz < 2:
                    continue
                err += A[z][zz].abs_upper() * t[z] ** KK * t[zz] ** KK
        if all(Bd[kk].abs_lower() > err for kk in Bd):
            K = KK
            log(f"  Region I (a,b >= K) certified with K = {K}: tail bound {err.upper().str(10)} < min|B| = {min(Bd[kk].abs_lower() for kk in Bd).str(10)}")
            break
    assert K is not None
    a0s, b0s = [], []
    for side in ('II', 'III'):
        for f in range(K):
            if side == 'II':      # b = f fixed, sum over z of z^a beta_z(f)
                amp = [sum((Vm[z][kk, 0] * Cacb[kk, f] for kk in range(d)), acb(0)) for z in range(nz)]
            else:                 # a = f fixed, sum over z of z^b gamma_z(f)
                amp = [sum((Vm[z][kk, 0] * Cacb[f, kk] for kk in range(d)), acb(0)) for z in range(nz)]
            pe = (par_sum - f) % 2
            dom = amp[0] + (-1) ** pe * amp[1]
            assert not dom.contains(0), (side, f)
            e = pe
            while e < max(k, 1):
                e += 2
            while True:
                err = sum((amp[z].abs_upper() * t[z] ** e for z in range(2, nz)), arb(0))
                if dom.abs_lower() > err:
                    break
                e += 2
                assert e < 5000
            (a0s if side == 'II' else b0s).append(e)
    log(f"  Region II  (b < K fixed): a0(b) = {a0s}")
    log(f"  Region III (a < K fixed): b0(a) = {b0s}")

    def covered(a, b):
        return (a >= K and b >= K) or (b < K and a >= a0s[b]) or (a < K and b >= b0s[a])
    big = 4 * (K + max(a0s + b0s)) + 10
    unc = [(a, s - a) for s in range(big) for a in range(s + 1)
           if s % 2 == par_sum and nfun(a, s - a) >= 3 and not covered(a, s - a)]
    nmax = max((nfun(a, b) for a, b in unc), default=0)
    log(f"  uncovered (a,b): {unc}  -> exact check needed for n <= {nmax}")
    # exact check of uncovered ones right here (from the exact moment matrix)
    for a, b in unc:
        assert a <= Lmax and b <= Lmax
        assert (int(C0[a, b]), int(C1[a, b])) != (0, 0), ("ZERO", a, b)
    log(f"  exact values at uncovered (a,b): {[int(C0[a, b]) // den for a, b in unc]}  (all nonzero)")
    summary.append((et, i, K, nmax, min(Bd[kk].abs_lower() for kk in Bd)))
log("\n=== summary ===")
for et, i, K, nmax, bmin in summary:
    log(f"  m={m} {et} i={i}: K={K}, uncovered n <= {nmax} (checked exactly), min|B| >= {bmin.str(8)}")
log(f"time {time.time()-t0:.1f}s")
open(f'/home/sid/work/gt/odd-torus/ws-W4/prove_gen_m{m}_output.txt', 'w').write("\n".join(out) + "\n")
