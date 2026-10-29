# 04. Computer proofs of the LECC for zero-sum graphs where both standard methods fail

## The claim

For each graph `G` listed under "Results" at the end, `ch'(G) = chi'(G) = k`. Equivalently,
`L(G)` is `k`-choosable. These are among the open graphs of `RESULTS.md` R2. For each of them:

- the uniform Alon–Tarsi coefficient vanishes, so Schauz's method fails (R1);
- no kernel-perfect orientation exists, so Galvin's method fails (theorem of note `03`).

## The method: `choosability.py --reduce`

Let `H = L(G)`, with `n` vertices and lists of size `k`. A list assignment is **bad** if `H` has
no proper colouring from it. We show no bad assignment exists. Each step below is a lemma, with
its one-line proof.

**(P) Precheck.** For every vertex `v`, `H - v` has a monomial with nonzero coefficient and all
exponents at most `k-1`. By the Combinatorial Nullstellensatz, `H - v` is `k`-choosable, and so
is every proper induced subgraph of `H`.

**(C) Criticality.** Under (P), let `L` be bad, `v` a vertex and `c` in `L(v)`. Then `c` lies in
the list of some neighbour of `v`.
*Proof.* Otherwise colour `H - v` from `L` (possible by (P)) and give `v` the colour `c`. That
colours `H`, a contradiction.

**(B) Palette.** Under (C), every colour lies in at least 2 lists. There are `nk` list slots,
so at most `nk/2` distinct colours. Rename them into `{0, ..., nk/2 - 1}`.

**(S) Symmetry.** Rename the colours in order of first appearance along `v_0, v_1, ...`. Then
whenever colour `c >= 1` lies in `L(v_i)`, colour `c-1` lies in some `L(v_j)` with `j <= i`.
Renaming colours does not change badness, (C) or (R).

**(R) Reducible colour classes.** Write `A(c)` for the set of vertices whose list contains `c`.
Suppose `I ⊆ A(c)` is independent and `H - I` has a nonzero monomial `x^t` with:

- `t_w <= k-2` for `w` in `A(c) \ I`;
- `t_w <= k-1` elsewhere.

Then `L` is colourable.
*Proof.* Colour `I` with `c` and delete `c` from the lists of `A(c) \ I`. Those lists now have
size `k-1 > t_w`, and the others size `k > t_w`. The Combinatorial Nullstellensatz colours
`H - I` from the reduced lists, and none of them uses `c`.

This condition depends only on the set `A(c)`. So a bad `L` has no colour class `A` with
`I ⊆ A ⊆ I ∪ Z(t)`, where `Z(t) = {w : t_w <= k-2}`.

**(CEGAR) The loop.** A SAT solver searches for an assignment satisfying "lists of size `k`",
(B), (S), (C) and (R). It also must not admit any colouring found so far.

- If it proposes `L`, a second solver looks for colourings from `L`. If there are any, up to 8
  are added as exclusions and the loop repeats. If there are none, `L` is bad; it would be
  checked by exhaustive search and reported.
- If the first solver reports UNSAT, no bad assignment exists, so `H` is `k`-choosable.

## Validation

- `tests/test_choosability.py`:
  - on 79 random graphs with 4 to 6 vertices, compares against **brute force** over every list
    assignment (no theory at all);
  - on 120 random graphs with 6 to 9 vertices, compares `--reduce` against the plain search
    without (R).

  All agree, with many choosable and non-choosable cases.
- Known cases come out right:
  - choosable: `L(K_4)`, `L(K_{3,3})`, `L(prism)`, `C_4`, `K_{2,3}`, `K_{2,4}` with 3 colours;
  - not choosable, with the bad assignment verified exhaustively: `C_5`, `C_7`, `K_{3,3}` and
    `K_{3,6}` and `K_{2,4}` with 2 colours, `L(K_4)` with 2, `L(Petersen)` with 3.
- `verify_reduce.py` re-derives **every** Alon–Tarsi fact used, for (P) and (R), from the
  combinatorial side of the Alon–Tarsi theorem. It counts even minus odd Eulerian subgraphs of an
  orientation with the required out-degrees, with code independent of the coefficient expansion.
  For X: 12 precheck facts and 6972 reduction facts, all confirmed.

## Still to do before calling these results proved

1. ~~Run `verify_reduce.py` on every graph claimed below.~~ Done differently on 9 Oct: the
   overnight runs were killed by a reboot, and are replaced by unsat-core certificates
   (`core_check.py`, `verify_core.py`; see RESULTS R7). Only the (R) witnesses in the core are
   needed for soundness, and all of them pass, for all 5 graphs.
2. Have the outer solver emit a DRAT proof of UNSAT and check it with `drat-trim`, so the final
   SAT step is certified too.
3. A human reading of (P), (C), (B), (S) and (R). Each is a few lines, but they carry the proof.

## Results (2026-10-07)

From `data/choos_all.csv`, batch `run_all_choos.py` with a 20-minute limit per graph:

| graph6 | N | k | result | seconds | independent AT re-check (`verify_reduce.py`) |
|---|---|---|---|---:|---|
| `GCY^B_` (X) | 8 | 3 | **3-edge-choosable** | 1.3 | passed (12 + 6972 facts) |
| ``I?`amQoM?`` | 10 | 3 | **3-edge-choosable** | 30.6 | core certificate passed (9 Oct) |
| ``I?`bfAWF?`` | 10 | 3 | **3-edge-choosable** | 42.2 | core certificate passed (9 Oct) |
| `ICOedO[X?` | 10 | 3 | **3-edge-choosable** | 48.4 | core certificate passed (9 Oct) |
| `I?bEHow[?` | 10 | 3 | **3-edge-choosable** | 333.0 | core certificate passed (9 Oct) |
| `GEnbvG` | 8 | 4 | timeout: the first outer solve never finished | 1699 | not applicable |
| `GEnbvG` (lazy (R), 9 Oct) | 8 | 4 | **4-edge-choosable** | 1125 (1095 generating witnesses) | certificate passed (`data/lazy/GEnbvG.json`) |

These are **all 5 open cubic zero-sum graphs**, the degree-3 entries of R2.

**Why degree 4 and up stalls.** Adding (R) up front gives 201,177 witnesses × 32 colours
= 6.4 million clauses for `GEnbvG`, and the outer solver does not finish its first call. The
fix is engineering, not mathematics: add (R) **lazily**. When the outer solver proposes `L`, test
only its actual colour classes for reducibility and add a clause for those. Also prune witnesses
dominated by others.

**Cross-check that did not conclude.** Rerunning X without (S) timed out after 25 minutes
(187,651 rounds). That is expected, since without symmetry breaking the space is about 18!
times larger. It is not a contradiction. The test of (S) is the brute-force comparison in
`tests/test_choosability.py`, which uses no symmetry and agrees.
