"""Hunt for bad three-column windows (pin only) with at most 2 fully rigid rows.
Rows are drawn 'partly rigid' on purpose (two or three of A_t, B_t, D_t equal), the hardest kind.
Run: python cut3_hunt.py P N SEED"""
import random, sys
from cut3 import window_bad_pairs
P, N, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(seed)
r3 = lambda: frozenset(random.sample(range(P), 3))
found = 0
for it in range(N):
    X = r3(); A = []; B = []; D = []
    for t in range(5):
        mode = random.choice(['XXX', 'XXY', 'XYX', 'YXX', 'XXX', 'XYZ'])
        Y = r3(); Z = r3(); m = {'X': X, 'Y': Y, 'Z': Z}
        A.append(m[mode[0]]); B.append(m[mode[1]]); D.append(m[mode[2]])
    rig = sum(A[t] == B[t] == D[t] for t in range(5))
    if rig > 2: continue
    if A[0] == X and random.random() < 0.5: A[0] = r3()
    if window_bad_pairs(A, B, D):
        found += 1
        print('BAD with', rig, 'fully rigid rows:', [sorted(a) for a in A], [sorted(b) for b in B], [sorted(d) for d in D], flush=True)
print(f'P={P}: {N} draws, {found} bad windows with <= 2 fully rigid rows')
