# Open problems in scope: list edge colouring and its neighbours

Compiled 2026-10-07. Main sources:

- the survey by Vasudevan, Somasundaram and Narayanan, *List-Coloring and Chromatic-Choosability:
  A Dynamic Survey*, arXiv:2606.31702 (June 2026), cited below as **[S]** with its numbering;
- U. Schauz, *Orientations of 1-Factorizations and the List Chromatic Index of Small Graphs*,
  arXiv:1705.00484 (2017), cited as **[Sch17]**;
- A. Jafari, *The List Edge-Coloring Conjecture for New Infinite Families*, arXiv:2608.22895
  (2026), cited as **[J26]**.

"Status" means what those sources say. Where I have not checked anything published after
them, the entry says so.

Notation: `chi'(G)` is the chromatic index, `ch'(G)` the list chromatic index, `chi_ell(G)` the
list chromatic number, and `AT(G)` the Alon–Tarsi number. A graph is **class 1** if
`chi'(G) = Delta(G)` and **class 2** if `chi'(G) = Delta(G) + 1`.

The problems are sorted by how realistic they are for us, not by how famous they are.

---

## The centre: the List Edge Colouring Conjecture (LECC)

> **LECC** [S, Conj. 8.4]. For every (multi)graph `G`, `ch'(G) = chi'(G)`.
> Equivalently [S, Conj. 8.5], `chi_ell(L(G)) = chi(L(G))` for every line graph `L(G)`.

In the language of the Dinitz chapter: Galvin proved this for every bipartite `G`, so for every
"shape" of cells in a grid. The conjecture says the same thing for any graph. Known cases
[S, §8.2]: bipartite multigraphs (Galvin), `K_{2n+1}` (Häggkvist–Janssen), `K_{p+1}` (Schauz
2014), `K_{p-1}` and `K_{2p}` ([J26], August 2026), 2-connected regular planar class-1
graphs (Ellingham–Goddyn), series-parallel graphs, line-perfect graphs, multicircuits, graphs
that become bipartite after deleting one vertex, and planar graphs with `Delta >= 12`
(Borodin–Kostochka–Woodall). Asymptotically, `ch'(G) <= (1 + o(1)) Delta` (Kahn).

Solving the whole conjecture is not a realistic capstone target. The items in tier A are
pieces of it small enough to finish.

---

## Tier A: concrete, small, and a result in days to weeks is plausible

### A1. The Schauz zero-sum graphs (the most concrete target)

**Problem.** Prove the LECC for the regular class-1 graphs on 8 and 10 vertices where
Schauz's method fails [Sch17, §4.1]:

- on 8 vertices, exactly **3** graphs: the complement of `C_3 ∪ C_5`, one further graph, and
  its complement;
- on 10 vertices, **51** graphs out of 164 regular class-1 graphs: 5 of degree 3, 17 of degree 4,
  18 of degree 5, 8 of degree 6 and 3 of degree 7.

**Why the standard method fails here.** For a `k`-regular class-1 graph with lists of size `k`,
the Alon–Tarsi method has exactly one monomial to check, and its coefficient is the signed count
of 1-factorizations (proper `k`-edge-colourings), even ones minus odd ones. On these graphs the
count is exactly zero, so the method says nothing. Schauz observes that each one seems to have a
symmetry of order 2 that swaps even and odd colourings, and writes that *"it should be possible
to prove the List Edge Coloring Conjecture for all found zero-sum graphs with other methods."*
He did not do it.

**Why it suits us.**

- The objects are finite and small. `L(G)` has 20 vertices for the complement of `C_3 ∪ C_5`.
- The method that fails is Alon–Tarsi. The **kernel method** of the Dinitz chapter is a
  separate route, and this repository already has code for kernel-perfect orientations
  (`list-colouring/kernel_search.py`, `galvin.py`) and two theorems saying where that method
  cannot work:
  - note `11`: cubic class-1 graphs with a triangle;
  - note `12`: even complete graphs.
- A clean outcome either way is reportable. Either the kernel method proves the LECC for some
  zero-sum graphs, or our obstruction theorems explain why it cannot.

**First step.** Reproduce Schauz's census of zero-sum graphs (3 on 8 vertices, 51 on 10). Then
test each one for a kernel-perfect orientation of `L(G)` with `Delta+ <= k - 1`.

**Status check still needed.** No follow-up paper settling these cases turned up in a search on
2026-10-07, but that search was not exhaustive. Before claiming novelty, check the papers that
cite [Sch17].

### A2. The LECC for every graph on at most 10 vertices

**Problem.** Finish the programme of [Sch17, §4]: prove `ch'(G) = chi'(G)` for every graph with
at most 10 vertices. Besides A1, Schauz lists three gaps:

