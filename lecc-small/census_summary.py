"""Summarise data/census_N*.csv (Phase 2) and write data/zero_sum_N*.g6.

K_10 (k = 9) and K_10 minus a perfect matching (k = 8) are not in census_N10.csv: about 1e9
colourings each, too many for at_sign.py. Both are settled already (Jafari 2026; Rabern), and
neither is a candidate here.
Run: env/bin/python census_summary.py
"""
import collections
import csv

import networkx as nx

for N in (8, 10):
    rows = list(csv.DictReader(open(f"data/census_N{N}.csv")))
    cls1 = [r for r in rows if int(r["colourings_v0_fixed"]) > 0]
    zs = [r for r in cls1 if int(r["S"]) == 0]
    byk = dict(sorted(collections.Counter(int(r["k"]) for r in zs).items()))
    print(f"N={N}: graphs={len(rows)} class1={len(cls1)} class2={len(rows) - len(cls1)} "
          f"zero-sum={len(zs)} by degree {byk}")
    with open(f"data/zero_sum_N{N}.g6", "w") as f:
        f.writelines(r["graph6"] + "\n" for r in zs)

zs = [nx.from_graph6_bytes(l.strip().encode()) for l in open("data/zero_sum_N8.g6")]
C = nx.complement(nx.disjoint_union(nx.cycle_graph(3), nx.cycle_graph(5)))
print("N=8: complement of C3+C5 among zero-sum:", any(nx.is_isomorphic(C, g) for g in zs))
print("N=8: the k=3 and k=4 zero-sum graphs are complements:",
      nx.is_isomorphic(nx.complement(zs[0]), zs[1]))
