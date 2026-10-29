# A1 results (verified only)

Novelty audit of every result below: note `05` (9 Oct).

Every line cites the script and data that reproduce it. Labels: **reproduced** (matches a
published result), **new?** (not found in the literature so far, not yet claimed), **known**.

## R1. Schauz's census, reproduced. Label: reproduced.

`at_sign.py`, `census_summary.py` → `data/census_N8.csv`, `data/census_N10.csv`.

| `N` | regular graphs (deg 3 to 7) | class 2 | zero-sum | zero-sum by degree 3, 4, 5, 6, 7 |
|---|---:|---:|---:|---|
| 8 | 16 | 0 | **3** | 1, 1, 1, 0, 0 |
| 10 | 164 | 3 | **51** | 5, 17, 18, 8, 3 |

This matches arXiv:1705.00484, §4.1, exactly:

- the 3 zero-sum graphs on 8 vertices include the complement of `C_3 ∪ C_5`;
- the other two are complements of each other;
- the split on 10 vertices is the same;
- there are 3 class-2 graphs.

`K_10` and `K_10` minus a perfect matching (degrees 9 and 8) were not enumerated, since they
have about `10^9` colourings each. Both are settled already, so neither is a candidate.

## R2. Which zero-sum graphs are already covered. Label: new? (bookkeeping).

`known.py` → `data/known_N*.csv`, `data/uncovered_N*.g6`.

- **8 vertices:** none of the 3 is covered by a known theorem. None is bipartite, planar,
  bipartite after deleting a vertex, line-perfect, or complete.
- **10 vertices:** 2 of the 51 are bipartite (Galvin): a cubic graph and `K_{5,5}`. The other 49
  are covered by nothing. None of the 51 is planar, so Ellingham–Goddyn covers none.

**So 52 regular graphs remain open:** 3 on 8 vertices and 49 on 10.

## R3. The kernel method fails on all 52. Label: new? (follows from R5).

`kernel_sat.py` → `data/kernel_N8.csv`, `data/kernel_N10.csv`. All 52 are UNSAT: `L(G)` has no
kernel-perfect orientation with `Delta+ <= k-1`, so Lemma 1 cannot prove the LECC for any of
them.

Combined with R1, **both standard tools provably fail on every open case**. The method behind
Schauz's suggestion that they "should be provable with other methods" must therefore be a third
one.

## R4. `C_5 × K_2` is settled. Label: closes an open item of note `11`.

All 34 tight rank systems were enumerated. None is kernel-perfect, by brute force and by the
odd-ring test (`tests/test_lemma.py`). The SAT solver agrees.

## R5. Theorem: the kernel method works on a regular graph only if it is bipartite. Label: new? (proof in `03`).

> A simple `k`-regular `G` has a kernel-perfect orientation of `L(G)` with
> `Delta+ <= k-1` if and only if `G` is bipartite.

- **Proof:** note `03`, in 9 steps.
- **Machine confirmation:** 1923 regular graphs (`data/kernel_all_small.csv`,
  `data/kernel_N12_k4.csv`). SAT exactly on the 29 bipartite ones, UNSAT on the other 1894.
- **Special cases it contains:** notes `11` and `12`, R3 and R4.
- **Literature:** the characterisation it builds on is Borodin–Kostochka–Woodall 1998. Not found
  in McDonald 2015 either; see note `03`.

## R6. The odd-ring lemma. Label: known (BKW 1998), restated.

The stable-matching restatement is in note `02`. It is machine-checked against brute force in
both directions in `tests/test_lemma.py`.

## R7. The LECC for all 5 open cubic zero-sum graphs. Label: new? Certified by computer (9 Oct).

`choosability.py --reduce` (method and soundness in note `04`) proves `ch' = 3` for X
(`GCY^B_`, 8 vertices) and the 4 open cubic graphs on 10 vertices. For these graphs both
standard methods provably fail (R1, R3).

Certificates (`core_check.py` → `data/cores/<graph>.json`, checked by `verify_core.py` →
`data/cores/<graph>.verify.txt`). The search is rerun with a selector per (R) witness; the
unsat core keeps only the witnesses the refutation used. The checker shares no code with the
search and re-checks every (P) fact and every core (R) fact by counting Eulerian subgraphs, every
blocked colouring, and the UNSAT of the rebuilt CNF with a second solver (Glucose 4):

| graph6 | N | core / all (R) witnesses | blocked colourings | check |
|---|---:|---:|---:|---|
| `GCY^B_` (X) | 8 | 892 / 6972 | 136 | passed |
| ``I?`amQoM?`` | 10 | 4636 / 73657 | 2016 | passed |
| ``I?`bfAWF?`` | 10 | 4473 / 75994 | 3248 | passed |
| `ICOedO[X?` | 10 | 5809 / 73302 | 8000 | passed |
| `I?bEHow[?` | 10 | 7723 / 70276 | 181936 | passed |

The Eulerian count uses `verify_core.euler_diff_frontier`, which agrees with
`alontarsi.euler_diff` on 600 random orientations (`tests/test_euler_frontier.py`).

Also checked: brute-force and plain-search cross-validation (`tests/test_choosability.py`).

Still to do: a DRAT certificate for the final UNSAT (building `drat-trim` needs Sid's go-ahead,
since it fetches external code), and a human reading of note `04`.

## R8. The LECC for `GEnbvG` (8 vertices, 4-regular, open). Label: new? Certified by computer (9 Oct).

`lazy_choos.py` (the search of note `04` with (R) added lazily) proves `ch' = 4`, so `L(G)` is
4-choosable, for the open 4-regular zero-sum graph `GEnbvG` (`L(G)` has 16 vertices).

- Run log `data/lazy/GEnbvG.log`: precheck 240 s, generating 201177 witnesses 1095 s, search 30 s
  (309 rounds). The proof used 2235 witnesses and 48 blocked colourings.
- Certificate `data/lazy/GEnbvG.json`. `verify_core.py` passes it: 16 precheck facts, 2235
  witnesses, 48 colourings, and the rebuilt CNF (93600 clauses) is UNSAT under Glucose 4.
- Sanity check of the lazy search: it reproves X (`data/lazy/GCY^B_.json`, certificate passes).

Earlier, adding all witnesses up front (6.4 million clauses) timed out after 28 minutes.
Still to do: DRAT for the final UNSAT, as for R7.
