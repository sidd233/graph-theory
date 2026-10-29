import itertools
from kp import torus, eulerian_orientations, build, has_kernel, kernel_perfect

def brute_kernel(U,out,adj,N):
    vs=[v for v in range(N) if U>>v&1]
    for r in range(len(vs)+1):
        for S in itertools.combinations(vs,r):
            Sm=sum(1<<v for v in S)
            if any(adj[v]&Sm for v in S): continue
            if all(out[v]&Sm for v in vs if not Sm>>v&1): return True
    return False

# 1) count Eulerian orientations of C3xC3 by brute force over all 2^18
N,E=torus(3,3); cnt=0
for bits in range(1<<len(E)):
    od=[0]*N
    for k,(a,b) in enumerate(E):
        od[a if bits>>k&1 else b]+=1
    if all(d==2 for d in od): cnt+=1
print("C3xC3 Eulerian orientations, brute force:",cnt,"| backtracking:",len(eulerian_orientations(N,E)))

# 2) fast kernel test vs brute kernel test on every induced subdigraph, for several orientations
import random; random.seed(0)
ors=eulerian_orientations(N,E); bad=0; tests=0
for arcs in random.sample(ors,30):
    out,adj=build(N,arcs)
    for U in range(1,1<<N):
        tests+=1
        if has_kernel(U,out,adj)!=brute_kernel(U,out,adj,N): bad+=1
print(f"kernel test disagreements: {bad} / {tests}")

# 3) same check on C3xC5 for 5 random orientations, random subsets
N,E=torus(3,5); ors=eulerian_orientations(N,E); bad=0; tests=0
for arcs in random.sample(ors,5):
    out,adj=build(N,arcs)
    for _ in range(3000):
        U=random.randrange(1,1<<N); tests+=1
        if has_kernel(U,out,adj)!=brute_kernel(U,out,adj,N): bad+=1
print(f"C3xC5 kernel test disagreements: {bad} / {tests}")
