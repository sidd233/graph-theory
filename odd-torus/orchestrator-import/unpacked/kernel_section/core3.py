# Clean library (no side effects) for C3 x Cn orientations encoded by (eps=+1, p).
import itertools
def third(x,y): return 3-x-y
def orient(p):
    n=len(p); idx=lambda r,c: r*n+c; arcs=[]
    for c in range(n):
        T,S=p[c-1],p[c]; M=3-T-S
        arcs += [(idx(S,c),idx(M,c)),(idx(S,c),idx(T,c)),(idx(M,c),idx(T,c))]
        for r in range(3):
            a,b=idx(r,c),idx(r,(c+1)%n)
            arcs.append((b,a) if r==p[c] else (a,b))
    return 3*n,arcs
def proper_colourings(n):
    for p in itertools.product(range(3),repeat=n):
        if all(p[c]!=p[(c+1)%n] for c in range(n)) and p[0]==0: yield p
def latin(p): n=len(p); return all(len({p[c],p[(c+1)%n],p[(c+2)%n]})==3 for c in range(n))
def cycle_vertices(p,b):
    n=len(p); vs=[]
    for c in range(n):
        a=b[c-1]; vs.append((a,c))
        if a!=b[c]: vs.append((b[c],c))
    return vs
def check_cycle(p,b):
    n=len(p); N,arcs=orient(p); A=set(arcs); idx=lambda r,c: r*n+c
    verts=[idx(r,c) for r,c in cycle_vertices(p,b)]; U=set(verts); L=len(verts)
    cyc=all((verts[i],verts[(i+1)%L]) in A for i in range(L))
    inside=sum(1 for u,v in arcs if u in U and v in U)
    return cyc and inside==L and L%2==1 and len(U)==L
def construct(p):
    n=len(p); b=[third(p[i],p[(i+1)%n]) for i in range(n)]
    for c in range(n):
        if len({p[c],p[(c+1)%n],p[(c+2)%n]})==3 and p[(c+3)%n]==p[(c+1)%n]:
            b[c]=p[(c+1)%n]; return tuple(b)
    return None
