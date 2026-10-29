"""Phase 3: which zero-sum graphs are already covered by known LECC theorems?

Tests, each a theorem proving ch'(G) = chi'(G):
  bipartite          Galvin (1995)
  planar             Ellingham and Goddyn (1996): d-regular d-edge-colourable planar
                     multigraphs are d-edge-choosable (all our graphs are regular class 1)
  bip_minus_vertex   Peterson and Woodall: G - v bipartite for some v
  line_perfect       Peterson and Woodall: no odd cycle of length >= 5
  complete           K_n results (Haggkvist-Janssen, Schauz, Jafari)
Run: env/bin/python known.py   -> data/known_N8.csv, data/known_N10.csv, summary on stdout
"""
import csv

import networkx as nx


def has_long_odd_cycle(G):
    """True iff G has an odd cycle of length >= 5 (simple cycles via chordless search is not
    enough, so we use networkx simple_cycles on the undirected graph; fine at 10 vertices)."""
    for c in nx.simple_cycles(G):
        if len(c) >= 5 and len(c) % 2 == 1:
            return True
    return False


def coverage(G):
    n = G.number_of_nodes()
    tests = {
        "bipartite": nx.is_bipartite(G),
        "planar": nx.check_planarity(G)[0],
        "bip_minus_vertex": any(nx.is_bipartite(G.subgraph(set(G) - {v})) for v in G),
        "line_perfect": not has_long_odd_cycle(G),
        "complete": G.number_of_edges() == n * (n - 1) // 2,
    }
    return tests


def main():
    for N in (8, 10):
        out = []
        for line in open(f"data/zero_sum_N{N}.g6"):
            g6 = line.strip()
            G = nx.from_graph6_bytes(g6.encode())
            k = next(iter(dict(G.degree()).values()))
            t = coverage(G)
            covered = [name for name, v in t.items() if v]
            out.append({"graph6": g6, "N": N, "k": k,
                        "triangles": sum(nx.triangles(G).values()) // 3,
                        "two_connected": nx.is_biconnected(G),
                        **t, "covered_by": "+".join(covered) or "-"})
        with open(f"data/known_N{N}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
        unc = [r for r in out if r["covered_by"] == "-"]
        print(f"N={N}: zero-sum={len(out)} covered={len(out) - len(unc)} uncovered={len(unc)}")
        for r in out:
            if r["covered_by"] != "-":
                print(f"   covered  {r['graph6']}  k={r['k']}  by {r['covered_by']}")
        byk = {}
        for r in unc:
            byk[r["k"]] = byk.get(r["k"], 0) + 1
        print(f"   uncovered by degree: {dict(sorted(byk.items()))}")
        with open(f"data/uncovered_N{N}.g6", "w") as f:
            f.writelines(r["graph6"] + "\n" for r in unc)


if __name__ == "__main__":
    main()
