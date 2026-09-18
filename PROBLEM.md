# The problem

**Goal: improve the bound on the list colouring problem, using 2-d kernels.**

**Source:** M. Aigner and G. M. Ziegler, *Proofs from THE BOOK*, chapter 33,
"The Dinitz problem", pages 221 to 226. That chapter is a chapter about list colouring, and
its Lemma 1 is the bound this project is trying to improve. Everything below is in its
notation.

**Companion:** `~/work/acads/sem7/8_rp/graph_theory_research_plan.pdf`, the capstone research
plan submitted to the supervisor, T. K. Mishra, NIT Rourkela. That plan is about the
structural characterization of digraphs with 2-d kernels, and those results are considered
good. The supervisor's direction is that the next step is to improve the list colouring bound.
That is this project's goal.

---

## 1. The statement

For a graph `G = (V, E)`, a **list colouring** assigns to each vertex `v` a set `C(v)` of
colours and asks for a colouring `c : V -> union of C(v)` with `c(v)` in `C(v)` and adjacent
vertices differently coloured. The **list chromatic number** `chi_ell(G)`, also written
`ch(G)`, is the smallest `k` such that a list colouring exists whenever `|C(v)| = k` for all
`v`.

Since ordinary colouring is the case where all `C(v)` are equal,

```
chi(G) <= chi_ell(G)      for every graph G.
```

The inequality can be arbitrarily bad: there are graphs with `chi(G) = 2` and `chi_ell(G)`
arbitrarily large, the smallest example being `K_{2,4}`, which has `chi = 2` and
`chi_ell = 3`.

### THE PROBLEM

> **Lower the upper bound on `chi_ell(G)` that Lemma 1 of chapter 33 provides.**

Lemma 1 gives `chi_ell(G) <= Delta+(D) + 1` for a suitable orientation `D`. The aim is to
replace the `+ 1` accounting by something that charges one colour against **two** units of
out-degree, giving roughly

```
chi_ell(G) <= ceil(Delta+(D) / 2) + 1,
```

by strengthening the kernel in Lemma 1 to a **2-d kernel**.

### What this problem is not

Chapter 33 closes, on page 226, with a one-sentence open question: does
`chi(H) = chi_ell(H)` hold for every line graph `H`? That is the List Colouring Conjecture.
It is an **exactness** claim, that two numbers already known are equal, and it is a different
question from lowering a bound. Notes `06` to `12` in `list-colouring/`, and the LaTeX
document `latex/kernel-orientations-of-line-graphs.tex`, were written against that target
during a period when this document wrongly named it as the goal. **They are kept because the
star lemma and the even-complete-graph theorem in them are real results, but they are not the
goal.** Do not treat work on line graphs as progress here without saying plainly that it is a
change of target.

---

## 2. The method to be improved, as given in the chapter

### Lemma 1 (the kernel lemma), page 223

For a directed graph `G_vec`, a **kernel** `K` is a set of vertices such that

  (i) `K` is independent in `G`, and
  (ii) for every `u` not in `K` there is a `v` in `K` with an edge `u -> v`.

> **Lemma 1.** Let `G_vec` be a directed graph and suppose that for each vertex `v` the colour
> set `C(v)` satisfies `|C(v)| >= d+(v) + 1`. If every induced subgraph of `G_vec` possesses a
> kernel, then there is a list colouring of `G` with a colour from `C(v)` for each `v`.

The proof is induction on `|V|`. Pick a colour `c`, let `A(c)` be the vertices whose list
contains `c`, take a kernel `K(c)` of the induced subgraph on `A(c)`, colour all of `K(c)`
with `c`, and delete `K(c)` and `c`. For every `v` in `A(c)` outside `K(c)`, condition (ii)
drops `d+(v)` by at least one while the list drops by exactly one, so the hypothesis survives.

**This exchange of one colour for one unit of out-degree is the whole strength of the method,
and it is the only place the kernel property is used.** Replacing (ii) by 2-domination is
meant to buy two units of out-degree per colour, which is where the halving would come from.

### Lemma 2 (stable matchings), page 224

Every bipartite graph with rankings at every vertex has a stable matching. Proved by the
Gale and Shapley proposal algorithm. This is how the chapter manufactures a kernel in **every**
induced subgraph, which is the hereditary condition Lemma 1 needs.

### The Theorem, page 225

