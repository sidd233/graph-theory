# Broader open problems in graph theory

Compiled 2026-10-07 from general knowledge, not from a systematic search. Statuses are as I
understand them. Re-check any entry against recent literature before investing time in it.

Each entry has a one-line statement, a status, and a fit rating:

- **near**: uses this project's kernel or list colouring tools;
- **mid**: graph colouring, but different tools;
- **far**: a different area.

---

## Kernels and digraphs (closest to the tools we already have)

| Problem | Statement in plain words | Status | Fit |
|---|---|---|---|
| Small quasi-kernel conjecture (Erdős–Székely, 1976) | Every digraph with no source has a quasi-kernel (an independent set reaching every vertex in at most 2 steps) with at most half the vertices. | open; proved for some classes | near |
| Laborde–Payan–Xuong conjecture | Every digraph has an independent set that meets every longest directed path. | open | near |
| Seymour's second neighbourhood conjecture | Every oriented graph has a vertex with at least as many vertices at distance 2 as at distance 1. | open; known for tournaments | near |
| Caccetta–Häggkvist conjecture | A digraph on `n` vertices with minimum out-degree `r` has a directed cycle of length at most `ceil(n/r)`. | open, even for `r = n/3` | mid |

The quasi-kernel conjecture is the one most tied to this repository. A quasi-kernel is a
distance relaxation of a kernel, and our census tool already enumerates kernel-type sets.

## Colouring

| Problem | Statement in plain words | Status | Fit |
|---|---|---|---|
| Total Colouring Conjecture (Behzad, Vizing) | `chi''(G) <= Delta + 2`. | open; known for `Delta <= 5` | mid |
| Overfull Conjecture (Chetwynd–Hilton) | A graph with `Delta > n/3` is class 2 only if it contains an overfull subgraph with the same `Delta`. | open; large cases recently proved | mid |
| Goldberg–Seymour conjecture | `chi'(G) <= max(Delta + 1, ceil(Gamma))` for multigraphs. | a proof was posted by Chen, Jing and Zang (2019); I have not checked whether it has been accepted | mid |
| Reed's `omega, Delta, chi` conjecture | `chi(G) <= ceil((Delta + 1 + omega) / 2)`. | open | near (`PROBLEM.md` §4 already met it) |
| Hadwiger's conjecture | A graph with no `K_t` minor is `(t-1)`-colourable. | open for `t >= 7` | far |
| Erdős–Hajnal conjecture | Graphs excluding a fixed induced subgraph have a polynomially large clique or independent set. | open | far |
| Albertson's conjecture | If `chi(G) = r`, the crossing number of `G` is at least that of `K_r`. | open for large `r` | far |
| Petersen colouring conjecture (Jaeger) | Every bridgeless cubic graph has a Petersen colouring. | **claimed disproof, 2026**: Goedgebeur et al., arXiv:2608.10028, 52-vertex counterexamples and an infinite family | settled if the claim holds |

## Flows, cycles, decompositions

| Problem | Statement in plain words | Status | Fit |
|---|---|---|---|
| Tutte's 5-flow conjecture | Every bridgeless graph has a nowhere-zero 5-flow. | open (6-flows known, Seymour) | far |
| Cycle double cover conjecture | Every bridgeless graph has a family of cycles covering each edge exactly twice. | open | far |
| Berge–Fulkerson conjecture | Every bridgeless cubic graph has six perfect matchings covering each edge exactly twice. | open | mid |
| Graceful tree conjecture | Every tree has a graceful labelling. | open (Ringel's conjecture proved for large `n`) | far |
| Reconstruction conjecture | A graph on at least 3 vertices is determined by its deck of vertex-deleted subgraphs. | open | far |

## Settled recently (useful context, not targets)

- Ringel's conjecture: proved for large `n` (Montgomery, Pokrovskiy and Sudakov, 2020).
- Erdős–Faber–Lovász: proved for large `n` (Kang, Kelly, Kühn, Methuku and Osthus, 2021).
- 1-factorization conjecture: proved for large even `n` (Csaba, Kühn, Lo, Osthus and Treglown,
  2016).
- Hedetniemi's conjecture: disproved (Shitov, 2019).

---

## Assessment

Of these, the only ones I would put next to the in-scope list are the **small quasi-kernel
conjecture** and the **Laborde–Payan–Xuong conjecture**. Both are statements about kernel-like
sets in digraphs, the objects this project has spent months building tools for. Everything else
either needs machinery we do not have or has resisted decades of work by specialists.
