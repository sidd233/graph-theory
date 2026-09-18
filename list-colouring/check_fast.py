"""Reproduce the n=6 result with the fast test before trusting it."""
from fractions import Fraction
from sweep import classes, acyclic
from fast import survives
n = 6
pool = list(classes(n))
print(f"n={n}: {len(pool)} graphs, {sum(1 for a in pool if acyclic(a,n))} forests")
for lam in [Fraction(1), Fraction(4,5), Fraction(3,4), Fraction(2,3), Fraction(1,2)]:
    s = [a for a in pool if survives(a, n, lam.numerator, lam.denominator)]
    print(f"  lam={lam}: {len(s)} survive"
          f"   (all forests: {all(acyclic(a,n) for a in s)})")
