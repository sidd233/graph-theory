"""Joint census, using the star-lemma reduction on the kernel side.

Kernel side: enumerate every linear-order system M with M(u,v)+M(v,u) <= chi'-1 and
no cyclic triangle (both necessary), then run the full kernel-perfectness test on the
orientation each one gives.  The method WORKS for G iff some M passes both.
Alon-Tarsi side: AT(L(G)) <= chi'(G).
"""
from itertools import combinations, permutations
from at_fast import alon_tarsi_fast, line_graph_edges
from galvin import chromatic_index, line_graph
from bkw import kernel_perfect_bkw as kernel_perfect
import sys
pc = int.bit_count


def all_orders(n, adjlist, k):
    deg = [len(adjlist[u]) for u in range(n)]
    tri = [(a, b, c) for a, b, c in combinations(range(n), 3)
           if b in adjlist[a] and c in adjlist[b] and c in adjlist[a]]
    edges = [(u, v) for u in range(n) for v in adjlist[u] if u < v]
    rank = {e: i for i, e in enumerate(edges)}
    fire = {e: [] for e in edges}
    for (a, b, c) in tri:
        fire[max((a,b),(b,c),(a,c), key=lambda e: rank[e])].append((a, b, c))
    M = [[None] * n for _ in range(n)]

    def cyclic(i, j, l):
        ef = M[j][i] > M[j][l]; fg = M[l][j] > M[l][i]; ge = M[i][l] > M[i][j]
        return (ef and fg and ge) or (not ef and not fg and not ge)

    def go(t):
        if t == len(edges):
            yield [r[:] for r in M]; return
        u, v = edges[t]
        uu = {M[u][w] for w in adjlist[u] if M[u][w] is not None}
        vv = {M[v][w] for w in adjlist[v] if M[v][w] is not None}
        for a in range(deg[u]):
            if a in uu: continue
            for b in range(deg[v]):
                if b in vv or a + b > k - 1: continue
                M[u][v], M[v][u] = a, b
                if not any(cyclic(*x) for x in fire[(u, v)]):
                    yield from go(t + 1)
                M[u][v] = M[v][u] = None
    yield from go(0)


def kernel_works(edges, n, adjlist, k):
    adjL, m = line_graph(edges, n)
    for M in all_orders(n, adjlist, k):
        out = [0] * m
        for a in range(m):
            for b in range(m):
                if a != b and (adjL[a] >> b) & 1:
                    w = (set(edges[a]) & set(edges[b])).pop()
                    ea = [x for x in edges[a] if x != w][0]
                    eb = [x for x in edges[b] if x != w][0]
                    if M[w][ea] > M[w][eb]:
                        out[a] |= 1 << b
        if max((pc(x) for x in out), default=0) <= k - 1 and kernel_perfect(out, adjL, m):
            return True
    return False


maxn, maxe = int(sys.argv[1]), int(sys.argv[2])
seen = set(); tally = {(1,1):0,(1,0):0,(0,1):0,(0,0):0}; notes = {(1,0):[],(0,1):[],(0,0):[]}
for n in range(2, maxn + 1):
    pairs = list(combinations(range(n), 2))
    for code in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if (code >> i) & 1]
        if not edges or len(edges) > maxe: continue
        if len({x for e in edges for x in e}) != n: continue
        key = min(tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))
                  for p in permutations(range(n)))
        if key in seen: continue
        seen.add(key)
        adjlist = [[] for _ in range(n)]
        for u, v in edges:
            adjlist[u].append(v); adjlist[v].append(u)
        k = chromatic_index(edges, n)
        kr = 1 if kernel_works(edges, n, adjlist, k) else 0
        at = 1 if alon_tarsi_fast(line_graph_edges(edges)[0], len(edges)) <= k else 0
        tally[(kr, at)] += 1
        if (kr, at) in notes and len(notes[(kr, at)]) < 8:
            notes[(kr, at)].append((edges, k))
    print(f"  through n={n}: both={tally[(1,1)]} kernel-only={tally[(1,0)]} "
          f"AT-only={tally[(0,1)]} NEITHER={tally[(0,0)]}", flush=True)
print(f"\n{'':18s} {'AT works':>10} {'AT fails':>10}")
print(f"{'kernel works':18s} {tally[(1,1)]:>10} {tally[(1,0)]:>10}")
print(f"{'kernel fails':18s} {tally[(0,1)]:>10} {tally[(0,0)]:>10}")
for cell, lab in [((1,0),"kernel only"),((0,1),"Alon-Tarsi only"),((0,0),"NEITHER")]:
    if notes[cell]:
        print(f"\n{lab}:")
        for e, c in notes[cell]: print(f"    chi'={c} G={e}")
