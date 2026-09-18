# 13. Cutting the induction off at three vertices: the class is complete bipartite

**Status: proved, and exhaustively verified to `n = 8`.**
Script: `list-colouring/three_hereditary.py`.

## The question

`latex/hereditary-2-d-kernels-are-arcless.tex` shows that a class closed under induced
subdigraphs in which every member has a 2-d kernel is arcless. The proof works by dragging
you down to two vertices, which is below the size floor of a 2-d kernel.

The proposed repair is to stop one step earlier. Three vertices is the smallest digraph that
has both an arc and a 2-d kernel, so it is the natural floor.

**Definition.** `D` is **3-hereditary** when every induced subdigraph of `D` on at least 3
vertices has a 2-d kernel.

The arcless theorem does not apply, since two-vertex subdigraphs are now out of scope, and the
class is not empty. So the repair works as stated. The question is whether the class it
produces is rich enough to carry a colouring theorem.

## The three-vertex case, in full

**Lemma 13.1.** Let `D` have exactly 3 vertices. Then `D` has a 2-d kernel if and only if
either `D` has no arcs, or there are two non-adjacent vertices `a, b` and the third vertex `x`
satisfies `x -> a` and `x -> b`.

*Proof.* Let `K` be a 2-d kernel. If `K = V` then independence makes `D` arcless. If `K` is
empty there is an excluded vertex with no out-neighbour in `K`, which is not 2-dominated. If
`|K| = 1`, an excluded vertex needs two out-arcs into `K` landing on two distinct vertices,
and `K` has only one, so no excluded vertex can exist; but `|V \ K| = 2 > 0`. Hence `|K| = 2`,
say `K = {a, b}`, which is independent, and the remaining vertex `x` is 2-dominated, giving
`x -> a` and `x -> b`. The converse is immediate. QED

## The classification

**Theorem 13.2.** Let `D` be 3-hereditary. Then the underlying graph of `D` is complete
bipartite, with one side possibly empty.

*Proof.* Two applications of Lemma 13.1.

**No triangle.** Let `u, v, w` be pairwise adjacent. The induced subdigraph on them has an arc
and no non-adjacent pair, so by Lemma 13.1 it has no 2-d kernel. So the underlying graph is
triangle-free.

**Non-adjacency is transitive.** Suppose `u, v` are non-adjacent and `v, w` are non-adjacent,
with `u, w` distinct and adjacent. Consider the induced subdigraph on `{u, v, w}`. It has an
arc, so by Lemma 13.1 it needs a non-adjacent pair with the third vertex pointing to both.
The only non-adjacent pairs are `{u, v}` and `{v, w}`. For `{u, v}` the third vertex is `w`,
which would need `w -> v`, impossible since `v, w` are non-adjacent. For `{v, w}` the third
vertex is `u`, which would need `u -> v`, impossible for the same reason. So there is no 2-d
kernel, a contradiction. Hence `u, w` are non-adjacent.

Transitivity makes non-adjacency an equivalence relation on `V`, so the complement of the
underlying graph is a disjoint union of cliques, which is to say the underlying graph is
complete multipartite. Three or more non-empty parts would contain a triangle, so there are at
most two. QED

**Corollary 13.3.** Every 3-hereditary digraph has chromatic number at most 2.

For completeness, the orientations are pinned down too, by the same lemma.

**Theorem 13.4.** For `n >= 3`, `D` is 3-hereditary if and only if `D` is one of:

  1. arcless;
  2. a **star**: a centre `c` with `c -> w` for every other vertex `w`, the other `n-1 >= 2`
     vertices pairwise non-adjacent, and an arbitrary subset of the reverse arcs `w -> c`;
  3. a **bidirected complete bipartite** graph `K_{a,b}` with `a, b >= 2`, every edge carrying
     both arcs.

