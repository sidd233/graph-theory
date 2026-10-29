import sys
from collections import Counter
from kp import torus, eulerian_orientations, build, has_kernel
m,n=int(sys.argv[1]),int(sys.argv[2])
N,E=torus(m,n); ors=eulerian_orientations(N,E)
# for each orientation, smallest induced subdigraph with no kernel (search by size)
from itertools import combinations
sizes=Counter(); kinds=Counter()
def is_directed_cycle(U,out):
    vs=[v for v in range(N) if U>>v&1]
    return all(bin(out[v]&U).count('1')==1 for v in vs) and all(bin(sum(1 for u in vs if out[u]>>v&1)).count('1')>0 and sum(1 for u in vs if out[u]>>v&1)==1 for v in vs)
for arcs in ors:
    out,adj=build(N,arcs); found=None
    for k in range(1,N+1):
        for S in combinations(range(N),k):
            U=sum(1<<v for v in S)
            if not has_kernel(U,out,adj): found=(k,U); break
        if found: break
    sizes[found[0]]+=1
    kinds['odd directed cycle' if is_directed_cycle(found[1],out) else 'other']+=1
print(f"C{m}xC{n}: size of smallest kernel-less induced subdigraph, over {len(ors)} orientations:",dict(sorted(sizes.items())))
print("  is it an induced directed cycle?",dict(kinds))
