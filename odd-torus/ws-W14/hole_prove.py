"""Prove c_mu(n) != 0 for every odd n >= 5, for each placement mu with c_mu(n) != 0 for n = 5..41.
c_mu(2j+5) = tr(K T^(2j+1)); T h1(T^2) h2(T^2) = 0 (W4, E2) so the real part a_j and the w-part b_j of
c_mu(2j+5) = a_j + b_j w each satisfy the order-6 recurrence H = h1 h2 for j >= 0. For one part that is
not identically zero: minimal recurrence over Q is h1, h2 or h1h2 (found exactly from 19 terms, rigorous
since 19 - 6 >= 6); all its roots have nonzero amplitude; certified dominance gives j0; check j < j0 exactly.
Run: python hole_prove.py"""
import json, flint
# my T = 3^5 * T_W4 (no 1/3 vertex factors), so roots in y = x^2 scale by c2 = 243^2
c2 = 243 ** 2
h1 = [5 * c2 ** 2, 10 * c2, 1]; h2 = [25 * c2 ** 4, 100 * c2 ** 3, 110 * c2 ** 2, 35 * c2, 1]
H = [0] * 7
for i, x in enumerate(h1):
    for j, y in enumerate(h2): H[i + j] += x * y
ann = lambda r, s: all(sum(r[k] * s[i + k] for k in range(len(r))) == 0 for i in range(len(s) - len(r) + 1))
flint.ctx.prec = 200
def roots(p):
    out = []
    for z, m in flint.fmpz_poly(p).complex_roots():
        assert m == 1 and z.imag.contains(0); out.append(z.real)
    return sorted(out, key=lambda y: -abs(y))
data = json.load(open('hole_coeff.json')); nz = json.load(open('hole_nonzero.json'))
proved = 0; bad = []
for key, seq in data.items():
    if not nz[key]: continue
    a = [v[0] for v in seq]; b = [v[1] for v in seq]
    assert ann(H, a) and ann(H, b), key
    ok = False
    for part in (a, b):
        if not any(part): continue
        r = next(p for p in (h1, h2, H) if ann(p, part))
        ys = roots(r); d = len(ys)
        assert all(abs(ys[0]) > abs(y) for y in ys[1:])
        M = flint.arb_mat([[ys[i] ** j for i in range(d)] for j in range(d)])
        beta = M.solve(flint.arb_mat([[part[j]] for j in range(d)]))
        b0 = beta[0, 0]
        if b0.contains(0): continue
        j0 = 0
        while not (abs(b0) > sum((abs(beta[i, 0]) * (abs(ys[i]) / abs(ys[0])) ** j0 for i in range(1, d)), flint.arb(0))):
            j0 += 1
        if j0 <= len(part) and all(part[j] != 0 for j in range(j0)):
            ok = True; break
    if ok: proved += 1
    else: bad.append(key)
print('placements proved nonzero for every odd n >= 5:', proved, '; not proved:', len(bad))
json.dump(sorted(set(k for k, v in nz.items() if v) - set(bad)), open('hole_proved.json', 'w'))
