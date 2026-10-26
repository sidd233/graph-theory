# Cross-check: transfer-matrix formula (tmlib, exact over Q(omega)) vs orchestrator's direct coeff_mod (mod p).
# Usage: python crosscheck.py m n1,n2,...
import sys
sys.path.insert(0, '.')
from tmlib import build, powers, c_col, c_row
import orch_exactp as ox
m = int(sys.argv[1]); ns = [int(x) for x in sys.argv[2].split(',')]
p, wp = ox.p, ox.R[1]
def red(z):
    x, y = z
    return (x.numerator * pow(x.denominator, -1, p) + y.numerator * pow(y.denominator, -1, p) * wp) % p
B = build(m)
for n in ns:
    Tp = powers(B['T'], n)
    agree = dis = zero = 0
    for i in range(m):
        for j in range(1, n):          # column edge, w=(i,j), j != 0
            ex = c_col(B, i, j - 1, n - 1 - j, Tp)
            d = ox.coeff_mod(m, n, ('col', 0, 0), (i, j))
            agree += red(ex) == d; dis += red(ex) != d; zero += ex == (0, 0)
    for i in range(1, m):
        for j in range(n):             # row edge, w=(i,j), i != 0
            jj = j if j > 0 else n
            ex = c_row(B, i, jj - 1, n - jj, Tp)
            d = ox.coeff_mod(m, n, ('row', 0, 0), (i, j))
            agree += red(ex) == d; dis += red(ex) != d; zero += ex == (0, 0)
    print(f"m={m} n={n}: positions={agree+dis} agree={agree} disagree={dis} exact_zero={zero}", flush=True)
