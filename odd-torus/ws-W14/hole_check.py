"""Sanity checks for hole_coeff.py: (1) tr(T^n) = 0 for odd n, != 0 for even n (full torus, Alon-Tarsi);
(2) for placements with c != 0 at n = 5, random lists of sizes 3 - mu on G' are always colourable (SAT)."""
import itertools, json, random
exec(open('hole_coeff.py').read().split('results = {}')[0].split("border = ")[0])
def trpow(k):
    P = T
    for _ in range(k - 1): P = mmul(P, T)
    return sum(P[i][i][0] for i in range(30)), sum(P[i][i][1] for i in range(30))
for k in (3, 4, 5, 6, 7):
    print('full torus C5 x C%d: tr(T^n) =' % k, trpow(k))
from pysat.solvers import Solver
nz = json.load(open('hole_nonzero.json'))
n = 5
block = {(r, c) for r in (1, 2, 3) for c in (0, 1)}
V = [(r, c) for r in range(5) for c in range(n) if (r, c) not in block]
E = [((r, c), ((r + 1) % 5, c)) for r in range(5) for c in range(n)] + [((r, c), (r, (c + 1) % n)) for r in range(5) for c in range(n)]
E = [(a, b) for a, b in E if a not in block and b not in block]
pos = {'p1': (1, n - 1), 'p2': (2, n - 1), 'p3': (3, n - 1), 'q1': (4, 0), 'q2': (0, 0), 'r1': (4, 1), 'r2': (0, 1), 's1': (1, 2), 's2': (2, 2), 's3': (3, 2)}
names = ['p1', 'p2', 'p3', 'q1', 'q2', 'r1', 'r2', 's1', 's2', 's3']
random.seed(4); fails = 0; tests = 0
keys = [k for k, v in nz.items() if v]
for key in random.sample(keys, 60):
    mu = {pos[nm]: int(ch) for nm, ch in zip(names, key)}
    for _ in range(30):
        L = {v: random.sample(range(5), 3 - mu.get(v, 0)) for v in V}
        S = Solver(name='glucose4'); idx = {}; k = 0
        for v in V:
            lits = []
            for c in L[v]: k += 1; idx[(v, c)] = k; lits.append(k)
            S.add_clause(lits)
        for a, b in E:
            for c in L[a]:
                if (b, c) in idx: S.add_clause([-idx[(a, c)], -idx[(b, c)]])
        tests += 1
        if not S.solve(): fails += 1
        S.delete()
print(f'random list tests on placements with c != 0: {tests}, uncolourable: {fails}')
