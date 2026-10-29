# Correct dependency: changing b_c affects columns c and c+1 and the inducedness checks of
# columns c-1, c, c+1, which involve b_{c-2..c+2}; rule-A values there depend on p_{c-2..c+3}.
import itertools
from gadget import third
def check_cols(p,b,cols,n):
    from gadget import valid_and_steps
    return valid_and_steps(p,b,cols)
def tri(w): return ''.join('A' if w[i]==w[i+2] else 'R' for i in range(len(w)-2))
res={}
for p6 in itertools.product(range(3),repeat=6):
    if any(p6[i]==p6[i+1] for i in range(5)) or p6[0]!=0: continue
    n=12; c=5; p=[None]*n
    for i in range(6): p[c-2+i]=p6[i]
    # fill rest properly (irrelevant to the checked columns)
    for i in list(range(c+4,n))+list(range(0,c-2)):
        prev=p[(i-1)%n]; nxt=p[(i+1)%n]
        p[i]=next(x for x in range(3) if x!=prev and x!=nxt)
    assert all(p[i]!=p[(i+1)%n] for i in range(n))
    A=[third(p[i],p[(i+1)%n]) for i in range(n)]
    cols=range(c-1,c+2)
    base=check_cols(p,A,cols,n); assert base is not None
    ok=[]
    for v in range(3):
        if v==A[c]: continue
        b=A[:]; b[c]=v
        s=check_cols(p,b,cols,n)
        if s is not None and (s-base)%2==1: ok.append(v)
    res[p6]=ok
from collections import defaultdict
by=defaultdict(set)
for p6,ok in res.items(): by[tri(p6)].add(bool(ok))
for k in sorted(by): print("triple types at boundaries c-1, c, c+1, c+2:",k,"-> gadget:",by[k])
print()
for p6,ok in sorted(res.items()):
    if ok: print("p_{c-2..c+3} =",p6,tri(p6),"| rule A b_c =",third(p6[2],p6[3]),"-> new b_c =",ok)
