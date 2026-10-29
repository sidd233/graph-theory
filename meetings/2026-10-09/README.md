# Meeting, Friday 9 October 2026, 5:00 PM

> **Update 2026-10-07 (Sid):** no short handout. The explanatory PDF is written only once the
> results are judged enough. Current candidate story and next steps: `lecc-small/PLAN.md`,
> "Decisions".

Sid is away the following week, so this meeting has to leave the prof agreeing on a target and
holding something concrete. The next update (16 October) goes by email.

## What we show

Three items, in order of priority. Item 1 alone makes a valid meeting. Items 2 and 3 make it a
strong one.

### 1. The landscape and a proposed target (status: drafted)

A one-page summary of `open-problems/in-scope.md`:

- **The rectangle is solved.** `chi_ell(K_m □ K_n) = max(m, n)`, by Galvin, and Janssen (1993)
  for `(n-1) x n`. Arbitrary shapes are solved by Borodin–Kostochka–Woodall. Moving past
  bipartite underlying graphs is exactly the List Edge Colouring Conjecture.
- **Proposed target, A1.** Prove the LECC for Schauz's zero-sum graphs: 3 graphs on 8 vertices
  and 51 on 10. These are the cases his 2017 attack left open, where the Alon–Tarsi count
  vanishes.
- **Backups.**
  - A4: `chi_ell(C_{2m+1} □ C_{2n+1}) = 3`, the closest non-bipartite relative of the Dinitz
    square.
  - A5: the `K_{5,q}` gap.
  - A6: `K_n` for `n = 50, 56, 64, ...`.

### 2. The rectangle, written properly (status: not started; label: known, exposition)

Two pages in `latex/`. The Book's proof of Galvin's theorem carries over word for word to an
`m x n` array:

1. take a Latin rectangle with entries `1..n`;
2. orient rows towards the larger entry and columns towards the smaller;
3. then `d+ <= (n - e) + (e - 1) = n - 1`, and the stable matching lemma gives a kernel in every
   induced subgraph.

Then state the Borodin–Kostochka–Woodall version for arbitrary shapes. This answers the prof's
literal question from last week and shows the induction is understood.

### 3. First computation on A1 (status: DONE, 2026-10-07; see `lecc-small/RESULTS.md`)

Outcome, in one breath:

- Schauz's census reproduced exactly: 3 zero-sum graphs on 8 vertices, 51 on 10.
- 52 of them are not covered by any known theorem.
- The kernel method fails on all 52.
- The reason is a theorem (`lecc-small/03-regular-bipartite-theorem.md`): **for a regular graph,
  Galvin's kernel method works if and only if the graph is bipartite.** It is not found in the
  literature so far, it subsumes our notes `11` and `12`, and it is confirmed on 1923 graphs.

The handout should lead with the theorem and its proof, then the census as context. Ask the
prof to choose between directions (a), (b) and (c) in `lecc-small/PLAN.md`.

Original plan for this item:

1. **Reproduce** Schauz's zero-sum census on 8 vertices: 3 graphs among the regular class-1
   graphs. The 10-vertex census of 51 graphs follows if time allows.
2. **Test the kernel method** on the 3 graphs on 8 vertices: does `L(G)` have a kernel-perfect
   orientation with `Delta+ <= k - 1`? If yes, that proves the LECC for that graph. That is
   probably **new**, pending a check of the papers citing Schauz. If no, we explain why, using
   notes `11` and `12`.

Tools needed: networkx (already in `census-tool/env`), a generator for regular graphs (nauty's
`geng` or pynauty, the latter already installed), and our kernel search code.

## Questions for the prof

1. Is the LECC the direction he wants, and is A1 an acceptable first target?
2. Would he rather see the algebraic route (A6, congruences as in Jafari 2026) or the
   combinatorial and computational route (A1, A4)?
3. What should the 16 October email contain, given Sid is away?

## Timeline

| When | What |
|---|---|
| Wed 7 Oct, evening | lists and plan (done); go-ahead on item 3 |
| Thu 8 Oct | item 3, Schauz census and kernel test; item 2 drafted |
| Fri 9 Oct, by 2 PM | handout compiled and checked; buffer until 5 PM |
