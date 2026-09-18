"""Why the refinement can never win.

A rounding gain exists exactly when  ceil(lam*d) < d, i.e. lam*d <= d-1, i.e.
        d >= 1/(1-lam).
A degree d is BAD (the method cannot handle one out-arc there) exactly when
        ceil(lam*d) == ceil(lam*(d-1)),
and the smallest bad degree turns out to be the same threshold.  So the moment
Delta+ is large enough for the refinement to buy anything, it is also large enough
to contain a vertex sitting at a bad out-degree, and a two-element colour class
{u, v} across an out-arc from such a u is unusable.  The gain and the obstruction
switch on together.
"""
from fractions import Fraction
GRID = sorted({Fraction(a, b) for b in range(2, 10) for a in range(1, b + 1)})
print(f"{'lam':>6} {'gain needs d >=':>16} {'smallest bad d':>16}  {'same?':>6}")
for lam in GRID:
    p, q = lam.numerator, lam.denominator
    if lam == 1:
        continue
    thr = Fraction(1, 1 - lam)
    gain_d = -(-thr.numerator // thr.denominator) if thr.denominator > 1 else int(thr) + 1
    gain_d = min(d for d in range(1, 200) if -((-p * d) // q) < d)
    bad_d = min((d for d in range(1, 200)
                 if -((-p * d) // q) == -((-p * (d - 1)) // q)), default=None)
    print(f"{str(lam):>6} {gain_d:>16} {str(bad_d):>16}  {str(gain_d == bad_d):>6}")
