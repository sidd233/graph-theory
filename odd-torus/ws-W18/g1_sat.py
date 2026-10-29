"""G1 (common X) as a SAT question on abstract labels. Vertices of C5 x Cn get one of k labels.
Premises: (i) no three consecutive identical columns; (ii) every hole (t, j) is a seam of type N, L, R or M,
or a sea: at most 4 of its 16 vertices differ from some label X.
Negated conclusion: for every label X, some hole has at least 5 vertices not labelled X.
UNSAT means: under the premises, one label X works as the sea label for every hole.
Run: python g1_sat.py n k"""
import sys, itertools
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
n, k = int(sys.argv[1]), int(sys.argv[2])
pool = IDPool(); cnf = CNF()
y = lambda r, c, l: pool.id(('y', r % 5, c % n, l))
for r in range(5):
    for c in range(n):
        cnf.append([y(r, c, l) for l in range(k)])
        for a, b in itertools.combinations(range(k), 2): cnf.append([-y(r, c, a), -y(r, c, b)])
def eq(u, v):                       # aux variable: labels of u and v are equal
    key = ('eq',) + tuple(sorted([u, v]))
    e = pool.id(key)
    if key not in eq.done:
        eq.done.add(key)
        (r1, c1), (r2, c2) = u, v
        for l in range(k):
            cnf.append([-e, -y(r1, c1, l), y(r2, c2, l)])   # e and u=l => v=l
            cnf.append([e, -y(r1, c1, l), -y(r2, c2, l)])   # u=l and v=l => e
    return e
eq.done = set()
norm = lambda r, c: (r % 5, c % n)
# (i) no triple
for j in range(n):
    cnf.append([-eq(norm(r, j), norm(r, j + 1)) for r in range(5)] + [-eq(norm(r, j + 1), norm(r, j + 2)) for r in range(5)])
def hole(t, j):
    W = [t - 1, t, t + 1]
    verts = [norm(r, c) for r in W for c in (j - 1, j, j + 1, j + 2)] + [norm(r, c) for r in (t + 2, t + 3) for c in (j, j + 1)]
    return W, verts
bigs = {l: [] for l in range(k)}
for t in range(5):
    for j in range(n):
        W, verts = hole(t, j)
        opts = []
        def typevar(name, eqs):
            v = pool.id(('type', t, j, name)); opts.append(v)
            for e in eqs: cnf.append([-v, e])
        low = [norm(r, j) for r in (t + 2, t + 3)]
        full = [eq(norm(r, j), norm(r, j + 1)) for r in (t + 2, t + 3)]
        typevar('N', [eq(norm(r, a), norm(r, a + 1)) for r in W for a in (j - 1, j, j + 1)] + full)
        typevar('L', [eq(norm(r, a), norm(r, a + 1)) for r in W for a in (j, j + 1)] + full)
        typevar('R', [eq(norm(r, a), norm(r, a + 1)) for r in W for a in (j - 1, j)] + full)
        typevar('M', [eq(norm(r, j - 1), norm(r, j)) for r in W] + [eq(norm(r, j + 1), norm(r, j + 2)) for r in W])
        for X in range(k):
            v = pool.id(('sea', t, j, X)); opts.append(v)
            lits = [-y(r, c, X) for (r, c) in verts]          # count vertices NOT labelled X
            enc = CardEnc.atmost(lits=lits, bound=4, vpool=pool, encoding=EncType.seqcounter)
            for cl in enc.clauses: cnf.append([-v] + cl)
            b = pool.id(('big', t, j, X)); bigs[X].append(b)
            enc2 = CardEnc.atleast(lits=lits, bound=5, vpool=pool, encoding=EncType.seqcounter)
            for cl in enc2.clauses: cnf.append([-b] + cl)
        cnf.append(opts)
for X in range(k): cnf.append(bigs[X])      # negated conclusion
with Solver(name='cadical153', bootstrap_with=cnf.clauses) as S:
    res = S.solve()
    print(f'n = {n}, labels = {k}: counterexample to G1 {"FOUND" if res else "none (UNSAT)"}')
    if res:
        m = set(x for x in S.get_model() if x > 0)
        for r in range(5): print('   ', ''.join(str(next(l for l in range(k) if y(r, c, l) in m)) for c in range(n)))
