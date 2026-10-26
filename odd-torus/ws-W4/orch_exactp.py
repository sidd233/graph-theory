# Copied from orchestrator-import/unpacked/kernel_section/exactp.py (coeff_mod only, no top-level run),
# used as an independent second computation of c_w mod p directly over the 3^m column assignments.
import numpy as np, itertools
def prime(q): return q>1 and all(q%d for d in range(2,int(q**.5)+1))
p=1000003; assert prime(p) and p%3==1
for g in range(2,100):
    w=pow(g,(p-1)//3,p)
    if w!=1: break
R=[1,w,w*w%p]; assert (1+R[1]+R[2])%p==0
inv3=pow(3,p-2,p)
def coeff_mod(m,n,e,wv):
    S=list(itertools.product(range(3),repeat=m))
    X=np.array([[R[i] for i in s] for s in S],dtype=np.int64)
    base=np.ones(len(S),dtype=np.int64)
    for r in range(m): base=base*X[:,r]%p*inv3%p
    def colw(c):
        v=base.copy()
        for r in range(m):
            if e==('col',r,c): continue
            v=v*((X[:,r]-X[:,(r+1)%m])%p)%p
        if wv[1]==c: v=v*X[:,wv[0]]%p
        return v
    def rowm(c):
        M=np.ones((len(S),len(S)),dtype=np.int64)
        for r in range(m):
            if e==('row',r,c): continue
            M=M*((X[:,r][:,None]-X[:,r][None,:])%p)%p
        return M
    P=np.eye(len(S),dtype=np.int64)
    for c in range(n):
        A=colw(c)[:,None]*rowm(c)%p
        P=(P@A)%p
    return int(np.trace(P)%p)
