# Search for a 3-list assignment of C_m x C_n (palette {0..q-1}) with no proper colouring.
# CEGAR: master SAT proposes lists L; checker SAT tries to colour; each colouring found
# becomes a blocking clause on L. Master UNSAT => no bad assignment with this palette.
import sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from kp import torus
m,n,q=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
overlap = len(sys.argv)>4 and sys.argv[4]=='overlap'
N,E=torus(m,n)
pool=IDPool()
l=lambda v,a: pool.id(('l',v,a))
master=Cadical153()
for v in range(N):
    for cl in CardEnc.equals([l(v,a) for a in range(q)],bound=3,vpool=pool,encoding=EncType.seqcounter).clauses:
        master.add_clause(cl)
for a in range(3): master.add_clause([l(0,a)])           # colour renaming: L(0)={0,1,2}
if overlap:                                                # valid for graphs where edge-deletion AT holds
    for u,v in E:
        aux=[]
        for a in range(q):
            z=pool.id(('z',u,v,a)); aux.append(z)
            master.add_clause([-z,l(u,a)]); master.add_clause([-z,l(v,a)])
        master.add_clause(aux)
def colour(L):
    s=Cadical153(); x=lambda v,a: v*q+a+1
    for v in range(N):
        s.add_clause([x(v,a) for a in L[v]])
        for a in range(q):
            if a not in L[v]: s.add_clause([-x(v,a)])
    for u,v in E:
        for a in range(q): s.add_clause([-x(u,a),-x(v,a)])
    if not s.solve(): return None
    mod=set(t for t in s.get_model() if t>0)
    return [next(a for a in L[v] if x(v,a) in mod) for v in range(N)]
it=0; t0=time.time()
while True:
    if not master.solve():
        print(f"C{m}xC{n} palette {q}{' +overlap' if overlap else ''}: NO bad list assignment exists (master UNSAT after {it} colourings, {time.time()-t0:.0f}s)",flush=True); break
    mod=set(t for t in master.get_model() if t>0)
    L=[[a for a in range(q) if l(v,a) in mod] for v in range(N)]
    c=colour(L)
    if c is None:
        print(f"C{m}xC{n} palette {q}: BAD LIST ASSIGNMENT FOUND: {L}",flush=True); break
    master.add_clause([-l(v,c[v]) for v in range(N)])
    it+=1
    if it%20000==0: print(f"  {it} colourings blocked, {time.time()-t0:.0f}s",flush=True)
