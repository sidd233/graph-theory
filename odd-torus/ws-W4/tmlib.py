# W4 transfer-matrix library: exact construction over Z[omega] for C_m x C_n minus one edge.
#
# Conventions (identical to orchestrator coeff.py / exactp.py):
#   vertex (r, c), r in Z_m (row), c in Z_n (column);
#   column edges (r,c) -> (r+1,c), row edges (r,c) -> (r,c+1);
#   c_w = [x_w prod_{v != w} x_v^2] P_{G-e}
#       = sum over phi in {1,w,w^2}^V of  phi(w) * prod_v (phi(v)/3) * prod_{arcs u->v, != e} (phi(u)-phi(v))
#   (Lason / Karasev-Petrov with A_v = cube roots of unity, N_v(a) = 3/a, applied to x_w * P_{G-e}).
#
# Column state s = (s_0..s_{m-1}) with s_r in {0,1,2} meaning colour omega^{s_r}.
# Transfer matrices (rows: state of column c, cols: state of column c+1):
#   T[s,t]  = W(s) R(s,t),   W(s) = prod_r (s_r/3) prod_r (s_r - s_{r+1}),  R(s,t) = prod_r (s_r - t_r)
#   damaged column (edge e = ('col',0,0)): W_e(s) omits the r = 0 factor (s_0 - s_1).
#   damaged row step (edge e = ('row',0,0)): R_e(s,t) omits the r = 0 factor (s_0 - t_0).
# Exact elements of Q(omega) are pairs (x, y) of Fractions meaning x + y*omega.
#
# Formulas (derived in REPORT.md, Section "Setup"):
#   column edge, w = (i, j), 1 <= j <= n-1:  c = tr(G T^a D_i T^b), a = j-1, b = n-1-j  (a+b = n-2)
#       G = T' E, E[s,t] = W_e(s) R(s,t) (s damaged-proper, t proper), T'[s,t] = W(s) R(s,t) (s proper, t damaged-proper)
#   row edge, w = (i, j), i != 0, j = 1..n (j = n means column 0): c = tr(H T^a D_i T^b), a = j-1, b = n-j (a+b = n-1)
#       H[s,t] = W(s) R_e(s,t)
#   D_i = diag(omega^{s_i}).
from fractions import Fraction as F
import itertools
import flint

ONE = (F(1), F(0))
ZERO = (F(0), F(0))
CUBE = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(-1))]   # 1, w, w^2 = -1-w


def mul(p, q):
    a, b = p
    c, d = q
    # (a+bw)(c+dw) = ac + (ad+bc) w + bd w^2 = (ac-bd) + (ad+bc-bd) w
    return (a * c - b * d, a * d + b * c - b * d)


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def scal(p, k):
    return (p[0] * k, p[1] * k)


def proper_states(m, skip=None):
    """colourings s of C_m with s_r != s_{r+1} for all r except r = skip"""
    out = []
    for s in itertools.product(range(3), repeat=m):
        if all(s[r] != s[(r + 1) % m] for r in range(m) if r != skip):
            out.append(s)
    return out


def W(s, skip=None):
    m = len(s)
    v = ONE
    for r in range(m):
        v = mul(v, scal(CUBE[s[r]], F(1, 3)))
    for r in range(m):
        if r == skip:
            continue
        v = mul(v, sub(CUBE[s[r]], CUBE[s[(r + 1) % m]]))
    return v


def Rf(s, t, skip=None):
    v = ONE
    for r in range(len(s)):
        if r == skip:
            continue
        v = mul(v, sub(CUBE[s[r]], CUBE[t[r]]))
    return v


class ZWMat:
    """matrix over Q(omega): (A0 + A1*omega) / den with A0, A1 fmpz_mat, den positive int"""

    def __init__(self, A0, A1, den=1):
        self.A0, self.A1, self.den = A0, A1, den

    @staticmethod
    def from_entries(rows):
        nr, nc = len(rows), len(rows[0])
        den = 1
        for row in rows:
            for (x, y) in row:
                den = lcm(den, x.denominator, y.denominator)
        A0 = flint.fmpz_mat(nr, nc, [int(x * den) for row in rows for (x, y) in row])
        A1 = flint.fmpz_mat(nr, nc, [int(y * den) for row in rows for (x, y) in row])
        return ZWMat(A0, A1, den)

    def __matmul__(self, o):
        P = self.A0 * o.A0
        Q = self.A1 * o.A1
        C0 = P - Q
        C1 = self.A0 * o.A1 + self.A1 * o.A0 - Q
        return ZWMat(C0, C1, self.den * o.den)

    def nrows(self):
        return self.A0.nrows()

    def ncols(self):
        return self.A0.ncols()

    def trace(self):
        """exact trace as (Fraction, Fraction)"""
        t0 = sum(int(self.A0[k, k]) for k in range(self.A0.nrows()))
        t1 = sum(int(self.A1[k, k]) for k in range(self.A1.nrows()))
        return (F(t0, self.den), F(t1, self.den))

    def entry(self, i, j):
        return (F(int(self.A0[i, j]), self.den), F(int(self.A1[i, j]), self.den))

    def to_acb(self, prec_ctx=None):
        w = flint.acb(-0.5, 0) + flint.acb(0, 1) * flint.arb(3).sqrt() / 2
        nr, nc = self.nrows(), self.ncols()
        M = flint.acb_mat(nr, nc)
        for i in range(nr):
            for j in range(nc):
                M[i, j] = (flint.acb(int(self.A0[i, j])) + flint.acb(int(self.A1[i, j])) * w) / self.den
        return M


def lcm(*xs):
    from math import gcd
    r = 1
    for x in xs:
        r = r * x // gcd(r, x)
    return r


def build(m):
    S = proper_states(m)
    Se = proper_states(m, skip=0)
    Ws = {s: W(s) for s in Se}
    Wes = {s: W(s, skip=0) for s in Se}
    T = [[mul(Ws[s], Rf(s, t)) for t in S] for s in S]
    Tp = [[mul(Ws[s], Rf(s, t)) for t in Se] for s in S]
    E = [[mul(Wes[s], Rf(s, t)) for t in S] for s in Se]
    H = [[mul(Ws[s], Rf(s, t, skip=0)) for t in S] for s in S]
    Ds = []
    for i in range(m):
        Ds.append([[CUBE[s[i]] if s == t else ZERO for t in S] for s in S])
    out = dict(S=S, Se=Se,
               T=ZWMat.from_entries(T), Tp=ZWMat.from_entries(Tp), E=ZWMat.from_entries(E),
               H=ZWMat.from_entries(H), D=[ZWMat.from_entries(D) for D in Ds])
    out['G'] = out['Tp'] @ out['E']
    return out


def identity(k):
    A0 = flint.fmpz_mat(k, k)
    for i in range(k):
        A0[i, i] = 1
    return ZWMat(A0, flint.fmpz_mat(k, k), 1)


def powers(T, N):
    """list [T^0, ..., T^N] exactly"""
    out = [identity(T.nrows())]
    for _ in range(N):
        out.append(out[-1] @ T)
    return out


def c_col(B, i, a, b, Tp=None):
    Tp = Tp or powers(B['T'], a + b)
    return (B['G'] @ Tp[a] @ B['D'][i] @ Tp[b]).trace()


def c_row(B, i, a, b, Tp=None):
    Tp = Tp or powers(B['T'], a + b)
    return (B['H'] @ Tp[a] @ B['D'][i] @ Tp[b]).trace()


def fmt(z):
    return f"{z[0]} + ({z[1]})w"
