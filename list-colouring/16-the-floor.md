# 16. Obstruction B, measured: the floor holds

**Status: stated precisely, verified on every graph to 6 vertices, not proved.**
Script: `list-colouring/floor.py`.

`PROBLEM.md` has carried a floor of roughly `mad/2 + 1` under this family of methods since it
was written, with a standing note that it had never been independently re-derived and was
carrying a lot of weight. It decides whether the target is reachable at all, so it should have
been the first thing checked, and it is the thing this project has deferred most often.

Theorem 14.4 makes it measurable, which it was not before.

## Stating it properly

Write `D*(G) = min over orientations D of Delta+(D)`. By Hakimi this equals
`max over subgraphs H of ceil(|E(H)|/|V(H)|)`, which is about `mad(G)/2`. The ordinary kernel
method cannot prove anything below `D* + 1`, because it cannot choose an orientation with
smaller `Delta+`.

Theorem 14.4 gives the 2-d kernel method, for any orientation `D`,

```
ch(G) <= ceil(Delta+(D)/2) + max(1, r(D)),
```

so halving would push under `D* + 1` unless the remainder compensates exactly.

> **Floor.** For every graph `G`,
> `min over orientations D of [ ceil(Delta+(D)/2) + max(1, r(D)) ] >= D*(G) + 1`.

This is the negation of the criterion in note `14`: the floor holds exactly when
`r <= floor(Delta+/2)` is never attainable. Two loose statements from different notes turn out
to be the same statement.

## Computing `r` without enumerating list assignments

`r(D)` is the largest induced subdigraph of `D` admitting a stalling list assignment. The
assignments do not have to be enumerated.

**Lemma 16.1.** `W` admits a stalling list assignment if and only if the union of its **bad**
sets is `V(W)`, where `S` is bad when no legitimate `K` in the sense of Definition 14.1 lies
inside it.

*Proof.* If `(W, L)` is stalled then every colour class `S_c` is bad, and every vertex lies in
some class because every list is nonempty, so the bad sets cover `V(W)`. Conversely, let bad
sets `B_1, .., B_m` cover `V(W)` and put `M = max_v f(d+(v))`. Give each `B_i` its own `M`
colours, all with class `B_i`, and let `L(v)` be the colours of the bad sets containing `v`.
Then `|L(v)| >= M >= f(d+(v))`, so the assignment is valid, and every class is bad. QED

Singletons are never bad, since `K = S` is legitimate with nothing outside it, so bad sets have
at least two elements and coverage is a real condition.

## The measurement

Over every graph on at most 6 vertices, minimising over all orientations:

```
  n  graphs  beat the floor  meet it exactly  fall short of it
  2       2               0                1                 0
  3       4               0                2                 1
  4      11               0                6                 4
  5      34               0               11                22
  6     156               0               27               128
```

**No graph beats the floor.** 47 of the 207 meet it exactly and the other 160 do worse than the
ordinary kernel method's own floor. The halving never once converts into a bound below
`D* + 1`.

A caveat on what this compares. `D* + 1` is the floor of the ordinary kernel method, not what
that method achieves, since achieving it needs a kernel-perfect orientation which often does
not exist. The comparison is therefore against an idealised competitor. But the target was
always to get *below* `D* + 1`, and nothing does.

## Why, structurally

Note `14.6` found the escape that makes any of this possible: `ceil(d/2)` drops on a single
out-neighbour when `d` is odd, so one out-arc can pay for one colour. That escape is what
rescued (R2) from the two-vertex barrier. It cannot, however, carry an induction.

**Lemma 16.2.** No digraph keeps every out-degree odd in every induced subdigraph.

*Proof.* If `D` has an arc `u -> v` with `d+_D(u)` odd, then in the induced subdigraph `D - v`
the out-degree of `u` is `d+_D(u) - 1`, which is even. If `D` has no arc, every out-degree is
`0`, which is even. QED

Verified exhaustively: of the 3, 16, 218 and 9608 digraphs on 2 to 5 vertices, none qualifies.

The induction changes `d+(u)` by exactly the number of out-arcs it consumes at `u`, so using
the escape at `u` flips `u` out of the odd case immediately. The escape is a boundary effect
available at particular vertices at particular moments, never a property the argument can lean
on. That is the same fact note `15` sees from the other side: the class where the escape works
everywhere has degeneracy at most 2.

## Verdict for the goal

**The clean halving is not reachable by this family, and the project should stop aiming at it.**

The three obstructions the project has collected are one obstruction. The two-vertex barrier
says you cannot always get two out-arcs. The parity escape says one out-arc is sometimes
enough. Lemma 16.2 says "sometimes" cannot be upgraded to "always". The floor is what you
measure when all three are in force at once.

What survives is the Reed-shaped target that note `01` already identified on separate grounds,
`ceil((Delta + 1 + omega)/2)`, where the extra `omega/2` is paid for exactly the vertices the
barrier forces us to excuse. Note `14` reduces that to one bounded question: whether the
remainder can be paid at `omega/2` rather than `omega`, by reusing colours the induction has
already spent instead of demanding fresh ones in the base case of Theorem 14.4.

That question is worth asking. `ceil(Delta+/2) + 1` is not.

## What would overturn this

The floor is verified, not proved, and only to 6 vertices. It would be overturned by a single
graph with an orientation whose stalled subdigraphs are all smaller than `floor(Delta+/2)`.
Lemma 16.2 says the parity escape will not produce one. A proof of the floor, or a
counterexample at 7 or 8 vertices, would settle it; `floor.py` extends directly, though the
orientation count makes 7 vertices roughly a hundred times the work.