> **Theorem (Galvin).** `chi_ell(S_n) = n` for all `n`.

`S_n` is the graph on the `n^2` cells of an `n` by `n` array, two cells adjacent when they
share a row or a column. The proof takes a Latin square, orients `S_n` horizontally from
smaller to larger entry and vertically the other way, giving `d+ = n - 1` everywhere, and then
uses a stable matching to produce a kernel in every induced subgraph. Lemma 1 then applies.

**This is the template to imitate.** The Dinitz proof is the worked example of all three
requirements being met at once, and it is the reason to believe the 2-d kernel version might
be made to work.

---

## 3. The three requirements, which are the core of the problem

A class `C` of digraphs delivers `chi_ell(G) <= ceil(Delta+/2) + 1` exactly when:

  - **(R1) Existence.** Every `G` in the graph class has an orientation `D` in `C` whose
    `Delta+` is small. A 2-d kernel has to exist at all.
  - **(R2) Heredity.** `C` is closed under the deletion at Step 4 of the induction, and since
    Step 2 is applied to `D[S]` for a set `S` the adversary controls, `C` must be closed under
    **arbitrary induced subdigraphs**. The 2-d kernel has to survive when one is removed,
    exactly as in the Dinitz proof, where a stable matching supplies a kernel for every
    induced subgraph rather than only for the whole graph.
  - **(R3) Mapping.** The list colouring problem has to be mapped onto such a class: the
    independent set produced at Step 2 must actually do the accounting work at Step 5.

**Solving (R1), (R2) and (R3) together is the core of this problem.** Each alone is
approachable. The difficulty is entirely in the interaction, and (R2) is the one that bites.
Everything else in the induction is bookkeeping.

### The weakest honest form of (R3)

A vertex `u` outside `K` only loses the colour `c` if it is **adjacent** to a vertex of `K`.
A vertex with no neighbour in `K` pays nothing and needs no compensation. So Step 5 goes
through under the weaker

> **(star)** For every `W` and every `S` inside `W`, there is a nonempty independent `K`
> inside `S` such that every `u` in `S \ K` **adjacent to `K`** has at least two out-neighbours
> in `K`.

Any barrier should be tested against (star), not against the stronger "`K` is a 2-d kernel of
`D[S]`", so that a failure is conclusive rather than an artefact of demanding too much.

---

## 4. What this project has established, and the two obstructions that must be answered

Recorded in full in `list-colouring/`, with code for every number.

### Obstruction A: the two-vertex barrier, against (R2) as literally stated

**Proposition.** No digraph with an arc satisfies (star).

*Proof.* Let `u -> v` be an arc. Take `S = {u, v}`. The nonempty independent subsets of `S`
are `{u}` and `{v}`. If `K = {v}` then `u` is adjacent to `K` and `|N+(u) cap K| <= 1 < 2`.
If `K = {u}`, the same for `v`. No choice works. QED

Verified exhaustively over all 3, 63 and 4095 digraphs with at least one arc on 2, 3 and 4
vertices, in `list-colouring/verify_barrier.py`. In every case the smallest failing `S` has
size 2, so the two-vertex configuration is the whole obstruction and not one of many.

**Consequence as stated:** a class closed under induced subdigraphs in which every member has
a 2-d kernel is a class of arcless digraphs, so the conditional theorem is vacuous. Two
vertices cannot 2-dominate each other. Proved in full as
`latex/hereditary-2-d-kernels-are-arcless.tex`.

**Corrected, 2026-09-16. The barrier is not fatal to (R2).** (star) demands two out-neighbours
in `K`. The accounting lemma demands only that `f` drop by one, and with
`f(d) = ceil(d/2) + 1` a single out-neighbour does that whenever `d+(u)` is odd. The single
arc `u -> v` therefore passes: take `K = {v}`, and `f(1) - f(0) = 1`. So the barrier closes the
2-d kernel demand, not the requirement the proof consumes. Notes `14` and `15`.

Restating (R2) with the correct object gives the **parity-processable** digraphs, and that
class is emphatically not arcless: 154 of its 155 members on 6 vertices carry an arc. It is,
however, sparse, with at most `n` edges and degeneracy at most 2 up to `n = 7`, and always
bipartite, so it still carries no useful bound. (R2) for every `S` is closed on merit rather
than by the barrier. See `list-colouring/parity_processable.py`.

