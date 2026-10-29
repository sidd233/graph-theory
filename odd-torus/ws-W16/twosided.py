"""Two-sided pair lemma test: lists B (middle block), fixed triples T (from lists A) and T' (from lists A').
Is there a triple of B with a pattern compatible with some pattern of T, and a pattern compatible with some
pattern of T' ? Also the one-sided version. Run: python twosided.py"""
import itertools, random
from seam_multi import colcols, compat, triples
random.seed(21)
one_fail = two_fail = tot = 0
for it in range(400):
    P = random.choice([4, 5, 6])
    mk = lambda: [frozenset(random.sample(range(P), 3)) for _ in range(5)]
    B = mk()
    def near(L):
        out = []
        for r in range(5):
            if random.random() < 0.5: out.append(L[r])
            else:
                keep = random.sample(sorted(L[r]), 2); new = random.choice([c for c in range(P) if c not in L[r]])
                out.append(frozenset(keep + [new]))
        return out
    A, A2 = near(B), near(B)
    TA, TA2, TB = triples(A), triples(A2), triples(B)
    T = random.choice(TA); T2 = random.choice(TA2)
    tot += 1
    one = any(any(compat(p, q) for p in T for q in tb) for tb in TB)
    two = any(any(compat(p, q) for p in T for q in tb) and any(compat(p, q) for p in T2 for q in tb) for tb in TB)
    one_fail += not one; two_fail += not two
    if not two and two_fail <= 2:
        print('TWO-SIDED FAILS: B', [''.join(map(str,sorted(l))) for l in B], 'T', T, "T'", T2)
print(f'{tot} tests: one-sided fails {one_fail}, two-sided fails {two_fail}')
