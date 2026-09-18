"""Joint census, pushed up in size.  Which of the two methods covers each G?"""
from itertools import combinations, permutations
from at_fast import alon_tarsi_fast, line_graph_edges
from galvin import chromatic_index, line_graph
from kernel_search import find
import sys
pc = int.bit_count

maxn, maxe = int(sys.argv[1]), int(sys.argv[2])
seen = set()
tally = {(1,1):0, (1,0):0, (0,1):0, (0,0):0}
notes = {(1,0):[], (0,1):[], (0,0):[]}
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
        adjL, m = line_graph(edges, n)
        ci = chromatic_index(edges, n)
        kr = 1 if find(adjL, m, ci - 1) else 0
        at = 1 if alon_tarsi_fast(line_graph_edges(edges)[0], m) <= ci else 0
        tally[(kr, at)] += 1
        if (kr, at) in notes and len(notes[(kr, at)]) < 6:
            notes[(kr, at)].append((edges, ci))
    print(f"  through n={n}: both={tally[(1,1)]} kernel-only={tally[(1,0)]} "
          f"AT-only={tally[(0,1)]} NEITHER={tally[(0,0)]}")
print(f"\n{'':18s} {'AT works':>10} {'AT fails':>10}")
print(f"{'kernel works':18s} {tally[(1,1)]:>10} {tally[(1,0)]:>10}")
print(f"{'kernel fails':18s} {tally[(0,1)]:>10} {tally[(0,0)]:>10}")
for cell, lab in [((1,0),"kernel only"), ((0,1),"Alon-Tarsi only"), ((0,0),"NEITHER")]:
    if notes[cell]:
        print(f"\n{lab}:")
        for e, c in notes[cell]:
            print(f"    chi'={c} G={e}")
