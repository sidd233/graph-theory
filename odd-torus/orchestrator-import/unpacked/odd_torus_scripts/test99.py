import sys, time, random
from kp import torus, build
from lift2 import lift2, kp33
sys.setrecursionlimit(100000)
K=kp33()
def induced_odd_dicycle(N,out,adj,budget=3_000_000):
    steps=0
    for s in range(N):
        stack=[(s,1<<s,1)]
        while stack:
            v,used,L=stack.pop(); steps+=1
            if steps>budget: return 'BUDGET'
            o=out[v]
            while o:
                w=(o&-o).bit_length()-1; o&=o-1
                if w<s: continue
                if w==s:
                    if L>=3 and L%2==1:
                        U=used
                        if all(bin(out[x]&U).count('1')==1 and bin(adj[x]&U).count('1')==2 for x in range(N) if U>>x&1):
                            return L
                    continue
                if used>>w&1: continue
                if adj[w]&used&~(1<<v)&~(1<<s): continue
                stack.append((w,used|1<<w,L+1))
    return None
for (m,n) in [(9,9),(9,15),(15,15)]:
    res=[]
    for b in K:
        N,arcs=lift2(b,3,3,m,n); out,adj=build(N,arcs)
        assert all(bin(o).count('1')==2 for o in out)
        res.append(induced_odd_dicycle(N,out,adj))
    print(f"C{m}xC{n} 2D lifts: induced odd directed cycle search ->",res,flush=True)
