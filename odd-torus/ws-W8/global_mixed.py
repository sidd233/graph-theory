"""Global 'every cut bad' search over a given set of bad windows (pin at row 0), any palette.
Classifies all evaders of C5 x Cn and tests each one of unknown type for colourability (pysat).
alpha is not modelled here (windows were found bad with alpha fresh, the conservative case).
Run: python global_mixed.py BADFILE n"""
import sys, itertools
from collections import Counter
from pysat.solvers import Solver
W = set()
for l in open(sys.argv[1]):
    w = l.split(); W.add((tuple(int(h, 16) for h in w[1:6]), tuple(int(h, 16) for h in w[7:12])))
n = int(sys.argv[2])
rot = lambda c, r: tuple(c[(t + r) % 5] for t in range(5))
def bad(a, b, r): return (rot(a, r), rot(b, r)) in W
dom = sorted({rot(c, r) for a, b in W for c in (a, b) for r in range(5)})
print('bad windows', len(W), '; columns next to a cut:', len(dom))
def trig_ok(cm1, c0, c1, c2):
    return all(c0[r] == c1[r] or (bad(c1, c2, r) and bad(c0, cm1, r)) for r in range(5))
sols = []; seq = []
def go():
    if len(seq) == n:
        if all(trig_ok(seq[(j-1) % n], seq[j], seq[(j+1) % n], seq[(j+2) % n]) for j in range(n)):
            sols.append(tuple(seq))
        return
    for c in dom:
        seq.append(c); k = len(seq)
        if k < 4 or trig_ok(seq[k-4], seq[k-3], seq[k-2], seq[k-1]): go()
        seq.pop()
go()
def kind(s):
    rows = [tuple(c[r] for c in s) for r in range(5)]
    if all(len(set(rw)) == 1 for rw in rows): return 'row-constant'
    if all(len(set(c)) == 1 for c in s): return 'column-constant'
    nonc = [r for r in range(5) if len(set(rows[r])) > 1]
    if len(nonc) == 1 and len({rows[r][0] for r in range(5) if r not in nonc}) == 1: return 'one free row'
    return 'OTHER'
def colourable(s):
    V = [(r, j) for r in range(5) for j in range(n)]; idx = {}
    S = Solver(name='glucose4'); var = 0; cl = []
    for (r, j) in V:
        cols = [c for c in range(16) if s[j][r] >> c & 1]
        lits = []
        for c in cols: var += 1; idx[(r, j, c)] = var; lits.append(var)
        S.add_clause(lits)
    for (r, j) in V:
        for (r2, j2) in (((r + 1) % 5, j), (r, (j + 1) % n)):
            for c in range(16):
                if (r, j, c) in idx and (r2, j2, c) in idx: S.add_clause([-idx[(r, j, c)], -idx[(r2, j2, c)]])
    return S.solve()
cnt = Counter(kind(s) for s in sols)
print(f'n = {n}: evaders {len(sols)}', dict(cnt))
others = [s for s in sols if kind(s) == 'OTHER']
print('OTHER evaders colourable:', sum(colourable(s) for s in others), 'of', len(others))
for s in others[:3]: print('  example columns:', [[format(x, 'x') for x in c] for c in s])
