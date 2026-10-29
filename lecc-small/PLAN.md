# A1: the LECC for Schauz's zero-sum graphs

**Read this file first in every session that works on A1.** It is the single source of truth
for what is done and what comes next. Update the status board and the session log before
stopping, even mid-task.

---

## Status board

| Phase | What | Status |
|---|---|---|
| 0 | Novelty check: who cites Schauz 2017 | **done**: 3 citing papers (OpenAlex), none settles the zero-sum graphs. The 2018 journal version (J. Discrete Algorithms 52–53, 182–191, downloaded by Sid 2026-10-07) has the same §4.1 text: the zero-sum cases are still open there and kernels are not tried. |
| 1 | Tooling: venv, nauty `geng`, SAT solver | **done**: `lecc-small/env` (networkx, python-sat, ortools); nauty 2.8.9 built at `~/tools/src/nauty2_8_9/geng`; counts 16 and 166 match |
| 2 | Alon–Tarsi census | **done**: reproduces Schauz exactly (RESULTS R1) |
| 3 | Filter by known theorems | **done**: 52 open graphs (3 on 8 vertices, 49 on 10) (RESULTS R2) |
| 4 | Odd-ring lemma | **done**: it is BKW 1998, restated (note `02`); machine-checked both directions |
| 5 | Kernel test on the open graphs | **done**: all 52 UNSAT (RESULTS R3) |
| 5b | (unplanned) Theorem: kernel method on regular `G` works iff `G` bipartite | **proved** (note `03`), confirmed on 1923 graphs (RESULTS R5) |
| 6 | Certificates | not needed for A1 (no SAT results); `verify_cert.py` is ready for later use |
| 7 | Write-up for 9 Oct; explanatory PDF | waits until Sid judges the results enough (no handout) |
| 8 | Positive results: computer proof of `ch'(G) = k` for the open graphs | **all 5 cubic ones proved and certified** (9 Oct: unsat-core certificates, `core_check.py` + `verify_core.py`, RESULTS R7). DRAT not done (needs Sid's OK to fetch drat-trim). Degree 4: lazy (R) in `lazy_choos.py`, first run on `GEnbvG` 9 Oct (see session log). |

## ▶ UPDATE 2026-10-09, 1:30 PM

- The machine rebooted on 9 Oct, so the overnight `verify_reduce.py` jobs died with no output.
  Replaced by step 2 below (unsat-core check), which Sid approved: all 5 cubic certificates pass
  (RESULTS R7). Steps 1 and 2 of the old list are done.
- `verify_core.py` uses a frontier version of the Eulerian count (about 18 s to under 0.1 s
  per fact), cross-checked in `tests/test_euler_frontier.py`.
- Step 3 (DRAT) is blocked: fetching drat-trim from GitHub needs Sid's explicit go-ahead.
- Step 4 started: `lazy_choos.py` (lazy (R)); certificates go to `data/lazy/`. Sanity: X passes.
- Reading copy of notes 03 and 04 for Sid: `latex/_build/lecc-small-reading.pdf`.
- **R8: `GEnbvG` (degree 4) proved and certified by `lazy_choos.py`.** Witness generation
  (18 min) is the bottleneck, not the search (30 s).
- About 1:48 PM: launched `lazy_choos.py` (with `timeout 10000`, so until about 4:35 PM) on `GFzvvW`
  (8 vertices, k=5) and the degree-4 graphs on lines 4 to 7 of `data/uncovered_N10.g6`.
  Logs: `data/lazy/N8_2.log`, `data/lazy/N10_<line>.log`. Certificates appear in `data/lazy/`;
  check each with `verify_core.py` before recording it.
- **Outcome (1:51 PM): both bigger runs died of memory.** `at_fast.coeffs` (the full coefficient
  DP) needs more than 7 GB on `L(G)` with 20 vertices, in the precheck already. The 10-vertex
  degree-4 job and `GFzvvW` (k=5) were killed by the watchdog (`data/lazy/watchdog.log`).
  Proposed fix (not started, discuss with Sid first): drop the coefficient DP. For (P), and for
  (R) on demand per colour class, search for an *orientation* with the required out-degree caps
  and test EE != EO with `verify_core.euler_diff_frontier` (fast, little memory). Sound, since
  every fact found is still an Alon–Tarsi certificate; incomplete, since a miss only means
  falling back to blocking colourings.

## RESUME HERE (written at the end of the 2026-10-07 session, Sid stopped for the night)

**Where we are, in three lines.**
- **Theorem R5** is proved: for a regular graph, the kernel method works if and only if the graph
  is bipartite (note `03`).
- **R7:** all 5 open cubic zero-sum graphs are proved 3-edge-choosable by computer
  (note `04`, `choosability.py --reduce`). Final certification of the 4 graphs on 10 vertices
  is pending.
- Degree 4 and up are not reached yet.

**Background jobs left running overnight** (started about 8:40 PM, 7 Oct):
- 4 × `verify_reduce.py` on the 4 cubic graphs on 10 vertices. Output goes to
  `data/verify/*.txt`, but **only at the end**, because Python buffers it.
- Estimated 10 to 20 hours in total. Check with:
  `ps -eo pid,etime,args | grep "[v]erify_reduce"` and `cat data/verify/*.txt`.
- **Success** means each file ends with `(R) N reducibility witnesses: independent AT check passes`
  and `exit=0`.
- **Any `exit=` other than 0, or an AssertionError, means a real problem.** Stop and investigate
  before claiming R7.
- If the jobs were killed (for example by a reboot), it does not matter much: the core-based check
  in step 2 replaces them.

**Do these next, in order:**
1. **Read the background job results** (above). Record them in note `04` (the "Results" table)
   and in RESULTS R7.
2. **Unsat-core check (proposed to Sid, not yet approved; ask first).** Rerun the search on each
   of the 5 cubic graphs with one selector literal per (R) witness, passed as assumptions. After
   UNSAT, get the core from `get_core()`, then run the independent check on only those witnesses
   (a variant of `verify_reduce.py`). Minutes instead of hours, and a small certificate. Save the
   cores in `data/cores/`.
3. **DRAT certificate** for the final UNSAT. Build `drat-trim` into `~/tools`, have CaDiCaL write
   the proof (`with_proof=True` in pysat), and check it.
4. **Degree 4 and up: lazy (R).**
   - In `choosability.py`, stop adding all witnesses up front. On each proposed `L`, test its
     colour classes for reducibility (Alon–Tarsi on `H - I` with the caps from (R)) and add only
     clauses that fire. Also drop dominated witnesses.
   - First target: `GEnbvG` (8 vertices, `k = 4`, `L(G)` has 16 vertices). It timed out at 0
     rounds with 6.4 million up-front clauses.
   - Then the `k = 5` graph on 8 vertices (complement of `C_3 ∪ C_5`), then the 45 graphs on 10
     vertices with `k >= 4` via `run_all_choos.py` (graph6 strings contain backticks, so never
     drive this from bash).
5. **Sid reads notes `03` and `04`** step by step. No human has checked either yet. Then decide
   whether the results are "enough" for the explanatory PDF.

**Pitfalls met this session (avoid them):**
- `pkill -f <pattern>` kills the calling shell too, because the pattern appears in its own
  command line. Kill by PID from `ps -eo pid,args | awk '/pattern/ && !/awk/ && !/bash -c/'`.
- Never pass graph6 strings through bash double quotes: backticks and backslashes break them.
- Python 3.14 multiprocessing uses forkserver, so pass parameters as arguments, not lambdas or
  module globals.
- Brute-force choosability is only feasible for `n <= 6` with `k = 2`, and `n <= 5` with `k = 3`.

**Decisions (Sid, 2026-10-07):**

- **No short handout.**
- **The explanatory PDF is written only once Sid judges the results "enough".** The current set
  (theorem R5 plus census R1 and R2) is a candidate for that, not yet the final set.
- **The Friday story so far:** a concrete open target (Schauz's 52 graphs); the state of the art
  reproduced independently; a theorem showing Galvin's kernel method cannot reach any
  non-bipartite regular graph, including all 52; so we built a third method, which proves the LECC
  for all 5 cubic open graphs (R7, pending certification). Then ask the prof which way next:
  (a), (b) or (c) below.
- **Before Friday: do a bit more.** See "Next action".
- **Sid must read note `03` step by step before presenting it.** No human has checked it yet.

**Next action:** see "RESUME HERE" above. (The earlier choice was option 1, a computer proof
for X. Sid approved it and it succeeded. Option 2, extensions of R5, remains open for later.)

**Open question for the prof** (decides what follows Friday): the kernel method is now provably
out for every open case. Which way next?

- **(a)** Finish A1 by a third method. The first target is the smallest open graph, the cubic
  zero-sum graph `X` on 8 vertices (`GCY^B_`, `L(X)` has 12 vertices), by a computer-assisted
  3-choosability proof.
- **(b)** Develop R5 into a short paper. Extend it to multigraphs, to non-regular graphs, and to
  `Delta + 1` lists (McDonald's open question on the smallest `k` for proper orientations).
- **(c)** Switch to A4.

**Deadline:** meeting Fri 9 Oct 2026, 5:00 PM. No handout (Sid's decision). The explanatory
PDF is written only once Sid judges the results enough.

---

## 1. The problem in one paragraph

The List Edge Colouring Conjecture says `ch'(G) = chi'(G)` for every graph. Schauz
(arXiv:1705.00484) tried to prove it for all graphs on at most 10 vertices with the Alon–Tarsi
method. For a `k`-regular class-1 graph `G` with lists of size `k`, that method has exactly one
monomial to test, `prod_e x_e^(k-1)`, and its coefficient is a signed count of proper
`k`-edge-colourings. On **zero-sum** graphs the count is 0, so the method says nothing. He found:

- 3 such graphs on 8 vertices: the complement of `C_3 ∪ C_5`, a graph `X`, and its complement;
- 51 on 10 vertices: 5 of degree 3, 17 of degree 4, 18 of degree 5, 8 of degree 6 and 3 of
  degree 7, out of 164 regular class-1 graphs.

He left them open. **Our goal:** prove the LECC for as many of them as possible with a different
method, the kernel method of the Dinitz chapter, and say exactly why it fails on the rest.

## 2. The mathematics we rely on

### 2.1 The Alon–Tarsi coefficient for line graphs of regular graphs (Phase 2)

Let `G` be `k`-regular on an even number `N` of vertices, and fix a reference order of the edges
at each vertex. Every proper `k`-edge-colouring `c` gives each vertex `v` a permutation `pi_v`,
which sends the `i`-th edge at `v` to its colour. The coefficient of `prod_e x_e^(k-1)` in the
graph polynomial of `L(G)` is a nonzero constant times

```
S(G) = sum over proper k-edge-colourings c of  prod_v sgn(pi_v(c)).
```

*Derivation, to be written out in note 01.* Use the interpolation (Quantitative Nullstellensatz)
formula with colour set `A = {a_0, ..., a_{k-1}}`:

- Only proper colourings contribute.
- In each vertex's clique, the factor equals `sgn(pi_v)` times the Vandermonde of `A`.
- The denominator is the same for every colouring, since each colour class is a perfect matching.

A colour permutation `sigma` multiplies the product by `sgn(sigma)^N = 1`, so we may fix the
colours at vertex 0 and multiply by `k!`. **Zero-sum means `S(G) = 0`.** Being zero does not
depend on the reference orders.

### 2.2 The kernel method as stable roommates (Phases 4 and 5)

- **Star lemma** (note `09`). In a kernel-perfect orientation of `L(G)`, the edges at each vertex
  `u` are linearly ordered. Write `r_u(v)` in `{0, ..., d(u)-1}` for the rank of edge `uv` at
  `u`, where 0 is best and every arc points to the better edge. Then `d+(uv) = r_u(v) + r_v(u)`.
- **Tightness.** Lists of size `k` need `d+ <= k-1`. Summing over the edges of a `k`-regular
  graph forces equality: `r_u(v) + r_v(u) = k - 1` for every edge.
- **Kernels are stable matchings.** For an edge set `S`, a set `M ⊆ S` is a kernel of `D[S]`
  exactly when `M` is a stable matching of the roommates instance `(V, S)` with preferences
  `r`. Independent in `L(G)` means `M` is a matching. Every `e = uv` outside `M` pointing into
  `M` means `u` or `v` is matched to someone it ranks higher, which is the definition of `e` not
  blocking.
- **Odd ring.** An odd ring is a cycle `a_1 a_2 ... a_m` of `G` with `m >= 3` odd, such that
  every `a_i` ranks `a_{i+1}` above `a_{i-1}`, with indices taken mod `m`.

> **Lemma (odd rings).** A linear-order orientation of `L(G)` is kernel-perfect if and only if
> the preference system has no odd ring.

*Proof sketch, to be written out in note 02.*

- (⇐) Every sub-instance `(V, S)` also has no odd ring. By Tan (1991), using stable partitions,
  or by Chung (2000), an instance with no odd ring has a stable matching, and that matching is a
  kernel of `D[S]`.
- (⇒) Take `S` to be the edges of an odd ring. Any matching misses some `a_i`. Then the edge
  `a_{i-1} a_i` blocks: `a_i` is unmatched, and `a_{i-1}` is either unmatched or matched to
  `a_{i-2}`, whom it ranks below `a_i`. So `D[S]` has no kernel.

**Consequence.** Proving the LECC for `G` by the kernel method is equivalent to finding ranks
`r_u(v)` such that:

1. each vertex's ranks are a permutation of `{0, ..., k-1}`;
2. `r_u(v) + r_v(u) = k-1` on every edge;
3. there is no odd ring.

This is a finite constraint problem, and testing a candidate takes time polynomial in the number
of odd cycles. It replaces the `2^|E|` kernel check in `list-colouring/kernel_search.py`.

**Literature to cite or check.**

- J. J. M. Tan, *A necessary and sufficient condition for the existence of a complete stable
  matching*, J. Algorithms 12 (1991).
- K.-S. Chung, *On the existence of stable roommate matchings*, Games Econom. Behav. 33 (2000).
- F. Maffray, *Kernels in perfect line-graphs*, JCTB 55 (1992).
- Aharoni and Fleiner, *On a lemma of Scarf* (2003).

The lemma may already be in the literature in this form. Check Maffray and Aharoni–Fleiner
before calling it ours. Present it as "a reformulation" unless it turns out to be new.

### 2.3 Known theorems that may already cover some zero-sum graphs (Phase 3)

The LECC is already known for:

- bipartite graphs (Galvin 1995);
- 2-connected regular planar class-1 graphs (Ellingham and Goddyn 1996);
- graphs with a vertex whose deletion leaves a bipartite graph (Peterson and Woodall);
- line-perfect graphs, those with no odd cycle of length at least 5 (Peterson and Woodall);
- `K_n`, by the complete graph results.

`K_{3,3}` is zero-sum but bipartite, and Schauz says so. He does not seem to have filtered the
others.

## 3. Phase-by-phase plan

### Phase 0: novelty check (30 minutes, hard stop)

1. Query Semantic Scholar for papers citing arXiv:1705.00484:
   `https://api.semanticscholar.org/graph/v1/paper/arXiv:1705.00484/citations?fields=title,year,externalIds`.
2. Search for `"zero-sum" "list edge" Schauz` and for "list edge coloring conjecture small graphs".
3. Record what was found in Section 5 below. **Decision:** if someone has already settled the
   zero-sum graphs, stop A1 and switch to A4. Otherwise continue.

### Phase 1: tooling (1 hour, hard stop)

1. Create a venv at `lecc-small/env` with networkx and python-sat (`pysat`). Use OR-Tools CP-SAT
   if it installs on Python 3.14; otherwise use pysat alone.
2. Build nauty from source into `~/tools/nauty`, in a fresh directory, and use `geng`.
   - Fallback: Meringer's regular graph lists, or the House of Graphs website.
3. **Sanity counts** for connected `k`-regular graphs, using `geng -c -d k -D k N`:
   - `N = 8`: degree 3 gives 5, degree 4 gives 6, degree 5 gives 3, degree 6 gives 1,
     degree 7 gives 1. Total 16.
   - `N = 10`: degree 3 gives 19, degree 4 gives 59, degree 5 gives 60, degree 6 gives 21,
     degree 7 gives 5, degree 8 gives 1, degree 9 gives 1. Total 166.

   166 = 164 class 1 + 2 class 2 (the Petersen graph and one other), which matches Schauz.

   If the counts disagree, stop and find out why before going on.

### Phase 2: the Alon–Tarsi census (Thursday morning)

`lecc-small/at_sign.py`, or a C helper if Python is too slow at `N = 10` with high degree.

1. For each regular graph, enumerate proper `k`-edge-colourings with the colours at vertex 0
   fixed, by backtracking. Accumulate `prod_v sgn(pi_v)` incrementally from inversion counts.
   Also count the colourings: a count of 0 means class 2.
2. **Validation before trusting anything:**
   - `K_4`: `S != 0` (Schauz, `K_{p+1}` with `p = 3`).
   - `K_{3,3}`: `S = 0` (Schauz; note `08` found `EE - EO = 0`).
   - `K_6`, `K_8`: `S != 0`.
   - Cross-check `S` against a direct Alon–Tarsi coefficient computation, `EE - EO` over
     Eulerian subdigraphs, on `K_4` and `K_{3,3}`, using `list-colouring/alontarsi.py`.
3. **Expected:** 3 zero-sum graphs on 8 vertices, including the complement of `C_3 ∪ C_5`, and
   51 on 10 vertices with the degree split 5, 17, 18, 8, 3. Any mismatch is itself a finding:
   record it, re-check, and do not proceed on the mismatched set until it is explained.
4. Output `lecc-small/data/zero_sum_N8.g6` and `zero_sum_N10.g6`, plus `census.csv`. Each row
   holds graph6, `N`, `k`, the number of colourings, and `S`.

Time box: if `N = 10` with degrees 6 and 7 is too slow in Python by noon Thursday, finish
`N = 8` and the low degrees, and move the enumeration to C.

### Phase 3: filter by known theorems (1 hour)

`lecc-small/known.py`. For each zero-sum graph, test:

- bipartite;
- planar (`networkx.check_planarity`), with 2-connectivity;
- bipartite after deleting one vertex;
- no odd cycle of length at least 5;
- complete.

Output a table of graphs covered and by which theorem, and the **uncovered list**, which is the
real target. This table is a Friday item on its own.

### Phase 4: the odd-ring lemma, verified (in parallel with Phase 2)

1. Write the proof carefully as note `lecc-small/02-odd-ring-lemma.md`, with the small steps
   set out as in the rest of the project.
2. **Empirical cross-check.** Over every rank system satisfying conditions 1 and 2 on `K_4`, the
   prism, `K_{3,3}`, `C_5 × K_2` and `K_{2,2,2}`, compare "no odd ring" with the brute-force
   `kernel_perfect` from `list-colouring/kernel_search.py`. They must agree on every system.
3. **Regression against earlier notes:**
   - `K_{3,3}` admits a system: Galvin.
   - `K_4` and the prism admit none: the triangle theorem, note `11`.
   - `K_6` admits none: note `12`.
   - Also settle `C_5 × K_2`, left undecided in note `11`. That closes an open item of ours.

### Phase 5: kernel test on the uncovered zero-sum graphs (Thursday afternoon)

`lecc-small/kernel_sat.py`.

1. Variables: one-hot `x[u,v,a]`, meaning "the rank of `uv` at `u` is `a`".
2. Constraints:
   - permutation at each vertex;
   - `x[u,v,a] ⇔ x[v,u,k-1-a]`;
   - order literals `p[u,v,w]`, meaning "`u` ranks `v` above `w`", defined from the one-hot
     variables.
3. Odd rings. For every odd cycle and both directions, add the clause "not all `p` along the
   ring". If the number of cycles is too large, add these lazily: solve, find a ring in the
   model, add its clause, repeat.
4. Symmetry: fix the ranks at vertex 0. The `k`-cycle reversal symmetry is optional.
5. Run the 8-vertex uncovered graphs first, then the 10-vertex ones in increasing order of `k`.
6. Record per graph: SAT, with the rank table saved as `data/cert_<id>.json`, or UNSAT, with
   the solve time and a DRAT proof if pysat or CaDiCaL can emit one.

### Phase 6: certificates (must happen before any claim)

For every SAT result, an **independent** checker `verify_cert.py`, which shares no code with the
solver, re-checks:

1. the permutation and sum conditions;
2. no odd ring, by full cycle enumeration with networkx `simple_cycles` on the undirected graph;
3. where `|E| <= 22`, brute-force kernel-perfectness of the actual orientation of `L(G)`.

Only a graph passing all three goes into RESULTS.md as "LECC proved".

### Phase 7: write-up

1. Friday handout, about 4 pages, in `meetings/2026-10-09/`:
   - the problem;
   - Schauz's gap;
   - the odd-ring lemma;
   - the census table;
   - the results;
   - what is next.
2. The explanatory PDF Sid asked for comes after there are substantial results. It is written
   for Sid to read and explain to the prof: every step, every definition, worked small examples
   (`K_{3,3}` as the Galvin case, `K_4` as the failure), and how to reproduce each number.
   Planned at `latex/lecc-small-explained.tex`.

## 4. Decision tree, so we do not go around in circles

```
Phase 0 finds the zero-sum graphs already settled  -> stop A1, switch to A4.
Phase 1 counts disagree with the known counts      -> fix the generator before anything else.
Phase 2 zero-sum counts disagree with Schauz       -> re-check the sign derivation on K_4 and
                                                      K_{3,3}; if our code checks out, the
                                                      disagreement is a reportable finding.
Phase 4 cross-check finds a disagreement           -> the lemma or the code is wrong; stop and
                                                      resolve, do not run Phase 5.
Phase 5, for each uncovered graph:
    SAT    -> Phase 6 certificate -> "LECC proved for G" (new, pending the Phase 0 check)
    UNSAT  -> "neither Alon-Tarsi nor kernels reach G"; record it, look for a structural
              reason (note 11 style), and leave G for the method list in section 6.
```

**Things not to do before Friday:**

- non-regular or odd-order graphs, Schauz's other gaps (that is A2, later);
- new methods for UNSAT graphs;
- re-deriving the floor or 2-d kernel material;
- polishing code beyond what the checks need.

## 5. Findings so far

*(append as phases complete; each line cites the script that produced it; full list in RESULTS.md)*

- 2026-10-07: census reproduced (R1); 52 open graphs (R2); kernel method fails on all of them
  (R3); `C_5 × K_2` settled (R4); **theorem R5**, proof in note `03`.

- 2026-10-07: smallest uncovered even `K_n` is `K_50` (`open-problems/uncovered_complete.py`).
  Context only, not part of A1.

## 6. Methods for graphs where both methods fail (after Friday)

1. **Hybrid induction.** Run Lemma 1 steps while kernels exist, then switch to Alon–Tarsi on the
   remainder with the reduced list sizes. The coefficient of a non-uniform monomial may be
   nonzero even though the uniform one vanishes.
2. **Embedding.** Add a perfect matching to get a `(k+1)`-regular graph whose `S != 0`, which
   gives `ch' <= k+1`, not `k`. That is not enough for class 1, so use it only for bookkeeping.
3. **Direct choosability search** for the smallest cases. `L(G)` has 12 vertices for the cubic
   8-vertex case. This is a 2QBF-style search with symmetry breaking.
4. **Schauz's suggestion:** case analysis on the lists, using the order-2 symmetry that
   causes the zero sum.

## 7. File layout

```
lecc-small/
  PLAN.md              this file
  RESULTS.md           verified results only, with certificates
  01-at-sign.md        derivation of S(G)                       (Phase 2)
  02-odd-ring-lemma.md lemma and proof                          (Phase 4)
  at_sign.py           Alon-Tarsi census
  known.py             filter by known theorems
  kernel_sat.py        kernel test (SAT with odd-ring clauses)
  verify_cert.py       independent certificate checker
  tests/               regression tests (K_4, K_{3,3}, prism, K_6, C_5 x K_2)
  data/                graph6 lists, census.csv, certificates
```

## 8. Session log

| Date and time | Who | Did | Next |
|---|---|---|---|
| 2026-10-07 evening | Claude | wrote this plan; found the odd-ring reformulation | Phase 0 |
| 2026-10-07 night | Claude | Phases 0 to 5 done; proved theorem R5 (note `03`); RESULTS.md written | Friday material |
| 2026-10-07, about 8:00 PM | Claude | Phase 8: `choosability.py` (CEGAR search with precheck, criticality, symmetry breaking and reducible colour classes). L(X) is 3-choosable in 0.5 s. `verify_reduce.py` re-checks all 6984 Alon-Tarsi facts for X independently: passes. Brute force and plain search agree (`tests/test_choosability.py`). The no-symmetry rerun of X timed out (inconclusive, expected) | batch over all 52 |
| 2026-10-07, about 8:40 PM | Claude | batch: all 5 cubic open graphs choosable; `GEnbvG` (k=4) timed out at 0 rounds; batch stopped; `verify_reduce` started on the 4 cubic graphs on 10 vertices | certify; lazy (R) for k >= 4 |
| 2026-10-07, about 11:30 PM | Claude | wrote RESUME HERE; verify_reduce jobs left running overnight (estimated 10 to 20 hours) | follow RESUME HERE |
| 2026-10-09, 1:10 to 1:30 PM | Claude | reboot killed verify jobs; unsat-core certificates for all 5 cubic graphs, all pass; RESULTS R7 and note 04 updated; reading PDF of notes 03 and 04; `lazy_choos.py` written, X passes, `GEnbvG` started (stop by 2:30 PM) | meeting 5 PM |
