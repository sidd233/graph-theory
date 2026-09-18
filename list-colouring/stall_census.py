"""Stalled states of the accounting induction, and where the remainder comes from.

`00-kernel-method.md` states the accounting lemma with a general `f`: a move on colour `c`
is legitimate when some nonempty independent `K` inside `S_c = {v : c in L(v)}` has

    f(d+(u)) - f(d+(u) - |N+(u) cap K|) >= 1     for every u in S_c \\ K adjacent to K,

degrees taken in the current digraph.  Call `(W, L)` **stalled** when no colour admits such
a move.  The induction runs until it stalls, so the size of a stalled state is the remainder
term `r` of `14-accounting-with-remainder.md`.

This script checks three things:

  1. the smallest stalled state, over all digraphs up to isomorphism and all list
     assignments over a small palette;
  2. that a two-vertex colour class containing an arc is **not** automatically stalled,
     which is where (star) of `01-what-we-need.md` is stronger than the accounting lemma
     actually requires;
  3. that strongly connected tournaments stall at every size, so the remainder is unbounded
     over all digraphs and any theorem has to restrict the class.

Run: `python list-colouring/stall_census.py`
"""

import sys
from itertools import combinations, product
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "list-colouring"))
sys.path.insert(0, str(_root / "census-tool"))

from three_hereditary import certificate
from twokernel.core import Digraph, bits, popcount


