"""Which of the two methods proves the conjecture for each small G?

kernel  : does L(G) have a kernel-perfect orientation with Delta+ <= chi'(G) - 1?
          (Lemma 1 of chapter 33; this is what Galvin builds for bipartite G)
AT      : is AT(L(G)) <= chi'(G)?
          (Alon-Tarsi)
Both are sufficient.  Neither implies the other, as S_3 and L(K_4) show.
The interesting cell is where BOTH fail.
"""
from itertools import combinations, permutations
from at_fast import alon_tarsi_fast, line_graph_edges
from galvin import chromatic_index, line_graph, kernel_perfect
import sys
pc = int.bit_count


def kernel_route(edges, n):
    adj, m = line_graph(edges, n)
    k = chromatic_index(edges, n)
    cap = k - 1
    pairs = [(i, j) for i in range(m) for j in range(i + 1, m) if (adj[i] >> j) & 1]
    for code in range(1 << len(pairs)):
        out = [0] * m
        for t, (i, j) in enumerate(pairs):
            if (code >> t) & 1: out[i] |= 1 << j
            else:               out[j] |= 1 << i
        if max((pc(x) for x in out), default=0) > cap:
            continue
        if kernel_perfect(out, adj, m):
            return True, k
    return False, k


maxn, maxe = int(sys.argv[1]), int(sys.argv[2])
seen = set()
tally = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
notes = {(True, False): [], (False, True): [], (False, False): []}
for n in range(2, maxn + 1):
    for code in range(1 << (n * (n - 1) // 2)):
        pairs = list(combinations(range(n), 2))
        edges = [pairs[i] for i in range(len(pairs)) if (code >> i) & 1]
        if not edges or len(edges) > maxe: continue
        if len({x for e in edges for x in e}) != n: continue
        key = min(tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))
                  for p in permutations(range(n)))
        if key in seen: continue
        seen.add(key)
        le, m = line_graph_edges(edges)
        kr, ci = kernel_route(edges, n)
        at = alon_tarsi_fast(le, m)
        cell = (kr, at <= ci)
        tally[cell] += 1
        if cell in notes and len(notes[cell]) < 4:
            notes[cell].append((edges, ci, at))
print(f"{'':22s} {'AT works':>10} {'AT fails':>10}")
print(f"{'kernel works':22s} {tally[(True,True)]:>10} {tally[(True,False)]:>10}")
print(f"{'kernel fails':22s} {tally[(False,True)]:>10} {tally[(False,False)]:>10}")
for cell, label in [((True, False), "kernel only"), ((False, True), "Alon-Tarsi only"),
                    ((False, False), "NEITHER")]:
    if notes[cell]:
        print(f"\n{label}:")
        for edges, ci, at in notes[cell]:
            print(f"    chi'={ci} AT={at} G={edges}")
