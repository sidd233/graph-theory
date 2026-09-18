# 8. The List Colouring Conjecture: current status (checked September 2026)

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## Statement

**Conjecture (Vizing; Gupta; Albertson and Collins; Bollobas and Harris; independently, 1970s).**
For every loopless multigraph `G`, the list chromatic index equals the chromatic index:

```
ch'(G) = chi'(G).
```

In words: when colouring **edges** rather than vertices, lists never cost you anything. It
appeared in print in 1985 and is one of the central open problems in the area.

Note this is a *chromatic-choosability* statement, which is false for vertex colouring
(`ch` can far exceed `chi`, as `K_{m,m}` shows). The claim is that line graphs are special.

## Status: OPEN in general

What is known:

| result | statement | method |
|---|---|---|
| Galvin 1995 | true for **bipartite** multigraphs; also settles the Dinitz conjecture | **kernel method** |
| Kahn 1996 | true **asymptotically**: `ch' <= (1 + o(1)) Delta` | probabilistic |
| Haggkvist and Janssen | `ch'(K_n) <= n`, which settles **odd-order** complete graphs | |
| bounded treewidth, large `Delta` | `ch' = chi' = Delta` | |
| arXiv 2608.22895 (2026) | true for `K_{p-1}` and `K_{2p}` for odd primes `p` | **Alon-Tarsi** |

The unresolved complete-graph case is concentrated in **even order**: `chi'(K_{2n}) = 2n - 1`
and the conjecture asserts `ch'(K_{2n}) = 2n - 1`. Even-order complete graphs are still open
in general, despite the two new infinite families above.

## Why this is the natural home for the tools in this project

Both methods we have built are live here, and they are the two methods that have actually
produced results on it.

**Kernels.** Galvin's proof is the kernel method. He defined a specific orientation of the
line graph of a bipartite graph and showed it is kernel-perfect with out-degree at most
`Delta - 1`. McDonald (arXiv 1508.01820) formalised this as a **Galvin orientation** of a
line graph, proved that a proper Galvin orientation with respect to `k` implies the graph is
`k`-list-edge-colourable, and showed the converse fails. She examined the property on
"bipartite plus an edge", the Petersen graph, cliques, and simple graphs with no odd cycle of
length 5 or more.

**Alon-Tarsi.** The 2026 complete-graph result is a polynomial-method argument, using a
determinant-to-Pfaffian bridge for `K_{p-1}` and a weighted Burnside reduction over signed
one-factorizations for `K_{2p}`. The authors report a "full-support valuation barrier"
appearing at four or more vertex blocks, which is where that approach currently stops.

So the floor established in `05-alon-tarsi.md` is not an obstacle here. On line graphs the
target `chi'` is around `Delta`, which sits **above** the `mad/2` floor, not below it. The
conjecture is not asking for a bound below what these methods can reach. It is asking for
exactness, which is a different kind of question and one these methods can answer.

## Honest assessment of difficulty

This is a fifty-year-old named conjecture that strong people have worked on, and the recent
progress on it uses specialist algebra (Pfaffian sign structure, cyclic starters,
skew-circulant cofactors). It is not a problem to expect to settle.

Two entry points that are proportionate:

  1. **Computational, on the Alon-Tarsi side.** Compute Alon-Tarsi numbers of line graphs of
     small graphs and look for structure, which is what "Orientations of 1-Factorizations and
     the List Chromatic Index of Small Graphs" (arXiv 1705.00484) does. Our `alontarsi.py`
     already computes exactly this quantity, validated. Line graphs are dense, so the arc
     enumeration needs replacing with a better coefficient routine first.
  2. **Structural, on the kernel side, and closer to this project's existing taste.**
     McDonald's question of *which* line graphs admit a proper Galvin orientation is a
     kernel-perfectness question about a specific family of orientations. That is the same
     kind of object the 2-d kernel census was built to study, and the census machinery in
     `census-tool/` transfers.

## Sources

  - Edge list colouring conjecture, Open Problem Garden: http://www.openproblemgarden.org/op/edge_list_coloring_conjecture
  - McDonald, On Galvin orientations of line graphs and list-edge-colouring: https://arxiv.org/abs/1508.01820
  - The List Edge-Coloring Conjecture for Two New Infinite Families of Complete Graphs (2026): https://arxiv.org/html/2608.22895
  - Orientations of 1-Factorizations and the List Chromatic Index of Small Graphs: https://arxiv.org/pdf/1705.00484
  - List-Coloring and Chromatic-Choosability, a Dynamic Survey (2026): https://arxiv.org/abs/2606.31702
