"""Re-check a NONE result from its checkpoint, independently of the search loop.

1. Rebuild the master CNF from scratch: (L) lists of size k, the chosen symmetry/hypothesis
   constraints (same flags as the run), every stored cut AND its images under the same symmetry
   maps (recomputed here).
2. Verify EVERY clause that came from a cut (originals and images) with verify_cuts.verify_cut,
   i.e. re-derive the peeling certificate.
3. Solve the rebuilt CNF with a different SAT solver (default glucose4; option kissat via a DIMACS
   file is not used). UNSAT here confirms the run's final answer.
Optionally (--drat FILE) write a DRAT proof from glucose4 and the CNF in DIMACS (FILE.cnf).

Run: python certify.py torus M N Q CKPT [same flags as the run] [--solver NAME] [--drat FILE]
"""
import argparse
import time

from pysat.solvers import Solver

import cegar2
from graphs import adjacency, torus, complete_bipartite
from verify_cuts import verify_cut

ap = argparse.ArgumentParser()
ap.add_argument("kind")
ap.add_argument("a", type=int)
ap.add_argument("b", type=int)
ap.add_argument("q", type=int)
ap.add_argument("ckpt")
for f in ["colsym", "gsym", "crit", "overlap", "fix0"]:
    ap.add_argument("--" + f, action="store_true")
ap.add_argument("--orbit", choices=["graph", "colour", "both"])
ap.add_argument("--k", type=int, default=3)
ap.add_argument("--solver", default="glucose4")
ap.add_argument("--drat")
A = ap.parse_args()
import json
d = json.load(open(A.ckpt))
N, E = cegar2.build(A.kind, A.a, A.b)
adj = adjacency(N, E)
t0 = time.time()
S = cegar2.Search(N, E, A.q, A.k, colsym=A.colsym, fix0=A.fix0,
                  gsym=(A.a, A.b) if A.gsym else None, crit=A.crit, overlap=A.overlap,
                  solver="minisat22", log=lambda s: None)
maps = cegar2.orbit_maps(A, N) if A.orbit else []
clauses = list(S.base)
nver = nbad = 0
for cut in d["cuts"]:
    imgs = [[tuple(x) for x in cut]]
    for pv, pc in maps:
        imgs.append([("n", pv[x[1]], pc[x[2]]) if x[0] == "n"
                     else ("y", pv[x[1]], sorted(pc[a] for a in x[2]), x[3]) for x in cut])
    for img in imgs:
        nver += 1
        if not verify_cut(N, E, A.k, img, adj):
            nbad += 1
        clauses.append([S.lit(x) for x in img])
# aux definitions for y-literals were added to S.master by S.lit; collect them too
aux = []
for (tag, w, X, t), y in S.yvar.items():
    import itertools
    for Y in itertools.combinations(X, len(X) - t + 1):
        aux.append([-y] + [S.l[w, a] for a in Y])
clauses += aux
print(f"certify {A.kind} {A.a} {A.b} q={A.q} {A.ckpt}: {len(d['cuts'])} cuts, {nver} cut "
      f"clauses incl. images verified, {nbad} INVALID; CNF has {len(clauses)} clauses "
      f"({time.time() - t0:.0f}s)", flush=True)
t1 = time.time()
if A.drat:
    with Solver(name="glucose4", bootstrap_with=clauses, with_proof=True) as s:
        r = s.solve()
        if not r:
            with open(A.drat, "w") as f:
                f.write("\n".join(s.get_proof()) + "\n")
    from pysat.formula import CNF
    CNF(from_clauses=clauses).to_file(A.drat + ".cnf")
else:
    with Solver(name=A.solver, bootstrap_with=clauses) as s:
        r = s.solve()
print(f"independent re-solve with {A.solver if not A.drat else 'glucose4+proof'}: "
      f"{'SAT (disagrees!)' if r else 'UNSAT (agrees)'} in {time.time() - t1:.1f}s", flush=True)
