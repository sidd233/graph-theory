"""Checks every step of the odd strip lemma (m = 3) in the book, with its orientation:
column edges (i,c)->(i+1,c), row edges (i,c)->(i,c+1); rows i in Z3, columns c = 1..l.
Exact arithmetic in Z[w], w a primitive cube root of unity: (x, y) means x + y*w.
(1) Steps 2 and 3: column factor = (1 - w^e)^3 = -e*g and row factor = g*chi(b - a), g = 3(w - w^2).
(2) Formula (*): c_mu = 3^(-3l) * sum over column-proper colourings of P(a) prod a_v^(1 + mu(v)),
    compared with the closed form 3^(1-3l) g^(2l-1) (w^(2s) - w^s) (w^(2k) - w^k)^(l-1) and with +-3^((l-1)/2).
(3) For l = 3, c_mu is also read off directly from the expanded graph polynomial (sympy)."""
import itertools, sympy
def mul(p, q): return (p[0]*q[0] - p[1]*q[1], p[0]*q[1] + p[1]*q[0] - p[1]*q[1])
def add(p, q): return (p[0] + q[0], p[1] + q[1])
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
W = [(1, 0), (0, 1), (-1, -1)]                       # w^0, w^1, w^2
wp = lambda e: W[e % 3]
def pw(p, n):
    r = (1, 0)
    for _ in range(n): r = mul(r, p)
    return r
g = mul((3, 0), sub(wp(1), wp(2)))
chi = {0: 0, 1: -1, 2: 1}
for e in (1, -1):
    assert pw(sub((1, 0), wp(e)), 3) == mul((-e, 0), g)
    for a in range(3):
        col = (1, 0)
        for i in range(3): col = mul(col, sub(wp(a + e*i), wp(a + e*(i + 1))))
        assert col == mul((-e, 0), g)
        for b in range(3):
            row = (1, 0)
            for i in range(3): row = mul(row, sub(wp(a + e*i), wp(b + e*i)))
            assert row == mul((chi[(b - a) % 3], 0), g)
            row = (1, 0)
            for i in range(3): row = mul(row, sub(wp(a + e*i), wp(b - e*i)))
            assert row == (0, 0)                     # opposite epsilons: some row has equal colours
print('Steps 2 and 3: column and row factors agree with -e*g and g*chi (all a, b, e)')
pats = [(a, e) for a in range(3) for e in (1, -1)]
def coef_by_sum(l, mu):
    tot = (0, 0)
    for cols in itertools.product(pats, repeat=l):
        ex = {(i, c): cols[c][0] + cols[c][1]*i for i in range(3) for c in range(l)}
        val = (1, 0)
        for c in range(l):
            for i in range(3): val = mul(val, sub(wp(ex[i, c]), wp(ex[(i + 1) % 3, c])))
            if c < l - 1:
                for i in range(3): val = mul(val, sub(wp(ex[i, c]), wp(ex[i, c + 1])))
            if val == (0, 0): break
        if val == (0, 0): continue
        val = mul(val, wp(sum(ex[v]*(1 + mu.get(v, 0)) for v in ex)))
        tot = add(tot, val)
    assert tot[1] == 0 and tot[0] % 3**(3*l) == 0
    return tot[0] // 3**(3*l)
def closed(l, s, k):
    v = mul(pw(g, 2*l - 1), mul(sub(wp(2*s), wp(s)), pw(sub(wp(2*k), wp(k)), l - 1)))
    v = mul((3, 0), v)
    assert v[1] == 0 and v[0] % 3**(3*l) == 0
    return v[0] // 3**(3*l)
for l in (3, 5, 7):
    for r, r2, two_first in itertools.product(range(3), range(3), (True, False)):
        if r == r2: continue
        mu = {(r, 0): 2, (r2, l - 1): 1} if two_first else {(r, 0): 1, (r2, l - 1): 2}
        k = 1 if two_first else 2
        s = sum(m*i for (i, c), m in mu.items()) % 3
        c1 = coef_by_sum(l, mu)
        assert c1 == closed(l, s, k) and abs(c1) == 3**((l - 1)//2), (l, mu, c1)
    print(f'l = {l}: all 12 shapes give c_mu = closed form = +-3^{(l-1)//2}')
l = 3
x = {(i, c): sympy.Symbol(f'x{i}{c}') for i in range(3) for c in range(l)}
P = sympy.Integer(1)
for c in range(l):
    for i in range(3):
        P *= x[i, c] - x[(i + 1) % 3, c]
        if c < l - 1: P *= x[i, c] - x[i, c + 1]
poly = sympy.Poly(sympy.expand(P), *x.values())
for r, r2 in itertools.permutations(range(3), 2):
    mu = {(r, 0): 2, (r2, l - 1): 1}
    mono = tuple(2 - mu.get(v, 0) for v in x)
    assert poly.coeff_monomial(mono) == coef_by_sum(l, mu)
print('l = 3: coefficient read directly from the expanded polynomial equals formula (*)')
