"""The 3-hereditary class: does cutting the induction off at 3 vertices buy anything?

`latex/hereditary-2-d-kernels-are-arcless.tex` proves that a class closed under induced
subdigraphs in which every member has a 2-d kernel is arcless.  That proof works by
dragging you down to two vertices, which is below the size floor of a 2-d kernel: an
excluded vertex needs two out-arcs into the set, landing on two distinct vertices, so the
set has at least two elements whenever anything sits outside it.

The natural repair is to stop one step earlier.  Call `D` **3-hereditary** when every
induced subdigraph on at least 3 vertices has a 2-d kernel.  The arcless theorem cannot
touch this, since two-vertex subdigraphs are now out of scope, and the class is not empty:
the out-star, one centre with arcs to k >= 2 pairwise non-adjacent leaves, is 3-hereditary.

This script decides whether the class is *rich* enough to carry a colouring theorem.  A
bound proved only for a class of chromatic number 2 is not progress on the goal, because
the bound is beaten there by the trivial argument.

It does two things:

  1. enumerates the class exhaustively up to isomorphism, and
  2. checks the enumeration against `classify`, the closed form proved in
     `list-colouring/13-three-hereditary-is-bipartite.md`.

Method.  3-heredity is itself closed under induced subdigraphs, so the class on `n`
vertices is built by canonical augmentation from the class on `n-1` vertices rather than
by filtering all digraphs on `n` vertices.  The condition is vacuous on 1 and 2 vertices,
so the base level is all 3 digraphs on 2 vertices.

Run: `python list-colouring/three_hereditary.py [max_n]`   (default 8)
"""

import sys
from itertools import permutations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "census-tool"))

from twokernel.core import Digraph, bits, has_2kernel, popcount


# ------------------------------------------------------------------------------------
# exact isomorphism certificate
# ------------------------------------------------------------------------------------
#
# `twokernel.canon.certificate` falls back to a Weisfeiler-Leman canonical form capped at
# CANON_MAX_N = 7 vertices when pynauty is absent, and above the cap it returns a key that
# is not canonical, so duplicates survive.  Certificates here are therefore computed
# locally, and only for digraphs that already passed the membership test, which keeps the
# cost down because the class turns out to be thin and highly structured.


def certificate(D):
    """A value equal for two digraphs exactly when they are isomorphic.

    Vertices are split by the isomorphism-invariant pair of degrees, refined once by the
    multiset of neighbours' pairs.  The certificate is the lexicographic minimum of the
    arc set over every permutation respecting the resulting ordered classes, which is
    exact because any isomorphism respects them.  Arcless digraphs are short-circuited,
    since there every vertex is equivalent and the minimum is over `n!` identical values.
    """
    n = D.n
    if D.num_arcs == 0:
        return (n, "arcless")
    base = [(popcount(D.out[v]), popcount(D.inn[v])) for v in range(n)]
    refined = [(base[v], tuple(sorted(base[w] for w in bits(D.adj[v])))) for v in range(n)]
    blocks = {}
    for v in range(n):
        blocks.setdefault(refined[v], []).append(v)
    ordered = [blocks[key] for key in sorted(blocks)]

    best = None
    for choice in product(*(permutations(b) for b in ordered)):
        pos, i = {}, 0
        for block in choice:
            for v in block:
                pos[v] = i
                i += 1
        arcs = tuple(sorted((pos[u], pos[w]) for u, w in D.arcs()))
        if best is None or arcs < best:
            best = arcs
    return (n, tuple(len(b) for b in ordered), best)


# ------------------------------------------------------------------------------------
# the class
# ------------------------------------------------------------------------------------


def is_three_hereditary(D):
    """Every induced subdigraph on at least 3 vertices has a 2-d kernel."""
    s = D.full
    while True:
        if popcount(s) >= 3 and not has_2kernel(D.sub(s)):
            return False
        if s == 0:
            return True
        s = (s - 1) & D.full


