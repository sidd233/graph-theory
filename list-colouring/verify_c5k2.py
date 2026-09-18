"""Two follow-ups.

(1) The triangle test is VACUOUS for triangle-free G, so C_5 x K_2 passing it proves
    nothing on its own.  Build the orientation its order gives and run the full
    kernel-perfectness test on L(C_5 x K_2).
(2) Does the triangle obstruction hold for every triangle-containing regular class-1
    graph, or just the ones tried so far?
"""
from tight_general import search
from galvin import line_graph, chromatic_index, kernel_perfect
from itertools import combinations
import sys
pc = int.bit_count


def orient_from_M(edges, n, M, adjlist):
    """The star lemma turns M into the orientation of L(G): for e, f sharing w,
    e -> f exactly when M[w][other end of e] > M[w][other end of f]."""
    m = len(edges)
    adjL, _ = line_graph(edges, n)
    out = [0] * m
    for a in range(m):
        for b in range(m):
            if a == b or not (adjL[a] >> b) & 1:
                continue
            w = (set(edges[a]) & set(edges[b])).pop()
            ea = [x for x in edges[a] if x != w][0]
            eb = [x for x in edges[b] if x != w][0]
            if M[w][ea] > M[w][eb]:
                out[a] |= 1 << b
    return out, adjL, m


def run_full(name, edges, n):
    adjlist = [[] for _ in range(n)]
    for u, v in edges:
        adjlist[u].append(v); adjlist[v].append(u)
    k = chromatic_index(edges, n)
    M = search(n, adjlist, k)
    if M is None:
        print(f"  {name}: no order, Lemma 1 fails"); return
    out, adjL, m = orient_from_M(edges, n, M, adjlist)
    d = max(pc(x) for x in out)
    kp = kernel_perfect(out, adjL, m)
    print(f"  {name}: order found, Delta+(L(G)) = {d} (need <= {k-1}), "
          f"kernel-perfect = {kp}"
          f"  -> Lemma 1 {'PROVES' if kp and d <= k-1 else 'does not prove'} this case")


print("(1) full check on the triangle-free non-bipartite case:")
c5k2 = ([(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+1)%5) for i in range(5)]
        + [(i,5+i) for i in range(5)])
run_full("C_5 x K_2", c5k2, 10)

print("\n(2) more triangle-containing regular class-1 graphs:")
for name, edges, n in [
    ("K_3,3,3", [(i,j) for i in range(9) for j in range(i+1,9) if i//3 != j//3], 9),
    ("K_5 minus PM?  K_4", [(i,j) for i in range(4) for j in range(i+1,4)], 4),
    ("C_3 x K_2 (prism)", [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)], 6),
]:
    adjlist = [[] for _ in range(n)]
    for u, v in edges:
        adjlist[u].append(v); adjlist[v].append(u)
    k = chromatic_index(edges, n)
    tri = sum(1 for a,b,c in combinations(range(n),3)
              if b in adjlist[a] and c in adjlist[b] and c in adjlist[a])
    sol = search(n, adjlist, k)
    print(f"  {name:20s} Delta={max(len(a) for a in adjlist)} chi'={k} "
          f"triangles={tri}  {'order exists' if sol else 'NO ORDER: Lemma 1 fails'}")
