# 02. Kernels in line graphs are stable matchings; the odd-ring lemma

**Credit.** This is a restatement of a known theorem. Borodin, Kostochka and Woodall
(*On kernel-perfect orientations of line graphs*, Discrete Math. 191 (1998) 45–49) proved that
an orientation of a line graph is kernel-perfect if and only if every clique has a kernel and
every directed odd cycle has a chord or pseudochord. What follows is the same fact in the
language of stable matchings, which is how the chapter 33 proof of Dinitz already thinks.

## The dictionary

Let `D` be an orientation of `L(G)` in which every star, meaning the set of edges at a vertex,
is transitively oriented. This is forced by kernel-perfectness, by the star lemma in
`list-colouring/09`. Read the transitive order at `u` as **`u`'s preference list**: `u` prefers
`v` to `w` if the edge `uw` points to `uv`. For an edge set `S`, consider the stable roommates
instance with agents `V(G)`, acceptable pairs `S`, and these preferences.

> **A set `M ⊆ S` is a kernel of `D[S]` if and only if `M` is a stable matching of the instance.**

The two halves of the definition line up one for one:

- `M` independent in `L(G)` means no two edges of `M` share a vertex, so `M` is a matching.
- Every `e = uv` in `S \ M` points into `M` means `u` or `v` is matched by `M` to someone it
  prefers to the other end of `e`. That is exactly the condition that `e` does not block `M`.

So Lemma 2 of chapter 33 (stable matchings in bipartite graphs) **is** "kernels exist in line
graphs of bipartite graphs", and Galvin's proof is this dictionary applied once.

## The lemma

An **odd ring** is a cycle `a_1 ... a_m` of `G` with `m >= 3` odd, in which every `a_i` prefers
`a_{i+1}` to `a_{i-1}`, indices mod `m`.

> **Lemma.** A star-transitive orientation of `L(G)` is kernel-perfect if and only if the
> preference system has no odd ring.

*Proof.*

- **(⇒)** On the edges of an odd ring, `D` is a directed odd cycle, which has no kernel. See
  Step 3 of note `03`.
- **(⇐)** Removing acceptable pairs cannot create an odd ring, so every sub-instance `(V, S)` is
  free of odd rings. A roommates instance with strict preferences and no odd ring has a stable
  matching: J. J. M. Tan, J. Algorithms 12 (1991), via stable partitions, since an odd party of a
  stable partition is an odd ring; or K.-S. Chung, Games Econom. Behav. 33 (2000). By the
  dictionary, that matching is a kernel of `D[S]`. ∎

## Machine check

`tests/test_lemma.py` compares "no odd ring" with brute-force kernel-perfectness, which tests
every vertex subset of `L(G)`:

- on every tight rank system of `K_4`, the prism, `K_{3,3}`, `Q_3`, `K_{2,2,2}` and `C_5 × K_2`;
- on 400 random arbitrary rank systems on each of 9 non-bipartite graphs.

Both kernel-perfect and non-kernel-perfect systems occur in large numbers, so both directions
are exercised. Every case agrees.

## Why it matters here

It turns "every one of `2^|E|` induced subdigraphs has a kernel" into "no odd cycle is a ring".
That makes `kernel_sat.py` run in seconds where `list-colouring/kernel_search.py` could not
finish `C_5 × K_2`. It is also the lens through which the theorem of note `03` became visible.
