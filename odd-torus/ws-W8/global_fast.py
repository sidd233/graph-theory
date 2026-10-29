"""Faster global 'every cut bad' search (same model as global_mixed.py).
For a column c and pin row r, P[c][r] = set of columns d with (c, d) a bad window at pin r.
A trigger between consecutive columns a, b (rows R where they differ) needs
   next column  in  P[b][r] for all r in R   (forward cut bad)
   prev column  in  P[a][r] for all r in R   (backward cut bad).
WLOG (cyclic shift) columns 0 and 1 differ, unless the assignment is row-constant.
Run: python -u global_fast.py BADFILE n"""
import sys
from collections import Counter, defaultdict
from pysat.solvers import Solver
W = set()
for l in open(sys.argv[1]):
    w = l.split(); W.add((tuple(int(h, 16) for h in w[1:6]), tuple(int(h, 16) for h in w[7:12])))
n = int(sys.argv[2])
rot = lambda c, r: tuple(c[(t + r) % 5] for t in range(5))
unrot = lambda c, r: tuple(c[(t - r) % 5] for t in range(5))
P = defaultdict(lambda: defaultdict(set))
for a, b in W:
    for r in range(5):
        P[unrot(a, r)][r].add(unrot(b, r))
dom = sorted(P)
print('bad windows', len(W), '; columns that can sit next to a cut:', len(dom), flush=True)
R = lambda a, b: [r for r in range(5) if a[r] != b[r]]
def fwd(a, b):                       # allowed next columns after the pair (a, b)
    rs = R(a, b)
    if not rs: return None           # no constraint
    s = None
    for r in rs:
        s = P[b][r] if s is None else s & P[b][r]
        if not s: return set()
    return s
def back_ok(prev, a, b):
    return all(prev in P[a][r] for r in R(a, b))
def ok4(cm1, c0, c1, c2):
    rs = R(c0, c1)
    return all(c2 in P[c1][r] and cm1 in P[c0][r] for r in rs)
sols = []
def go(seq):
    k = len(seq)
    if k == n:
        if all(ok4(seq[(j-1) % n], seq[j], seq[(j+1) % n], seq[(j+2) % n]) for j in range(n)): sols.append(tuple(seq))
        return
    f = fwd(seq[-2], seq[-1])
    cands = f if f is not None else ([seq[-1]] + [c for c in dom if c != seq[-1]])
    for c in cands:
        if c != seq[-1] and not back_ok(seq[-2], seq[-1], c): continue
        go(seq + [c])
for c0 in dom:
    for c1 in dom:
        if c1 == c0 or R(c0, c1) == []: continue
        if not P[c1] or not P[c0]: continue
        go([c0, c1])
def kind(s):
    rows = [tuple(c[r] for c in s) for r in range(5)]
    if all(len(set(rw)) == 1 for rw in rows): return 'row-constant'
    if all(len(set(c)) == 1 for c in s): return 'column-constant'
    nonc = [r for r in range(5) if len(set(rows[r])) > 1]
    if len(nonc) == 1 and len({rows[r][0] for r in range(5) if r not in nonc}) == 1: return 'one free row'
    return 'OTHER'
def colourable(s):
    idx = {}; S = Solver(name='glucose4'); var = 0
    for r in range(5):
        for j in range(n):
            lits = []
            for c in range(16):
                if s[j][r] >> c & 1: var += 1; idx[(r, j, c)] = var; lits.append(var)
            S.add_clause(lits)
    for r in range(5):
        for j in range(n):
            for (r2, j2) in (((r + 1) % 5, j), (r, (j + 1) % n)):
                for c in range(16):
                    if (r, j, c) in idx and (r2, j2, c) in idx: S.add_clause([-idx[(r, j, c)], -idx[(r2, j2, c)]])
    return S.solve()
cnt = Counter(kind(s) for s in sols)
print(f'n = {n}: evaders (counted with cyclic shifts) {len(sols)}', dict(cnt), flush=True)
others = sorted({s for s in sols if kind(s) == 'OTHER'})
print('OTHER evaders colourable:', sum(colourable(s) for s in others), 'of', len(others), flush=True)
for s in others[:3]: print('  example columns:', [[format(x, 'x') for x in c] for c in s])