1. graphs that cannot be extended to a small regular graph;
2. the three small regular class-2 graphs, one of which is the Petersen graph;
3. odd-order graphs whose natural extensions run into the open cases of A1.

**Assessment.** This is A1 plus bookkeeping. It is a natural follow-on if A1 works, and the
result would be a clean, quotable theorem ("the LECC holds for all graphs on at most 10
vertices").

### A3. Cubic class-1 graphs are 3-edge-choosable

**Problem.** Is `ch'(G) = 3` for every cubic graph with `chi'(G) = 3`? This is the case
`Delta = 3` of the LECC for class-1 graphs. Every cubic graph is 4-edge-choosable (the
`Delta = 3` case of the weaker bound `ch' <= Delta + 1`), so the open question is whether 3
colours always suffice. Known: bipartite (Galvin) and planar (Ellingham–Goddyn).

**Why it suits us.** It is the smallest open degree. Note `11` already proves the kernel method
cannot handle such graphs when they contain a triangle. The five cubic zero-sum graphs on 10
vertices from A1 are the first test cases. Good families to try: Möbius ladders, generalised
Petersen graphs `GP(n, k)` of class 1, and other non-planar cubic class-1 families.

**Status.** Open as far as I know. The survey does not list it as solved, but I have not checked
it against recent literature.

### A4. The product of two odd cycles

**Problem** [S, Conj. 11.3, from Lu et al.]. `chi_ell(C_{2m+1} □ C_{2n+1}) = 3`.

**Status.** Open per [S]. Here `AT = 4`, so the Alon–Tarsi method provably cannot give 3. The
smallest case, `C_3 □ C_3 = K_3 □ K_3 = L(K_{3,3})`, is the 3 by 3 Dinitz square and is solved by
Galvin. So the conjecture is a direct, non-bipartite relative of the Dinitz problem.

**Why it suits us.**

- The kernel method needs a kernel-perfect orientation with out-degree at most 2 everywhere on a
  4-regular graph, which is exactly a kernel-perfect Eulerian orientation. Searching for one is
  well defined, and our tools already do this.
- `C_3 □ C_5` (15 vertices) and `C_5 □ C_5` (25 vertices) are small enough for computer search.
- A proof for one infinite family, such as `C_3 □ C_{2n+1}`, would already be a publishable
  partial result.

This is not the LECC itself, but it is the closest relative of the Dinitz square on the list.

### A5. The `K_{5,q}` gap

**Problem** [S, §6]. `chi_ell(K_{5,q})` is 4 or 5 for every `14 <= q <= 175`, and the exact
value is open. The question is the largest `q` for which `K_{5,q}` is still 4-choosable.

**Why it is attractive.** It reduces to a finite computation. Fix lists of size 4 on the 5-vertex
side. Each vertex on the large side, with list `T`, blocks exactly the colourings of the small
side whose colour set contains `T`. So `K_{5,q}` fails to be 4-choosable exactly when, for some
lists on the small side, `q` four-element sets block every colouring. That is a set-cover
problem over a finite, symmetry-reducible family, and it is the kind of problem a modern ILP or
SAT solver can attack.

**Why it might be harder than it looks.** If it really were this easy, someone would likely have
done it. The search space of list assignments on the small side needs a careful symmetry
reduction. The problem is off the LECC line.

**Status check still needed.** The survey (June 2026) calls it open. I have not checked for a
recent paper on it.

### A6. Complete graphs of even order outside the known families

**Problem.** The LECC for `K_n` is now known for all odd `n` and for even `n` of the forms
`p + 1`, `p - 1` and `2p` with `p` an odd prime. The smallest even orders left are

```
n = 50, 56, 64, 76, 92, 116, 120, 124, 144, 154, ...
```

(computed by `open-problems/uncovered_complete.py`, assuming no other result covers them).

**Assessment.** The method is a number-theoretic congruence for the signed count of
1-factorizations, as in [J26]. Brute force is impossible at `n = 50`. This is a real open
problem with a recent and active line of work, but it needs a new congruence idea. It is a
candidate if the prof likes the algebraic side. Note `12` proves the kernel method cannot do
it.

---

## Tier B: open, with clear footholds, but each is a serious project

### B1. Planar graphs of moderate maximum degree

The LECC holds for planar graphs with `Delta >= 12`, and for several smaller `Delta` under extra
conditions (forbidden cycles, girth). For example, March 2025: planar, `Delta >= 6`, every
7-cycle induced. The open range is general planar graphs with `Delta` from 5 to 11. The method
is discharging. It is a well-trodden field, so progress here means a long technical paper.

### B2. The list version of Vizing's theorem

Is `ch'(G) <= Delta(G) + 1` for every simple graph? This is weaker than the LECC. It is known
for `Delta <= 4`, and `Delta = 5` is the first open case.

### B3. Treewidth 3

Lang (2015) proved Halin graphs are `Delta`-edge-choosable and graphs of treewidth 3 are
`(Delta + 1)`-edge-choosable. Whether the LECC itself holds for treewidth 3 is open.
Series-parallel graphs (treewidth 2) are done.

### B4. Claw-free perfect graphs with clique number at least 5 [S, Conj. 8.3]

Is `chi_ell(G) = chi(G)` for every claw-free perfect graph? This contains line graphs of
bipartite graphs, so it contains Dinitz and Galvin. It is open for non-peculiar claw-free
perfect graphs with `omega >= 5`. It is the most natural next step after Galvin in a different
direction: generalise the class of conflict graphs rather than the underlying graph. Kernel
methods are natural here.

### B5. The list Borodin–Kostochka conjecture for claw-free graphs [S, Conj. 8.2]

Every graph with `Delta >= 9` and no clique of size `Delta` is `(Delta - 1)`-choosable. For
claw-free graphs it is proved when `Delta >= 69` and open when `9 <= Delta <= 68`. Lowering 68
is a concrete quantitative target.

### B6. The List Total Colouring Conjecture [S, Conj. 9.1]

`ch''(G) = chi''(G)` for every multigraph. This is the total-colouring analogue of the LECC. It
is known for forests, cycles, and bipartite graphs with `chi'' = Delta + 2`.

### B7. Smaller questions from the survey

- [S, §11.2] For which `G` is `G □ P_n` chromatic-choosable? When is `C_{2k+1} □ P_n^r`
  chromatic-choosable?
- [S, §11.2] If `chi_ell(G) = AT(G)` and `chi_ell(H) = AT(H)`, is `chi_ell(G □ H) = AT(G □ H)`?
- [S, §11.1] (Allagan) Given `a, b >= 2`, what is the smallest `t` with
  `chi_ell(K_{a,b} ∨ K_t) = chi(K_{a,b} ∨ K_t)`?
- [S, §9.1] Is there a planar `G` with `chi_ell(G^2) >= chi(G^2) + 2`?
- [S, §10] If `G` is claw-free, is `G^k` chromatic-choosable for every `k >= 2`, or at least for
  some `k`?
- [S, §6] The exact value of `chi_ell(K_{6,q})` for `12 <= q <= 2101`, and of `chi_ell(K_{7,q})`
  for `8 <= q <= 31031`. These are harder versions of A5.

---

## Tier C: famous and open, not realistic as targets

- The LECC in full [S, Conj. 8.4].
- Improving Kahn's `ch'(G) <= Delta + o(Delta)` to `Delta + O(1)`.
- The LCC for all claw-free graphs [S, Conj. 8.1].
- Alon's conjecture: `chi_ell(G) <= c log Delta(G)` for bipartite `G` [S, Conj. 6.1].
- Borowiecki et al. on Cartesian products [S, Conj. 11.1, 11.2].
- Noel: is `chi_ell(G^2)` bounded by a function of `chi(G^2)`, or by `c chi log chi`? [S, §9].
- Noel: `chi_ell(G) <= chi_ell(K_{m*k})` for `k`-chromatic `G` on at most `mk` vertices
  [S, Conj. 7.3].
- The lexicographic product constant [S, §11.3].

---

## Listed as conjectures in the survey but already settled (do not chase)

| Survey item | Statement | Settled by |
|---|---|---|
| Conj. 3.1 | planar graphs are 5-choosable | proved, Thomassen |
| Conj. 3.2 | some planar graph is not 4-choosable | proved, Voigt |
| Conj. 7.1, 7.2 | Ohba's conjecture | proved, Noel, Reed and Wu |
| Conj. 9.2, 9.3 | List Square Colouring Conjecture, and its planar form | disproved, Kim and Park; Hasanvand |
| Conj. 13.2 | weak `(a:b)`-choosability | disproved, Dvořák et al. (a 4-choosable graph that is not `(8:2)`-choosable) |
| Conj. 13.1 | `(a:b)`-choosability equivalence | status not clear from the survey; check before using |
| the rectangle | `chi_ell(K_m □ K_n) = max(m, n)` | Galvin (1995); Janssen (1993) for `(n-1) x n` |

---

## Recommendation for Friday

Lead with **A1**. It is the LECC itself, so it matches what the prof is pushing for. It is
small and finite, it was left open by name in a published attack, and it uses the kernel
machinery this project already built. Keep **A4** as a second line, since it is the closest
non-bipartite relative of the Dinitz square, and **A5** as a computational fallback. Ask the
prof which of A1, A4 and A6 he would rather see.
