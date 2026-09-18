# 9. The kernel method provably cannot prove the conjecture, and it stops at K_4

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## The target, in the chapter's own terms

Aigner and Ziegler, *Proofs from THE BOOK*, chapter 33, last page:

> Does `chi(H) = chi_ell(H)` hold for every line graph `H`?

Equivalently `ch'(G) = chi'(G)` for every multigraph `G`. This is the **List Colouring
Conjecture**, open since the 1970s. Galvin proved the bipartite case in 1995, using Lemma 1
of that same chapter, which is the kernel lemma the whole 2-d kernel programme was built on.

## What the kernel method needs

Lemma 1 says: if every induced subdigraph of an orientation has a kernel, then `G` is
`L`-colourable whenever `|C(v)| >= d+(v) + 1`. Applied to `H = L(G)`, proving the conjecture
for a given `G` by this route requires exactly:

> `L(G)` has a **kernel-perfect** orientation with `Delta+ <= chi'(G) - 1`.

That is definition-free, so it can be decided by exhaustive search on small graphs, with no
guessing at how "Galvin orientation" should be generalised.

## Result

| `G` | `chi'` | need `Delta+ <=` | kernel-perfect orientation of `L(G)`? |
|---|---:|---:|---|
| `C_4` (bipartite) | 2 | 1 | exists |
| `P_4` (bipartite) | 2 | 1 | exists |
| `K_{2,3}` (bipartite) | 3 | 2 | exists |
| `C_5` | 3 | 2 | exists |
| triangle | 3 | 2 | exists |
| **`K_4`** | **3** | **2** | **none exists** |

`K_4` is the first place the method dies, and the reason is a counting argument:

`L(K_4)` is the octahedron: 6 vertices, 12 edges, 4-regular, 8 triangles. Needing
`Delta+ <= 2` on 12 arcs over 6 vertices forces **every** out-degree to be exactly 2. There
are 38 such orientations, and **all 38 contain a directed triangle**. A directed triangle has
no kernel, so none of them is kernel-perfect.

## Why this matters more than any of the earlier negatives

The conjecture **is true** for `K_4`: `chi'(K_4) = 3`, and `AT(L(K_4)) = AT(octahedron) = 3`,
which we computed in section 7 of these notes. So Alon-Tarsi proves the `K_4` case, and the
kernel method provably cannot.

That reframes this whole project. The 2-d kernel programme was refining a tool that **cannot
reach the target problem even in principle**, and fails at the smallest non-bipartite complete
graph. The three earlier negatives (the single-arc barrier, the path-on-four barrier, the
degeneracy comparison) were all symptoms of refining the wrong base.

Consistent with the literature: McDonald (arXiv 1508.01820) shows that admitting a proper
Galvin orientation is strictly stronger than being `k`-list-edge-colourable, and examines
cliques among her cases. The `K_4` computation here is a concrete instance of that gap.

## What this says about where to go

  - **Kernels are not enough for this conjecture.** Not "hard to extend": provably
    insufficient at `K_4`. Galvin's theorem is essentially the end of that road, and the
    bipartite hypothesis is doing real work, not just simplifying the proof.
  - **Alon-Tarsi is the live tool on the same problem.** It proves `K_4` where kernels cannot,
    and the 2026 progress on complete graphs (arXiv 2608.22895, families `K_{p-1}` and
    `K_{2p}` for odd primes `p`) is Alon-Tarsi based. The hard open case is complete graphs of
    **even** order.
  - The `alontarsi.py` machinery here already computes the relevant quantity and is validated.
    Applying it to line graphs needs a faster coefficient routine, since line graphs are dense.

## Open, concrete, and sized for this project

For which `G` does `L(G)` have a kernel-perfect orientation with `Delta+ <= chi'(G) - 1`?
Bipartite `G` always do (Galvin). `K_4` does not. Charting that boundary on small graphs is
a well-defined question, our census machinery answers it, and the answer would say exactly
how far Galvin's method reaches.
