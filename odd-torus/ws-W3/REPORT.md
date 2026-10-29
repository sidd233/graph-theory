# W3: 2-d kernels in tori

Setting and notation:
- A 2-d kernel of G is an independent set S such that every vertex outside S has at least 2 neighbours in S. This is Włoch's "(2-d)-kernel".
- T(m, n) = C_m □ C_n with vertices (r, c), r ∈ Z_m, c ∈ Z_n.
- Row r = {c : (r, c) ∈ S} ⊆ Z_n. Column c = {r : (r, c) ∈ S} ⊆ Z_m.
- MIS = maximal independent set of a cycle.
- P = Perrin numbers: 3, 0, 2, 3, 2, 5, 5, 7, 10, 12, 17, .... P(k) is the number of MIS of C_k for k ≥ 2. For k = 2 these are {0} and {1} of the 2-cycle.
- m, n ≥ 3 throughout unless stated otherwise.

**Connection to A4 (3-choosability of odd tori): weak.** When gcd(2m+1, 2n+1) = 1 the odd torus has no 2-d kernel at all. When one exists it is a single undirected set; the kernel method needs kernels in every induced subdigraph of an orientation, and the hereditary 2-d kernel version is already known to be vacuous (latex/hereditary-2-d-kernels-are-arcless.tex). A 2-d kernel S allows one colouring step (colour S, every other vertex loses 2 neighbours), but only with a colour common to all lists, which arbitrary 3-lists do not give. So this workstream settles a side question about the tool and corrects a published theorem. It does not move A4.

