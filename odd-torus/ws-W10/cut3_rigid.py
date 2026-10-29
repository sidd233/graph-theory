"""Three-column cut, pin only: among nearly constant windows (palette 5, K changed lists), how many
fully rigid rows (A_t = B_t = D_t) do the bad ones have, and does every window with at most R
fully rigid rows come out good?  Run: python cut3_rigid.py K"""
import itertools, sys
from collections import Counter
from cut3 import window_bad_pairs
K = int(sys.argv[1]); P = 5
base = frozenset({0, 1, 2})
subs = [frozenset(s) for s in itertools.combinations(range(P), 3) if frozenset(s) != base]
bad_by = Counter(); all_by = Counter()
for pos in itertools.combinations(range(15), K):
    for vals in itertools.product(subs, repeat=K):
        L = [base] * 15
        for p, v in zip(pos, vals): L[p] = v
        A, B, D = L[0:5], L[5:10], L[10:15]
        rig = sum(A[t] == B[t] == D[t] for t in range(5))
        all_by[rig] += 1
        if window_bad_pairs(A, B, D): bad_by[rig] += 1
print(f'K = {K}: fully rigid rows -> (bad, total):', {r: (bad_by[r], all_by[r]) for r in sorted(all_by)})
