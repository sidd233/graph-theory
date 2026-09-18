# 14. THEOREM: Lemma 1 cannot prove the conjecture for any even complete graph

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

This settles, for the kernel method, the whole of the hard open case of the conjecture.

## Statement

> **Theorem.** Let `m >= 4` be even. Then `L(K_m)` has **no** kernel-perfect orientation with
> `Delta+ <= chi'(K_m) - 1 = m - 2`. Consequently **Lemma 1 of chapter 33 cannot prove
> `ch'(K_m) = chi'(K_m)`**, for any even `m`.

`chi'(K_m) = m - 1` for even `m`, and whether `ch'(K_m) = m - 1` is exactly the open case the
literature is stuck on. The theorem says the chapter's own method is unavailable there, for
every even `m` at once.

## Proof

**Step 1 (the star lemma, section `09`).** In a kernel-perfect orientation of `L(G)`, the edges
at each vertex `u` of `G` form a clique whose every subset needs a sink, so that clique is a
transitive tournament. Write `M(u,v)` for the number of edges at `u` that `uv` points to. Each
row `M(u, .)` is a bijection onto `{0, 1, ..., d_u - 1}`, and for `e = uv`,
`d+(e) = M(u,v) + M(v,u)`. For two edges `e, f` sharing `w`, `e -> f` iff `M(w, e\w) > M(w, f\w)`.

**Step 2 (the budget is exactly consumed).** For `K_m` with `m` even, every degree is `m - 1`
and `chi' = m - 1`, so

```
|E(L(K_m))| = m * C(m-1, 2) = m(m-1)(m-2)/2 = (m-2) * |E(K_m)|,
```

and `d+ <= m - 2` over `|E(K_m)|` vertices of `L(K_m)` leaves no slack. Hence, writing
`s = m - 2`,

```
M(u,v) + M(v,u) = s     for every edge uv.
```

**Step 3 (fix an extreme pair).** Fix any vertex `i`. Row `i` is a bijection onto `{0,...,s}`,
so there is a unique neighbour `j` with `M(i,j) = 0`, and then `M(j,i) = s - 0 = s`.

**Step 4 (every triangle through `ij` forces one inequality).** Let `k` be any vertex other
than `i` and `j`, so `ijk` is a triangle of `K_m` and `ij, jk, ik` is a triangle of `L(K_m)`.

  - At `j`: `ij -> jk` iff `M(j,i) > M(j,k)`. Now `M(j,i) = s` is the largest value in row `j`
    and `M(j,k) != M(j,i)`, so this **always** holds.
  - At `i`: `ik -> ij` iff `M(i,k) > M(i,j) = 0`. Now `M(i,k) != 0` since `0` is taken by `j`
    in row `i`, so this **always** holds.
  - At `k`: `jk -> ik` iff `M(k,j) > M(k,i)`, i.e. `s - M(j,k) > s - M(i,k)`, i.e.
    `M(i,k) > M(j,k)`.

The first two arcs are `ij -> jk` and `ik -> ij`. If the third is `jk -> ik` the triangle is the
directed cycle `ij -> jk -> ik -> ij`, which has no kernel. So kernel-perfectness forces the
third arc the other way, and since `M(k,i) != M(k,j)` gives `M(i,k) != M(j,k)`,

```
M(i,k) < M(j,k)      for every k outside {i, j}.
```

**Step 5 (sum, and contradict).** There are `m - 2 = s` such `k`. Summing the inequality:

```
sum over k of M(i,k) = (row i total) - M(i,j) = s(s+1)/2 - 0   = s(s+1)/2
sum over k of M(j,k) = (row j total) - M(j,i) = s(s+1)/2 - s
```

so `s(s+1)/2 < s(s+1)/2 - s`, that is `0 < -s`. Since `s = m - 2 >= 2`, this is false. No such
`M` exists, so no kernel-perfect orientation of `L(K_m)` is thin enough. QED

## Checks

  - Exhaustive search over all orderings finds no valid `M` for `K_4`, `K_6` and `K_8`,
    agreeing with the theorem (`tight.py`).
  - For `K_4` this also agrees with the wholly independent brute-force search over all 4096
    orientations of the octahedron in section `07`.
  - The proof uses only `m` even (so that `chi' = m - 1` and the budget is tight) and `s >= 1`.

