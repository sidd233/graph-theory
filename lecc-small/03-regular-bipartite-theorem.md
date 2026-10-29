# 03. Theorem: for regular graphs, the kernel method works only on bipartite graphs

## Statement

> **Theorem.** Let `G` be a simple `k`-regular graph with `k >= 1`. Then `L(G)` has a
> kernel-perfect orientation with maximum out-degree at most `k - 1` **if and only if** `G` is
> bipartite.

"If" is Galvin's theorem. "Only if" is the new direction. Through Lemma 1 of chapter 33, it says:

> **Corollary.** For a regular graph `G` that is not bipartite, the kernel method (Lemma 1 with
> lists of size `Delta(G)`) cannot prove `ch'(G) = Delta(G)`. This holds whatever the true value
> of `ch'(G)` is.

It contains, as special cases:

- the triangle theorem (note `11` of `list-colouring/`);
- the even-complete-graph theorem (note `12`);
- the undecided case `C_5 × K_2`;
- the kernel-method failure on all 52 of Schauz's open zero-sum graphs (`data/kernel_N8.csv`,
  `data/kernel_N10.csv`).

**Novelty.** Not found in Borodin–Kostochka–Woodall 1998, which characterises kernel-perfect
line graph orientations, nor in McDonald 2015 (arXiv:1508.01820). McDonald proves the `K_n`
case only for her restricted "Galvin orientations", and shows that the Petersen graph *does*
have one with 4 = `Delta + 1` colours. So the barrier is specific to the tight budget
`k = Delta` on regular graphs. Status: **not found in the literature; not yet claimed as new.**

## Proof

Throughout, `D` is a kernel-perfect orientation of `L(G)` with `d+(e) <= k - 1` for every edge
`e` of `G`.

**Step 1 (ranks).** By the star lemma (note `09`), for each vertex `u` the `k` edges at `u`
induce a transitive tournament in `D`. Let `r_u(v)` be the number of edges at `u` that the edge
`uv` points to, which is its rank at `u`, with 0 the best. At each `u` the ranks are exactly
`0, 1, ..., k-1`. Since `G` is simple, two edges share at most one vertex, so every arc of `D`
lies in exactly one star, and

```
d+(uv) = r_u(v) + r_v(u).
```

**Step 2 (tightness).**

```
sum over edges uv of d+(uv) = sum over vertices u of (0 + 1 + ... + (k-1))
                            = |V| k(k-1)/2 = |E| (k-1).
```

Each term is at most `k - 1`, so every term equals `k - 1`:

```
r_u(v) + r_v(u) = k - 1    for every edge uv.
```

**Step 3 (no odd ring).** Call an odd cycle `a_1 a_2 ... a_m` of `G` (`m` odd, at least 3) an
**odd ring** if every `a_i` ranks `a_{i+1}` above `a_{i-1}`, indices mod `m`. Suppose one exists.
Let `S` be its edge set and `e_i = a_i a_{i+1}`.

- In `L(G)`, the edge `e_i` is adjacent only to `e_{i-1}` and `e_{i+1}` within `S`, because the
  cycle is simple. For `m = 3` all three are adjacent, which is the same statement.
- At `a_i`, the edge `e_i` is ranked above `e_{i-1}`, so `e_{i-1} -> e_i`.
- Hence `D[S]` is a directed cycle of odd length, which has no kernel. That contradicts
  kernel-perfectness.

So `G` has no odd ring.

**Step 4 (an orientation of `G`).** Put `y(u,v) = r_u(v) - (k-1)/2`. By Step 2,
`y(v,u) = -y(u,v)`. Orient edge `uv` as `u -> v` in a digraph `O` when `y(u,v) < 0`, that is,
when `u` ranks `v` in its better half. Let `M_0` be the set of edges with `y = 0`, which leaves
them unoriented.

- If `k` is even, `y` is never 0, so `M_0` is empty.
- If `k` is odd, `y(u,v) = 0` exactly when `r_u(v) = (k-1)/2`. By Step 2 this happens exactly
  when `r_v(u) = (k-1)/2` as well. Each vertex has exactly one edge of middle rank, so `M_0` is a
  perfect matching.

At every vertex, the out-arcs of `O` are the edges of rank below `(k-1)/2` and the in-arcs are
those of rank above it. There are `floor(k/2)` of each. So `O` is a balanced (Eulerian)
orientation of `G - M_0`.

**Step 5 (admissible cycles are rings).** Traverse a cycle `a_1 -> a_2 -> ... -> a_m -> a_1`.
Then `a_i` ranks `a_{i+1}` above `a_{i-1}` exactly when

```
r_{a_i}(a_{i+1}) < r_{a_i}(a_{i-1})
  <=>  y(a_i, a_{i+1}) < y(a_i, a_{i-1}) = -y(a_{i-1}, a_i)
  <=>  y(a_{i-1}, a_i) + y(a_i, a_{i+1}) < 0.
```

