# 2. What we need, and the wall in front of it

## The three requirements

Reading Steps 1 to 6 of `00-kernel-method.md` with 2 in place of 1 at Step 5, a class `C`
of digraphs delivers `ch(G) <= ceil(Delta+/2) + 1` exactly when:

  - **(R1)** every `G` in our graph class has an orientation `D` in `C` with small `Delta+`;
  - **(R2)** `C` is closed under the deletion performed at Step 4, and, because Step 2 is
    applied to `D[S]` for a set `S` the adversary controls, `C` must be closed under
    **arbitrary induced subdigraphs**;
  - **(R3)** every member of `C` admits, at Step 2, an independent set doing the work of
    Step 5.

This is the plan as stated: a class that always has a 2-d kernel, and that survives the
deletion so the argument repeats. (R2) is the part that bites, and it is worth being
precise about what (R3) really needs, because the honest version is weaker than "2-d kernel".

## The weakest usable form of (R3)

A vertex `u` outside `K` only loses the colour `c` if it is **adjacent** to a vertex of
`K`. A vertex with no neighbour in `K` pays nothing and needs no compensation. So Step 5
goes through under:

> **(star)** For every `W` and every `S` inside `W`, there is a nonempty independent
> `K` inside `S` such that every `u` in `S \ K` **adjacent to `K`** has at least two
> out-neighbours in `K`.

(star) is strictly weaker than "`K` is a 2-d kernel of `D[S]`", since it excuses the
non-neighbours. It is the real requirement.

## The barrier

**Proposition.** No digraph with an arc satisfies (star).

*Proof.* Let `u -> v` be an arc. Take `W = V` and `S = {u, v}`. The nonempty subsets of
`S` are `{u}`, `{v}` and `{u, v}`; the last is not independent. If `K = {v}`, then `u` is
adjacent to `K` and `|N+(u) cap K| <= |K| = 1 < 2`. If `K = {u}`, the same for `v`. No
choice works. QED

Verified exhaustively: over all 3, 63 and 4095 digraphs with at least one arc on 2, 3 and
4 vertices (digons allowed), **none** satisfies (star), and in every single case the
smallest failing `S` has size 2. See `verify_barrier.py`.

**Consequence.** The hypothesis "every induced subdigraph has a 2-d kernel" is satisfied only
by arcless digraphs, so the conditional theorem `ch <= ceil(Delta+/2) + 1` is vacuous. The
plan as literally stated cannot work: a class closed under induced subdigraphs in which
every member has a 2-d kernel is a class of edgeless graphs.

This also explains the two barrier experiments already in `barrier.py`. E-B2 (no
orientation with an arc is hereditarily 2-d kernelled) is this proposition. E-B1
(`t`-kernel-perfect forces `Delta+ <= t`) is the same two-vertex argument with a degree
threshold inserted: pick `u` with ambient out-degree above `t` and any out-neighbour `v`,
and `S = {u, v}` kills it again.

The obstruction is not about the graph being complicated. It is about **colour classes of
size two containing an edge**. Two vertices cannot 2-dominate each other.

## Calibrating the target, before choosing a way round

Independently of the method, is `ceil(Delta+/2) + 1` even a true statement about any
interesting class? Taking `D` to be the best possible orientation (`min Delta+`, which by
Hakimi's theorem equals `max over subgraphs H of ceil(|E(H)|/|V(H)|)`), the bound
`chi <= ceil(min Delta+ / 2) + 1` fails for:

| n | graphs | fail `chi <= D+1` | fail `chi <= ceil(D/2)+1` |
|---|---:|---:|---:|
| 3 | 4 | 1 | 1 |
| 4 | 11 | 3 | 4 |
| 5 | 34 | 12 | 21 |
| 6 | 156 | 54 | 121 |

The first failure is the triangle: `min Delta+ = 1`, bound 2, `chi = 3`. Then `C_5` and
`K_4`. (These are not counterexamples to the kernel method itself, because kernel-perfectness
forces `Delta+` back up. They measure how aggressive the halved bound is.)

In the symmetric setting (`G` read as a digraph with both arcs, where `d+ = d`) the same
accounting gives `ch <= ceil(Delta/2) + 1`. Testing that against Reed's form on all graphs
up to 6 vertices:

| n | graphs | fail `chi <= ceil(Delta/2)+1` | fail Reed `chi <= ceil((Delta+1+omega)/2)` |
|---|---:|---:|---:|
| 3 | 4 | 1 | 0 |
| 4 | 11 | 2 | 0 |
| 5 | 34 | 8 | 0 |
| 6 | 156 | 26 | 0 |

The halved bound fails on 26 of the 156; adding `omega/2` of slack repairs every one of
them. See `verify_reed.py`.

The shape that survives these is **Reed's**: `chi <= ceil((Delta + 1 + omega)/2)`. It is a
halving result carrying about `omega/2` of extra slack, and that slack is exactly what
rescues `K_3`, `C_5` and `K_4`. So the honest target for this route is Reed-shaped, and a
natural guess is that the `omega/2` is the price of the vertices the barrier forces us to
excuse. The list version of the Reed bound is the prize.

## Five ways round the barrier, ranked by my estimate of the odds

**(B1) Stop quantifying over every `S`.** We choose which colour to process. We need only
that **some** colour class admits a good `K` at each step, and colour classes are coupled:
`sum over c of |V_c| = sum over v of |L(v)| >= n k`. A size-2 colour class is cheap for the
adversary to plant once, but it cannot plant one for every colour while keeping all lists
large. This turns a hereditary structural question into a counting and scheduling question,
and it is the break that fits the barrier best, because the barrier is a statement about one
tiny `S`, not about the graph.

**(B2) Stop demanding a uniform invariant; allow slack and amortise.** With
`f(d) = ceil(d/2) + 1` we have `f(d) - f(d-1) = 1` for `d` odd and `0` for `d` even. So a
vertex hit by the bad case loses nothing at all half the time, and the deficit in the bad
case is exactly 1. Track `Phi(v) = |L(v)| - 1 - ceil(d+(v)/2)` and allow it to dip if repaid.
A parity-aware argument has genuine room here.

**(B3) Go fractional.** Ask for `x : V -> [0,1]` with `x` fractionally independent and
`sum over N+(v) of x >= 2`. Fractional kernels always exist (Scarf's lemma, via Aharoni and
Holzman), which is the strongest available hint that the integral demand is the wrong one.
The question is whether a fractional 2-d kernel can drive Step 5 directly.

**(B4) Change what the induction deletes.** The barrier is attached to deleting a colour.
Thomassen-style inductions delete a vertex and strengthen the hypothesis instead, and are
immune to it.

**(B5) Ask for less.** A gain only on high out-degree vertices, giving something like
`(1 - eps) Delta+`, rather than a clean halving.
