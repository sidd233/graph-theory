# W7 method A: exact strip coefficients c_S for H = C_m x P_l (m = 5 by default) via the
# Lason / Karasev-Petrov formula with every A_v = {1, w, w^2} and the extra factor phi(v)^mu(v):
#   c_S = [prod x^2](P * prod x^mu) = sum_phi P(phi) prod_v (phi(v)^{1+mu(v)} / 3).
# Conventions as W1: vertex (r,c), r in Z_m, columns c = 1..l; column edge (r,c)->(r+1,c), row edge (r,c)->(r,c+1).
# Column state s in {0,1,2}^m (colour w^{s_r}); W(s) = prod_r (w^{s_r}/3) prod_r (w^{s_r} - w^{s_{r+1}});
# R(s,t) = prod_r (w^{s_r} - w^{t_r}); T = diag(W) R (same T as W4).
# For a in {0,1,2}^m:  x_a(s) = W(s) w^{<a,s>}.  Then for l >= 2:
#   c_S(l) = x_{mu_1}^T R T^{l-2} x_{mu_l},   mu_1 / mu_l = multiplicities on the first / last column.
# Exact arithmetic in Q(omega) (flint fmpz_mat pairs). Output: one line per (l, S).
# Usage: python strip5.py lmin lmax [m]
import sys, itertools, time
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W7')
from fractions import Fraction as F
from tmlib import proper_states, W, Rf, mul, CUBE, ZWMat, ONE

def setup(m):
    S = proper_states(m)
    Ws = {s: W(s) for s in S}
    A = [a for a in itertools.product(range(3), repeat=m) if sum(a) <= m]
    def x(a, s):
        e = sum(ai * si for ai, si in zip(a, s)) % 3
        return mul(Ws[s], CUBE[e])
    X = ZWMat.from_entries([[x(a, s) for s in S] for a in A])          # |A| x 30
    R = ZWMat.from_entries([[Rf(s, t) for t in S] for s in S])
    T = ZWMat.from_entries([[mul(Ws[s], Rf(s, t)) for t in S] for s in S])
    XT = ZWMat(X.A0.transpose(), X.A1.transpose(), X.den)               # 30 x |A|
    return S, A, X, R, T, XT

def all_coeffs(m, lmin, lmax):
    S, A, X, R, T, XT = setup(m)
    L = X @ R
    out = {}
    cur = L                                   # L T^{l-2}
    for l in range(2, lmax + 1):
        if l >= lmin:
            M = cur @ XT
            for i, a in enumerate(A):
                for j, b in enumerate(A):
                    if sum(a) + sum(b) == m:
                        out[(l, a, b)] = M.entry(i, j)
        cur = cur @ T
    return A, out

if __name__ == '__main__':
    lmin, lmax = int(sys.argv[1]), int(sys.argv[2])
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    t0 = time.time()
    A, out = all_coeffs(m, lmin, lmax)
    print(f"# strip coefficients c_S, H = C{m} x P_l, l = {lmin}..{lmax}, method A (transfer, |A_v| = 3)")
    print("# columns: l mu_first(rows 0..m-1) mu_last(rows 0..m-1) c_S")
    bad = 0
    for (l, a, b), z in sorted(out.items()):
        if z[1] != 0 or z[0].denominator != 1:
            bad += 1
        print(l, ''.join(map(str, a)), ''.join(map(str, b)), z[0] if z[1] == 0 else f"{z[0]}+({z[1]})w")
    print(f"# non-integer values: {bad}; time {time.time()-t0:.1f}s")
