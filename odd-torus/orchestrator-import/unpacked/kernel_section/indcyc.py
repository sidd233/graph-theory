import sys, random
from kp import torus, eulerian_orientations, build

def find_induced_odd_dicycle(N,out,adj,maxlen=None):
    # DFS for induced directed cycles; returns one odd one if found
    best=None
    for s in range(N):
        # paths starting at s, only through vertices > s (each cycle found once, from its min vertex)
        stack=[(s,1<<s,[s])]
        while stack:
            v,used,path=stack.pop()
            for w in range(s,N):
                if not (out[v]>>w&1): continue
                if w==s:
                    L=len(path)
                    if L>=3 and L%2==1:
                        U=used
                        # induced: each vertex has exactly one out- and in-neighbour inside U
                        if all(bin(out[x]&U).count('1')==1 for x in path) and all(bin(adj[x]&U).count('1')==2 for x in path):
                            return path
                    continue
                if used>>w&1: continue
                # keep path induced-chordless: w must not be adjacent to earlier path vertices except v (and s allowed as closing)
                if adj[w]&used&~(1<<v)&~(1<<s): continue
                if maxlen and len(path)>=maxlen: continue
                stack.append((w,used|1<<w,path+[w]))
    return None

def random_eulerian(N,E,rng):
    # random Eulerian orientation via randomized backtracking (one solution)
    import kp
    random.seed(rng.random())
    return kp.eulerian_orientations(N,E,limit=1,shuffle=True)[0]

if __name__=='__main__':
    m,n=int(sys.argv[1]),int(sys.argv[2]); mode=sys.argv[3]
    N,E=torus(m,n); rng=random.Random(1)
    if mode=='all':
        ors=eulerian_orientations(N,E)
    else:
        ors=[random_eulerian(N,E,rng) for _ in range(int(mode))]
    lens={}; none=0
    for arcs in ors:
        out,adj=build(N,arcs)
        c=find_induced_odd_dicycle(N,out,adj)
        if c is None: none+=1
        else: lens[len(c)]=lens.get(len(c),0)+1
    print(f"C{m}xC{n} [{mode}] orientations checked: {len(ors)}; with an induced odd directed cycle: {len(ors)-none}; WITHOUT: {none}; lengths found: {dict(sorted(lens.items()))}",flush=True)
