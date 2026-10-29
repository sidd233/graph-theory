# Talking points, Friday 9 October 2026, 5:00 PM (for Sid, not a handout)

Show on screen: `latex/_build/lecc-small-reading.pdf` (notes 03 and 04) and
`lecc-small/RESULTS.md`.

## 1. The target (1 minute)

- The LECC: `ch'(G) = chi'(G)`. Schauz (2017) attacked all graphs on at most 10 vertices with
  Alon–Tarsi.
- For a `k`-regular class-1 graph, Alon–Tarsi has one monomial to test, and its coefficient is a
  signed count of `k`-edge-colourings. On "zero-sum" graphs it is 0, so the method is silent.
- He left those open: 3 on 8 vertices, 51 on 10. We reproduced his census exactly (R1). After
  removing those covered by known theorems, **52 remain open** (R2).

## 2. The theorem (3 minutes; the main mathematical content)

> For a simple `k`-regular graph `G`, `L(G)` has a kernel-perfect orientation with
> out-degree at most `k - 1` **if and only if** `G` is bipartite.

- So Galvin's kernel method can never prove the LECC for a non-bipartite regular graph, and
  that includes all 52.
- Proof idea in one line: tightness forces `r_u(v) + r_v(u) = k - 1`; ranks split each vertex's
  edges into a "better half" and a "worse half", giving an Eulerian orientation; an odd cycle
  that follows it would be an odd ring, which has no kernel; parity then forces bipartite.
- Status: not found in BKW 1998 or McDonald 2015. Say "we have not found it in the
  literature", not "new". Ask him if he knows it.
- Machine check: 1923 regular graphs, SAT on exactly the 29 bipartite ones.

## 3. A third method, and what it proves (2 minutes)

- Both standard methods provably fail on the 52, so we built a third: a SAT-based search over
  list assignments, pruned by lemmas that each have a one-line proof (note 04: (P), (C), (B),
  (S), (R)).
- **Result: the LECC holds for all 5 open cubic zero-sum graphs** (X on 8 vertices, 4 on 10).
- Certified: an independent checker, sharing no code with the search, re-checks every
  Alon–Tarsi fact by counting Eulerian subgraphs, and a second SAT solver re-confirms the final
  UNSAT. Not yet done: a DRAT proof trace.
- **Degree 4 too:** the method, with one engineering change (adding the reducibility clauses
  lazily), proves the LECC for `GEnbvG`, the open 4-regular graph on 8 vertices. Certified the
  same way (R8). That makes **6 of the 52** open graphs settled today.
- Remaining: 1 on 8 vertices (degree 5) and 45 on 10 vertices (degrees 4 to 7). The search
  itself is fast; the bottleneck is computing Alon–Tarsi coefficients, which runs out of memory
  (over 7 GB) on these larger line graphs. Planned fix: find the Alon–Tarsi facts through
  orientations and Eulerian counts instead, which needs little memory.

## 4. The question for him

Which way next?
- **(a)** push the computer method through the remaining 46 (1 on 8 vertices, 45 on 10),
  aiming to settle all 52;
- **(b)** turn the theorem into a short paper (extend to multigraphs, non-regular graphs,
  `Delta + 1` lists);
- **(c)** switch to A4, `chi_ell(C_{2m+1} □ C_{2n+1}) = 3`.

Also: what should the 16 October email contain (you are away that week)?

## If he asks...

- *"Is the computer proof trustworthy?"* Every lemma it uses is a few lines. The solver's
  answer is re-checked by independent code and a second solver. The method agrees with brute
  force on 79 small graphs and finds the known bad cases (for example `L(Petersen)` with 3).
- *"Why can't kernels work?"* The theorem. Show Step 2 (tightness) and Step 5 (admissible odd
  cycle = odd ring).
- *"Is the theorem known?"* Not found in BKW 1998, McDonald 2015, McDonald–Puleo 2017 (consistent
  with it), or anything citing BKW. Two sources unchecked: Blumenthal's 2016 Auburn thesis (on
  Galvin's theorem and stable matchings) and Woodall's 2001 survey. Ask him if he knows it.
  Details: `lecc-small/05-novelty-check.md`.
- *"Is the computer method new?"* No: SAT-based choosability is published (Kirchweger, Peitl,
  Seka, Szeider, AAAI 2026, for vertex colouring). What is new is the 6 settled cases.
