"""The star-lemma search for any G, not just the regular class-1 case.

Kernel-perfect orientation of L(G)  =>  a linear order at each vertex of G
    M(u, .) is a bijection onto {0, ..., d_u - 1},   d+(uv) = M(u,v) + M(v,u).
Lemma 1 with lists of size k therefore needs  M(u,v) + M(v,u) <= k - 1  everywhere,
plus kernel-perfectness.  A necessary part of the latter: no triangle of G may come
out cyclic in L(G).  With p = M(i,j), q = M(j,k), r = M(i,k) and t = the relevant
comparisons, the triangle is cyclic exactly when

    (M(j,i) > q and r > M(k,i) and r > p)  reading the three shared vertices,

written out directly below to avoid sign slips.

NO solution  =>  Lemma 1 provably cannot prove the conjecture for that G.
A solution   =>  inconclusive, since cyclic triangles are only part of the condition.
"""
from itertools import combinations
from galvin import chromatic_index


def search(n, adjlist, k):
    verts = range(n)
    deg = [len(adjlist[u]) for u in verts]
    tri = [(a, b, c) for a, b, c in combinations(verts, 3)
           if b in adjlist[a] and c in adjlist[b] and c in adjlist[a]]
    edges = [(u, v) for u in verts for v in adjlist[u] if u < v]
    rank = {e: i for i, e in enumerate(edges)}
    tri_at = {e: [] for e in edges}
    for (a, b, c) in tri:
        last = max((a, b), (b, c), (a, c), key=lambda e: rank[e])
        tri_at[last].append((a, b, c))
    M = [[None] * n for _ in verts]

    def cyclic(i, j, l):
        # edges e=ij, f=jl, g=il ; shared vertices j, l, i
        if any(M[a][b] is None for a, b in ((i,j),(j,l),(i,l))):
            return False
        ef = M[j][i] > M[j][l]          # e -> f at j
        fg = M[l][j] > M[l][i]          # f -> g at l
        ge = M[i][l] > M[i][j]          # g -> e at i
        return (ef and fg and ge) or (not ef and not fg and not ge)

    def go(t):
        if t == len(edges):
            return [row[:] for row in M]
        u, v = edges[t]
        used_u = {M[u][w] for w in adjlist[u] if M[u][w] is not None}
        used_v = {M[v][w] for w in adjlist[v] if M[v][w] is not None}
        for a in range(deg[u]):
            if a in used_u:
                continue
            for b in range(deg[v]):
                if b in used_v or a + b > k - 1:
                    continue
                M[u][v], M[v][u] = a, b
                if not any(cyclic(*x) for x in tri_at[(u, v)]):
                    r = go(t + 1)
                    if r: return r
                M[u][v] = M[v][u] = None
        return None
    return go(0)


def run(name, edges, n, bipartite):
    adjlist = [[] for _ in range(n)]
    for u, v in edges:
        adjlist[u].append(v); adjlist[v].append(u)
    k = chromatic_index(edges, n)
    D = max(len(a) for a in adjlist)
    sol = search(n, adjlist, k)
    cls = 1 if k == D else 2
    print(f"  {name:18s} Delta={D} chi'={k} (class {cls}) "
          f"{'bipartite' if bipartite else 'NON-bip  '}  "
          f"{'order exists' if sol else 'NO ORDER: Lemma 1 fails'}")


print("bipartite (Galvin's theorem covers these, so an order must exist):")
run("K_3,3", [(i,3+j) for i in range(3) for j in range(3)], 6, True)
run("K_4,4", [(i,4+j) for i in range(4) for j in range(4)], 8, True)
run("cube Q_3", [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                 (0,4),(1,5),(2,6),(3,7)], 8, True)
run("C_6", [(i,(i+1)%6) for i in range(6)], 6, True)

print("\nnon-bipartite, regular, class 1 (the tight regime):")
run("K_4", [(i,j) for i in range(4) for j in range(i+1,4)], 4, False)
run("K_6", [(i,j) for i in range(6) for j in range(i+1,6)], 6, False)
run("prism", [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)], 6, False)
run("K_2,2,2", [(i,j) for i in range(6) for j in range(i+1,6) if j-i != 3], 6, False)
run("C_5 x K_2", [(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+1)%5) for i in range(5)]
               + [(i,5+i) for i in range(5)], 10, False)

print("\nnon-bipartite, NOT in the tight regime (class 2, so there is slack):")
run("C_5", [(i,(i+1)%5) for i in range(5)], 5, False)
run("C_7", [(i,(i+1)%7) for i in range(7)], 7, False)
run("Petersen", [(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+2)%5) for i in range(5)]
              + [(i,5+i) for i in range(5)], 10, False)