## Results
- [PROVED] Line lemma: S is a 2-d kernel of C_m □ C_n iff every row is an MIS of C_n and every column is an MIS of C_m.
- [PROVED] Classification: every 2-d kernel has the form S = {(r, c) : (c − s·r) mod d ∈ K'}, with s = ±1, d = gcd(m, n), and K' an MIS of the cycle Z_d. Every such set is a 2-d kernel.
- [PROVED] C_m □ C_n has a 2-d kernel iff gcd(m, n) > 1. This settles items 1 to 3 of the brief for all m, n.
- [PROVED] Number of 2-d kernels: 0 if d = 1, 2P(d) if d is odd, 2P(d) − 2 if d is even.
- [PROVED] Every kernel has size (mn/d)·k with ⌈d/3⌉ ≤ k ≤ ⌊d/2⌋, and every such k occurs. So i₂ = min size = mn·⌈d/3⌉/d, and max size = mn·⌊d/2⌋/d.
- [PROVED] Uniform construction for every d ≥ 2, prime or not: S = {(r + c) mod d ∈ K'}.
  - p = 2: checkerboard (K' = {0} on the 2-cycle multigraph).
  - p = 3: K' = {0}.
  - p ≥ 5: K' = {0, 2, ..., p − 3}.
- [PROVED] Covering lemma: the preimage of a 2-d kernel under a covering map (multiplicities counted) is a 2-d kernel. It is not needed, given the uniform construction.
- [PROVED] Bednarz and Włoch, Ann. UMCS Sect. A 70(2) (2016) 1 to 8, Theorem 2.5 and Corollary 2.6 are false.
  - Thm 2.5 says a kernel exists iff "both even or n = m". Counterexamples: C_3 □ C_6, C_3 □ C_9, C_5 □ C_10, C_6 □ C_9. For C_3 □ C_6, take (r + c) mod 3 = 0.
  - Cor 2.6 says the count is 2 when both are even and 2n for odd squares. True counts: C_6 □ C_6 = 8, C_8 □ C_8 = 18, C_9 □ C_9 = 24, C_11 □ C_11 = 44.
- [COMPUTER-VERIFIED, m from 3 to 20, all n] Column transfer digraph:
  - every nontrivial SCC is a simple cycle;
  - every arc inside an SCC is a pure shift;
  - the exact n-set is {n ≥ 3 : gcd(m, n) > 1}.
- [COMPUTER-VERIFIED, m ≤ 14, n ≤ 40] SAT existence equals [gcd > 1] in all 456 cases. Every model is diagonal.
- [COMPUTER-VERIFIED] The count formula matches SAT enumeration (95 tori, m ≤ 12, n ≤ 16) and SAT-free brute force (all mn ≤ 64).
- [COMPUTER-VERIFIED, m ≤ n ≤ 12] γ₂ and i₂ table (MILP, all optimal, re-confirmed by SAT with cardinality constraints). In this range i₂ = γ₂ exactly when 3 | d, or for (5,5), (5,10), (8,8), (11,11).
- [COMPUTER-VERIFIED, a ≤ b ≤ c ≤ 9] 3D table: 57 of 84 triples have a kernel. Neither gcd(a, b, c) nor the pairwise gcds decide existence:
  - 36 triples have a kernel although gcd(a, b, c) = 1;
  - 14 triples have no kernel although some pairwise gcd is > 1, e.g. (3,7,7), (5,7,7), (3,4,4).
- [PROVED] K_3 reduction: if Δ(G) ≤ 5, then C_3 □ G has a 2-d kernel iff G has a fall 3-colouring. A fall 3-colouring is a proper 3-colouring in which every vertex sees both other colours, i.e. a partition into 3 independent dominating sets.
- [PROVED] Rigidity: every fall 3-colouring f of C_b □ C_c has a constant step ε = ±1 along one of the two axes. Hence C_b □ C_c is fall 3-colourable iff 3 | b or 3 | c.
- [PROVED] C_3 □ C_b □ C_c has a 2-d kernel iff 3 | b or 3 | c. For (3, 7, 7), C_7 □ C_7 cannot be split into 3 independent dominating sets.
- [COMPUTER-VERIFIED, exact for all c ≥ 3] Layer transfer digraph, cases where C_a □ C_b □ C_c has a kernel:

  | (a, b) | c with a 2-d kernel |
  |---|---|
  | (3,3) | every c |
  | (3,4), (3,5), (3,7) | 3 \| c |
  | (3,6) | every c |
  | (4,4) | every c except 3, 5, 7 |
  | (4,5) | 5 \| c |

  (4,6) and larger exceeded the 3 GB cap.
- [PROVED] Layered construction: stacking 2-d kernels of C_a □ C_b, with consecutive layers disjoint, gives a kernel. This works iff the disjointness graph of the 2D kernels has a closed walk of length c. Among a ≤ b ≤ c ≤ 9 it explains every YES except (4,4,9) and (4,8,9), whose kernels are all non-layered.
- [CONJECTURED] In 3D a kernel exists only if some pairwise gcd is > 1. True for all 84 triples up to 9; no proof.

## Proofs

P1, line lemma.
- (⇐) Every edge lies in a row or a column, so S is independent. A vertex v outside S has one S-neighbour in its row and another in its column.
- (⇒) Suppose positions c − 1, c, c + 1 of row r are all outside S.
  - (r, c) has no S-neighbour in its row, so (r ± 1, c) ∈ S.
  - (r, c − 1) has neighbours (r, c) ∉ S, (r, c − 2), and (r ± 1, c − 1). The last two are adjacent to (r ± 1, c) ∈ S, so they are not in S.
  - So (r, c − 1) has at most 1 S-neighbour, a contradiction.
- So every row has no "11" and no "000", which means it is an MIS. This uses m, n ≥ 3. Columns are the same. ∎

P2, classification. Unroll the rows to R_t, t ∈ Z. P1 gives three facts:
- (a) each R_t is an MIS, so its gaps are 2 or 3;
- (b) R_t ∩ R_{t+1} = ∅;
- (c) R_{t−1} ∪ R_t ∪ R_{t+1} = Z_n.

Step 1. R_{t+1} has exactly one point in each gap of R_t: the midpoint of a 2-gap, or one of the two points of a 3-gap. So all rows have the same size k. Write the point as p_i + e_i with e_i ∈ {1, g_i − 1}. By (c), R_{t−1} takes the other point of each 3-gap, at offset g_i − e_i.

Step 2. Apply Step 1 at row t + 1 with labels carried along. Then E^(t)_j = e_{j+t} (labels mod k), and the gap lengths are G^(t)_j = b_j + e_{j+t}, where b_j = g_j − e_j ∈ {1, 2}.

Step 3. Gaps are at most 3, so (e_i, b_j) ≠ (2, 2) for all i, j, because j + t runs over all residues for t from 0 to k − 1. So either e ≡ 1, giving R_{t+1} = R_t + 1 for all t, or b ≡ 1, giving R_{t+1} = R_t − 1 for all t.

So R_t = R_0 + s·t. Then R_m = R_0 forces R_0 to be invariant under +m, hence under +d. Then R_0 is the preimage of an MIS K' of Z_d, and none exists when d = 1. The converse follows from P1, since Z_n → Z_d is a covering of cycles. ∎

Count: two choices (s, K') give the same S only for the two checkerboards, which arise once for each s. Sizes are |S| = (mn/d)·|K'|.

P3, transfer equivalence.
- States are pairs (A, B) of disjoint independent subsets of Z_m.
- There is an arc (A, B) → (B, C) iff C is independent, B ∩ C = ∅, and every r ∉ B has [r ∈ A] + [r ∈ C] + [r ± 1 ∈ B] ≥ 2.
- For n ≥ 3, closed walks of length n with a marked start correspond one to one with 2-d kernels:
  - the state conditions give independence;
  - the arc into (X_j, X_{j+1}) checks domination of column j, whose 4 neighbours are distinct because m, n ≥ 3.
- n = 2 corresponds to the multigraph C_m □ C_2. n = 1 is impossible, since A = ∅ fails domination.
- Exactness: a closed walk stays in one SCC, and every SCC was found to be a simple cycle, so the lengths are exactly the multiples of its size. No Wielandt or Frobenius threshold is needed.
- In 3D the SCCs need not be simple cycles. There the boolean powers M^t of each SCC are computed until a repeat M^t = M^s appears. From then on the sequence is periodic, so trace(M^c) is known exactly for every c.

P4, covering lemma. Let π be a covering, bijective on neighbourhoods counted as multisets, and T a 2-d kernel of the quotient.
- An edge inside π⁻¹(T) would map to an edge inside T, so π⁻¹(T) is independent.
- The ≥ 2 T-neighbours of π(v) lift to ≥ 2 neighbours of v. ∎

P5, K_3 reduction.
- Each triangle (the C_3 fibre) holds at most one S-vertex.
- An empty triangle at p would need 6 distinct neighbours of p: 2 for each of the 3 colours. That is impossible when Δ ≤ 5.
- So f(p) = the S-position in the triangle at p is defined everywhere.
- Independence of S means f is a proper colouring. Domination of (x, p) with x ≠ f(p) means p has a neighbour of colour x. ∎

P6, rigidity. Write α, β ∈ {±1} for the colour steps along the two axes, read mod 3.
- The square sums α + β' − β − α' are even, at most 4 in absolute value, and ≡ 0 mod 3, so they are 0. So local integer heights h exist, and a fall colouring means every vertex has neighbours at h + 1 and h − 1.
- Take a row maximum v at height H, so both row neighbours are at H − 1. It needs H + 1 from (y, z ± 1).
- If (y, z + 1) = H + 1: then (y ± 1, z + 1) = H, so (y, z + 1) is again a row maximum, and it forces (y, z + 2) = H + 2. Inductively β ≡ +1 on column y. The case (y, z − 1) = H + 1 is the mirror image and gives β ≡ −1.
- Every column has the same winding (sum the square relation along a row). So β ≡ ε everywhere, and then 3 | c.
- If there are no row turns at all, then α ≡ ε everywhere and 3 | b.
- Conversely, f = y + g(z), with g any proper 3-colouring of C_c, works when 3 | b. ∎

## Evidence
All commands run in odd-torus/ws-W3 with PY=/home/sid/work/gt/odd-torus/env/bin/python.
- transfer.py: `$PY transfer.py 3 20 > transfer_m3-20.txt`. Took 5.9 s and 0.99 GB RSS (transfer_m3-20_time.txt).
  - For every m: `shift_property=True every_SCC_simple_cycle=True all_periods_share_factor_with_m=True`.
  - The column patterns on cycles are exactly the MIS of C_m.
  - The n-set up to 60 equals {gcd > 1}.
- sat_check.py:
  - `exist 14 40` → sat_exist_m3-14_n3-40.txt, "disagreements with gcd>1: 0";
  - `count 12 16` → sat_count_m3-12_n3-16.txt, "disagreements: 0", all_diagonal=True;
  - `brute 64` → brute_count_upto64v.txt, "disagreements: 0".
- constructions.py → constructions.txt:
  - 6074 construction cases with m, n ≤ 40, 0 failures;
  - 358 covering lifts of SAT-found kernels, 0 failures;
  - the MIS counts are the Perrin numbers;
  - pictures for p = 4, 3, 5, 7, 11, 13;
  - 3D sum construction, 139 cases, 0 failures.
- min_size.py: `12` → min_size_upto12.txt, all statuses optimal, 0 disagreements with the closed forms.
- gamma2_sat.py: `12` → gamma2_sat_upto12.txt, 0 disagreements.
- 3D scripts:
  - torus3d.py: `9` → torus3d_upto9.txt;
  - torus3d_summary.py → torus3d_summary.txt;
  - torus3d_layers.py: `predict 9` → torus3d_layered_prediction.txt (2 differences: (4,4,9) and (4,8,9));
  - torus3d_transfer.py → torus3d_transfer_small.txt (4.2 s, 0.55 GB).
- fall3.py: `24` → fall3_upto24.txt, 0 disagreements with "3|b or 3|c" for b, c ≤ 24, and 0 against the 3D SAT a = 3 row.
- fall3_rigidity.py → fall3_rigidity.txt. In all 13 tori every fall 3-colouring has a constant step along one axis, e.g. C_6 □ C_6: 252 of 252, C_3 □ C_9: 1020 of 1020. The counts match 2χ(C_c;3)[3|b] + 2χ(C_b;3)[3|c] − 12[3|b and 3|c], where χ(C_k;3) = 2^k + 2(−1)^k.
- coordinator_check.py (written by the coordinating session, own SAT encoding, not W3's code): `$PY coordinator_check.py > coordinator_check.txt`, enumerates all 2-d kernels for 3 ≤ m ≤ 10, m ≤ n ≤ 12 and compares with 2P(d) − 2[d even]: `disagreements: 0`; e.g. `C3 x C6: 6 2-d kernels`, `C6 x C6: 8`, `C9 x C9: 24`.

Per-m table (exact for all n ≥ 3; L = number of independent sets of C_m):

| m | L | arcs | nontrivial SCCs | states on cycles | SCC lengths | exact n-set |
|---|---|---|---|---|---|---|
| 3 | 4 | 6 | 2 | 6 | 3 | 3 \| n |
| 4 | 7 | 32 | 1 | 2 | 2 | 2 \| n |
| 5 | 11 | 40 | 2 | 10 | 5 | 5 \| n |
| 6 | 18 | 140 | 3 | 8 | 2, 3 | 2 \| n or 3 \| n |
| 7 | 29 | 224 | 2 | 14 | 7 | 7 \| n |
| 8 | 47 | 640 | 3 | 18 | 2, 8 | 2 \| n |
| 9 | 76 | 1176 | 4 | 24 | 3, 9 | 3 \| n |
| 10 | 123 | 3008 | 5 | 32 | 2, 5, 10 | 2 \| n or 5 \| n |
| 11 | 199 | 5984 | 4 | 44 | 11 | 11 \| n |
| 12 | 322 | 14384 | 7 | 56 | 2, 3, 12 | 2 \| n or 3 \| n |
| 13 | 521 | 29952 | 6 | 78 | 13 | 13 \| n |
| 14 | 843 | 69504 | 9 | 100 | 2, 7, 14 | 2 \| n or 7 \| n |
| 15 | 1364 | 148576 | 12 | 136 | 3, 5, 15 | 3 \| n or 5 \| n |
| 16 | 2207 | 337920 | 13 | 178 | 2, 8, 16 | 2 \| n |
| 17 | 3571 | 733312 | 14 | 238 | 17 | 17 \| n |
| 18 | 5778 | 1648832 | 21 | 314 | 2, 3, 9, 18 | 2 \| n or 3 \| n |
| 19 | 9349 | 3609088 | 22 | 418 | 19 | 19 \| n |
| 20 | 15127 | 8061952 | 31 | 552 | 2, 5, 10, 20 | 2 \| n or 5 \| n |

States on cycles = 2P(m) − 2[m even]. The SCC lengths 4 and 6 never occur, because no MIS of C_4 or C_6 has exact period 4 or 6.

Size table, γ₂ / i₂ / max 2-d kernel ("–" = no 2-d kernel):

| m×n | γ₂ | i₂ | max |
|---|---|---|---|
| 3×3 | 3 | 3 | 3 |
| 3×4 | 5 | – | – |
| 3×5 | 6 | – | – |
| 3×6 | 6 | 6 | 6 |
| 3×7 | 8 | – | – |
| 3×8 | 9 | – | – |
| 3×9 | 9 | 9 | 9 |
| 3×10 | 11 | – | – |
| 3×11 | 12 | – | – |
| 3×12 | 12 | 12 | 12 |
| 4×4 | 7 | 8 | 8 |
| 4×5 | 8 | – | – |
| 4×6 | 10 | 12 | 12 |
| 4×7 | 12 | – | – |
| 4×8 | 12 | 16 | 16 |
| 4×9 | 15 | – | – |
| 4×10 | 16 | 20 | 20 |
| 4×11 | 17 | – | – |
| 4×12 | 19 | 24 | 24 |
| 5×5 | 10 | 10 | 10 |
| 5×6 | 12 | – | – |
| 5×7 | 14 | – | – |
| 5×8 | 16 | – | – |
| 5×9 | 18 | – | – |
| 5×10 | 20 | 20 | 20 |
| 5×11 | 22 | – | – |
| 5×12 | 24 | – | – |
| 6×6 | 12 | 12 | 18 |
| 6×7 | 16 | – | – |
| 6×8 | 18 | 24 | 24 |
| 6×9 | 18 | 18 | 18 |
| 6×10 | 22 | 30 | 30 |
| 6×11 | 24 | – | – |
| 6×12 | 24 | 24 | 36 |
| 7×7 | 19 | 21 | 21 |
| 7×8 | 21 | – | – |
| 7×9 | 24 | – | – |
| 7×10 | 27 | – | – |
| 7×11 | 28 | – | – |
| 7×12 | 32 | – | – |
| 8×8 | 24 | 24 | 32 |
| 8×9 | 27 | – | – |
| 8×10 | 30 | 40 | 40 |
| 8×11 | 33 | – | – |
| 8×12 | 36 | 48 | 48 |
| 9×9 | 27 | 27 | 36 |
| 9×10 | 33 | – | – |
| 9×11 | 36 | – | – |
| 9×12 | 36 | 36 | 36 |
| 10×10 | 37 | 40 | 50 |
| 10×11 | 40 | – | – |
| 10×12 | 44 | 60 | 60 |
| 11×11 | 44 | 44 | 55 |
| 11×12 | 48 | – | – |
| 12×12 | 48 | 48 | 72 |

3D table: Y = 2-d kernel exists, . = none, for c from b to 9.

| a,b | c values | result |
|---|---|---|
| 3,3 | 3 to 9 | Y Y Y Y Y Y Y |
| 3,4 | 4 to 9 | . . Y . . Y |
| 3,5 | 5 to 9 | . Y . . Y |
| 3,6 | 6 to 9 | Y Y Y Y |
| 3,7 | 7 to 9 | . . Y |
| 3,8 | 8, 9 | . Y |
| 3,9 | 9 | Y |
| 4,4 | 4 to 9 | Y . Y . Y Y |
| 4,5 | 5 to 9 | Y . . . . |
| 4,6 | 6 to 9 | Y . Y Y |
| 4,7 | 7 to 9 | Y . . |
| 4,8 | 8, 9 | Y Y |
| 4,9 | 9 | Y |
| 5,5 | 5 to 9 | Y Y Y Y Y |
| 5,6 | 6 to 9 | Y . . Y |
| 5,7 | 7 to 9 | . . . |
| 5,8 | 8, 9 | Y . |
| 5,9 | 9 | Y |
| 6,6 | 6 to 9 | Y Y Y Y |
| 6,7 | 7 to 9 | Y . Y |
| 6,8 | 8, 9 | Y Y |
| 6,9 | 9 | Y |
| 7,7 | 7 to 9 | Y Y Y |
| 7,8 | 8, 9 | Y . |
| 7,9 | 9 | Y |
| 8,8 | 8, 9 | Y Y |
| 8,9 | 9 | Y |
| 9,9 | 9 | Y |

Why (3, 7, 7) has no kernel:
- By P5 and P6, a kernel would need 3 | 7.
- Layering also fails: the 14 2-d kernels of C_7 □ C_7 have a disjointness graph with closed walks of lengths {2, 4, 6, 7, 8, 9} only, so none of length 3 or 5. C_3 □ C_7 has no 2-d kernels at all.
- Coverings give nothing: 3 and 7 are prime, so the only proper quotients would use C_1, which is not a cycle.
- In 3D the covering argument only gives existence when gcd(a, b, c) > 1, via the sum construction. That condition is far from necessary.

Literature:
- Bednarz, Włoch, "On (2-d)-kernels in the cartesian product of graphs", Ann. UMCS Sect. A 70(2) (2016) 1 to 8, doi 10.17951/a.2016.70.2.1. Open-access PDF: https://journals.umcs.pl/a/article/download/4513/3256.
  - Closest prior work. Same definition as ours (independent and 2-dominating), and × is the Cartesian product (checked in the PDF by the coordinating session).
  - Thm 2.1: products of bipartite graphs have two disjoint (2-d)-kernels (correct).
  - Thm 2.5, verbatim: "Let n, m ≥ 3 be integers. A graph Cn × Cm has a (2 − d)-kernel if and only if n and m are even or n = m." False: C_3 □ C_6 has 6 (coordinator_check.txt).
  - Cor 2.6, verbatim: "If m, n are even, then σ(2−d)(Cn × Cm) = 2. If n is odd, then σ(2−d)(Cn × Cn) = 2n." False: C_6 □ C_6 has 8, C_9 □ C_9 has 24.
  - The proof assumes each copy of C_m holds an MIS of size ⌊m/2⌋.
- Works citing it: 11 entries from OpenAlex, checked by title and abstract. None revisits C_m □ C_n or corrects Thm 2.5.
  - **P. Bednarz, "On (2-d)-kernels in the tensor product of graphs", Symmetry 13 (2021) 230, doi 10.3390/sym13020230.** Read 2026-10-29; PDF and text in references/papers/bednarz-2021-symmetry-tensor.{pdf,txt}.
    - Thm 6(ii): C_n × C_m (tensor) has a 2-d kernel for all n, m ≥ 3 (existence only).
    - Thm 9: σ(C_n × C_3) = 3 + P(n). Brute force agrees for n from 3 to 12.
    - No count for C_n × C_m with m ≥ 4, so no count for odd squares beyond n = 3. Since C_3 × C_3 ≅ C_3 □ C_3, Thm 9 gives σ = 6 there, which agrees with our 2P(3).
    - Cites the 2016 Cartesian paper only as "some results were obtained in [23]". No correction of Thm 2.5.
    - Verdict: does not contain our 2D classification, existence criterion or count.
  - The others are about other objects: Bednarz–Paja 2021 (generalised Petersen graphs); Michalski–Bednarz 2021 (corona and G-join); Michalski–Włoch 2020; Michalski et al. 2022; Kosiorowska et al. 2023 (two papers); Bednarz–Pirga 2024; U. Bednarz 2020 and 2021 ((1,1,2)-kernels).
- Włoch, Australas. J. Combin. 53 (2012) 273 to 284: origin of the notion. Not re-read.
- γ₂ of tori: "Chen–Zhang (2019)" not found. Leads, none verified:
  - Shaheen 2009 (bounds only);
  - a ResearchGate item, "On the 2-domination number of Cartesian product of two cycles" (267184321), said to cover m = 3 to 7; the page is blocked, so authors and year are unverified;
  - Garzón, Martínez, Moreno, Puertas 2022 (cylinders);
  - Rao–Talon 2019 (planar grids).
  So the γ₂ table is not checked against literature. Our γ₂(C_3 □ C_n) values fit n + [3 ∤ n] for n ≤ 12.
- i₂ of tori: nothing found. Shaheen's paper on toroidal digraphs covers ordinary independent domination, not this.
- Fall colourings: Dunbar et al. 2000 and Lyle, DAM 157 (2009). No statement about C_b □ C_c found, so P6 may or may not be known.

Novelty verdict: the 2D results correct a published false theorem. Bednarz 2021 (read 2026-10-29) does not contain them; only the C_3 × C_3 = C_3 □ C_3 case overlaps. Still to do: a Google Scholar "cited by" search on Bednarz–Włoch 2016. Nothing found contains the 3D results (P5, P6, the a = 3 criterion, the exact c-sets).

## Cross-checks
- 2D: the theorem, the transfer digraph (m ≤ 20), SAT existence (456 cases), SAT enumeration (95 tori), SAT-free brute force (mn ≤ 64), and the coordinating session's own SAT enumeration (m ≤ 10, n ≤ 12) all agree.
- Sizes: the closed forms, exact MILP and SAT with cardinality all agree for m, n ≤ 12.
- Constructions: checked by the definition, and covering lifts of SAT-found kernels: no failures.
- 3D: the SAT table and the layer transfer agree on the 7 (a, b) cases. The a = 3 row, P5 with P6, and a separate fall-colouring SAT check (b, c ≤ 24) agree. P6 agrees with exhaustive enumeration of fall 3-colourings (13 tori).

## Problems / disagreements
- The orchestrator's notes are consistent with what was found. Two remarks:
  - The Wielandt-type bound is unnecessary in 2D, because every SCC is a simple cycle. In 3D exact repeats are detected instead of assuming a bound.
  - p = 2 needs no special case: the 2-cycle multigraph gives the checkerboard directly.
- The published literature (Bednarz–Włoch 2016, Thm 2.5 and Cor 2.6) is contradicted by counterexamples checked by the definition, SAT, brute force, and an independent SAT encoding.
- Bednarz 2021 was unreadable here at the time; read on 2026-10-29, see Literature.
- The Chen–Zhang γ₂ values were not found.
- The (4,6) layer transfer exceeded the 3 GB cap.
- Process slip: in one api.unpaywall.org query (looking for an open-access copy of Bednarz 2021), the W3 agent passed Sid's email address as the required parameter. It should not have. It was the only such use.
- An automated MDPI download was blocked by the permission system. It was not retried.
- Process note: the subagent harness refused to let the W3 agent write this file, so the coordinating session saved it from the agent's report.

## Next
1. Sid reads Bednarz, Symmetry 13 (2021) 230, and runs a Google Scholar "cited by" search on Bednarz–Włoch 2016 to see if anyone has noted the error.
2. If the results are new, write P1, P2, the count, P5 and P6 as a short LaTeX note in latex/, framed as a correction of Thm 2.5.
3. 3D: prove or refute "kernel ⇒ some pairwise gcd > 1". Understand the non-layered kernels of C_4 □ C_4 □ C_c for odd c ≥ 9.
4. Only if it serves A4: check whether any of this transfers to kernels of orientations. Expected not to.

## Round 2 addendum (2026-10-29): proof audit, grid-quotient form, novelty search

Proof audit (main session, by hand):
- P1 (line lemma), both directions: correct for m, n ≥ 3.
- P2, Step 2 written out. Let R_t have points p_i, gaps g_i, next-row offsets e_i, previous-row offsets b_i = g_i − e_i. Then R_{t+1} has gaps G_i = b_i + e_{i+1}, and the offset of R_t inside gap i of R_{t+1} is again b_i. So going down one row, b stays fixed and e shifts by one index. Every row is an MIS, so G ≤ 3 for every row, hence (e_j, b_i) ≠ (2, 2) for all i, j. Then e ≡ 1 (R_{t+1} = R_t + 1) or b ≡ 1 (R_{t+1} = R_t − 1), and the same holds for every later row. Correct.
- Wrap-around, d = 1 non-existence, count with the two checkerboard coincidences: correct.
- P5 and P6: correct. P6 can be shortened: one column with constant step ε already gives εc ≡ 0 mod 3, so the "every column has the same winding" step is not needed.

Grid-quotient form (sketch proved, computer-verified). Let G = Z²/L, where L avoids ±(1,0), ±(0,1), ±(2,0), ±(0,2), ±(1,1), ±(1,−1), so that Z² → G is a covering of simple 4-regular graphs. Put d_± = gcd{y ∓ x : (x, y) ∈ L}. Then the 2-d kernels of G are exactly the images of the L-invariant diagonal sets {y ∓ x ∈ K}, and
  σ(G) = P(d_+) + P(d_−) − 2·[d_+ and d_− both even],   P = Perrin, P(1) = 0.
Proof: P4 in both directions (a covering preserves independence and S-neighbour counts), then P1 and P2 on Z² with bi-infinite rows.
- C_m □ C_n: d_+ = d_− = gcd(m, n). This gives the main theorem.
- Tensor C_m × C_n (each component is a grid quotient via i = u + v, j = u − v):
  - m, n odd: P(m) + P(n);
  - m odd, n even: P(2m) + P(n) − 2;
  - both even: (P(m) + P(n) − 2)².
  This contains Bednarz 2021, Thm 9 (m = 3), as the case m = 3.
- Circulant C_N(a, b), connected, simple, 4-regular: d_± = gcd(N, a ± b). So it has a 2-d kernel iff gcd(N, a + b) > 1 or gcd(N, a − b) > 1.
- Evidence: grid_quotient_check.py: `64 30` → grid_quotient_check.txt. Tensor: 49 cases with mn ≤ 64, 0 disagreements. Circulants: 798 cases with N ≤ 30, 0 disagreements. An earlier, larger tensor run was stopped part way (grid_quotient_check_partial_tensor.txt: 49 more cases up to C4 x C21, 0 disagreements).

Novelty search (2026-10-29):
- Bednarz 2021 (tensor): read; see Literature above.
- Its 10 OpenAlex citers, screened by abstract: none on Cartesian products of cycles or grid quotients.
- Bednarz, Michalski, Paja, Opuscula Math. 46(2) (2026) 139 to 152: existence of independent (1,1)-dominating sets (= 2-d kernels) in tensor and strong products, existence only. It cites the 2016 paper with no correction, so the error was still uncorrected in 2026. Alias to search for: "independent (1,1)-dominating set" (Hedetniemi et al. 2008).
- zbMATH 1352.05159 (the 2016 paper): summary only, no critical review.
- Web searches for independent 2-domination, 2-d kernels, (1,1)-domination and idomatic partitions of tori, grids and circulants: nothing found that classifies or counts them.
- Fall colourings: Kaul and Mitillos (Graphs Combin. 2019) give 3 ∈ Fall(G) and H 3-colourable ⇒ G □ H fall 3-colourable, which is the "if" direction of P6. The "only if" direction (rigidity) was not found. They note that C5 □ C5 is fall 5-colourable although C5 is not, so a converse is not automatic.
- Not done: Google Scholar lists (MDPI and Scholar block automated access), MathSciNet, and the 5 Scholar citers of Bednarz 2021 that are missing from OpenAlex. Semantic Scholar rate-limited the query.
- Formal write-up of the grid-quotient theorem and its three corollaries (tori, tensor products, circulants): latex/2-d-kernels-grid-quotients.tex → latex/_build/2-d-kernels-grid-quotients.pdf (23 pages, every step written out). It now also contains the 3D results: the triangle reduction (P5), a full classification of fall 3-colourings of C_b □ C_c (P6, strengthened: every fall 3-colouring has the form εy + g(z) or h(y) + εz), their count 2χ(c)[3|b] + 2χ(b)[3|c] − 12[3|b and 3|c] with χ(k) = 2^k + 2(−1)^k, and hence σ(C_3 □ C_b □ C_c). Checked by threed_check.py `9` → threed_check.txt: 28 tori with 3 ≤ b ≤ c ≤ 9, 0 disagreements, every kernel has one vertex per triangle fibre.
