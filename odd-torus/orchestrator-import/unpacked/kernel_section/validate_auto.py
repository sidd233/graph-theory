# Validate automaton kernel test against the direct kernel search on actual digraphs.
import random
from automaton import *
from latin_lift import *
from kp import build, has_kernel
random.seed(7)
def digraph(cols, n):           # cols: list of n column-type tuples
    arcs=[]; idx=lambda r,c: r*n+c
    for c in range(n):
        for (r,s) in column_arcs(cols[c]): arcs.append((idx(r,c),idx(s,c)))
        ra=row_arcs(cols[c],cols[(c+1)%n])
        for r in ROWS:
            a,b=idx(r,c),idx(r,(c+1)%n)
            arcs.append((a,b) if ra[r]==+1 else (b,a))
    return 3*n,arcs
def auto_kernel(cols,n,Us):
    P=None
    for c in range(n):
        T=trans(column_arcs(cols[c]), row_arcs(cols[c-1],cols[c]), Us[c])
        P=T if P is None else mul(P,T)
    return trace(P)
bad=0; tot=0
for L in latin_squares():
    for n in (3,6,9):
        cols=[L[c%3] for c in range(n)]
        N,arcs=digraph(cols,n); out,adj=build(N,arcs)
        assert all(bin(o).count('1')==2 for o in out)
        for _ in range(400):
            Us=[frozenset(r for r in ROWS if random.random()<0.75) for c in range(n)]
            U=sum(1<<(r*n+c) for c in range(n) for r in Us[c])
            tot+=1
            if auto_kernel(cols,n,Us)!=has_kernel(U,out,adj): bad+=1
print(f"automaton vs direct kernel search: {bad} disagreements in {tot} induced subdigraphs")
# also a non-Latin orientation family: random column types with random row arcs is not degree-2,
# but kernel existence logic does not need degree 2, so test it too
from itertools import permutations
P3=list(permutations('SMT'))
for _ in range(300):
    n=random.choice([4,5,7]); cols=[random.choice(P3) for c in range(n)]
    rowsets=[{r:random.choice([1,-1]) for r in ROWS} for c in range(n)]
    arcs=[]; idx=lambda r,c: r*n+c
    for c in range(n):
        for (r,s) in column_arcs(cols[c]): arcs.append((idx(r,c),idx(s,c)))
        for r in ROWS:
            a,b=idx(r,c),idx(r,(c+1)%n); arcs.append((a,b) if rowsets[c][r]==1 else (b,a))
    N=3*n; out,adj=build(N,arcs)
    for _ in range(30):
        Us=[frozenset(r for r in ROWS if random.random()<0.75) for c in range(n)]
        U=sum(1<<(r*n+c) for c in range(n) for r in Us[c])
        Pm=None
        for c in range(n):
            T=trans(column_arcs(cols[c]), rowsets[c-1], Us[c]); Pm=T if Pm is None else mul(Pm,T)
        tot+=1
        if trace(Pm)!=has_kernel(U,out,adj): bad+=1
print(f"including random orientations: {bad} disagreements in {tot}")
