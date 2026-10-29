"""W10: what do non-colourable fills of the pentagonal prism C5 x K2 look like?
u-cycle u0..u4, v-cycle v0..v4, rungs u_t v_t. Lists: |L(u0)| = 3, all others 2.
Random sampling over small palettes; prints failure rate and a classification of failures by
(how many v-lists are equal to the most common v-list, same for u-lists).
Run: python prism5_sample.py"""
import random, itertools
from collections import Counter
def colourable(U, V):
    order = [('u', t) for t in range(5)] + [('v', t) for t in range(5)]
    col = {}
    def nb(s, t):
        o = 'v' if s == 'u' else 'u'
        return ((s, (t + 1) % 5), (s, (t - 1) % 5), (o, t))
    def go(i):
        if i == 10: return True
        s, t = order[i]
        for c in (U if s == 'u' else V)[t]:
            if all(col.get(w) != c for w in nb(s, t)):
                col[(s, t)] = c
                if go(i + 1): return True
                del col[(s, t)]
        return False
    return go(0)
random.seed(3)
for P in (3, 4, 5, 6):
    fails = []; N = 40000
    for _ in range(N):
        U = [frozenset(random.sample(range(P), 3))] + [frozenset(random.sample(range(P), 2)) for _ in range(4)]
        V = [frozenset(random.sample(range(P), 2)) for _ in range(5)]
        if not colourable(U, V): fails.append((U, V))
    print(f'palette {P}: {len(fails)} of {N} fail')
    C = Counter()
    for U, V in fails:
        cv = Counter(V).most_common(1)[0][1]; cu = Counter(U[1:]).most_common(1)[0][1]
        allv = len(set().union(*V)); allu = len(set().union(*U))
        C[(cv, cu, allv)] += 1
    print('   (max equal v-lists, max equal u-lists among u1..u4, colours used on v):', dict(C.most_common(8)))