*Proof sketch.* Necessity: by Theorem 13.2 the underlying graph is `K_{a,b}`. If `a, b >= 2`,
take `x` on the `a` side and `b1, b2` on the `b` side. In the triple `{x, b1, b2}` the only
non-adjacent pair is `{b1, b2}`, so Lemma 13.1 forces `x -> b1` and `x -> b2`; symmetrically
every vertex of the `b` side points to every vertex of the `a` side, so every edge is a digon.
If `a = 1`, the same argument applied to `{c, w1, w2}` forces the centre to point at every
other vertex, and the reverse arcs are unconstrained. Sufficiency: in case 2 an induced
subdigraph on at least 3 vertices either misses `c`, and is arcless, or contains `c` and at
least two leaves, which form a 2-d kernel. In case 3 an induced subdigraph on sides `A', B'`
takes `B'` as its 2-d kernel when `|B'| >= 2`, and `A'` when `|B'| <= 1`, one of which always
applies on at least 3 vertices. QED

## The census

`three_hereditary.py` enumerates the class up to isomorphism by canonical augmentation, which
is sound because 3-heredity is closed under induced subdigraphs, and asserts that every member
falls into Theorem 13.4. It does.

```
  n  members  max chi  max Delta+  shapes
  3        4        2           2  arcless x1, star x3
  4        6        2           3  arcless x1, bidirected K_{2,2} x1, star x4
  5        7        2           4  arcless x1, bidirected K_{2,3} x1, star x5
  6        9        2           5  arcless x1, bidirected K_{2,4} x1, bidirected K_{3,3} x1, star x6
  7       10        2           6  arcless x1, bidirected K_{2,5} x1, bidirected K_{3,4} x1, star x7
  8       12        2           7  arcless x1, bidirected K_{2,6} x1, bidirected K_{3,5} x1, bidirected K_{4,4} x1, star x8
```

The counts are `n + floor(n/2)`: one arcless digraph, `n` stars (the centre points at all
`n-1` others, and the reverse arcs form any of `n` subsets up to isomorphism), and
`floor(n/2) - 1` bidirected complete bipartite graphs. Linear growth. For comparison there
are 1540944 digraphs on 6 vertices.

A note on the tooling. `twokernel.canon.certificate` falls back to a Weisfeiler-Leman
canonical form capped at `CANON_MAX_N = 7` when pynauty is absent, and above the cap it
returns a key that is not canonical, so duplicates survive. A first run using it reported 148
members on 8 vertices. `three_hereditary.py` therefore computes its own exact certificate.
The two agree for `n <= 7`, which is a cross-check on both.

## Verdict for the goal

**This route is closed.**

The purpose of a 2-d kernel theorem is a bound of the shape `chi_ell(G) <= ceil(Delta+/2) + 1`.
On the 3-hereditary class that bound is worthless, for two separate reasons. (It is also
not even available: see the correction at the end of note `14`, which shows the induction
is not licensed here and that the per-vertex form is false on stars.)

First, every member has chromatic number at most 2. For stars `chi_ell = 2`, and for complete
bipartite graphs `chi_ell` is `O(log n)` by the standard counting argument. Both are known
without any kernel machinery.

Second, the bound is not merely redundant, it is much weaker than the truth. Theorem 13.4
leaves no choice of orientation: for `a, b >= 2` the only member on `K_{a,b}` is the
bidirected one, whose `Delta+` is `max(a, b)`. So the bound gives about `max(a, b)/2` where
the truth is `O(log max(a, b))`. The gap is exponential, and it cannot be closed by orienting
more cleverly, because a cleverer orientation leaves the class.

So the class is not a class of digraphs with an interesting colouring problem on it. It is a
list of stars and complete bipartite graphs.

## What this does and does not close

It closes the specific repair, which was to weaken (R2) by raising the floor of the induction
from 2 vertices to 3 while still quantifying over *every* induced subdigraph above the floor.

It does not close route (B1), which weakens (R2) in a different direction: quantify not over
every induced subdigraph but over the *colour classes the induction actually visits*. That is a
genuinely different hypothesis, and the reason it is different is worth stating.

