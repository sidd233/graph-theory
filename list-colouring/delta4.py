"""Does a triangle still force failure when Delta >= 4?

At Delta = 3 a single triangle is locally impossible (theorem in 11).  From Delta = 4
up, single triangles are locally fine, so if K_6, K_8 and K_2,2,2 still fail the cause
must be global.  Test more Delta >= 4 regular class-1 graphs WITH triangles, and some
triangle-free ones as controls.

NO order  => Lemma 1 provably fails for that G.
order     => inconclusive (the triangle test is only part of kernel-perfectness).
"""
from itertools import combinations
from tight_general import search
from galvin import chromatic_index


def mk(n, edges):
    adjlist = [[] for _ in range(n)]
    for u, v in edges:
        adjlist[u].append(v); adjlist[v].append(u)
    return edges, n, adjlist


def run(name, edges, n, adjlist):
    k = chromatic_index(edges, n)
    D = max(len(a) for a in adjlist)
    tri = sum(1 for a, b, c in combinations(range(n), 3)
              if b in adjlist[a] and c in adjlist[b] and c in adjlist[a])
    cls = 1 if k == D else 2
    sol = search(n, adjlist, k)
    print(f"  {name:22s} n={n:2d} Delta={D} chi'={k} class {cls} triangles={tri:3d}  "
          f"{'order exists' if sol else 'NO ORDER: Lemma 1 fails'}", flush=True)


print("Delta >= 4, regular, class 1, WITH triangles:")
run("K_2,2,2 (Delta 4)", *mk(6, [(i,j) for i in range(6) for j in range(i+1,6) if j-i != 3]))
run("K_4 box K_2 (Delta 4)", *mk(8, [(i,j) for i in range(4) for j in range(i+1,4)]
                                 + [(4+i,4+j) for i in range(4) for j in range(i+1,4)]
                                 + [(i,4+i) for i in range(4)]))
run("C_8(1,2) (Delta 4)", *mk(8, sorted({tuple(sorted((i,(i+d)%8))) for i in range(8)
                                         for d in (1,2)})))
run("K_8 minus PM (Delta 6)", *mk(8, [(i,j) for i in range(8) for j in range(i+1,8)
                                      if j-i != 4]))
run("K_6 (Delta 5)", *mk(6, [(i,j) for i in range(6) for j in range(i+1,6)]))

print("\ncontrols, triangle-free, regular, class 1 (triangle test is vacuous):")
run("K_4,4 (bipartite)", *mk(8, [(i,4+j) for i in range(4) for j in range(4)]))
run("C_5 x K_2", *mk(10, [(i,(i+1)%5) for i in range(5)]
                       + [(5+i,5+(i+1)%5) for i in range(5)]
                       + [(i,5+i) for i in range(5)]))
run("C_8(1,3) (Delta 4)", *mk(8, sorted({tuple(sorted((i,(i+d)%8))) for i in range(8)
                                         for d in (1,3)})))
