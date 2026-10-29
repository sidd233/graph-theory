"""W11: is C3 x Cn (n odd) colourable when every list has 3 colours except ONE vertex with 2?
(If yes, the folding lemma for C5 x Cn closes.) Exhaustive for C3 x C3 over a 4-colour palette,
random for C3 x C5 and C3 x C7. Run: python one_short.py"""
import itertools, random
from pysat.solvers import Solver
def graph(n):
    V = [(i, j) for i in range(3) for j in range(n)]
    E = [((i, j), ((i + 1) % 3, j)) for i in range(3) for j in range(n)] + \
        [((i, j), (i, (j + 1) % n)) for i in range(3) for j in range(n)]
    return V, E
def colourable(V, E, L):
    S = Solver(name='glucose4'); idx = {}; k = 0
    for v in V:
        lits = []
        for c in L[v]: k += 1; idx[(v, c)] = k; lits.append(k)
        S.add_clause(lits)
    for u, v in E:
        for c in L[u]:
            if (v, c) in idx: S.add_clause([-idx[(u, c)], -idx[(v, c)]])
    r = S.solve(); S.delete(); return r
# exhaustive C3 x C3, palette 4, short vertex = (0,0) (all vertices are equivalent by symmetry)
V, E = graph(3)
trip = [frozenset(t) for t in itertools.combinations(range(4), 3)]
pair = [frozenset(t) for t in itertools.combinations(range(4), 2)]
bad = 0; tot = 0
for p in pair:
    for rest in itertools.product(trip, repeat=8):
        L = {V[0]: p}; L.update({v: s for v, s in zip(V[1:], rest)}); tot += 1
        if not colourable(V, E, L): bad += 1; ex = L
print(f'C3xC3, palette 4, one 2-list: {tot} assignments, {bad} not colourable')
if bad: print('  example:', {k: sorted(v) for k, v in ex.items()})
random.seed(2)
for n in (5, 7):
    V, E = graph(n)
    for P in (4, 5):
        bad = 0; N = 20000
        for _ in range(N):
            L = {v: frozenset(random.sample(range(P), 3)) for v in V}
            L[V[0]] = frozenset(random.sample(sorted(L[V[0]]), 2))
            if not colourable(V, E, L): bad += 1
        print(f'C3xC{n}, palette {P}, one 2-list, random: {bad} of {N} not colourable')
