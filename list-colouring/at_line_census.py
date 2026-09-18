"""Census: does AT(L(G)) = chi'(G) for small G?

chi(L(G)) = chi'(G) <= chi_ell(L(G)) <= AT(L(G)).  So AT(L(G)) = chi'(G) PROVES the
conjecture for that G, and AT(L(G)) > chi'(G) means Alon-Tarsi cannot prove it for
that G, exactly as the octahedron computation showed for the kernel lemma at K_4.
"""
from itertools import combinations, permutations
from at_fast import alon_tarsi_fast, line_graph_edges
from galvin import chromatic_index
import sys
pc = int.bit_count

maxn = int(sys.argv[1]); maxe = int(sys.argv[2])
seen = set()
proved = failed = 0
fails = []
for n in range(2, maxn + 1):
    pairs = list(combinations(range(n), 2))
    for code in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if (code >> i) & 1]
        if not edges or len(edges) > maxe:
            continue
        # skip graphs with isolated vertices, they duplicate smaller n
        if len({x for e in edges for x in e}) != n:
            continue
        key = min(tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))
                  for p in permutations(range(n)))
        if key in seen:
            continue
        seen.add(key)
        m = len(edges)
        le, _ = line_graph_edges(edges)
        ci = chromatic_index(edges, n)
        at = alon_tarsi_fast(le, m)
        if at == ci:
            proved += 1
        else:
            failed += 1
            fails.append((n, edges, ci, at))
    print(f"  through n={n}: {proved} with AT(L(G)) = chi'(G), {failed} where AT is larger")
print(f"\ntotal {proved + failed} graphs: AT(L(G)) = chi'(G) in {proved}, "
      f"AT(L(G)) > chi'(G) in {failed}")
for n, edges, ci, at in fails[:10]:
    print(f"    n={n} chi'={ci} AT={at} edges={edges}")
