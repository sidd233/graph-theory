# 4. The colour-choice route (B1): worked out, and where it lands

## The correction that had to come first

The plain 2-d kernel framing asks every affected vertex for two edges into the coloured set.
That is too harsh. The induction carries `|L(v)| >= f(d(v))` with `f(d) = ceil(d/2) + 1`, and
a vertex `u` with `a` neighbours in the coloured set `K` survives iff `f(d) - f(d-a) >= 1`:

| `a` | condition | verdict |
|---|---|---|
| 0 | keeps the colour, loses nothing | fine |
| `>= 2` | `f` drops by at least 1 | fine |
| 1, `d` **odd** | `f(d) - f(d-1) = 1` | **fine** |
| 1, `d` **even** | `f(d) - f(d-1) = 0` | the only bad case |

So one edge into `K` is enough whenever the vertex currently has **odd degree**. Degrees are
taken in the whole current graph, not inside the colour class. This roughly doubles the
supply of usable colour classes and was absent from the earlier framing.

It does not rescue the hereditary route. Under the parity condition the hereditary demand
fails for any `G` containing a path on four vertices `x - u - v - y`: take `W` to be those
four, so `d_W(u) = d_W(v) = 2`, and let the colour class be `S = {u, v}`. Both endpoints are
even, so neither choice of `K` works. Hereditary is dead, parity or no parity.

## The exact stalling criterion

Call a colour class `S` **good** (in the current graph `W`) if some nonempty independent
`K` inside `S` satisfies the table above for every vertex of `S \ K`. Call a vertex `v`
**safe** if every colour class containing `v` is good.

**Proposition.** The method stalls at `W` if and only if no vertex of `W` is safe.

*Proof.* If `v` is safe, any colour in `L(v)` gives a good class, so we can proceed. If no
vertex is safe, each `v` lies in some bad class `S_v`; give `v` its own `f(d_W(v))` private
colours all with class `S_v`. Every list is large enough and every class is bad. QED

This is a much weaker demand than a hereditary 2-d kernel, so it was worth testing.

## What the criterion delivers

Exhaustive over all graphs up to 6 vertices, asking whether every induced subgraph has a
safe vertex:

| n | graphs | survive | forests |
|---|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 |
| 3 | 4 | 3 | 3 |
| 4 | 11 | 6 | 6 |
| 5 | 34 | 10 | 10 |
| 6 | 156 | 20 | 20 |

**The survivors are exactly the forests.** Spot checks agree at 7 and 8 vertices: trees,
spiders and subdivided stars survive; `C_4`, `C_6`, `C_8`, `K_{2,3}`, `K_{3,3}` and the cube
all fail, and every recorded failure is on an induced cycle.

Half of that is provable in two lines. **If `G` contains a cycle, the method stalls.** A
shortest cycle is induced, so take `W` to be its vertices. Every vertex of `W` then has
degree exactly 2, which is even, so for any edge `uv` of the cycle the class `S = {u, v}`
is bad. No vertex of `W` is safe. QED

## Verdict on the halving target

For a forest `ch = 2`, while the bound proved is `ceil(Delta/2) + 1`, which is never better
and usually much worse. So the method certifies nothing on the only class where it runs.

**The halving target `ch <= ceil(Delta/2) + 1` is dead by this route as well**, and now for
a sharper reason than the hereditary barrier: it is not that no class survives, it is that
the class that survives is exactly the one where the bound is worthless.

## Where life remains

The method does not fail abruptly. Aiming at `ch <= ceil(lam * Delta) + 1` for `lam` between
1/2 and 1, and counting survivors among the 156 graphs on 6 vertices:

| `lam` | 1 | 4/5 | 3/4 | 2/3 | 1/2 |
|---|---:|---:|---:|---:|---:|
| survivors | 156 | 145 | 115 | 63 | 20 |
| forests only? | no | no | no | no | **yes** |

At `lam = 2/3` and `3/4` the surviving class still contains triangles and non-bipartite
graphs, so it is not a degenerate class. Caveat: graphs on 6 vertices have `Delta <= 5`, and
for small `Delta` a coarse `lam` is indistinguishable from the greedy bound, so these middle
columns need re-running at larger `Delta` before they mean anything.

**The question this session leaves open, and the one worth attacking next:** what is the
smallest `lam` for which a genuinely rich class survives? `lam = 1` is free and `lam = 1/2`
is empty of content. The honest target is somewhere in between, and a bound of the form
`ch <= (3/4) Delta + 1` on a real class would still be a worthwhile theorem.

---

