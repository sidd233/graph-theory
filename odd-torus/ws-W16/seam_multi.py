"""Seam Lemma, k blocks (cyclic). Each block i has row lists A^i (5 rows). Choose one triple per block
(a colouring of C3 x C5 from the block's row lists); need a compatible pair at every seam i|i+1.
Exact search: for each block enumerate all triples; dynamic programming around the cycle.
Lists: heavy overlap between consecutive blocks. Run: python seam_multi.py"""
import itertools, random
def colcols(lists):
    return [c for c in itertools.product(*[sorted(l) for l in lists]) if all(c[r] != c[(r + 1) % 5] for r in range(5))]
compat = lambda p, q: all(p[r] != q[r] for r in range(5))
def triples(lists):
    cs = colcols(lists); out = []
    for i, x in enumerate(cs):
        for j in range(i + 1, len(cs)):
            if not compat(x, cs[j]): continue
            for k in range(j + 1, len(cs)):
                if compat(x, cs[k]) and compat(cs[j], cs[k]): out.append((x, cs[j], cs[k]))
    return out
def ok_pair(ta, tb): return any(compat(p, q) for p in ta for q in tb)
def cyclic_exists(T):
    k = len(T)
    for t0 in range(len(T[0])):
        reach = {t0}
        for i in range(1, k):
            reach = {b for b in range(len(T[i])) if any(ok_pair(T[i - 1][a], T[i][b]) for a in reach)}
            if not reach: break
        if any(ok_pair(T[k - 1][b], T[0][t0]) for b in reach): return True
    return False
random.seed(9)
for k in (3, 4):
    tot = fail = 0
    for it in range(60):
        P = random.choice([4, 5])
        blocks = [[frozenset(random.sample(range(P), 3)) for _ in range(5)]]
        for i in range(1, k):
            prev = blocks[-1]; nb = []
            for r in range(5):
                if random.random() < 0.6: nb.append(prev[r])
                else:
                    keep = random.sample(sorted(prev[r]), 2); new = random.choice([c for c in range(P) if c not in prev[r]])
                    nb.append(frozenset(keep + [new]))
            blocks.append(nb)
        T = [triples(b) for b in blocks]
        T = [t[:60] for t in T]                     # cap for speed (a subset: a found solution is still valid)
        tot += 1
        if not cyclic_exists(T):
            fail += 1
            if fail <= 2: print(f'k={k} NOT FOUND (with capped triples):', [[ ''.join(map(str,sorted(l))) for l in b] for b in blocks])
    print(f'k = {k} blocks: {tot} tests, construction not found in {fail}')
