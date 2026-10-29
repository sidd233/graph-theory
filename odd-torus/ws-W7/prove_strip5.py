"""W7: odd strip lemma for m = 5, every odd length, for the 74 shapes of ws-W8/shapes5.txt (both
orientations). Computer-assisted proof; every step exact or certified (arb ball arithmetic).

Setup (W7/strip5.py): c_S(l) = u^T T^(l-2) v with T the 30x30 transfer matrix of W4. W4 (E2) proves
T q1(T) q2(T) = 0 with q1 = h1(x^2), q2 = h2(x^2),
    h1(y) = y^2 + 10y + 5,   h2(y) = y^4 + 35y^3 + 110y^2 + 100y + 25   (both irreducible over Q).
For odd l = 2j+1 (j >= 1): s_j := c_S(2j+1) = u^T T (T^2)^(j-1) v, and T h1(T^2) h2(T^2) = 0, so
(s_j) satisfies the order-6 recurrence with characteristic polynomial H = h1*h2, for all j >= 1.

Proof for one shape:
 (1) Check exactly that s_1..s_13 (l = 3..27, from strip5_A_l2-27.txt) satisfy the H-recurrence
     (sanity check of the data against W4).
 (2) Minimal polynomial r of (s_j) over Q divides H, so r is 1, h1, h2 or h1*h2. Find the least one
     annihilating s_1..s_13. Rigour: if r annihilates 13 terms, t = r(E)s satisfies the H-recurrence
     and vanishes on 13 - deg r >= 7 >= 6 consecutive terms, so t = 0. r = 1 would mean s = 0.
 (3) r has simple roots (H squarefree). Minimality over Q is also minimality over C (the minimal
     recurrence is found by linear algebra over the field of the terms), so every root of r has a
     nonzero amplitude: s_j = sum_i beta_i y_i^j with all beta_i != 0.
 (4) Certify (arb) that the root y1 of r of largest modulus is unique, compute beta_i by solving the
     Vandermonde system, and find j0 with |beta1| > sum_{i>=2} |beta_i| (|y_i|/|y1|)^j0. Since every
     ratio is < 1, s_j != 0 for all j >= j0.
 (5) Check s_j != 0 exactly for 1 <= j < j0 (data up to j = 13; must have j0 <= 14).
Run: python prove_strip5.py
"""
from collections import defaultdict
from fractions import Fraction
import flint

h1 = [5, 10, 1]                     # coefficients, low degree first
h2 = [25, 100, 110, 35, 1]
def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    return out
H = pmul(h1, h2)
def annihilates(r, s):              # sum_k r_k s_{j+k} = 0 for all j where defined
    d = len(r) - 1
    return all(sum(r[k] * s[j + k] for k in range(d + 1)) == 0 for j in range(len(s) - d))

D = defaultdict(dict)
for line in open('/home/sid/work/gt/odd-torus/ws-W7/strip5_A_l2-27.txt'):
    if line.startswith('#'): continue
    l, a, b, v = line.split(); D[(a, b)][int(l)] = int(v)
shapes = [l.split() for l in open('/home/sid/work/gt/odd-torus/ws-W8/shapes5.txt').read().split('\n')[1:] if l.strip()]

flint.ctx.prec = 200
def roots(p):
    out = []
    for z, mult in flint.fmpz_poly(p).complex_roots():
        assert mult == 1 and z.imag.contains(0)          # simple, real (W4, E4): imag ball is exactly 0
        out.append(z.real)
    return out

ok_all = True; summary = defaultdict(int); j0max = 0
for c0, c3 in shapes:
    for key in ((c3, c0), (c0, c3)):                 # both orientations of the strip
        s = [D[key][2 * j + 1] for j in range(1, 14)]            # s_1..s_13
        assert annihilates(H, s), ('H-recurrence fails', key)
        r = next((p for p in (h1, h2, H) if annihilates(p, s)), None)
        assert r is not None and any(s), key
        ys = roots(r)
        ys.sort(key=lambda y: -abs(y))
        assert all(abs(ys[0]) > abs(y) for y in ys[1:]), 'dominant root not unique'
        d = len(ys)
        # amplitudes: sum_i beta_i y_i^j = s_j, j = 1..d
        M = flint.arb_mat([[ys[i] ** j for i in range(d)] for j in range(1, d + 1)])
        beta = M.solve(flint.arb_mat([[s[j - 1]] for j in range(1, d + 1)]))
        b = [beta[i, 0] for i in range(d)]
        assert not b[0].contains(0), 'dominant amplitude not certified nonzero'
        j0 = 1
        while not (abs(b[0]) > sum((abs(b[i]) * (abs(ys[i]) / abs(ys[0])) ** j0 for i in range(1, d)), flint.arb(0))):
            j0 += 1
        assert all(s[j - 1] != 0 for j in range(1, min(j0, 14))) and j0 <= 14, (key, j0)
        j0max = max(j0max, j0)
        summary['h1' if r == h1 else 'h2' if r == h2 else 'h1*h2'] += 1
print('shapes x orientations proved:', sum(summary.values()), dict(summary))
print('largest j0 needed:', j0max, '(exact nonzero check covers 1 <= j < j0, i.e. l = 3 ..', 2 * j0max - 1, ')')
print('RESULT: c_S(l) != 0 for every odd l >= 3, for all 74 shapes in both orientations')
