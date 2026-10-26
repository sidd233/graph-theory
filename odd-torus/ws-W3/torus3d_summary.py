"""Summarise torus3d_upto9.txt against simple arithmetic rules and the a = 3 theorem.
Run: python torus3d_summary.py > torus3d_summary.txt"""
from math import gcd
rows = []
for line in open("torus3d_upto9.txt"):
    p = line.split()
    if len(p) > 4 and p[0].isdigit():
        rows.append((int(p[0]), int(p[1]), int(p[2]), "YES" in line))
g3 = lambda a, b, c: gcd(gcd(a, b), c)
pair = lambda a, b, c: max(gcd(a, b), gcd(a, c), gcd(b, c)) > 1
print("total triples:", len(rows), " with kernel:", sum(r[3] for r in rows))
print("kernel although gcd(a,b,c) = 1:", [(a, b, c) for a, b, c, s in rows if s and g3(a, b, c) == 1])
print("no kernel although some pairwise gcd > 1:", [(a, b, c) for a, b, c, s in rows if not s and pair(a, b, c)])
print("kernel with all pairwise gcds = 1:", [(a, b, c) for a, b, c, s in rows if s and not pair(a, b, c)])
print("a = 3 rows agree with 'kernel iff 3 | b or 3 | c':",
      all(s == (b % 3 == 0 or c % 3 == 0) for a, b, c, s in rows if a == 3))
print("no kernel, all entries >= 4:", [(a, b, c) for a, b, c, s in rows if not s and a >= 4])
