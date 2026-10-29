import sys
from kp import torus, build
from indcyc import find_induced_odd_dicycle
m,n=int(sys.argv[1]),int(sys.argv[2])
N,E=torus(m,n)
deg_out=[0]*N; deg_in=[0]*N; arcs=[]; rem=[0]*N
for a,b in E: rem[a]+=1; rem[b]+=1
stats={'total':0,'without':0}; lens={}
def check():
    out,adj=build(N,arcs)
    c=find_induced_odd_dicycle(N,out,adj)
    stats['total']+=1
    if c is None:
        stats['without']+=1
        if stats['without']<=3: print("  orientation with NO induced odd dicycle:",arcs[:],flush=True)
    else: lens[len(c)]=lens.get(len(c),0)+1
    if stats['total']%200000==0: print("  progress",stats,flush=True)
def rec(k):
    if k==len(E): check(); return
    a,b=E[k]; rem[a]-=1; rem[b]-=1
    for u,v in ((a,b),(b,a)):
        if deg_out[u]<2 and deg_in[v]<2:
            deg_out[u]+=1; deg_in[v]+=1; arcs.append((u,v))
            if all(2-deg_out[x]<=rem[x] and 2-deg_in[x]<=rem[x] for x in (a,b)): rec(k+1)
            arcs.pop(); deg_out[u]-=1; deg_in[v]-=1
    rem[a]+=1; rem[b]+=1
rec(0)
print(f"C{m}xC{n} EXHAUSTIVE: {stats['total']} outdeg-2 orientations; without induced odd dicycle: {stats['without']}; cycle lengths found: {dict(sorted(lens.items()))}",flush=True)
