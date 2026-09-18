"""Would the halved bound be an improvement on the k=4 class, or is it already beaten?

For each member D with underlying graph G, compare
    halved   = ceil(Delta+(D)/2) + 1     the bound a 2-d kernel theorem would give
    kernel   = Delta+(D) + 1             the bound the ordinary kernel lemma gives
    colour   = degeneracy(G) + 1         the trivial greedy bound, always valid
    chi(G)                               the truth, from below
The route is only worth pursuing where halved < colour.
"""
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
        if popcount(s) >= k and not has_2kernel(D.sub(s)): return False
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

def degeneracy(D):
    adj = list(D.adj); alive = D.full; best = 0
    for _ in range(D.n):
        v = min(bits(alive), key=lambda u: popcount(adj[u] & alive))
        best = max(best, popcount(adj[v] & alive))
        alive &= ~(1 << v)
    return best

k = 4
level = all_digraphs_bf(k - 1)
print(f"cutoff k={k}")
print(f"{'n':>3} {'members':>7} {'halved<colour':>14} {'max gain':>9} {'max chi':>7}")
for n in range(k, 8):
    level = augment(level, n, k)
    wins, gain, chis = 0, 0, 0
    for D in level:
        dp = max(D.out_degree(v) for v in range(n))
        halved = -(-dp // 2) + 1
        colour = degeneracy(D) + 1
        if halved < colour:
            wins += 1
            gain = max(gain, colour - halved)
        chis = max(chis, chromatic_number(D))
    print(f"{n:>3} {len(level):>7} {wins:>14} {gain:>9} {chis:>7}")
