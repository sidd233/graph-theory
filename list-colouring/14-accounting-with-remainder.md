# 14. The accounting lemma with a remainder term

**Status: lemma proved; the stall facts exhaustively verified.**
Script: `list-colouring/stall_census.py`.

Note `00` states the accounting lemma in the form that assumes the induction runs all the way
to the empty digraph. It never does. This note carries the leftover explicitly, which turns
the vague hope "pay for the remainder somehow" into a number, and the number into a criterion
the route has to meet.

## Definitions

`D` is a digraph with underlying graph `G`. Degrees are always taken in the digraph currently
under consideration. `f : Z>=0 -> Z>=1` is non-decreasing with `f(0) >= 1`.

**Definition 14.1 (legitimate move).** Let `W` be an induced subdigraph of `D` with lists `L`.
A **legitimate move** is a colour `c` together with a nonempty independent set `K` inside
`S_c = {v in W : c in L(v)}` such that every `u` in `S_c \ K` **adjacent to `K`** satisfies

```
f(d+(u)) - f(d+(u) - |N+(u) cap K|) >= 1,      degrees in W.
```

**Definition 14.2 (stalled).** `(W, L)` is **stalled** when no colour admits a legitimate move.

**Definition 14.3 (processable down to `r`).** `D` is **`f`-processable down to `r`** when for
every induced subdigraph `W` with `|W| > r` and every list assignment `L` on `W` satisfying
`|L(v)| >= f(d+_W(v))`, the pair `(W, L)` is not stalled.

## The lemma

**Theorem 14.4.** Let `D` be `f`-processable down to `r`. Then `G` is `L`-colourable for every
list assignment with

```
|L(v)| >= f(d+_D(v)) + s,      s = max(0, r - 1),      for all v.
```

In particular `ch(G) <= f(Delta+(D)) + max(0, r - 1)`.

*Proof.* Put `s = max(0, r - 1)`. If `r = 0` the induction never stalls and the base case is
the empty digraph, so `s = 0` suffices; assume `r >= 1` below, where `s = r - 1`. We show by induction on `|W|` that every induced subdigraph `W` of
`D` with lists satisfying `|L(v)| >= f(d+_W(v)) + s` is `L`-colourable.

**Base, `|W| <= r`.** Every list has `|L(v)| >= f(d+_W(v)) + s >= f(0) + r - 1 >= r`, while
every vertex has at most `|W| - 1 <= r - 1` neighbours. Colour greedily in any order: when `v`
is reached at most `r - 1` of its neighbours are coloured and `|L(v)| >= r`, so a colour is
free.

**Step, `|W| > r`.** The lists satisfy `|L(v)| >= f(d+_W(v))`, so by hypothesis `(W, L)` is not
stalled; take a legitimate move `(c, K)`. Give colour `c` to every vertex of `K`, which is
proper because `K` is independent. Put `W' = W - K` and

```
L'(v) = L(v) \ {c}   if v is adjacent to K,
L'(v) = L(v)         otherwise.
```

This is the only choice that matters. A vertex with no neighbour in `K` may keep `c`, because
nothing it is adjacent to has been given `c`; a vertex adjacent to `K` has `c` removed and so
cannot clash later. The invariant survives in each case:

  - `u` adjacent to `K` and in `S_c`. Its list drops by exactly one, and
    `d+_{W'}(u) = d+_W(u) - |N+_W(u) cap K|`. Definition 14.1 gives
    `f(d+_W(u)) - f(d+_{W'}(u)) >= 1`, so
    `|L'(u)| = |L(u)| - 1 >= f(d+_W(u)) + s - 1 >= f(d+_{W'}(u)) + s`.
  - `u` adjacent to `K` but not in `S_c`. Then `c` is not in `L(u)`, so `L'(u) = L(u)`, and
    `d+` can only drop, and `f` is non-decreasing.
  - `u` not adjacent to `K`. Its list is unchanged and `d+` can only drop.

`W'` is an induced subdigraph of `D` and is smaller, so induction applies. QED

Setting `r = 0` recovers note `00`: no remainder, and no slack needed.

## The criterion this produces

With the 2-d kernel accounting `f(d) = ceil(d/2) + 1`, Theorem 14.4 gives

```
ch(G) <= ceil(Delta+/2) + max(1, r).
```

The `max` matters only in the degenerate cases `r = 0` and `r = 1`, where no slack is needed
and the bound is the clean `ceil(Delta+/2) + 1`.

For this to improve on the ordinary kernel bound `Delta+ + 1` we need
`ceil(Delta+/2) + r < Delta+ + 1`, that is

> **`r <= floor(Delta+ / 2)`.**

