"""Independent re-check of window5g.c verdicts WITH all 74 shapes (palette 4, real alpha).
Plain Python brute force, sharing no code with the C programs.
Samples windows the C code calls GOOD (with shapes) and windows it calls BAD. Run: python validate_shapes.py N"""
import itertools, random, sys
N = int(sys.argv[1]); random.seed(11)
shapes = [l.split() for l in open('shapes5.txt').read().split('\n')[1:] if l.strip()]
def colourable(A, B):
    order = [('u', t) for t in range(5)] + [('v', t) for t in range(5)]; col = {}
    def nb(s, t):
        o = 'v' if s == 'u' else 'u'
        return ((s, (t + 1) % 5), (s, (t - 1) % 5), (o, t))
    def go(i):
        if i == 10: return True
        s, t = order[i]
        for c in sorted((A if s == 'u' else B)[t]):
            if all(col.get(w) != c for w in nb(s, t)):
                col[(s, t)] = c
                if go(i + 1): return True
                del col[(s, t)]
        return False
    return go(0)
def verdict(L1, L2, alpha):
    X = []
    for x in itertools.product(*[sorted(L1[t]) + [None] for t in range(1, 5)]):
        x = (None,) + x
        if any(x[t] is not None and x[t] == x[t + 1] for t in range(1, 4)): continue
        if x[1] == alpha or x[4] == alpha: continue
        X.append(x)
    Y = [y for y in itertools.product(*[sorted(L2[t]) + [None] for t in range(5)])
         if all(y[t] is None or y[t] != y[(t + 1) % 5] for t in range(5))]
    red = lambda L, z: [L[t] - {z[t]} for t in range(5)]
    fails = [(x, y) for x in X for y in Y if not colourable(red(L1, x), red(L2, y))]
    if not fails: return True
    for c0, c3 in shapes:
        rows = [(0, t) for t in range(1, 5) if c0[t] == '1'] + [(1, t) for t in range(5) if c3[t] == '1']
        for cols in itertools.product(*[sorted((L2 if side else L1)[t]) for side, t in rows]):
            if all(any(((y if side else x)[t]) == c for (side, t), c in zip(rows, cols)) for x, y in fails):
                return True
    return False
good = [l.split() for l in open('all_q4_bad.txt') if l.startswith('BAD')]          # plan-bad windows (most are good with shapes)
badset = {tuple(l.split()[1:6] + l.split()[7:12]) for l in open('all_q4_stillbad_real.txt')}
cands = [w for w in good]
random.shuffle(cands)
agree = disagree = 0; nb = ng = 0
for w in cands:
    key = tuple(w[2:7] + w[8:13])
    L1 = [frozenset(c for c in range(4) if int(h, 16) >> c & 1) for h in w[2:7]]
    L2 = [frozenset(c for c in range(4) if int(h, 16) >> c & 1) for h in w[8:13]]
    alpha = next(c for c in range(4) if c not in L1[0])
    c_says_bad = key in badset
    if c_says_bad and nb >= N // 2: continue
    if not c_says_bad and ng >= N - N // 2: continue
    v = verdict(L1, L2, alpha)
    if v == (not c_says_bad): agree += 1
    else: disagree += 1; print('DISAGREE', w, 'C says bad' if c_says_bad else 'C says good')
    if c_says_bad: nb += 1
    else: ng += 1
    if nb + ng >= N: break
print(f'checked {nb} C-bad and {ng} C-good windows: {agree} agree, {disagree} disagree')
