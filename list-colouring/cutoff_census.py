"""Does raising the cutoff above 3 vertices give a richer class?"""
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "list-colouring"))
sys.path.insert(0, str(_root / "census-tool"))
from three_hereditary import certificate, chromatic_number
from twokernel.core import Digraph, bits, has_2kernel, popcount

def all_digraphs_bf(n):
    slots = [(u, v) for u in range(n) for v in range(n) if u != v]
    seen, out = set(), []
    for m in range(1 << len(slots)):
        D = Digraph.from_arcs(n, [slots[i] for i in range(len(slots)) if m >> i & 1])
        c = certificate(D)
        if c not in seen:
            seen.add(c); out.append(D)
    return out

def hered(D, k):
    s = D.full
    while True:
        if popcount(s) >= k and not has_2kernel(D.sub(s)):
            return False
        if s == 0: return True
        s = (s - 1) & D.full

def augment(prev, n, k):
    seen, out = set(), []
    new = n - 1
    for G in prev:
        base = list(G.arcs())
        for om in range(1 << new):
            for im in range(1 << new):
                D = Digraph.from_arcs(n, base + [(new,w) for w in bits(om)] + [(v,new) for v in bits(im)])
                if not hered(D, k): continue
                c = certificate(D)
                if c not in seen:
                    seen.add(c); out.append(D)
    return out

for k in (4, 5):
    level = all_digraphs_bf(k - 1)
    print(f"--- cutoff k={k}: every induced subdigraph on >= {k} vertices has a 2-d kernel", flush=True)
    for n in range(k, 9):
        level = augment(level, n, k)
        if not level:
            print(f"    n={n}: class is empty", flush=True); break
        chi = max(chromatic_number(D) for D in level)
        dmax = max(max(D.out_degree(v) for v in range(n)) for D in level)
        print(f"    n={n}: {len(level):5d} members, max chi = {chi}, max Delta+ = {dmax}", flush=True)
