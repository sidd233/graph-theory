"""Three-column cut on nearly constant windows: all 15 lists are {0,1,2} except at most K of them,
which are arbitrary 3-subsets of a palette of P colours. Pin only (no forbidden colours).
Run: python cut3_nearconst.py K P"""
import itertools, sys
from cut3 import window_bad_pairs
K, P = int(sys.argv[1]), int(sys.argv[2])
base = frozenset({0, 1, 2})
subs = [frozenset(s) for s in itertools.combinations(range(P), 3) if frozenset(s) != base]
tot = bad = 0; examples = []
for pos in itertools.combinations(range(15), K):
    for vals in itertools.product(subs, repeat=K):
        L = [base] * 15
        for p, v in zip(pos, vals): L[p] = v
        A, B, D = L[0:5], L[5:10], L[10:15]
        tot += 1
        if window_bad_pairs(A, B, D):
            bad += 1
            if len(examples) < 6: examples.append((pos, [sorted(v) for v in vals]))
print(f'K = {K}, palette {P}: {tot} windows, {bad} bad (pin only)')
for e in examples: print('   changed positions (C1 = 0..4, C2 = 5..9, C3 = 10..14):', e)
