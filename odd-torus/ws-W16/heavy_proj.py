"""Heavy seams: piecewise row-constant assignments (k blocks) where consecutive blocks differ by swapping one
colour in some rows. How often is the colour graph K(L) 3-colourable (so Lemma 4.6 colours the torus)?
When it is not, does the triple construction still work? Run: python heavy_proj.py"""
import itertools, random
from seam_multi import triples, compat, cyclic_exists
def three_col(lists):
    cols = sorted(set().union(*lists)); adj = {c: set() for c in cols}
    for L in lists:
        for a, b in itertools.combinations(L, 2): adj[a].add(b); adj[b].add(a)
    col = {}
    def go(k):
        if k == len(cols): return True
        c = cols[k]
        for v in range(3):
            if all(col.get(d) != v for d in adj[c]):
                col[c] = v
                if go(k + 1): return True
                del col[c]
        return False
    return go(0)
random.seed(5)
stats = {'proj': 0, 'triples_only': 0, 'neither': 0}
for it in range(150):
    P = random.choice([4, 5, 6]); k = random.choice([2, 3, 4])
    blocks = [[frozenset(random.sample(range(P), 3)) for _ in range(5)]]
    for i in range(1, k):
        prev = blocks[-1]; nb = []
        for r in range(5):
            if random.random() < 0.3: nb.append(prev[r])
            else:
                keep = random.sample(sorted(prev[r]), 2); new = random.choice([c for c in range(P) if c not in prev[r]])
                nb.append(frozenset(keep + [new]))
        blocks.append(nb)
    alllists = [l for b in blocks for l in b]
    if three_col(alllists): stats['proj'] += 1; continue
    T = [triples(b)[:60] for b in blocks]
    if cyclic_exists(T): stats['triples_only'] += 1
    else: stats['neither'] += 1; print('NEITHER:', [[''.join(map(str, sorted(l))) for l in b] for b in blocks])
print(stats)
