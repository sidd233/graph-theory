# Kernel existence in induced subdigraphs of an oriented C3 x Cn, column by column.
# A column orientation word: for column c, colarcs[c] = set of arcs (r,s) inside column c,
# rowarc[c][r] = +1 if (r,c)->(r,c+1), -1 if (r,c+1)->(r,c)   (edge between column c and c+1).
# State after column c: (K, P): K in {None,0,1,2} = kernel vertex of column c (a column is a
# triangle, so at most one), P = present non-kernel vertices of column c not yet absorbed
# (they must be absorbed by column c+1 through a row arc).
from itertools import combinations
ROWS=(0,1,2)
STATES=[(None,frozenset(P)) for k in range(4) for P in combinations(ROWS,k)] + \
       [(K,frozenset(P)) for K in ROWS for k in range(3) for P in combinations([r for r in ROWS if r!=K],k)]
IDX={s:i for i,s in enumerate(STATES)}
NS=len(STATES)
def trans(colarcs_next, rowarc_prev, U):
    """Boolean matrix: from state of column c to state of column c+1, where column c+1 has
    vertex set U, internal arcs colarcs_next, and rowarc_prev[r] is the arc between (r,c),(r,c+1)."""
    M=[0]*NS
    for i,(K,P) in enumerate(STATES):
        for Kn in [None]+[r for r in U]:
            if Kn is not None and K==Kn: continue                     # row edge (Kn,c)-(Kn,c+1)
            # pending vertices of column c must be absorbed by Kn via arc (r,c)->(r,c+1)
            if any(not (r==Kn and rowarc_prev[r]==+1) for r in P): continue
            Pn=set()
            for r in U:
                if r==Kn: continue
                ab = (Kn is not None and (r,Kn) in colarcs_next) or (K==r and rowarc_prev[r]==-1)
                if not ab: Pn.add(r)
            M[i]|=1<<IDX[(Kn,frozenset(Pn))]
    return tuple(M)
def mul(A,B):
    C=[]
    for a in A:
        row=0; x=a
        while x:
            j=(x&-x).bit_length()-1; x&=x-1; row|=B[j]
        C.append(row)
    return tuple(C)
def trace(A): return any(A[i]>>i&1 for i in range(NS))
def subsets():
    return [frozenset(c) for k in range(4) for c in combinations(ROWS,k)]
