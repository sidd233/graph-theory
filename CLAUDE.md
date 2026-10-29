# ~/work/gt

Graph theory research. **Read `PROBLEM.md` before starting research work in this repository.**

## The goal

**Solve an open problem in graph theory** (set by Sid on 2026-10-07). The working direction,
pushed by the supervisor, is the **List Edge Colouring Conjecture** (LECC),
`ch'(G) = chi'(G)`, equivalently `chi_ell(L(G)) = chi(L(G))`, and the problems next to it.
Galvin's solution of the Dinitz problem is the bipartite case. Candidate problems, tiered by
how realistic they are, are in `open-problems/in-scope.md`. **Agreed target (meeting 9 October
2026): the torus problem A4,** `chi_ell(C_{2m+1} □ C_{2n+1}) = 3`, work in `odd-torus/`. The
remaining zero-sum graphs (A1) are optional. See `meetings/2026-10-09/notes.md`.

**2-d kernels are a tool, not the goal.** Earlier sessions treated "improve the bound with 2-d
kernels" as the goal, which was a misreading. That work is recorded in `PROBLEM.md` and notes
`00` to `05` and `13` to `16`, and its results stand. The kernel method, 2-d kernels and
Alon–Tarsi are all tools to be used where they help.

If a direction does not lead towards solving an open problem, say so plainly rather than
presenting it as progress. Before claiming a result is new, check the literature that cites the
closest prior work.

## Layout

  - `PROBLEM.md` is the alignment document and the first thing to read.
  - `open-problems/` holds the candidate open problems: `in-scope.md` (the LECC and its
    neighbours) and `broader.md`.
  - `lecc-small/` is the current work, on the LECC for Schauz's small zero-sum graphs (A1).
    **Read `lecc-small/PLAN.md` first**: it has the status board, the next action and the
    decision tree. Verified results are in `lecc-small/RESULTS.md`.
  - `meetings/` holds one folder per weekly supervisor meeting (Fridays, 5:00 PM): what is
    shown, and what was agreed.
  - `list-colouring/` holds numbered notes `00` to `16`, `LOG.md` for the reasoning behind each
    step, and the Python that produced every number. Notes `06` to `12` are on the LECC and
    hold the kernel-method obstructions for it (star lemma, triangle theorem, even complete
    graphs).
  - `census-tool/` is the 2-d kernel census, with `FINDINGS.md` separating proved,
    exhaustively verified, and conjectured.
  - `latex/` holds formal write-ups, `references/` the papers and books.
  - `~/work/acads/sem7/8_rp/` holds the capstone research plan shown to the supervisor.

## Conventions

  - Prose for the user uses no em dashes and no en dashes in ranges. Write "from a to b".
  - Formal documents are academically formal and broken into small verifiable steps.
  - In this project a **2-d kernel** is independent plus 2-dominant, meaning every outside
    vertex has at least two out-arcs into the set. Always call it a "2-d kernel", never a
    "2-kernel" or a "k-kernel", so it is never confused with the distance-based `(k,l)`-kernel
    of the published literature.
  - Every claimed number should have a script in the repository that reproduces it.
  - Discuss the direction before running experiments.
