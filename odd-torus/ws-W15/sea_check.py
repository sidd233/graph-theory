"""Machine check of the general Sea Lemma construction (proof in the book): sum colouring
psi(i,j) = f(i) + g(j) on the sea, outside colours on defects not in T, X-colours on T.
Random seas X = {0,1,2} with random defects (outside colours from {3,4,5}); T chosen greedily to resolve
clashes (at most one per column, only defects with exactly one outside colour). When hypotheses (a)-(d)
hold, run the construction exactly as in the proof and verify the result. Run: python sea_check.py"""
import itertools, random
random.seed(7)
def proper_cycle(lists):
    n = len(lists)
    for first in lists[0]:
        col = [first]
        def go(j):
            if j == n: return col[0] != col[-1]
            for c in lists[j]:
                if c != col[-1]:
                    col.append(c)
                    if go(j + 1): return True
                    col.pop()
            return False
        if go(1): return list(col)
    return None
fs = [f for f in itertools.product(range(3), repeat=5) if all(f[i] != f[(i + 1) % 5] for i in range(5))]
checked = built = 0
for trial in range(4000):
    n = random.choice([5, 7, 9, 11]); X = {0, 1, 2}
    L = {(i, j): set(X) for i in range(5) for j in range(n)}
    for _ in range(random.randint(1, 2 * n)):
        v = (random.randrange(5), random.randrange(n)); k = random.choice([1, 1, 2])
        L[v] = set(random.sample(sorted(X), 3 - k)) | set(random.sample([3, 4, 5], k))
    D = [v for v in L if L[v] != X]
    O = {v: L[v] - X for v in D}
    nb = lambda v: [((v[0] + 1) % 5, v[1]), ((v[0] - 1) % 5, v[1]), (v[0], (v[1] + 1) % n), (v[0], (v[1] - 1) % n)]
    # greedy: colour defects with outside colours; on a clash move a defect with |O| = 1 into T if its column is free
    T = set(); cols_used = set(); c = {}
    ok = True
    for v in sorted(D):
        choices = [x for x in sorted(O[v]) if all(c.get(w) != x for w in nb(v) if w in c)]
        if choices: c[v] = choices[0]
        elif len(O[v]) == 1 and v[1] not in cols_used: T.add(v); cols_used.add(v[1])
        else: ok = False; break
    if not ok: continue
    checked += 1
    # construction from the proof
    phi = {v: (X - L[v]).pop() for v in T}
    done = False
    for f in fs:
        lists = []
        for j in range(n):
            vs = [v for v in T if v[1] == j]
            lists.append([x for x in range(3) if not vs or x != (phi[vs[0]] - f[vs[0][0]]) % 3])
        g = proper_cycle(lists)
        if g is None: continue
        psi = {(i, j): (f[i] + g[j]) % 3 for i in range(5) for j in range(n)}
        col = {v: (c[v] if v in c else psi[v]) for v in L}
        assert all(col[v] in L[v] for v in L), 'list violated'
        assert all(col[v] != col[w] for v in L for w in nb(v)), 'not proper'
        built += 1; done = True; break
    if not done:
        degenerate = len({v[1] for v in T}) == n and len({v[0] for v in T}) == 1 and len(set(phi.values())) == 1
        assert degenerate, ('construction failed outside the degenerate case', T)
print(f'instances satisfying (a)-(c): {checked}; colouring built and verified: {built}; failures outside case (d): 0')