## Where the proof gets its force

It never looks at a triangle in isolation. The local analysis of section `11` shows single
triangles are perfectly satisfiable once `Delta >= 4`, which is why `K_6` cannot be killed one
triangle at a time. The argument instead fixes the pair `(i, j)` at the extreme of row `i`,
which makes **every** triangle through `ij` point the same way, and then counts. The
contradiction comes from the row sums, not from any one triangle.

## Consequences

  - **The whole hard open case is closed to Lemma 1.** Whatever proves `ch'(K_{2n}) = 2n - 1`,
    it is not the kernel method.
  - This explains the shape of the literature directly: Galvin's theorem is bipartite, and the
    2026 progress on `K_{p-1}` and `K_{2p}` (arXiv 2608.22895) is **Alon-Tarsi**. Our theorem
    says kernels were never an option there.
  - The argument extends verbatim to any `Delta`-regular class-1 `G` having an edge `ij` with
    `N(i) \ {j}` contained in `N(j)`. For regular `G` that forces `N[i] = N[j]`, so the reach
    of this particular argument is exactly disjoint unions of even complete graphs. Extending
    it further needs a different way to aggregate the triangle inequalities.

---

## Relation to the literature (checked, September 2026)

Jessica McDonald, *On Galvin orientations of line graphs and list-edge-colouring*,
arXiv:1508.01820, proves:

> **Theorem 5 (McDonald).** `L(K_n)` has no proper **Galvin orientation** with respect to
> `chi'(K_n)`, for any `n >= 4`.

**This is not the same statement as ours, and ours is stronger.** A *Galvin orientation* in
her sense is built from one global `k`-edge-colouring `phi` of `G` together with a partition
of `V(G)` into `U` and `D`: at a vertex of `U` the incident edges are ordered by increasing
colour, at a vertex of `D` by decreasing colour. So every vertex uses **the same** colouring
and only chooses a direction.

Our theorem rules out **every** kernel-perfect orientation with `Delta+ <= chi' - 1`, not only
those of that shape. By the star lemma each vertex carries an arbitrary linear order, and for
non-bipartite `G` those orders need not come from any single global edge colouring: reading one
off would require `Delta - a_u(e) = a_v(e) + 1` consistently, which forces a `U`/`D` partition
with one end of every edge in each part, that is, forces `G` bipartite. So on `K_n` the family
of orders our theorem covers is strictly larger than the family of Galvin orientations.

In other words, McDonald's theorem says *Galvin's construction* does not reach cliques; ours
says *the kernel method itself* does not, however the orientation is built.

She also proves a positive companion, **Theorem 6**: `L(K_{Delta+1})` does have a proper Galvin
orientation with respect to roughly `floor(3 Delta / 2)`, and notes this is far from the best
known clique bound, Haggkvist and Janssen's `chi'_ell(K_n) <= n`. She cites Schauz for
`K_{p+1}`, `p` an odd prime.

**Status of our theorem: a strengthening of a published 2015 result, novelty not yet
confirmed.** The next check is Borodin, Kostochka and Woodall's characterisation of
kernel-perfect orientations of line graphs (her Theorem 2: an orientation of a line graph is
kernel-perfect iff every clique has a kernel and every directed odd cycle has a chord or
pseudochord) and the paper *On kernel-perfect orientations of line graphs*, Discrete Math.
Those are where the stronger statement would most plausibly already appear.

## Also settled by the literature check

  - `ch'(K_8) = 7` and `ch'(K_{10}) = 9` are **known**, by Rabern, via signed one-factorization
    counts: `K_8` has 5280 positive and 960 negative one-factorizations, so the Alon-Tarsi
    certificate is `4320 != 0`.
  - Combined with Haggkvist and Janssen for odd `n`, Schauz for `K_{p+1}`, and arXiv 2608.22895
    for `K_{p-1}` and `K_{2p}`, the smallest even complete graphs not covered by any of these
    appear to be around `K_20` and `K_24`.
