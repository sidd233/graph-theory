"""W14 (Blocker 3b): coefficients for G' = C5 x Cn minus the 3x2 block (rows 1,2,3; columns 0,1).
Border: p1,p2,p3 = (1..3, n-1); q1 = (4,0), q2 = (0,0); r1 = (4,1), r2 = (0,1); s1,s2,s3 = (1..3, 2).
For an end weight mu on the border (sum 5, values 0..2), c_mu(n) = [prod x^(2-mu)] P_{G'} (up to a
nonzero constant) = sum over cube-root colourings phi of P(phi) prod phi(v)^(1+mu(v)).
Orientation: (r,c)->(r+1,c), (r,c)->(r,c+1). Transfer along columns 2,3,...,n-1,0,1:
  c_mu(n) = tr(K T^(n-4)),  T = D R (plain full columns),  K = [D_p R_fp][D_0 R_pp][D_1 R_pf][D_s R].
Exact arithmetic in Z[w] (w^2 = -1 - w). Prints, for each placement, whether c_mu(n) != 0 for all odd n
in 5..41, and saves the sequences. Run: python hole_coeff.py"""
import itertools, json
# Z[w] elements as (a, b) = a + b w
def mul(p, q): a, b = p; c, d = q; return (a * c - b * d, a * d + b * c - b * d)
def add(p, q): return (p[0] + q[0], p[1] + q[1])
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
W = [(1, 0), (0, 1), (-1, -1)]
ZERO = (0, 0); ONE = (1, 0)
def wpow(e): return W[e % 3]
def mmul(A, B):
    n, m, k = len(A), len(B), len(B[0])
    C = [[ZERO] * k for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for l in range(m):
            a = Ai[l]
            if a == ZERO: continue
            Bl = B[l]
            row = C[i]
            for j in range(k):
                b = Bl[j]
                if b != ZERO: row[j] = add(row[j], mul(a, b))
    return C
full = [s for s in itertools.product(range(3), repeat=5) if all(s[r] != s[(r + 1) % 5] for r in range(5))]
part = [(a, b) for a in range(3) for b in range(3) if a != b]          # (e4, e0)
def Dfull(mu):   # mu: dict row -> weight
    out = []
    for s in full:
        v = ONE
        for r in range(5): v = mul(v, sub(wpow(s[r]), wpow(s[(r + 1) % 5])))
        for r in range(5): v = mul(v, wpow(s[r] * (1 + mu.get(r, 0))))
        out.append(v)
    return out
def Dpart(m4, m0):
    out = []
    for (e4, e0) in part:
        v = sub(wpow(e4), wpow(e0))
        v = mul(v, wpow(e4 * (1 + m4))); v = mul(v, wpow(e0 * (1 + m0)))
        out.append(v)
    return out
def Rff():
    return [[(lambda s, t: _prod([sub(wpow(s[r]), wpow(t[r])) for r in range(5)]))(s, t) for t in full] for s in full]
def _prod(xs):
    v = ONE
    for x in xs: v = mul(v, x)
    return v
def Rfp(): return [[_prod([sub(wpow(s[4]), wpow(t[0])), sub(wpow(s[0]), wpow(t[1]))]) for t in part] for s in full]
def Rpp(): return [[_prod([sub(wpow(s[0]), wpow(t[0])), sub(wpow(s[1]), wpow(t[1]))]) for t in part] for s in part]
def Rpf(): return [[_prod([sub(wpow(s[0]), wpow(t[4])), sub(wpow(s[1]), wpow(t[0]))]) for t in full] for s in part]
def diag_left(D, M): return [[mul(D[i], M[i][j]) for j in range(len(M[0]))] for i in range(len(M))]
R = Rff(); RFP = Rfp(); RPP = Rpp(); RPF = Rpf()
T = diag_left(Dfull({}), R)
# powers T^k for k = 1, 3, 5, ..., 37 (n = 5, 7, ..., 41)
pw = {}
P = T; pw[1] = P
T2 = mmul(T, T)
for k in range(3, 38, 2):
    P = mmul(P, T2); pw[k] = P
def tr(A, B):   # trace(A B)
    s = ZERO
    for i in range(len(A)):
        for j in range(len(B)):
            if A[i][j] != ZERO and B[j][i] != ZERO: s = add(s, mul(A[i][j], B[j][i]))
    return s
border = ['p1', 'p2', 'p3', 'q1', 'q2', 'r1', 'r2', 's1', 's2', 's3']
adj = [('p1', 'p2'), ('p2', 'p3'), ('q1', 'q2'), ('r1', 'r2'), ('q1', 'r1'), ('q2', 'r2'), ('s1', 's2'), ('s2', 's3')]
results = {}
for units in itertools.product(range(3), repeat=10):
    if sum(units) != 5: continue
    u = dict(zip(border, units))
    if any(u[a] == 2 and u[b] == 2 for a, b in adj): continue
    Dp = Dfull({1: u['p1'], 2: u['p2'], 3: u['p3']}); Ds = Dfull({1: u['s1'], 2: u['s2'], 3: u['s3']})
    D0 = Dpart(u['q1'], u['q2']); D1 = Dpart(u['r1'], u['r2'])
    K = mmul(mmul(mmul(diag_left(Dp, RFP), diag_left(D0, RPP)), diag_left(D1, RPF)), diag_left(Ds, R))
    seq = [tr(K, pw[k]) for k in range(1, 38, 2)]          # n = 5, 7, ..., 41
    results[''.join(map(str, units))] = seq
nz = {k: all(v != ZERO for v in s) for k, s in results.items()}
print('placements:', len(results), '; nonzero for every odd n from 5 to 41:', sum(nz.values()))
json.dump({k: [list(v) for v in s] for k, s in results.items()}, open('hole_coeff.json', 'w'))
json.dump(nz, open('hole_nonzero.json', 'w'))