The induction of Lemma 1 never asks for a 2-d kernel of an arbitrary induced subdigraph. At
each step it picks a colour `c` and asks for a 2-d kernel of `D[A(c)]`, where `A(c)` is the set
of vertices whose list still contains `c`. Quantifying over all induced subdigraphs is a
sufficient condition for that, and Theorem 13.2 shows it is a very expensive one. It is not
necessary.

**The corollary that matters for planning.** Raising the floor does not address the real
failure mode. `A(c)` can be small while `D` is large: a digraph on a thousand vertices in which
colour `c` appears in only two lists presents a two-vertex subdigraph on the *first* step. So
the obstruction is not confined to the bottom of the induction and cannot be fixed by a base
case. The step needs a choice rule, namely a proof that at each stage *some* colour is
processable. That remains the live question.

## Appendix: raising the cutoff further

The obvious generalisation is to cut off at `k` rather than 3: every induced subdigraph on at
least `k` vertices has a 2-d kernel. This is still closed under induced subdigraphs, so the
same canonical augmentation enumerates it, from a base of all digraphs on `k-1` vertices.

**At `k = 4` the class is genuinely richer, and Theorem 13.2 does not survive.** The
three-vertex lemma is no longer available, so triangles are no longer excluded, and they do
appear. Counts up to isomorphism, with `chi` of the underlying graph:

```
  cutoff k = 4                     cutoff k = 5
  n  members  max chi              n  members  max chi
  4       35        3              5      882        4
  5       70        3              6     2828        4
  6      120        3              7     7501        4
  7      192        3
  8      286        3
```

So the `k = 3` verdict is specific to `k = 3` and does not transfer by itself.

**An observed pattern, not a theorem.** The maximum chromatic number of the `k`-hereditary
class is 2 for `k = 3`, 3 for `k = 4` and 4 for `k = 5`, that is `k - 1` in each case, over
every size computed. If that holds in general it closes the whole cutoff family at once, and
for a reason with a pleasing shape. Cutting off at `k` means the induction stalls with at most
`k - 1` vertices left, so the remainder term of Theorem 14.4 is `r = k - 1` and the bound is

```
ch(G) <= ceil(Delta+/2) + (k - 1).
```

The class you buy would then have chromatic number at most exactly the remainder you pay for
it. Raising the cutoff to enrich the class costs precisely what the enrichment is worth, and
the halving never surfaces as a gain. Note that this is suggestive rather than decisive, since
`chi_ell` can exceed `chi` and it is `chi_ell` the bound is about.

Proving or breaking `max chi = k - 1` is a cheap and well-posed question, and it is the right
next thing to do on this branch if anyone returns to it.

**Is the bound worth anything there?** The test that matters is not the size of the class but
whether the halved bound would beat what is already free. Comparing, for each member,
`ceil(Delta+/2) + 1` against the greedy bound `degeneracy + 1`:

```
  n  members  members where halved < greedy  largest gain
  4       35                             7             1
  5       70                             9             1
  6      120                             8             2
  7      192                            29             1
```

So the halved bound is **not vacuous** on the `k = 4` class: it is a real improvement on about
15 per cent of members. But the improvement is 1 or 2 colours and is not growing with `n`,
where a genuine halving should give a gain proportional to `Delta`. And `chi` is stuck at 3
throughout.

**Honest status of this appendix.** These are observations on `n <= 7`, not a theorem. Two
things would settle it and neither is done:

  1. Is the `k = 4` class also classifiable, the way Theorem 13.2 classifies `k = 3`? If it
     has bounded chromatic number for every `n`, the same verdict applies to it.
  2. Does the largest gain grow with `n`, or stay at a small constant? Constant gain means the
     method buys an additive improvement rather than the multiplicative one that is the point
     of the project.

The `k = 5` class beyond `n = 7` was still computing when this note was written.