def augment(previous, n):
    """Every 3-hereditary digraph on n vertices, from the class on n-1 vertices.

    Sound because 3-heredity is closed under induced subdigraphs, so deleting a vertex
    from a member on n vertices leaves a member on n-1 vertices; every member is
    therefore reached by extending some member of the level below.
    """
    seen, result = set(), []
    new = n - 1
    for G in previous:
        base = list(G.arcs())
        for out_mask in range(1 << new):
            for in_mask in range(1 << new):
                arcs = base + [(new, w) for w in bits(out_mask)]
                arcs += [(v, new) for v in bits(in_mask)]
                D = Digraph.from_arcs(n, arcs)
                if not is_three_hereditary(D):
                    continue
                cert = certificate(D)
                if cert not in seen:
                    seen.add(cert)
                    result.append(D)
    return result


# ------------------------------------------------------------------------------------
# the closed form, checked against the enumeration
# ------------------------------------------------------------------------------------


def classify(D):
    """Which case of the classification `D` falls into, or None if it falls into none.

    Proved cases, for `n >= 3`:
      "arcless"        no arcs at all;
      "star"           a centre with an arc to each of the n-1 >= 2 others, which are
                       pairwise non-adjacent, plus an arbitrary subset of the reverse
                       arcs;
      "bidirected K_{a,b}"  complete bipartite with both sides of size >= 2, every edge
                       carrying both arcs.
    """
    n = D.n
    if D.num_arcs == 0:
        return "arcless"
    # complete bipartite? non-adjacency must be an equivalence with exactly two classes
    side = [-1] * n
    side[0] = 0
    stack = [0]
    while stack:
        v = stack.pop()
        for w in range(n):
            if w == v:
                continue
            want = 1 - side[v] if (D.adj[v] >> w & 1) else side[v]
            if side[w] == -1:
                side[w] = want
                stack.append(w)
            elif side[w] != want:
                return None
    a, b = side.count(0), side.count(1)
    if a == 0 or b == 0:
        return None
    centre_side = 0 if a == 1 else (1 if b == 1 else None)
    if centre_side is not None:
        c = side.index(centre_side)
        if all(D.out[c] >> w & 1 for w in range(n) if w != c):
            return "star"
        return None
    if D.is_symmetric():
        return f"bidirected K_{{{min(a, b)},{max(a, b)}}}"
    return None


def chromatic_number(D):
    """Exact chromatic number of the underlying graph, by backtracking on small n."""
    n, adj = D.n, D.adj
    for k in range(1, n + 1):
        colour = [-1] * n

        def place(v):
            if v == n:
                return True
            for c in range(min(k, max(colour[:v], default=-1) + 2)):
                if all(colour[u] != c for u in bits(adj[v]) if u < v):
                    colour[v] = c
                    if place(v + 1):
                        return True
                    colour[v] = -1
            return False

        if place(0):
            return k
    return n


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    level = [Digraph.from_arcs(2, a) for a in ([], [(0, 1)], [(0, 1), (1, 0)])]
    print(f"n=2: {len(level)} digraphs; 3-heredity is vacuous below 3 vertices")
    print()
    print(f"{'n':>3}  {'members':>7}  {'max chi':>7}  {'max Delta+':>10}  shapes")
    for n in range(3, max_n + 1):
        level = augment(level, n)
        if not level:
            print(f"{n:>3}  class is empty")
            break
        shapes = {}
        for D in level:
            kind = classify(D)
            assert kind is not None, f"outside the classification: {sorted(D.arcs())}"
            shapes[kind] = shapes.get(kind, 0) + 1
        chi = max(chromatic_number(D) for D in level)
        dmax = max(max(D.out_degree(v) for v in range(n)) for D in level)
        listed = ", ".join(f"{k} x{v}" for k, v in sorted(shapes.items()))
        print(f"{n:>3}  {len(level):>7}  {chi:>7}  {dmax:>10}  {listed}")
    print()
    print("Every member matched the classification, so every member is complete bipartite")
    print("and has chromatic number at most 2.")


if __name__ == "__main__":
    main()
