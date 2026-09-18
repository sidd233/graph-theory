# 12. Lemma 1 provably fails on `K_4`, `K_6` and `K_8`

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## The reduction

By the star lemma (`09`), a kernel-perfect orientation of `L(G)` is a **linear order at each
vertex of `G`**. Write `M(u,v)` for the number of edges at `u` that `uv` points to, so each row
of `M` is a bijection onto `{0, ..., d_u - 1}` and

```
d+(uv) = M(u,v) + M(v,u).
```

Lemma 1 of chapter 33 with lists of size `k` therefore needs `M(u,v) + M(v,u) <= k - 1`
everywhere. A triangle `ijk` of `G` is a triangle of `L(G)`, and reading its three shared
vertices gives, with `p = M(i,j)`, `q = M(j,k)`, `r = M(i,k)` in the tight case
`M(u,v) + M(v,u) = s`:

```
e -> f at j   iff   p + q < s
f -> g at l   iff   r > q
g -> e at i   iff   r > p
```

so the triangle is **cyclic**, hence has no kernel, exactly when

```
(p + q < s  and  r > p  and  r > q)   or   (p + q > s  and  r < p  and  r < q).
```

If no `M` avoids this on every triangle, then `L(G)` has no kernel-perfect orientation thin
enough, and **Lemma 1 cannot prove the conjecture for `G`**, whatever else is true.

## The result

| `G` | `Delta` | `chi'` | class | triangles | order exists? |
|---|---:|---:|---:|---:|---|
| `K_{3,3}`, `K_{4,4}`, `Q_3`, `C_6` | | | 1 | 0 | exists, as Galvin guarantees |
| **`K_4`** | 3 | 3 | 1 | 4 | **none** |
| **`K_6`** | 5 | 5 | 1 | 20 | **none** |
| **`K_8`** | 7 | 7 | 1 | 56 | **none** |
| prism `C_3 x K_2` | 3 | 3 | 1 | 2 | **none** |
| `K_{2,2,2}` | 4 | 4 | 1 | 8 | **none** |
| `C_5 x K_2` | 3 | 3 | 1 | 0 | passes the triangle test vacuously; **undecided**, see `11` |
| `C_5`, `C_7`, Petersen | | | 2 | | exists (class 2 leaves slack) |

The `K_4` row agrees with the independent exhaustive search over all 4096 orientations of the
octahedron in `07`, which is the check that the reduction is right.

## Why this is the result the project was looking for

**`K_{2n}` is the hard open case of the conjecture.** `chi'(K_{2n}) = 2n - 1`, and whether
`ch'(K_{2n}) = 2n - 1` is exactly what is not known in general. The three smallest instances
are `K_4`, `K_6`, `K_8`, and **Lemma 1 cannot prove any of them.**

This is not "we could not find an orientation". The search is exhaustive over the whole space
the star lemma leaves, so the conclusion is a proof of impossibility for the method.

It also explains the shape of the literature. Galvin's theorem is bipartite; the recent
progress on complete graphs (arXiv 2608.22895, `K_{p-1}` and `K_{2p}` for odd primes `p`) is
**Alon-Tarsi**, not kernels. Our computation says why: kernels are not available there at all.

## Where the obstruction lives

In the tight regime (`Delta`-regular, class 1) the budget is exactly consumed, so
`M(u,v) + M(v,u) = Delta - 1` with no slack anywhere, and every triangle must come out
acyclic. Two clean observations:

  - **Bipartite graphs solve the system** by a proper `Delta`-edge-colouring, counting up on
    one side and down on the other. The bipartition is exactly what decides which side counts
    which way, which is the precise role of Galvin's hypothesis.
  - **Every triangle-containing example tested fails.** `K_4`, `K_6`, `K_8`, the prism and
    `K_{2,2,2}` all have triangles and all fail. `C_5 x K_2` is triangle-free, so the triangle
    test says nothing about it and is passed vacuously.

**Working conjecture.** For `G` regular and class 1, a thin kernel-perfect orientation of
`L(G)` exists only if `G` is triangle-free. Bipartite implies triangle-free, so this would
contain Galvin's theorem's reach and would say that triangles, not odd cycles in general, are
what stop the kernel method.

Two things would settle it: a proof of the triangle case from the displayed cyclicity
condition, and the full kernel-perfectness check on `C_5 x K_2`, whose order passes the
triangle test but whose orientation has not yet been verified kernel-perfect. Both are running.