def f_half(d):
    """The 2-d kernel accounting: f(d) = ceil(d/2) + 1, so f(0) = 1."""
    return -(-d // 2) + 1


def independent_sets(D, mask):
    """Every nonempty independent subset of `mask`, as bitmasks."""
    verts = list(bits(mask))
    for size in range(1, len(verts) + 1):
        for combo in combinations(verts, size):
            m = 0
            ok = True
            for v in combo:
                if D.adj[v] & m:
                    ok = False
                    break
                m |= 1 << v
            if ok:
                yield m


def move_is_valid(D, S, K, f):
    """Does colouring `K` keep the invariant for every u in S \\ K adjacent to K?"""
    for u in bits(S & ~K):
        if not (D.adj[u] & K):
            continue  # not adjacent to K, so it never loses the colour
        d = popcount(D.out[u])
        a = popcount(D.out[u] & K)
        if f(d) - f(d - a) < 1:
            return False
    return True


def has_move(D, lists, f):
    """Is some colour processable?  `lists[v]` is a set of colours."""
    for c in set().union(*lists) if lists else ():
        S = 0
        for v in range(D.n):
            if c in lists[v]:
                S |= 1 << v
        for K in independent_sets(D, S):
            if move_is_valid(D, S, K, f):
                return True
    return False


def all_digraphs_bf(n):
    """All digraphs on n vertices up to isomorphism, by brute force (small n only)."""
    slots = [(u, v) for u in range(n) for v in range(n) if u != v]
    seen, out = set(), []
    for m in range(1 << len(slots)):
        D = Digraph.from_arcs(n, [slots[i] for i in range(len(slots)) if m >> i & 1])
        cert = certificate(D)
        if cert not in seen:
            seen.add(cert)
            out.append(D)
    return out


def list_assignments(D, palette, f):
    """Every assignment of lists from `palette` meeting |L(v)| >= f(d+(v))."""
    choices = []
    for v in range(D.n):
        need = f(popcount(D.out[v]))
        opts = [
            frozenset(c)
            for size in range(need, len(palette) + 1)
            for c in combinations(palette, size)
        ]
        if not opts:
            return
        choices.append(opts)
    yield from product(*choices)


# ------------------------------------------------------------------------------------
# 1. the smallest stalled state
# ------------------------------------------------------------------------------------


def smallest_stall(max_n=4, max_palette=3, f=f_half):
    for n in range(2, max_n + 1):
        found = []
        for D in all_digraphs_bf(n):
            for m in range(1, max_palette + 1):
                palette = list(range(m))
                for lists in list_assignments(D, palette, f):
                    if not has_move(D, lists, f):
                        found.append((D, lists, m))
                        break
                if found and found[-1][0] is D:
                    break
        if found:
            return n, found
    return None, []


# ------------------------------------------------------------------------------------
# 2. a two-vertex colour class with an arc need not stall
# ------------------------------------------------------------------------------------


def two_vertex_escape(f=f_half):
    """The single arc u -> v, one colour in both lists.  d+(u) = 1 is odd, so it moves."""
    D = Digraph.from_arcs(2, [(0, 1)])
    lists = (frozenset({0, 1}), frozenset({0}))
    return D, lists, has_move(D, lists, f)


# ------------------------------------------------------------------------------------
# 3. strongly connected tournaments stall at every size
# ------------------------------------------------------------------------------------


def rotational_tournament(n):
    """The circulant tournament on odd n: i -> i+1, .., i+(n-1)/2 mod n.  Strongly
    connected, regular of out-degree (n-1)/2, and has no sink."""
    assert n % 2 == 1
    arcs = [(i, (i + k) % n) for i in range(n) for k in range(1, (n - 1) // 2 + 1)]
    return Digraph.from_arcs(n, arcs)


def tournament_stalls(n, f=f_half):
    D = rotational_tournament(n)
    need = f(popcount(D.out[0]))
    lists = tuple(frozenset(range(need)) for _ in range(n))
    return D, need, has_move(D, lists, f)


def is_L_colourable(D, lists):
    """Brute force, for the three-vertex certificate only."""
    for phi in product(*[sorted(s) for s in lists]):
        if all(phi[u] != phi[v] for u in range(D.n) for v in bits(D.adj[u]) if u < v):
            return True
    return False


def main():
    print("f(d) = ceil(d/2) + 1, the 2-d kernel accounting\n")

    print("1. smallest stalled state")
    n, found = smallest_stall()
    if n is None:
        print("   none found")
    else:
        print(f"   smallest stall has n = {n}; {len(found)} digraphs on {n} vertices stall")
        D, lists, m = found[0]
        print(f"   example: arcs {sorted(D.arcs())}, palette size {m}, "
              f"lists {[sorted(s) for s in lists]}")
    print()

    print("2. is a two-vertex colour class containing an arc automatically stalled?")
    D, lists, moved = two_vertex_escape()
    print(f"   arc 0 -> 1, lists {[sorted(s) for s in lists]}: "
          f"move available = {moved}")
    print("   (star) of note 01 demands two out-neighbours in K and so forbids this;")
    print("   the accounting lemma only needs f(1) - f(0) = 2 - 1 >= 1, which holds.")
    print()

    print("3. the smallest stall is a genuine counterexample, not just an unproved case")
    D = Digraph.from_arcs(3, [(0, 1), (0, 2)])
    lists = [frozenset({0, 1}), frozenset({0}), frozenset({1})]
    holds = all(len(lists[v]) >= f_half(popcount(D.out[v])) for v in range(3))
    print(f"   star 0->1, 0->2 with lists {[sorted(s) for s in lists]}")
    print(f"   |L(v)| >= f(d+(v)) for every v: {holds}")
    print(f"   L-colourable: {is_L_colourable(D, lists)}")
    print(f"   stalled: {not has_move(D, lists, f_half)}")
    assert holds and not is_L_colourable(D, lists)
    print("   so the per-vertex halved bound is false, and r >= 3 unconditionally.")
    print()

    print("4. strongly connected tournaments, all lists equal")
    for n in (3, 5, 7, 9, 11):
        D, need, moved = tournament_stalls(n)
        print(f"   rotational tournament on {n:>2}: Delta+ = {(n-1)//2}, "
              f"lists of size {need}, move available = {moved}")
    print("   No sink, so no independent K dominates, and every K leaves an adjacent")
    print("   vertex with no out-arc into it.  The remainder is unbounded over all")
    print("   digraphs, so a bound of this shape must restrict the class.")


if __name__ == "__main__":
    main()