# 5. The large-degree sweep, and what it killed

## Faster exact test

Two prunes make the exact criterion cheap enough to run at 8 to 10 vertices (`fast.py`,
validated against the slow version: it reproduces 156, 145, 115, 63, 20 at `n = 6`).

Write `f(d) = ceil(lam*d) + 1` and call a degree `d` **bad** when `f(d) - f(d-1) = 0`, so a
vertex of that degree cannot pay for a lost colour with one edge. For `lam = (q-1)/q` the
bad degrees are exactly the multiples of `q`, so bad degrees have density `1 - lam`.

  - **Prune 1.** If the current graph has no bad-degree vertex, every colour class is good,
    since `K` = one vertex works. No search needed.
  - **Prune 2.** A class `S` is good as soon as some `u` in `S` has all of its `S`-neighbours
    of good degree. So a bad `S` must have every vertex adjacent, inside `S`, to a
    bad-degree vertex of `S`. That kills almost every subset immediately.

## Correction to section 4

Survival is **not** monotone in `lam`: the bad-degree sets for different `lam` are not nested
(`4/7` is bad at degrees 3, 5, 7 while `5/8` is bad at 3, 6, 8). So the right quantity is the
best bound over every surviving `lam`, not the first `lam` that survives.

With that fix, the claim in section 4 that the method certifies nothing on forests is
**wrong**. Forests survive at arbitrarily small `lam`, and then the bound is `ch <= 2`, which
is exactly right. The halving target `lam = 1/2` is a bad choice for forests, not a verdict
on them.

## The honest benchmark, and the result

The method is worth something only if it beats what is free: greedy `Delta + 1`, and the
degeneracy bound `ch <= degen + 1`.

| graph | `Delta` | greedy | `degen+1` | method | verdict |
|---|---:|---:|---:|---:|---|
| `K_{1,m}`, m = 3..9 | up to 9 | up to 10 | 2 | 2 | ties |
| `K_{2,3}` | 3 | 4 | 3 | 3 | ties |
| `K_{2,7}` | 7 | 8 | 3 | 5 | loses |
| `K_{3,3}`, `K_{4,4}`, `K_{5,5}` | 3, 4, 5 | 4, 5, 6 | 4, 5, 6 | 4, 5, 6 | ties |
| `C_4` to `C_9` | 2 | 3 | 3 | 3 | ties |
| cube `Q_3` | 3 | 4 | 4 | 4 | ties |

Then a direct hunt for any exception: **1600 random graphs on 6 to 9 vertices across six
densities, zero winners.** Searching only the `lam` that could possibly win makes this cheap,
because those are the small `lam`, which are exactly the hardest to survive.

**Finding.** In the symmetric setting the method never beats the degeneracy bound. It ties it
at best and is often worse. Conjecture, on that evidence: the method's bound is always at
least `degen + 1`.

## The flaw this exposed in the experiment, not just in the method

I ran the whole of sections 4 and 5 with `G` as an undirected graph, where out-degree equals
degree. **That is precisely the setting in which even the ordinary kernel method is worthless**,
since it degenerates to `ch <= Delta + 1`, the greedy bound. The kernel method's entire power
comes from using an **orientation**: by Hakimi, `min Delta+ = max over subgraphs of
ceil(|E(H)|/|V(H)|)`, which can be about half the degeneracy.

| graph | `Delta` | `degen+1` | `min Delta+ + 1` | 2-d kernel dream |
|---|---:|---:|---:|---:|
| `K_{3,3}` | 3 | 4 | 3 | 2 |
| `K_{4,4}` | 4 | 5 | 3 | 2 |
| `K_{5,5}` | 5 | 6 | 4 | 3 |
| cube `Q_3` | 3 | 4 | 3 | 2 |

So there is real room below the degeneracy bound, and it is all in the oriented setting,
which I did not test. The symmetric result stands as a theorem about a setting with no
headroom in it, which is much weaker evidence than it first looked.

## Where this leaves the project

  - Halving is dead three times over: hereditarily, with parity, and now with free colour
    choice. Stop proposing it.
  - The symmetric setting is settled and empty. Stop testing there.
  - **The next experiment is the same machinery run on orientations**, where a vertex pays with
    out-edges only and `Delta+` is roughly half the degeneracy. The parity correction, the
    safe-vertex criterion, the two prunes and the `lam` sweep all carry over unchanged. The
    extra difficulty is real and must be handled: a vertex loses a colour when any neighbour
    is coloured, but only pays out-degree for out-neighbours, which is exactly what ordinary
    kernel-perfectness is there to fix.
