"""Kernel method on the toroidal grid T(m, n) = C_m x C_n with lists of size 3.

Question: does T(m, n) have an orientation with every out-degree at most 2 that is
kernel-perfect?  (T is 4-regular with 2mn edges, so out-degree <= 2 forces exactly 2: an
Eulerian orientation.)  If yes, the kernel lemma gives ch(T) <= 3.

Method: SAT over edge orientations with out-degree exactly 2 (pysat, CaDiCaL), refined lazily.
Each candidate orientation is checked by kp_check.c, which returns a smallest kernel-less
induced subdigraph D[S].  The clause "not this orientation on the edges inside S" is added,
together with its images under all automorphisms of the torus (translations, reflections, and
the transposition when m = n).  Ends with a kernel-perfect orientation (checked on every
induced subdigraph) or UNSAT (no such orientation exists).

Run: ../lecc-small/env/bin/python kernel_torus.py m n [--all]
"""
import argparse
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

from kpc import find_kernelless


def torus(m, n):
    """Vertices (i, j) numbered i*n + j; edges as (u, w) pairs in canonical direction."""
    idx = lambda i, j: (i % m) * n + (j % n)
    edges = []
    for i in range(m):
        for j in range(n):
            edges.append((idx(i, j), idx(i + 1, j)))  # vertical
            edges.append((idx(i, j), idx(i, j + 1)))  # horizontal
    return idx, edges


def automorphisms(m, n):
    """Vertex permutations of the torus: translations, reflections, transposition if m = n."""
    maps = []
    for a in range(m):
        for b in range(n):
            for si in (1, -1):
                for sj in (1, -1):
                    maps.append(lambda i, j, a=a, b=b, si=si, sj=sj: ((si * i + a) % m, (sj * j + b) % n))
                    if m == n:
                        maps.append(lambda i, j, a=a, b=b, si=si, sj=sj: ((sj * j + b) % n, (si * i + a) % m))
    perms = set()
    for f in maps:
        perms.add(tuple(f(v // n, v % n)[0] * n + f(v // n, v % n)[1] for v in range(m * n)))
    return sorted(perms)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("n", type=int)
    ap.add_argument("--all", action="store_true", help="enumerate all kernel-perfect orientations")
    args = ap.parse_args()
    m, n = args.m, args.n
    N = m * n
    idx, edges = torus(m, n)
    pool = IDPool()
    var = {}
    for e, (u, w) in enumerate(edges):
        var[(u, w)] = pool.id(("e", e))  # true: u -> w
        var[(w, u)] = -var[(u, w)]
    nbrs = [[] for _ in range(N)]
    for u, w in edges:
        nbrs[u].append(w)
        nbrs[w].append(u)
    solver = Cadical153()
    for v in range(N):
        lits = [var[(v, w)] for w in nbrs[v]]
        cnf = CardEnc.equals(lits=lits, bound=2, vpool=pool, encoding=EncType.seqcounter)
        solver.append_formula(cnf.clauses)
    perms = automorphisms(m, n)
    t0 = time.time()
    refinements = 0
    sizes = {}
    found = 0
    while solver.solve():
        model = set(l for l in solver.get_model() if l > 0)
        out = [0] * N
        for (u, w), x in var.items():
            if x > 0 and x in model:
                out[u] |= 1 << w
            elif x < 0 and -x not in model:
                out[u] |= 1 << w
        S = find_kernelless(out)
        if S == 0:
            found += 1
            arcs = [(u, w) for u in range(N) for w in range(N) if out[u] >> w & 1]
            print(f"KERNEL-PERFECT orientation #{found} after {refinements} refinements:")
            print("  arcs (i,j)->(i',j'):", " ".join(f"{u // n}{u % n}>{w // n}{w % n}" for u, w in arcs))
            if not args.all:
                break
            solver.add_clause([-var[a] for a in arcs])  # block exactly this orientation
            continue
        refinements += 1
        k = bin(S).count("1")
        sizes[k] = sizes.get(k, 0) + 1
        inside = [(u, w) for u in range(N) if S >> u & 1 for w in nbrs[u]
                  if S >> w & 1 and out[u] >> w & 1]
        for p in perms:
            solver.add_clause([var[(p[w], p[u])] for u, w in inside])
        if refinements % 200 == 0:
            print(f"  {refinements} refinements, {time.time() - t0:.0f}s, kernel-less sizes {dict(sorted(sizes.items()))}",
                  file=sys.stderr, flush=True)
    else:
        if found == 0:
            print(f"UNSAT: T({m},{n}) has no kernel-perfect orientation with out-degree <= 2")
    print(f"T({m},{n}): {found} kernel-perfect found, {refinements} refinements, "
          f"kernel-less set sizes {dict(sorted(sizes.items()))}, {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
