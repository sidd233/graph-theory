import sys, random, itertools
sys.setrecursionlimit(10000)

def torus(m,n):
    V=[(r,c) for r in range(m) for c in range(n)]; idx={v:i for i,v in enumerate(V)}
    E=set()
    for r in range(m):
        for c in range(n):
            a=idx[(r,c)]
            for b in (idx[((r+1)%m,c)], idx[(r,(c+1)%n)]):
                E.add((min(a,b),max(a,b)))
    return len(V), sorted(E)

def has_kernel(U, out, adj):
    # kernel of induced subdigraph on bitmask U: independent S, every v in U\S has out-arc into S
    status={}
    verts=[v for v in range(len(out)) if U>>v&1]
    def ok_out(v,S,O):
        # v is OUT: needs some out-neighbour in U not yet OUT
        return (out[v]&U&~O)!=0
    def rec(S,O):
        und=U&~S&~O
        # propagate: any undecided vertex all of whose out-nbrs (in U) are OUT must be IN
        changed=True
        while changed:
            changed=False
            x=und
            while x:
                v=(x&-x).bit_length()-1; x&=x-1
                if (out[v]&U&~O)==0:
                    if adj[v]&S: return False
                    S|=1<<v; O|=adj[v]&U&~S; und=U&~S&~O; changed=True; break
            # check OUT vertices still satisfiable / satisfied
        y=O
        while y:
            v=(y&-y).bit_length()-1; y&=y-1
            if (out[v]&U&~O)==0: return False
        if und==0:
            y=O
            while y:
                v=(y&-y).bit_length()-1; y&=y-1
                if (out[v]&S)==0: return False
            return True
        v=(und&-und).bit_length()-1
        if not (adj[v]&S) and rec(S|1<<v, O|(adj[v]&U&~S)): return True
        return rec(S, O|1<<v)
    return rec(0,0)

def kernel_perfect(N,out,adj,full=True):
    for U in range(1,1<<N):
        if not has_kernel(U,out,adj): return False, U
    return True, None

def eulerian_orientations(N,E,limit=None,shuffle=False):
    deg_out=[0]*N; deg_in=[0]*N; res=[]; arcs=[]
    order=E[:]
    if shuffle: random.shuffle(order)
    rem=[0]*N
    for a,b in order: rem[a]+=1; rem[b]+=1
    def rec(k):
        if limit and len(res)>=limit: return
        if k==len(order): res.append(arcs[:]); return
        a,b=order[k]; rem[a]-=1; rem[b]-=1
        choices=[(a,b),(b,a)]
        if shuffle: random.shuffle(choices)
        for u,v in choices:
            if deg_out[u]<2 and deg_in[v]<2:
                deg_out[u]+=1; deg_in[v]+=1; arcs.append((u,v))
                if deg_out[a]+rem[a]>=2-0 or True:
                    if 2-deg_out[a]<=rem[a]+0 and 2-deg_in[a]<=rem[a] and 2-deg_out[b]<=rem[b] and 2-deg_in[b]<=rem[b]:
                        rec(k+1)
                arcs.pop(); deg_out[u]-=1; deg_in[v]-=1
        rem[a]+=1; rem[b]+=1
    rec(0); return res

def build(N,arcs):
    out=[0]*N; adj=[0]*N
    for u,v in arcs: out[u]|=1<<v; adj[u]|=1<<v; adj[v]|=1<<u
    return out,adj

if __name__=='__main__':
    m,n=int(sys.argv[1]),int(sys.argv[2])
    N,E=torus(m,n)
    ors=eulerian_orientations(N,E)
    print(f"C{m} x C{n}: {N} vertices, {len(E)} edges, {len(ors)} Eulerian orientations (all outdeg = indeg = 2)",flush=True)
    good=0; first=None
    for arcs in ors:
        out,adj=build(N,arcs)
        ok,_=kernel_perfect(N,out,adj)
        if ok:
            good+=1
            if first is None: first=arcs
    print("kernel-perfect ones:",good)
    if first: print("example:",first)
