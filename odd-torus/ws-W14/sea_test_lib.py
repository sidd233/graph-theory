import itertools, re
E=[(0,1),(1,2),(3,4),(4,5),(0,3),(1,4),(2,5)]
onb={0:[6,10],1:[7],2:[8,9],3:[13,12],4:[14],5:[15,11]}
for k,vs in onb.items(): E+=[(k,v) for v in vs]
E+=[(6,7),(7,8),(9,10),(11,12),(9,11),(10,12),(13,14),(14,15)]
adj={i:set() for i in range(16)}
for a,b in E: adj[a].add(b); adj[b].add(a)
pos={0:(-1,0),1:(0,0),2:(1,0),3:(-1,1),4:(0,1),5:(1,1),6:(-1,-1),7:(0,-1),8:(1,-1),9:(2,0),10:(3,0),11:(2,1),12:(3,1),13:(-1,2),14:(0,2),15:(1,2)}
def generalized_sea(lists):
    """exists S (colour set) with pi: S -> Z3 bijective on every sea list (lists inside S), defects = lists not
       inside S coloured from colours outside S (at most one T-vertex per column using a pi-colour)."""
    cols=sorted(set().union(*lists))
    for r in range(3, len(cols)+1):
        for S in itertools.combinations(cols, r):
            S=set(S); sea=[v for v in range(16) if lists[v] <= S]
            if not sea: continue
            # pi must be proper on the co-occurrence graph of sea lists
            adjc={c:set() for c in S}
            for v in sea:
                for a,b in itertools.combinations(lists[v],2): adjc[a].add(b); adjc[b].add(a)
            Sl=sorted(S); pi={}
            def colpi(i):
                if i==len(Sl): return True
                c=Sl[i]
                for x in range(3):
                    if all(pi.get(d)!=x for d in adjc[c]):
                        pi[c]=x
                        if colpi(i+1): return True
                        del pi[c]
                return False
            if not colpi(0): continue
            D=[v for v in range(16) if v not in sea]; O={v:sorted(lists[v]-S) for v in D}
            if any(not O[v] for v in D): continue
            Tc=[v for v in D if len(O[v])==1]
            for k in range(0,3):
                for T in itertools.combinations(Tc,k):
                    if len({pos[v][1] for v in T})<len(T): continue
                    Dp=[v for v in D if v not in T]; col={}
                    def go(i):
                        if i==len(Dp): return True
                        v=Dp[i]
                        for c in O[v]:
                            if all(col.get(w)!=c for w in adj[v] if w in col):
                                col[v]=c
                                if go(i+1): return True
                                del col[v]
                        return False
                    if go(0): return (S,T)
    return None
def parse(txt):
    return [[frozenset(c for c in range(16) if int(h,16)>>c&1) for h in m.group(1).split()+m.group(2).split()]
            for m in re.finditer(r'FAIL block((?: [0-9a-f]+){6}) border((?: [0-9a-f]+){10})', txt)]
