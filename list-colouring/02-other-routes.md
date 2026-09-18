# 3. Other routes to a better list-colouring bound (brief scan)

Ordered by how well they fit what we already have.

**1. Alon-Tarsi / Combinatorial Nullstellensatz.** `ch(G) <= AT(G)`, where `AT(G)` is the
least `Delta+(D) + 1` over orientations `D` in which the numbers of even and odd spanning
Eulerian subdigraphs differ. Same shape as the kernel method (an orientation with small
out-degree) but **with no hereditary requirement**, so the single-arc barrier simply does
not apply. It gives `ch <= 3` for planar bipartite graphs.
**Correction (see `08`): it is NOT stronger than the kernel method.** The two are
incomparable. Galvin's own orientation of `S_3 = L(K_{3,3})` is kernel-perfect with
`Delta+ = 2` yet has `EE - EO = 0`, and `AT(S_3) = 4 > 3 = chi_ell(S_3)`.
This is the most promising near neighbour: our `Delta+/2` ambition would become a statement
about a low-degree monomial having a nonzero coefficient, which is a checkable algebraic
question rather than a structural one.

**2. Fractional kernels and Scarf's lemma.** Fractional kernels always exist (Aharoni and
Holzman); Aharoni, Berger and Ziv used this machinery for fractional relaxations of
Galvin's theorem. A fractional 2-d kernel is a clean LP object whose existence can be studied
on its own. Directly continues (B3) above.

**3. Probabilistic methods: Local Lemma, entropy compression, hard-core counting.**
Johansson and then Molloy: triangle-free implies `ch <= (1 + o(1)) Delta / ln Delta`.
Rosenfeld-style counting and the hard-core model method (Davies, de Joannis de Verclos,
Kang, Pirot) reprove these cleanly and give local versions. Important calibration: in the
triangle-free regime these already beat `Delta/2 + 1` comfortably. So a 2-d kernel theorem
there would have to justify itself by being explicit, structural and algorithmic, not by
the size of the bound.

**4. Reed-type bounds.** `chi <= ceil((Delta + 1 + omega)/2)`, and Reed's theorem that
`chi <= (1 - eps)(Delta + 1) + eps omega` for small `eps`. This is the established
"halving" target and, per the calibration in `01-what-we-need.md`, the shape our bound
should take. The list analogue is the natural prize and is much less settled than the
ordinary one; worth checking the current status carefully before committing.

**5. Thomassen-style induction.** Strengthen the statement (precolour a path, allow a few
short lists), delete a vertex rather than a colour. The method behind tight results such as
5-choosability of planar graphs. Immune to our barrier by construction.

**6. Correspondence (DP) colouring.** A strengthening of list colouring. Useful as a stress
test: an argument that survives the DP setting is more robust, but DP also destroys some
genuinely list-specific gains (planar bipartite has DP-chromatic number 4, not 3), so it
tells us which half of any gain is real.

**7. Hall-type conditions and f-choosability.** The Bondy, Boppana and Siegel setting is
already the `f = d+ + 1` case of a general Hall condition on lists. Worth knowing where the
general condition sits, since our accounting lemma is a special case of it.
