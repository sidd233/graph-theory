"""Exact checks of the individual steps of the PROVED derivation in REPORT.md (not a substitute
for the proof; a guard against algebra slips). States: phi(r) = w^(a + e r), a in Z3, e in {+1,-1}."""
import itertools
from zomega import Z, wpow, ISQ3

g = Z(3) * ISQ3
# Step 1: the proper colourings of a triangle by cube roots are exactly the 6 affine maps r -> a + e r
proper = [p for p in itertools.product(range(3), repeat=3) if len(set(p)) == 3]
affine = sorted({tuple((a + e * r) % 3 for r in range(3)) for a in range(3) for e in (1, -1)})
assert sorted(proper) == affine and len(affine) == 6
# Step 2: column product prod_r (phi(r) - phi(r+1)) = -e g, independent of a
for a in range(3):
    for e in (1, -1):
        d = Z(1)
        for r in range(3):
            d = d * (wpow(a + e * r) - wpow(a + e * (r + 1)))
        assert d == Z(-e) * g
# Step 3: row product prod_r (phi(r) - psi(r)) is 0 if slopes differ, g*chi(b-a) if equal,
#         chi(0) = 0, chi(1) = -1, chi(2) = +1
chi = {0: 0, 1: -1, 2: 1}
for a, b in itertools.product(range(3), repeat=2):
    for e, f in itertools.product((1, -1), repeat=2):
        p = Z(1)
        for r in range(3):
            p = p * (wpow(a + e * r) - wpow(b + f * r))
        assert p == (Z(0) if e != f else g * Z(chi[(b - a) % 3])), (a, b, e, f)
# Step 4: vertex weights prod_r phi(r)^(1 + mu_r) = w^(a M + e R), M = sum mu_r, R = sum r mu_r
for mus in itertools.product(range(3), repeat=3):
    M = sum(mus); R = sum(r * x for r, x in enumerate(mus))
    for a in range(3):
        for e in (1, -1):
            p = Z(1)
            for r in range(3):
                p = p * wpow((a + e * r) * (1 + mus[r]))
            assert p == wpow(a * M + e * R)
# Step 5: sum_d chi(d) w^(k d) = w^(2k) - w^k = mu_k; and g^2 = -27, 1/g = -g/27
for k in range(4):
    assert sum((Z(chi[d]) * wpow(k * d) for d in range(3)), Z(0)) == wpow(2 * k) - wpow(k)
assert g * g == Z(-27) and g.inv() == -g * Z(__import__("fractions").Fraction(1, 27))
print("all proof step checks passed")
