"""Seam Lemma, heavy overlap. Two blocks with row lists A_r, B_r (cyclic: two seams). Triples for a block =
colourings of C3 x C5 with row lists (three pairwise compatible column colourings). Check: is there a
triple for each block such that BOTH seams (A->B and B->A) have a compatible pair?
Lists drawn with heavy overlap: each B_r equals A_r, or shares two colours with it. Run: python seam_test.py"""
import itertools, random
def colcols(lists):          # proper colourings of the 5-cycle from row lists
    return [c for c in itertools.product(*[sorted(l) for l in lists]) if all(c[r] != c[(r + 1) % 5] for r in range(5))]
compat = lambda p, q: all(p[r] != q[r] for r in range(5))
def triples(lists):
    cs = colcols(lists); out = []
    for i, x in enumerate(cs):
        for j in range(i + 1, len(cs)):
            y = cs[j]
            if not compat(x, y): continue
            for k in range(j + 1, len(cs)):
                z = cs[k]
                if compat(x, z) and compat(y, z): out.append((x, y, z))
    return out
random.seed(3)
tot = fail = 0; heavy = 0
for it in range(400):
    P = random.choice([4, 5, 6])
    A = [frozenset(random.sample(range(P), 3)) for _ in range(5)]
    B = []
    for r in range(5):
        if random.random() < 0.5: B.append(A[r])
        else:
            keep = random.sample(sorted(A[r]), 2); new = random.choice([c for c in range(P) if c not in A[r]] or [None])
            B.append(frozenset(keep + [new]) if new is not None else A[r])
    if A == B: continue
    ov = sum(len(a & b) for a, b in zip(A, B))
    if ov < 9: continue
    heavy += 1
    TA, TB = triples(A), triples(B)
    assert TA and TB
    ok = any(any(compat(p, q) for p in ta for q in tb) and any(compat(q, p) for q in tb for p in ta) for ta in TA for tb in TB)
    tot += 1
    if not ok:
        fail += 1
        if fail <= 3: print('FAIL A', [sorted(a) for a in A], 'B', [sorted(b) for b in B])
print(f'heavy-overlap two-block seams tested: {tot}; triple construction fails: {fail}')
