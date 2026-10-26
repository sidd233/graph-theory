# Are the 12 kernel-perfect admissible orientations of C3 x C9 found by the old SAT code
# (odd-torus/kernel_torus.py --all) exactly the 12 Latin lifts (orch/latin_lift.py)?
# Input: the "arcs" lines of kernel_torus.py output (vertex (i,j) printed as "ij", arc "ij>i'j'").
# Run: ../env/bin/python ../kernel_torus.py 3 9 --all | ../env/bin/python kp39_are_lifts.py
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "orch"))
from latin_lift import latin_squares, column_arcs, row_arcs

n = 9
found = set()
for line in sys.stdin:
    if line.strip().startswith("arcs"):
        arcs = []
        for tok in line.split(":", 1)[1].split():
            a, b = tok.split(">")
            arcs.append(((int(a[0]), int(a[1:])), (int(b[0]), int(b[1:]))))
        found.add(frozenset(arcs))

lifts = set()
for L in latin_squares():
    arcs = set()
    for j in range(n):
        for (r, s) in column_arcs(L[j % 3]):
            arcs.add(((r, j), (s, j)))
        ra = row_arcs(L[j % 3], L[(j + 1) % 3])
        for r in range(3):
            u, v = (r, j), (r, (j + 1) % n)
            arcs.add((u, v) if ra[r] == +1 else (v, u))
    lifts.add(frozenset(arcs))

print(f"old SAT code: {len(found)} kernel-perfect orientations; Latin lifts: {len(lifts)}; "
      f"equal sets: {found == lifts}")
