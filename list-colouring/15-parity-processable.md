# 15. Requirement (R2), restated with the object the accounting actually needs

**Status: exhaustively verified to `n = 7`.**
Script: `list-colouring/parity_processable.py`.

## Why (R2) needed restating

Note `01` states requirement (R2) through condition (star): for every `W` and every `S` inside
`W` there is a nonempty independent `K` inside `S` such that every `u` in `S \ K` adjacent to
`K` has at least **two** out-neighbours in `K`. Proposition 01 kills it in three lines, and the
arcless theorem of `latex/hereditary-2-d-kernels-are-arcless.tex` is the same fact.

Note `14.6` shows (star) is stronger than the accounting lemma requires. The real condition is
Definition 14.1,

```
f(d+(u)) - f(d+(u) - |N+(u) cap K|) >= 1,      degrees taken in W,
```

and with `f(d) = ceil(d/2) + 1` a **single** out-neighbour in `K` suffices when `d+(u)` is odd.
So (star) throws away the odd case, and everything derived from (star) inherits that loss.

**Definition 15.1.** `D` is **parity-processable** when for every induced subdigraph `W` and
every `S` inside `W` there is a nonempty independent `K` inside `S` meeting Definition 14.1.

This is (R2) and (R3) together, stated correctly. It is closed under induced subdigraphs, so
the class is enumerated by canonical augmentation.

## The class is not arcless

```
  n  members  with an arc  max chi  max Delta+  max edges  max degeneracy
  2        3            2        2           1          1               1
  3        7            6        2           2          2               1
  4       21           20        2           3          4               2
  5       54           53        2           4          5               2
  6      155          154        2           5          6               2
  7      424          423        2           6          7               2
```

On 6 vertices, 154 of the 155 members carry an arc. **The two-vertex barrier does not close
(R2).** That claim has stood since note `01` and it is wrong as applied to the requirement the
proof consumes, rather than to the 2-d kernel demand. Correcting it is the substantive result
of this note.

## But it buys very little

The class is sparse and stays sparse. Across `n = 4` to `7` the maximum number of edges is
exactly `n` and the maximum degeneracy is exactly 2, so every member is at most unicyclic, and
every member is bipartite.

Digons are what kill density. Out-degree counts both arcs of a digon, so a digon pushes
out-degrees up and breaks the parity that the single-out-neighbour case depends on:

```
  directed C4:    parity-processable
  bidirected C4:  not
  bidirected C6:  not
  bidirected K3:  not
```

So the orientations that survive are genuinely one-way, and a one-way orientation that is
everywhere parity-friendly cannot also be dense.

The bound is not vacuous on the class. Comparing `ceil(Delta+/2) + 1` against the free greedy
bound `degeneracy + 1`, it wins on 1, 2, 9 and 27 members at `n = 4, 5, 6, 7` respectively. But
those wins are bound 2 against greedy 3, on graphs of degeneracy 2, where list colouring is
already understood.

## Verdict

**(R2) in its "for every `S`" form is closed**, now for the right reason rather than the wrong
one. It is not vacuous, as note `01` claimed, but the class it defines has degeneracy at most
2 and chromatic number 2, so no bound proved on it is progress on the goal.

What remains is exactly route (B1): stop quantifying over every `S`. The induction never faces
an adversarial `S`; it faces the colour classes `S_c` of an actual list assignment, and it
chooses which one to process. Theorem 14.4 already puts a number on how much that has to buy,
namely the remainder `r`, and the criterion is `r <= floor(Delta+/2)`.

So the project's open question is now a single sharp one:

> For which digraphs `D` is it true that every list assignment with
> `|L(v)| >= ceil(d+(v)/2) + 1` on every induced subdigraph `W` with `|W| > r` leaves some
> colour processable?

with `r` to be bounded by `floor(Delta+/2)`. Note `14.7` says the answer excludes strongly
connected tournaments, and note `14` argues the natural parameter is the clique number.
