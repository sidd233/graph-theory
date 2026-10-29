# Shapes for window5g: end weights (muC0, muC3) of the m = 5 strip with a pin (2) at row 0 of C0,
# every other entry 0 or 1, total 5, and c_S != 0 for EVERY odd strip length 3..27 (W7 data).
# The strip runs from C3 (first column) to C0 (last column); by the column-reflection symmetry
# zero-ness does not depend on which end is called first, and we use both orders to be safe.
from collections import defaultdict
D = defaultdict(dict)
for line in open('/home/sid/work/gt/odd-torus/ws-W7/strip5_A_l2-27.txt'):
    if line.startswith('#'): continue
    l, a, b, v = line.split(); D[(a, b)][int(l)] = int(v)
out = []
for (a, b), d in D.items():
    c0, c3 = b, a                      # first = C3 side, last = C0 side
    if c0[0] != '2' or any(ch not in '01' for ch in c0[1:] + c3): continue
    nz = all(d[l] != 0 for l in range(3, 28, 2))
    nz2 = all(D[(b, a)][l] != 0 for l in range(3, 28, 2)) if (b, a) in D else nz
    if nz and nz2: out.append((c0, c3))
print(len(out))
for c0, c3 in sorted(out): print(c0, c3)