**Why this is not yet the end.** The barrier is a statement about one tiny `S`, not about the
graph. The induction gets to **choose which colour to process**, and the colour classes are
coupled through `sum |C(v)|`. Quantifying over every `S` is therefore the assumption most
likely to be too strong. Weakening (R2) from "every induced subdigraph" to "some processable
colour class at each step" is route (B1) and is the most promising line.

### Obstruction B: the degree floor, against the size of the target

Any method in this family, kernels, 2-d kernels, or Alon-Tarsi, needs an orientation with
small `Delta+`. The graph polynomial has degree `|E|`, so some out-degree is at least `|E|/n`,
which puts a floor of roughly `mad/2 + 1` under the whole family. Recorded in
`list-colouring/05-alon-tarsi.md`.

**This floor has not been independently re-derived and is carrying a lot of weight.** It was
written quickly in a session that was moving fast. If it holds it caps how far the bound can
fall, and if it has a gap that gap is the project.

**The remainder term, added 2026-09-16.** The induction never reaches the empty digraph, so
the honest statement carries the size `r` of a stalled state. Theorem 14.4 of note `14` proves
`ch(G) <= f(Delta+) + r - 1` unconditionally, which for the halved accounting is
`ceil(Delta+/2) + r`. That beats the ordinary kernel bound exactly when

> `r <= floor(Delta+ / 2)`.

`r >= 3` unconditionally, since a three-vertex star stalls and is a genuine counterexample to
the per-vertex halved bound. Over all digraphs `r` is unbounded: strongly connected
tournaments stall at every size, and they have `n = 2 Delta+ + 1`, so they miss the criterion
by a factor of about four. Any theorem of this shape must therefore restrict the class, and
what it has to exclude is large cliques carrying no sink, which is where the clique number in
Reed's form comes from. See `list-colouring/stall_census.py`.

**Measured, 2026-09-16, and the floor holds.** Note `16` states it precisely: writing
`D*(G) = min over orientations Delta+`, which by Hakimi is about `mad/2`, the claim is

> `min over orientations D of [ ceil(Delta+(D)/2) + max(1, r(D)) ] >= D*(G) + 1`.

This is the negation of the criterion above, so the two are one statement. Over every graph on
at most 6 vertices, minimising over every orientation, **no graph beats the floor**: 47 of 207
meet it exactly and 160 do worse. The clean halving never converts into a bound below
`D* + 1`.

The structural reason is Lemma 16.2: no digraph keeps every out-degree odd in every induced
subdigraph, because deleting an out-neighbour of `u` flips the parity at `u`. So the parity
escape that rescues (R2) from the two-vertex barrier is a boundary effect, not something an
induction can lean on. The barrier, the escape and the floor are one obstruction seen three
times. Verified but not proved, and only to 6 vertices; see `list-colouring/floor.py`.

### Calibration: how aggressive the halved target is

With the best possible orientation, `chi <= ceil(Delta+/2) + 1` already fails for 121 of the
156 graphs on 6 vertices, the first failure being the triangle. So the naive halved bound
cannot hold on any broad class, and the realistic target carries slack, in the shape of Reed's
`ceil((Delta + 1 + omega)/2)`. On the same 156 graphs Reed's form fails zero times. Working
hypothesis: the `omega/2` slack is the price of exactly the vertices the barrier forces us to
excuse.

---

## 5. Standing instructions for work on this project

  1. The problem is the one in section 1, improving the bound. Do not silently substitute an
     adjacent problem, and in particular do not substitute the line graph conjecture.
  2. If a proposed direction does not serve section 1, say so plainly before proposing it.
  3. Use the chapter's notation: `chi_ell`, `C(v)`, `d+(v)`, kernel, `S_n`.
  4. Call the independent plus 2-dominating sets **2-d kernels**, never "2-kernels" and never
     "k-kernels", to keep them distinct from the distance-based `(k,l)`-kernel of the
     published literature.
  5. Before refining a method, check that the method can reach the target at all. Check the
     obstruction before running the experiment. Equally, check that the obstruction is stated
     against what the proof actually consumes: the two-vertex barrier stood for several notes
     as fatal to (R2) because it was stated against a sufficient condition rather than a
     necessary one.
  6. Discuss the direction before running experiments.
  7. Keep `list-colouring/LOG.md` current, recording the reasoning and not just the results.