Call the cycle **admissible** if every edge is either an arc of `O` traversed forwards, so
`y < 0`, or an edge of `M_0`, so `y = 0`. Two consecutive edges of a cycle share a vertex, so
they cannot both lie in the matching `M_0`. Hence in an admissible cycle every consecutive sum
is negative, and **every admissible odd cycle is an odd ring**. By Step 3, `G` has no admissible
odd cycle.

**Step 6 (strong connectivity).** In a balanced digraph every arc lies on a directed cycle.
Hence each connected component `H` of `G - M_0`, oriented by `O`, is strongly connected.

**Step 7 (each component is bipartite).** Suppose `H` is not bipartite.

- **No odd directed closed walk, so return paths are odd.** Suppose `H` has no directed closed
  walk of odd length. For each arc `x -> y`, pick a directed path `P_{yx}` from `y` to `x`, which
  exists by Step 6. Since `x -> y` followed by `P_{yx}` is a closed walk, `|P_{yx}|` is odd.
- **Build an odd closed walk.** Take an odd cycle `Z` of `H` and walk around it. Keep each arc
  traversed forwards, and replace each arc `x -> y` traversed backwards by `P_{yx}`. This gives a
  directed closed walk of length congruent to `|Z|`, which is odd. That contradicts the
  assumption, so `H` does have an odd directed closed walk.
- **Extract a cycle.** A directed closed walk splits into directed cycles whose lengths add up,
  so one of them is odd. A directed odd cycle of `O` is admissible, which contradicts Step 5.

So `H` is bipartite.

**Step 8 (`k` even).** `M_0` is empty, so `G` is the union of its components, each bipartite by
Step 7. So `G` is bipartite.

**Step 9 (`k` odd).** Fix a 2-colouring `col` of every component of `G - M_0`. Form the
multigraph `Γ` whose nodes are the components and whose edges are the edges of `M_0`, with
loops allowed. Give an edge `f = vu` of `M_0` the label `λ(f) = 1` if `col(v) = col(u)`, and 0
otherwise. Flipping the colouring of a component changes `λ` on its non-loop edges, so:

> `G` is bipartite if and only if every cycle of `Γ` has even label sum.

Suppose some cycle of `Γ` has odd label sum, and take one with the fewest edges.

- **It visits no component twice.** If it did, it would split into two shorter closed walks, one
  of them with odd sum. Write it as components `H_1, ..., H_t`, all distinct, with
  `f_i = v_i u_{i+1}` joining `H_i` to `H_{i+1}` (indices mod `t`; `t = 1` is a loop).
- **Entry and exit differ.** In `H_i` we enter at `u_i` and leave at `v_i`, and `u_i != v_i`
  because `M_0` is a matching.
- **Build a cycle in `G`.** By Step 6, choose a directed `O`-path `P_i` from `u_i` to `v_i` inside
  `H_i`. Then `Z = P_1 f_1 P_2 f_2 ... P_t f_t` is a simple cycle of `G`, because the components
  are distinct, and it is admissible.
- **Its length is odd.** `H_i` is bipartite, so `|P_i| ≡ col(u_i) + col(v_i) (mod 2)`. Regrouping
  the sum cyclically,

```
|Z| = sum_i |P_i| + t ≡ sum_i ( col(v_i) + col(u_{i+1}) + 1 ) ≡ sum_i λ(f_i) ≡ 1 (mod 2).
```

So `Z` is an admissible odd cycle, which contradicts Step 5. Therefore `G` is bipartite. ∎

## Remarks

- **What was not needed.** The proof never uses Tan or Chung (the hard direction of the
  odd-ring lemma, note `02`) or the class-1 hypothesis. It needs only:
  - the star lemma;
  - counting (tightness);
  - the fact that a directed odd cycle has no kernel.
- **Simple graphs only.** Step 1 uses simplicity: in a multigraph, parallel edges share two
  vertices. The multigraph case is open here.
- **Sharpness of the hypotheses.**
  - Regularity is what forces tightness. For non-regular graphs, McDonald's "bipartite plus an
    edge" shows the kernel method can succeed off the bipartite world.
  - The budget must be `k = Delta`. With `k = Delta + 1` the Petersen graph succeeds (McDonald,
    Theorem 4).

## Machine confirmation

- `kernel_sat.py` on every connected regular graph:
  - 6 and 8 vertices, every degree from 3 up;
  - 10 vertices, degrees 3 to 7;
  - cubic graphs on 12 vertices;
  - triangle-free cubic graphs on 14 vertices;
  - every 4-regular graph on 12 vertices.

  That is **1923 graphs** in total. SAT holds exactly on the bipartite ones: 29 SAT, 1894 UNSAT.
  Outputs: `data/kernel_all_small.csv`, `data/kernel_N12_k4.csv`.
- The odd-ring lemma used by the solver is cross-checked against brute-force kernel-perfectness
  in `tests/test_lemma.py`.
