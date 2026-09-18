"""(R2) again, with the object the accounting lemma really requires.

Note `01` states requirement (R2) using (star): for every `W` and every `S` inside `W` there
is a nonempty independent `K` inside `S` such that every `u` in `S \\ K` adjacent to `K` has at
least **two** out-neighbours in `K`.  Proposition 01 then kills it: no digraph with an arc
satisfies (star).

But (star) is stronger than Definition 14.1 requires.  The accounting lemma only asks for

    f(d+(u)) - f(d+(u) - |N+(u) cap K|) >= 1,      degrees in W,

and with `f(d) = ceil(d/2) + 1` that is satisfied by a *single* out-neighbour in `K` when
`d+(u)` is odd.  Note 14.6 exhibits the single arc `u -> v` passing, so the two-vertex barrier
does not apply to the real requirement.

Call `D` **parity-processable** when for every induced subdigraph `W` and every `S` inside `W`
such a `K` exists.  This is (R2) and (R3) together, stated correctly.  The property is closed
under induced subdigraphs, so the class is enumerated by canonical augmentation.

The question: is this class richer than arcless, the way the corrected barrier suggests it
should be?

Run: `python list-colouring/parity_processable.py [max_n]`
"""

import sys
from itertools import combinations
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "list-colouring"))
sys.path.insert(0, str(_root / "census-tool"))

from three_hereditary import certificate, chromatic_number
from twokernel.core import Digraph, bits, popcount


def f_half(d):
    return -(-d // 2) + 1


def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & mask


def independent_subsets(D, mask):
    verts = list(bits(mask))
    for size in range(1, len(verts) + 1):
        for combo in combinations(verts, size):
            m, ok = 0, True
            for v in combo:
                if D.adj[v] & m:
                    ok = False
                    break
                m |= 1 << v
            if ok:
                yield m


def pair_is_good(W, S, f):
    """Is there a legitimate K inside S?  Degrees are taken in W."""
    for K in independent_subsets(W, S):
        good = True
        for u in bits(S & ~K):
            if not (W.adj[u] & K):
                continue
            d = popcount(W.out[u])
            a = popcount(W.out[u] & K)
            if f(d) - f(d - a) < 1:
                good = False
                break
        if good:
            return True
    return False


def is_parity_processable(D, f=f_half):
    for wmask in submasks(D.full):
        if wmask == 0:
            continue
        W = D.sub(wmask)
        for smask in submasks(W.full):
            if smask == 0:
                continue
            if not pair_is_good(W, smask, f):
                return False
    return True


def augment(previous, n):
    seen, result = set(), []
    new = n - 1
    for G in previous:
        base = list(G.arcs())
        for out_mask in range(1 << new):
            for in_mask in range(1 << new):
                arcs = base + [(new, w) for w in bits(out_mask)]
                arcs += [(v, new) for v in bits(in_mask)]
                D = Digraph.from_arcs(n, arcs)
                if not is_parity_processable(D):
                    continue
                cert = certificate(D)
                if cert not in seen:
                    seen.add(cert)
                    result.append(D)
    return result


def degeneracy(D):
    adj, alive, best = list(D.adj), D.full, 0
    for _ in range(D.n):
        v = min(bits(alive), key=lambda u: popcount(adj[u] & alive))
        best = max(best, popcount(adj[v] & alive))
        alive &= ~(1 << v)
    return best


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    level = [Digraph.from_arcs(1, [])]
    print("parity-processable digraphs: every (W, S) admits a legitimate K\n")
    print(f"{'n':>3} {'members':>8} {'with an arc':>12} {'max chi':>8} {'max Delta+':>11}"
          f" {'max edges':>10} {'max degen':>10} {'halved<greedy':>14}")
    for n in range(2, max_n + 1):
        level = augment(level, n)
        if not level:
            print(f"{n:>3} class is empty")
            break
        arced = [D for D in level if D.num_arcs > 0]
        chi = max(chromatic_number(D) for D in level)
        dmax = max(max(D.out_degree(v) for v in range(n)) for D in level)
        wins = sum(
            1
            for D in level
            if -(-max(D.out_degree(v) for v in range(n)) // 2) + 1 < degeneracy(D) + 1
        )
        print(f"{n:>3} {len(level):>8} {len(arced):>12} {chi:>8} {dmax:>11}"
              f" {max(D.num_edges for D in level):>10}"
              f" {max(degeneracy(D) for D in level):>10} {wins:>14}")
    print()
    print("digons break the parity escape, so dense orientations do not survive:")
    for name, arcs in [
        ("directed C4  ", [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("bidirected C4", [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 0), (0, 3)]),
        ("bidirected C6", [(i, (i + 1) % 6) for i in range(6)]
                          + [((i + 1) % 6, i) for i in range(6)]),
        ("bidirected K3", [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]),
    ]:
        D = Digraph.from_arcs(max(max(a) for a in arcs) + 1, arcs)
        print(f"  {name}: parity-processable = {is_parity_processable(D)}")


if __name__ == "__main__":
    main()
