# Cross-check of lift_k_set.py through an independent code path: the old odd-torus/strip_dp.py
# (column DP over all induced subdigraphs, written 2026-10-12, before the orchestrator's code).
# For each of the 12 Latin squares and k = 1..KMAX, build the lifted orientation of C3 x C_{3k}
# as an arc function and ask strip_dp for a kernel-less induced subdigraph.
# Run: ../env/bin/python lift_vs_strip_dp.py 8   (from odd-torus/ws-W5)
import contextlib, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(here))     # old odd-torus/ (strip_dp)
sys.path.insert(0, os.path.join(here, "orch"))  # first, so orch/automaton.py shadows the old automaton.py
import strip_dp
from latin_lift import latin_squares, column_arcs, row_arcs

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8

def lift_arc(L, n):
    def arc(u, v):
        (i, j), (i2, j2) = u, v
        if j == j2:
            return (i, i2) in column_arcs(L[j % 3])
        if j2 == (j + 1) % n:          # u is the left end of the row edge
            return row_arcs(L[j % 3], L[j2 % 3])[i] == +1
        return row_arcs(L[j2 % 3], L[j % 3])[i] == -1   # v is the left end
    return arc

devnull = open(os.devnull, "w")
for t, L in enumerate(latin_squares()):
    bad = []
    for k in range(1, KMAX + 1):
        n = 3 * k
        with contextlib.redirect_stderr(devnull):
            S = strip_dp.find_kernelless(n, lift_arc(L, n))
        if S is not None:
            bad.append(k)
    print(f"square #{t}: strip_dp kernel-less for k in 1..{KMAX}: {bad}", flush=True)
