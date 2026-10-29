"""Phase 5: does L(G) have a kernel-perfect orientation with Delta+ <= k-1 (G k-regular)?

By the star lemma (list-colouring/09) and the odd-ring lemma (02-odd-ring-lemma.md) this is
equivalent to ranks r_u(v) in {0..k-1} with
  (1) each vertex's ranks a permutation of {0..k-1},
  (2) r_u(v) + r_v(u) = k-1 on every edge,
  (3) no odd ring: no odd cycle a_1..a_m with every a_i ranking a_{i+1} above a_{i-1}
      (above = smaller rank).
SAT encoding with pysat (CaDiCaL). Variables x[u,v,a] for u<v ("r_u(v) = a"); r_v(u) = a is the
same literal as x[u,v,k-1-a]. Order literals p[u,v,w] ("u ranks v above w") are defined
exactly from the x's. Ring clauses are added for every odd cycle up front.

Run: env/bin/python kernel_sat.py data/uncovered_N8.g6 [--cert-dir data/certs]
"""
import argparse
import json
import os
import sys
import time

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153


def odd_cycles(G):
    """Every odd simple cycle of G, once each, as a vertex list."""
    return [c for c in nx.simple_cycles(G) if len(c) % 2 == 1]


class Encoding:
    def __init__(self, G):
        self.G = G
        self.k = next(iter(dict(G.degree()).values()))
        self.pool = IDPool()
        self.clauses = []
        k = self.k
        for u, v in G.edges():
            for a in range(k):
                self.rank_lit(u, v, a)
        # (2) is built into rank_lit. Exactly one rank per edge, from u's side:
        for u, v in G.edges():
            lits = [self.rank_lit(u, v, a) for a in range(k)]
            self.add_card(lits)
        # (1) at each vertex, each rank value used exactly once
        for u in G:
            for a in range(k):
                self.add_card([self.rank_lit(u, v, a) for v in G[u]])
        # order literals
        for u in G:
            nb = sorted(G[u])
            for i, v in enumerate(nb):
                for w in nb[i + 1:]:
                    p = self.pool.id(("p", u, v, w))  # u ranks v above w
                    for a in range(k):
                        for b in range(k):
                            if a == b:
                                continue
                            # r_u(v)=a and r_u(w)=b  ->  p iff a < b
                            lit = p if a < b else -p
                            self.clauses.append([-self.rank_lit(u, v, a),
                                                 -self.rank_lit(u, w, b), lit])
        self.n_rings = 0

    def rank_lit(self, u, v, a):
        """Literal for r_u(v) = a."""
        if u < v:
            return self.pool.id(("x", u, v, a))
        return self.pool.id(("x", v, u, self.k - 1 - a))

    def prefers(self, u, v, w):
        """Literal for 'u ranks v above w'."""
        if v < w:
            return self.pool.id(("p", u, v, w))
        return -self.pool.id(("p", u, w, v))

    def add_card(self, lits):
        enc = CardEnc.equals(lits=lits, bound=1, vpool=self.pool, encoding=EncType.pairwise)
        self.clauses.extend(enc.clauses)

    def add_rings(self, cycles):
        for c in cycles:
            m = len(c)
            for seq in (c, c[::-1]):
                # forbid: every a_i prefers a_{i+1} over a_{i-1}
                self.clauses.append([-self.prefers(seq[i], seq[(i + 1) % m], seq[i - 1])
                                     for i in range(m)])
                self.n_rings += 1

    def decode(self, model):
        pos = {l for l in model if l > 0}
        r = {}
        for u, v in self.G.edges():
            for a in range(self.k):
                if self.rank_lit(u, v, a) in pos:
                    r[(u, v)] = a
                    r[(v, u)] = self.k - 1 - a
        return r


def solve(G):
    enc = Encoding(G)
    enc.add_rings(odd_cycles(G))
    t = time.time()
    with Cadical153(bootstrap_with=enc.clauses) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    return sat, (enc.decode(model) if sat else None), enc.n_rings, time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("g6file")
    ap.add_argument("--cert-dir", default="data/certs")
    args = ap.parse_args()
    os.makedirs(args.cert_dir, exist_ok=True)
    print("graph6,k,triangles,odd_ring_clauses,result,seconds")
    for line in open(args.g6file):
        g6 = line.strip()
        if not g6:
            continue
        G = nx.from_graph6_bytes(g6.encode())
        sat, r, nrings, secs = solve(G)
        tri = sum(nx.triangles(G).values()) // 3
        k = next(iter(dict(G.degree()).values()))
        print(f"{g6},{k},{tri},{nrings},{'SAT' if sat else 'UNSAT'},{secs:.2f}", flush=True)
        if sat:
            fn = os.path.join(args.cert_dir, g6.replace("/", "_") + ".json")
            with open(fn, "w") as f:
                json.dump({"graph6": g6, "k": k,
                           "ranks": [[u, v, a] for (u, v), a in sorted(r.items())]}, f)


if __name__ == "__main__":
    sys.exit(main())
