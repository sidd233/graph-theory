"""Alpha-aware global 'every cut bad' search (same model as global_mixed.py).
For a column c and pin row r, P[c][r] = set of columns d with (c, d) a bad window at pin r.
A trigger between consecutive columns a, b (rows R where they differ) needs
   next column  in  P[b][r] for all r in R   (forward cut bad)
   prev column  in  P[a][r] for all r in R   (backward cut bad).
WLOG (cyclic shift) columns 0 and 1 differ, unless the assignment is row-constant.
Run: python -u global_fast.py BADFILE n"""
import sys
from collections import Counter, defaultdict
from pysat.solvers import Solver
W = set()                      # (L1, L2, alpha) bad with the pin at row 0
for l in open(sys.argv[1]):
    if not l.startswith('BADA'): continue
    w = l.split(); W.add((tuple(int(h, 16) for h in w[3:8]), tuple(int(h, 16) for h in w[9:14]), int(w[1])))
n = int(sys.argv[2])
rot = lambda c, r: tuple(c[(t + r) % 5] for t in range(5))
unrot = lambda c, r: tuple(c[(t - r) % 5] for t in range(5))
P = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))   # P[c][r][alpha] = {d}
for a, b, al in W:
    for r in range(5):
        P[unrot(a, r)][r][al].add(unrot(b, r))
bits = lambda x: [c for c in range(16) if x >> c & 1]
dom = sorted(P)
print('bad windows', len(W), '; columns that can sit next to a cut:', len(dom), flush=True)
R = lambda a, b: [r for r in range(5) if a[r] != b[r]]
def fwd(a, b):                       # allowed next columns after the pair (a, b)
    rs = R(a, b)
    if not rs: return None           # no constraint
    s = None
    for r in rs:
        for al in bits(a[r] & ~b[r]):          # alpha in L(r,j) minus L(r,j+1): the cut is bad only if bad for every alpha
            t = P[b][r][al]
            s = set(t) if s is None else s & t
            if not s: return set()
    return s
def back_ok(prev, a, b):
    return all(prev in P[a][r][al] for r in R(a, b) for al in bits(b[r] & ~a[r]))
def ok4(cm1, c0, c1, c2):
    return all(c2 in P[c1][r][al] for r in R(c0, c1) for al in bits(c0[r] & ~c1[r])) and back_ok(cm1, c0, c1)
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
