# 05. Novelty check of the A1 results (9 October 2026, about 1:55 to 2:15 PM)

Which results are actually new? Checked against the papers citing the closest prior work
(OpenAlex and Semantic Scholar citation lists), targeted web searches, and the papers themselves
where accessible. Labels: **known**, **not new (reproduction)**, **new, not found in the
literature** (with what was checked), **unchecked**.

## Summary

| Result | Verdict |
|---|---|
| R1 census (3 + 51 zero-sum graphs) | not new: reproduces Schauz exactly |
| R2 filter (52 remain open) | bookkeeping; the extra filter by McDonald–Puleo G* below adds nothing |
| R6 odd-ring lemma | known (BKW 1998; Tan 1991; Chung 2000) |
| **R5 theorem** (kernel method on regular `G` works iff `G` bipartite) | **not found in the literature**; two sources unchecked |
| **R7 + R8** (LECC for 6 of the 52 open graphs) | **new, not found**: the cases are open in all literature found |
| The search method (SAT over list assignments) | **not new as a method**: SAT-based choosability is published (Kirchweger, Peitl, Seka, Szeider, AAAI 2026); cite it. Pruning by Alon–Tarsi-reducible colour classes may be a variation, not a contribution to lead with |

## R5: what was checked

- **Borodin, Kostochka, Woodall 1998** (*On kernel-perfect orientations of line graphs*): an
  orientation of a line graph is kernel-perfect iff every oriented odd cycle has a chord or
  pseudochord and every clique has a kernel. A characterisation of orientations, not of which
  graphs admit one with `Delta+ <= Delta - 1`. Our proof uses it only through the odd-ring step.
- **McDonald 2015** (arXiv:1508.01820): negative results only for her restricted "Galvin
  orientations": Theorem 5 (`K_n`, `n >= 4`) and Theorem 9 (one non-regular graph). Petersen
  has a proper Galvin orientation with 4 = `Delta + 1` colours (Theorem 4). R5 is stronger: every
  kernel-perfect orientation, every non-bipartite regular graph.
- **McDonald–Puleo 2017** (arXiv:1507.05933): graphs whose odd cycles pairwise share at most one
  edge (class G*) are `t`-edge-orientable for `t >= max(4, Delta)`. **Consistent with R5:**
  - they allow 2-cycles in orientations of `L(G)`; for `k`-regular `G`, the count in Step 2 of
    note `03` already forces the out-degree sum to equal the number of edges of `L(G)`, so
    2-cycles cannot occur, and R5 holds in their setting too;
  - no non-bipartite `k`-regular graph with `k >= 3` lies in G*. A leaf block would have one
    vertex of deficient degree `d` with `0 < d < k`: impossible for a bipartite block
    (`k|A| - d = k|B|`), for `K_4` and for a Θ-graph (internal path vertices have degree 2).
    So `G` is a single block: bipartite, `K_4` (3-regular, but then `t >= 4 > Delta`), or a Θ-graph
    (not regular).
  - The same argument shows **G* covers none of the 52 open graphs.**
- **Papers citing BKW 1998** (OpenAlex, 14): titles reviewed; none is about which graphs admit
  such orientations, except the two above and Blumenthal's thesis below.
- **Jafari 2026** (arXiv:2608.22895, LECC for `K_{p-1}`, `K_{2p}`): algebraic, no kernels.
- **2026 dynamic survey** (arXiv:2606.31702): abstract only; no sign of it.

**Unchecked (do before any claim):**
1. A. Blumenthal, *On Galvin's Theorem and Stable Matchings*, M.Sc. thesis, Auburn 2016
   (advisor J. McDonald). It "characterises graphs that have stable matchings with respect to
   their preference lists", which is the closest topic. The Auburn server refused connections
   on 9 Oct: <https://etd.auburn.edu/bitstream/handle/10415/5383/AMB_Thesis_Final.pdf?sequence=2>.
2. D. R. Woodall, *List colourings of graphs*, Surveys in Combinatorics 2001 (cites BKW 1998).
   Not accessible online.

**Honest framing.** The proof is about a page and elementary. It may be folklore among people who
work with Galvin's method, even if unpublished. Say "we have not found it in the literature"
and ask the prof whether he knows it.

## R7 and R8: why the 6 graphs are open

- Schauz (arXiv:1705.00484; J. Discrete Algorithms 2018) lists them as open.
- No paper citing Schauz settles them (3 citing papers, checked 7 Oct; Jafari 2026 does not
  mention them).
- **Alon–Tarsi cannot reach them in any form:** for `k`-regular `G`, `L(G)` has `|E|` vertices
  and `|E|(k-1)` edges, so a monomial with all exponents at most `k-1` must be the uniform one,
  whose coefficient is 0 here.
- **The kernel method cannot reach them** (R5).
- No known theorem covers them: not bipartite, planar, line-perfect, bipartite plus one vertex,
  complete, in G* (above), or Halin (Halin graphs are planar; Lang, arXiv:1504.05252).
- None is a named graph that might have its own literature: all six have small automorphism
  groups (orders 4 to 16), and none is `K_4 □ K_2`, a circulant tried, or a complement of one.

So `ch'(G) = chi'(G)` for these 6 graphs is **new as far as we can find**. It is a computer
result about 6 specific small graphs. Its weight comes from Schauz having named them as open and
from both standard methods provably failing on them, not from size.

## The method

Kirchweger, Peitl, Seka, Szeider, *Graph Choosability via SAT: Beyond the Nullstellensatz*,
AAAI 2026 (<https://ojs.aaai.org/index.php/AAAI/article/view/38441>): SAT Modulo Symmetries and
QBF for vertex choosability, with pen-and-paper pruning. Not about edge colouring or line graphs.
Our CEGAR search with Alon–Tarsi-reducible colour classes is a variation in the same spirit.
Cite it; do not present the method as new.
