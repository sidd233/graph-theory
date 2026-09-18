# ~/work/gt

Graph theory research. **Read `PROBLEM.md` before starting research work in this repository.**

## The goal

**Improve the bound on the list colouring problem, using 2-d kernels.**

Lemma 1 of *Proofs from THE BOOK*, chapter 33, gives `chi_ell(G) <= d+(v) + 1` whenever every
induced subgraph of an orientation has a kernel. Strengthening the kernel to a **2-d kernel**,
which is independent plus 2-dominating, should buy two units of out-degree per colour instead
of one and give roughly `ceil(Delta+/2) + 1`. That halving is the target.

The core of the problem is three requirements at once: graphs that **have** 2-d kernels, that
**still have** them on every induced subdigraph so the induction repeats, and onto which the
list colouring problem can actually be **mapped**. `PROBLEM.md` section 3 states them as (R1),
(R2) and (R3), and section 4 states the two obstructions that have to be answered.

Work on this project is aimed at that bound. If a direction does not serve it, say so plainly
rather than presenting it as progress.

**Not the goal:** the line graph conjecture `chi(H) = chi_ell(H)`, the one-sentence open
question closing chapter 33. An earlier session mistook it for the goal and wrote that into
this file, which misdirected several sessions. Notes `06` to `12` and
`latex/kernel-orientations-of-line-graphs.tex` were produced under that misreading. Their
results stand as mathematics but they are not progress on the goal.

## Layout

  - `PROBLEM.md` is the alignment document and the first thing to read.
  - `list-colouring/` is the current work: numbered notes `00` to `12`, `LOG.md` for the
    reasoning behind each step, and the Python that produced every number. Notes `00` to `05`
    are on the goal. Notes `06` to `12` are on the line graph conjecture and are off target.
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
