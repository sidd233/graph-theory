# Rule A: b_c = third(p_c, p_{c+1}). Valid, induced, step count = #rainbow boundaries (even length).
# Gadget: change b on a window of consecutive boundaries so that the cycle stays valid & induced
# and the number of column steps changes parity. Window = boundaries c..c+L-1 (b replaced there).
import itertools
def third(x,y): return 3-x-y
def valid_and_steps(p,b,cols):
    """check transitions and inducedness on the given columns (column c has entry b[c-1], exit b[c])"""
    n=len(p); steps=0
    for c in cols:
        c%=n; a=b[(c-1)%n]; x=b[c]
        if x==p[c] or a==p[(c-1)%n]: return None
        T,S=p[(c-1)%n],p[c]; M=3-T-S; order=(S,M,T)
        if a!=x:
            if order.index(a)>order.index(x): return None
            steps+=1
            if b[(c+1)%n]==a: return None
        else:
            if a==S: return None
    return steps
def gadgets_exist(p, c, L):
    n=len(p); A=[third(p[i],p[(i+1)%n]) for i in range(n)]
    cols=range(c-1, c+L+2)                      # columns touched by changes + neighbours for inducedness
    base=valid_and_steps(p,A,cols)
    for choice in itertools.product(range(3),repeat=L):
        b=A[:]
        for i,v in enumerate(choice): b[(c+i)%n]=v
        if b==A: continue
        s=valid_and_steps(p,b,cols)
        if s is not None and (s-base)%2==1: return choice
    return None
def has_gadget(p,Lmax):
    n=len(p)
    for L in range(1,Lmax+1):
        for c in range(n):
            g=gadgets_exist(p,c,L)
            if g is not None: return (c,L,g)
    return None
if __name__=='__main__':
    from winding import proper_colourings, latin, orient
    from verify_winding import check_cycle
    for n in (5,7,9,11,13,15):
        tot=fail=0; maxL=0
        for p in proper_colourings(n):
            if latin(p): continue
            tot+=1
            g=has_gadget(p,4)
            if g is None: fail+=1; continue
            c,L,ch=g; maxL=max(maxL,L)
            b=[third(p[i],p[(i+1)%n]) for i in range(n)]
            for i,v in enumerate(ch): b[(c+i)%n]=v
            assert check_cycle(p,tuple(b)), (p,b)
        print(f"n={n}: non-Latin {tot}, gadget found and cycle verified {tot-fail}, no gadget (L<=4) {fail}, max window used {maxL}",flush=True)