So the whole route now rests on one measurable quantity: how large a digraph can stall. This
is the number the earlier notes were gesturing at without naming.

## Three facts about stalling

All verified in `stall_census.py`.

**14.5. The smallest stalled state has 3 vertices.** No two-vertex state stalls. Exhaustively,
8 of the 16 digraphs on 3 vertices admit a stalled list assignment over a palette of at most 3
colours. The first one found is the out-star `0 -> 1`, `0 -> 2` with lists
`L(0) = {0,1}`, `L(1) = {0}`, `L(2) = {1}`. The hypothesis holds, since `f(d+(0)) = f(2) = 2`
and `f(d+(1)) = f(d+(2)) = f(0) = 1`, and the graph is not colourable: the leaves take the two
colours and the centre has nothing left. So `r >= 3` unconditionally, and the halved bound in
its per-vertex form is genuinely false, not merely unproved.

**14.6. A two-vertex colour class containing an arc does not stall.** This corrects the
framing of the barrier in note `01`. Condition (star) there demands that every `u` adjacent to
`K` have **two** out-neighbours in `K`, and Proposition 01 correctly shows no digraph with an
arc satisfies it. But (star) is strictly stronger than Definition 14.1 requires. On the single
arc `u -> v` with `c` in both lists, take `K = {v}`: then `|N+(u) cap K| = 1` and

```
f(d+(u)) - f(d+(u) - 1) = f(1) - f(0) = 2 - 1 = 1 >= 1,
```

so the move is legitimate. The gap is parity: `ceil(d/2)` does drop when `d` is odd, so one
out-neighbour is enough at odd out-degree. What (star) loses is exactly the odd case.

**This matters for planning.** The two-vertex barrier has been treated across notes `01` to
`13` as the thing that kills the route. It kills the *2-d kernel demand*. It does not kill the
*accounting requirement*, which is what Theorem 14.4 actually consumes. Route (B1) is
therefore in better shape than the barrier suggested, and route (B2), the parity idea, is not
a separate escape but the same observation.

**14.7. Strongly connected tournaments stall at every size.** Take the rotational tournament
on odd `n` and give every vertex the same list of size `f((n-1)/2)`. Every colour class is the
whole digraph, and independent sets are singletons `{w}`. A vertex `u` with `w -> u` is
adjacent to `w` but has `|N+(u) cap {w}| = 0`, so it loses a colour and gains nothing. Hence a
legitimate move needs `w` to be a sink, and a strongly connected tournament has none.

```
  rotational tournament on  3: Delta+ = 1, lists of size 2, move available = False
  rotational tournament on  5: Delta+ = 2, lists of size 2, move available = False
  rotational tournament on  7: Delta+ = 3, lists of size 3, move available = False
  rotational tournament on  9: Delta+ = 4, lists of size 3, move available = False
  rotational tournament on 11: Delta+ = 5, lists of size 4, move available = False
```

So over all digraphs `r` is unbounded, and worse, it is unbounded *in the wrong direction*:
these tournaments have `n = 2 Delta+ + 1`, so `r` exceeds `floor(Delta+/2)` by a factor of
about four. The criterion above is not merely unmet, it is violated by a growing margin.

## Where that leaves the route

Theorem 14.4 is unconditional, so the content is entirely in bounding `r`, and 14.7 says `r`
cannot be bounded over all digraphs. Any theorem of this shape must restrict the class, and
14.7 says precisely what it must exclude: large cliques carrying no sink. That is the
structural reason the clique number appears.

**The gap to the Reed shape, stated exactly.** If stalled states were cliques and we paid for
them at face value, `r = omega` and Theorem 14.4 gives

```
ch(G) <= ceil(Delta+/2) + omega,
```

whereas the target shape from `01` is Reed's `ceil((Delta + 1 + omega)/2)`, which spends about
`omega/2`. So face-value payment is off by a factor of two on the remainder term, and closing
that factor is a specific, bounded question rather than a vague hope. It asks whether the
greedy colouring of the remainder can reuse colours already spent by the induction, instead of
demanding `r` fresh ones as the base case of Theorem 14.4 currently does.

That is the next concrete thing to attack, and it is now a question about the base case rather
than about 2-d kernels at all.

## Correction to note 13

Note `13` says the halved bound is "available but worthless" on the 3-hereditary class. The
second half stands and the first is loose. 3-heredity does not license the induction at all,
because the induction is applied to colour classes `D[S_c]`, which can have two vertices, and
Theorem 13.4 gives no 2-d kernel there. Worse, 14.5 exhibits a stalled star, and stars are
members of the 3-hereditary class, so the per-vertex halved bound is outright false on it. The
correct statement is that the class fails to support the induction *and* would give an
exponentially weak bound if it did.
