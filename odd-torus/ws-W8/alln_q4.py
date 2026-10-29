"""Palette-4 theorem, global step for EVERY n. Columns that can sit next to a cut: dom (64).
Graph on states (a, b, c) of three consecutive columns; edge (a,b,c) -> (b,c,d) iff the trigger
between b and c (if any) has both cuts bad (ok4). A closed walk of length n is exactly an
assignment of C5 x Cn (palette 4) in which every cut is bad and every column lies in dom; any
assignment with every cut bad has all columns in dom unless it is row-constant.
Check: in every strongly connected component that carries a closed walk of ODD length, all columns
share one special type (column-constant, or rows other than k all equal to one set A).
Run: python alln_q4.py"""
import sys
from collections import defaultdict
sys.setrecursionlimit(1000000)
W = set()
for l in open('all_q4_stillbad_real.txt'):
    w = l.split(); W.add((tuple(int(h, 16) for h in w[1:6]), tuple(int(h, 16) for h in w[7:12])))
rot = lambda c, r: tuple(c[(t + r) % 5] for t in range(5))
bad = lambda a, b, r: (rot(a, r), rot(b, r)) in W
dom = sorted({rot(c, r) for a, b in W for c in (a, b) for r in range(5)})
def ok4(cm1, c0, c1, c2):
    return all(c0[r] == c1[r] or (bad(c1, c2, r) and bad(c0, cm1, r)) for r in range(5))
nxt = defaultdict(list)
states = [(a, b, c) for a in dom for b in dom for c in dom]
for (a, b, c) in states:
    for d in dom:
        if ok4(a, b, c, d): nxt[(a, b, c)].append((b, c, d))
print('states', len(states), 'edges', sum(len(v) for v in nxt.values()))
# Tarjan SCC (iterative)
index = {}; low = {}; onst = set(); st = []; comps = []; i = 0
for s0 in states:
    if s0 in index: continue
    work = [(s0, 0)]
    while work:
        v, k = work.pop()
        if k == 0:
            index[v] = low[v] = i; i += 1; st.append(v); onst.add(v)
        nbrs = nxt[v]
        if k < len(nbrs):
            work.append((v, k + 1)); w = nbrs[k]
            if w not in index: work.append((w, 0))
            elif w in onst: low[v] = min(low[v], index[w])
            continue
        for w in nbrs:
            if w in onst: low[v] = min(low[v], low[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = st.pop(); onst.discard(w); comp.append(w)
                if w == v: break
            comps.append(comp)
def types(col):
    t = set()
    if len(set(col)) == 1: t.add(('colconst',))
    for k in range(5):
        rest = {col[r] for r in range(5) if r != k}
        if len(rest) == 1: t.add(('free', k, next(iter(rest))))
    return t
bad_comps = 0; cyc = 0
for comp in comps:
    cs = set(comp)
    if len(comp) == 1 and comp[0] not in [w for w in nxt[comp[0]]]: continue
    # odd closed walk exists iff the component (as a digraph) is not bipartite w.r.t. walk parity
    col = {comp[0]: 0}; odd = False; stack = [comp[0]]
    while stack and not odd:
        v = stack.pop()
        for w in nxt[v]:
            if w not in cs: continue
            if w not in col: col[w] = 1 - col[v]; stack.append(w)
            elif col[w] == col[v]: odd = True; break
    if not odd: continue
    cyc += 1
    cols = {c for s in comp for c in s}
    common = None
    for c in cols:
        common = types(c) if common is None else common & types(c)
    if not common:
        bad_comps += 1
        print('NON-SPECIAL component with odd closed walks; size', len(comp), 'example columns:', [[format(x, 'x') for x in c] for c in list(cols)[:4]])
print('components carrying odd closed walks:', cyc, '; of these, not of one special type:', bad_comps)
