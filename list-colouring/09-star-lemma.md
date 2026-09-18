# 11. What a kernel-perfect orientation of a line graph must look like

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## Lemma (stars are linearly ordered)

> Let `D` be a kernel-perfect orientation of `L(G)`. Then for every vertex `v` of `G`, the
> arcs of `D` among the edges of `G` incident with `v` form a **transitive** tournament.
> Equivalently, `D` induces a **linear order** on `E(v)` for every `v`.

*Proof.* The set `E(v)` of edges at `v` is a clique in `L(G)`, since any two of them share `v`.
In a clique a kernel must be a single vertex, because a kernel is independent, and that vertex
must have no out-arc inside the clique, so it is a **sink**. Kernel-perfectness requires every
induced subgraph to have a kernel, so every subset of `E(v)` must contain a sink. A tournament
in which every subset has a sink is exactly a transitive tournament. QED

Verified exhaustively on all tournaments up to 6 vertices: "every subset has a sink" and
"transitive" pick out the same tournaments, 2, 8, 64, 1024 and 32768 of them respectively
(`stars.py`).

## What this says about Galvin's proof

Galvin orients `S_n` by the entries of a Latin square: along a row from the smaller entry to
the larger, along a column the other way. That gives a linear order on each row and each
column, which are exactly the sets `E(v)` for `K_{n,n}`.

**The lemma says he had no choice.** Any kernel-perfect orientation of a line graph is a
linear order at every vertex of `G`. The Latin square is not a convenient device, it is the
general shape of the only orientations that can work.

## The reduction this gives

Write `a_u(e)` for the number of edges `f` at `u` with `e -> f`, so `a_u` runs over
`{0, 1, ..., d_u - 1}` bijectively as `e` runs over `E(u)`. For an edge `e = uv`,

```
d+(e) = a_u(e) + a_v(e).
```

So Lemma 1 of chapter 33 applies to `L(G)` with lists of size `k` exactly when we can choose a
linear order at each vertex with `a_u(e) + a_v(e) <= k - 1` for every edge, **and** the
resulting orientation is kernel-perfect. That replaces a search over `2^|E(L(G))|` orientations
by a search over `prod over v of d_v!` orderings, and for `K_6` that is the difference between
`2^60` and about `10^12`.

## The tight regime: regular class 1 graphs

If `G` is `Delta`-regular with `chi' = Delta` (class 1), then

```
|E(L(G))| = N * C(Delta, 2) = (Delta - 1) * |E(G)|,
```

so the out-degree budget is **exactly** consumed and `a_u(e) + a_v(e) = Delta - 1` must hold
for **every** edge, with no slack anywhere. Writing `M(u,v) = a_u(uv)`, the requirement is

```
M(u,v) + M(v,u) = Delta - 1,   and   {M(u,w) : w ~ u} = {0, 1, ..., Delta - 1} for every u.
```

For bipartite `G` this is solved by any proper `Delta`-edge-colouring: set `M(u,v) = c(uv) - 1`
on one side and `M(v,u) = Delta - c(uv)` on the other. **That is Galvin's construction, and it
needs the bipartition to decide which side counts up and which counts down.**

For `K_4` the system above is satisfiable (take the `(Delta-1)/2` values on a perfect matching),
so the obstruction there is **not** counting. It is the triangles: `L(K_4)` contains triangles
coming from triangles of `K_4`, and every solution makes one of them a directed triangle.

**`K_{2n}`, the hard open case of the conjecture, is exactly this tight regular class 1 regime.**
