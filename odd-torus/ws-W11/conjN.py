"""Test Conjecture N on every known bad (window, alpha): there is a 3-set X with
(i) every list of C1 and C2 sharing >= 2 colours with X, and (ii) >= 3 rows of C2 equal to X.
Run: python conjN.py FILE..."""
import sys, itertools
pc = lambda x: bin(x).count('1')
def holds(L1, L2):
    cols = 0
    for x in L1 + L2: cols |= x
    for X in (sum(1 << c for c in t) for t in itertools.combinations([c for c in range(16) if cols >> c & 1], 3)):
        if all(pc(l & X) >= 2 for l in L1 + L2) and sum(l == X for l in L2) >= 3: return True
    return False
tot = bad = 0
for f in sys.argv[1:]:
    for l in open(f):
        if not l.startswith('BADA'): continue
        w = l.split(); L1 = [int(h, 16) for h in w[3:8]]; L2 = [int(h, 16) for h in w[9:14]]
        tot += 1
        if not holds(L1, L2): bad += 1; print('VIOLATES N:', l.strip())
print(f'{tot} bad (window, alpha) pairs; {bad} violate Conjecture N')
