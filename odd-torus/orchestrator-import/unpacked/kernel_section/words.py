# Encoding of orientations of C3 x Cn with Delta+ <= 2 and all columns transitive.
# Column letter = (types, d): types[r] in {S,M,T} (column source/middle/sink), d = row direction of
# the M vertex: +1 = in from left, out to right; -1 = in from right, out to left.
# Degrees force: S has both row arcs in, T both out, M one each.
from itertools import permutations
from automaton import *
LETTERS=[(tp,d) for tp in permutations('SMT') for d in (1,-1)]
RANK={'S':0,'M':1,'T':2}
def colarcs(tp): return {(r,s) for r in ROWS for s in ROWS if r!=s and RANK[tp[r]]<RANK[tp[s]]}
def need_left(tp,d,r):   # requirement of left endpoint (r,c) on edge to (r,c+1): +1 = L->R
    t=tp[r]; return +1 if t=='T' or (t=='M' and d==1) else -1
def need_right(tp,d,r):  # requirement of right endpoint (r,c+1)
    t=tp[r]; return +1 if t=='S' or (t=='M' and d==1) else -1
def rowarc(a,b):
    """arcs between column with letter a (left) and letter b (right); None if inconsistent"""
    out={}
    for r in ROWS:
        x=need_left(a[0],a[1],r); y=need_right(b[0],b[1],r)
        if x!=y: return None
        out[r]=x
    return out
def colmat(a,b,U):  # transfer into column with letter b from column with letter a
    return trans(colarcs(b[0]), rowarc(a,b), U)
if __name__=='__main__':
    from kp import torus, eulerian_orientations
    import itertools
    for n in (3,5,7):
        # word count
        cnt=0
        for w in itertools.product(range(len(LETTERS)),repeat=n):
            if all(rowarc(LETTERS[w[c]],LETTERS[w[(c+1)%n]]) is not None for c in range(n)): cnt+=1
        # direct count from enumeration: orientations whose 3 column triangles are all transitive
        N,E=torus(3,n); direct=0
        for arcs in eulerian_orientations(N,E):
            A=set(arcs); ok=True
            for c in range(n):
                v=[r*n+c for r in range(3)]
                cyc1=all(((v[i],v[(i+1)%3]) in A) for i in range(3)); cyc2=all(((v[(i+1)%3],v[i]) in A) for i in range(3))
                if cyc1 or cyc2: ok=False; break
            direct+=ok
        print(f"n={n}: consistent cyclic words {cnt}, orientations with all columns transitive {direct}")
