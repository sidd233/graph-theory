# W4: Edge deletion for m = 5, all odd n

## Results
- [PROVED, computer-assisted] For every odd n ≥ 3, every edge e of G = C₅ □ Cₙ and every vertex w not on the 5-cycle (column edge) or n-cycle (row edge) through e, the coefficient c_w = [x_w ∏_{v≠w} x_v²] P_{G−e} is a nonzero integer. Every computational step is exact (integer / Z[ω] arithmetic) or certified (arb/acb ball arithmetic), and is reproduced by the scripts below.
- [PROVED, consequence] So, by the Combinatorial Nullstellensatz, for odd n ≥ 3:
  - C₅ □ Cₙ − e is L-colourable whenever |L(v)| ≥ 3 for v ≠ w and |L(w)| ≥ 2.
  - C₅ □ Cₙ is L-colourable from 3-lists whenever some edge uv has L(u) ∩ L(v) = ∅.
- [PROVED, exact] The undamaged transfer matrix T (30 × 30, entries 0 or sixth roots of unity) is diagonalisable over C.
  - Its minimal polynomial is x·q₁(x)·q₂(x), with q₁ = x⁴ + 10x² + 5 and q₂ = x⁸ + 35x⁶ + 110x⁴ + 100x² + 25.
  - The nonzero eigenvalues are ±iλ for 6 values of λ, each with a rank-2 eigenprojector. The kernel has dimension 6.
- [PROVED, certified] The maximal modulus λ₁ ≈ 5.6232076309 is attained only by ±iλ₁.
  - λ₁² = (35 + 13√5 + √(1950 + 870√5))/4 ≈ 31.6204640602.
  - The next modulus is λ₂ = tan(2π/5) = √(5+2√5) ≈ 3.0776835372, so r ≤ 0.5473181393.
  - q₁ has the roots ±i·tan(π/5) and ±i·tan(2π/5).
- [PROVED, exact] Every dominant amplitude is a nonzero element of Q(ν), where ν = iλ₁.
- [PROVED] n₀ = 5. For every odd n ≥ 5 and every admissible w, dominance by ±iλ₁ with certified error bounds proves c_w ≠ 0. At n = 3 the bound covers all but 10 of the 22 positions; those 10 are exact (±9, ±18).
- [COMPUTER-VERIFIED, odd n from 3 to 201] c_w ≠ 0 exactly for all 91,300 (edge, w, n) cases. This is redundant but independent.
- [PROVED, computer-assisted, optional part] The same statement holds for C₇ □ Cₙ, all odd n ≥ 3.
  - T is 126 × 126 and diagonalisable. Its minimal polynomial is x times the product of the 4 distinct nonzero factors (degree 50).
  - There are 25 pairs ±iλ. The dominant pair is unique: λ₁ ≈ 15.1341506816, λ₂ ≈ 10.5906683275, r ≤ 0.69978610.
  - Dominance covers n ≥ 11. All leftovers (n ≤ 9) are checked exactly.

## The argument, as a proof

**Conventions.** These are those of coeff.py.
- Vertex (r, c), with r ∈ Z₅ the row and c ∈ Zₙ the column.
- Arcs are (r,c) → (r+1,c) and (r,c) → (r,c+1).
- Changing the orientation only flips the sign of P, so it does not affect whether c_w is zero.
- Translations preserve the orientation, so WLOG e = (0,0)(1,0) (column edge) or e = (0,0)(0,1) (row edge).
- "Off the cycle" means j ≠ 0 for a column edge and i ≠ 0 for a row edge.

**Step 0 (coefficient formula).**
- c_w = [∏ x_v²](x_w P_{G−e}), and deg(x_w P_{G−e}) = 2N.
- Apply Lasoń / Karasev–Petrov with every A_v = {1, ω, ω²}. Then N_v(a) = 3a² = 3/a.
- This gives c_w = Σ_φ φ(w) ∏_v (φ(v)/3) ∏_{u→v, uv≠e} (φ(u) − φ(v)).

**Step 1 (transfer matrices).**
- A column state is s ∈ {0,1,2}⁵, meaning colours ω^{s_r}.
- W(s) = ∏_r (ω^{s_r}/3) ∏_r (ω^{s_r} − ω^{s_{r+1}}), and R(s,t) = ∏_r (ω^{s_r} − ω^{t_r}).
- Matrices:
  - T = W·R on the 30 proper states.
  - E = W_e·R, where W_e omits the factor for e (48 × 30).
  - T′ = W·R (30 × 48).
  - G = T′E (30 × 30).
  - H = W·R_e, where R_e omits the row-0 factor (30 × 30).
  - D_i = diag(ω^{s_i}).
- Grouping the factors of Step 0 column by column gives:
  - Column edge, w = (i,j), 1 ≤ j ≤ n−1: c_w = c(a,b) := tr(G T^a D_i T^b) with a = j−1, b = n−1−j, so a + b = n−2 is odd.
  - Row edge, i ≠ 0, j ∈ {1,…,n} (j = n is column 0): c_w = tr(H T^a D_i T^b) with a = j−1, b = n−j, so a + b = n−1 is even and ≥ 2.

**Step 2 (exact spectral facts).**
- (E1) The characteristic polynomial of the 60 × 60 integer realification of T is x¹² q₁⁴ q₂⁴.
- (E2) T q₁(T) q₂(T) = 0 exactly, and q₁(T) q₂(T) ≠ 0.
- (E3) q₁q₂ is squarefree with nonzero constant term.
  - So μ = x q₁ q₂ has 13 simple roots, and T = Σ_z z P_z with P_z = μ(T)/((T − z) μ′(z)) (Lagrange).
  - Hence T^a = Σ_{z≠0} z^a P_z for every a ≥ 1. Call this (∗).
- (E4) q₁ = h₁(x²) and q₂ = h₂(x²), where h₁ and h₂ have only negative real roots. So every nonzero root is ±iλ with λ > 0.
  - q₂ = F(x²) with F(y) = y⁴ + 35y³ + 110y² + 100y + 25, which is irreducible over Q.
- Certified with acb_poly.roots at 300 bits:
  - The top two roots are ±iλ₁, λ₁ ∈ [5.62320763089573111160570889823 ± 4.3e-30].
  - Every other root has modulus ≤ 3.07768353717525340.
  - The projector ranks are 6 for z = 0 and 2 for each nonzero z.

**Step 3 (expansions).** Let t_z = |z|/λ₁, so t_{±ν} = 1 and t_z ≤ r otherwise. Let X = G or H.
- (I) For a, b ≥ 1: c = Σ A_{zz′} z^a z′^b, with A_{zz′} = tr(X P_z D_i P_{z′}).
- (II) For b fixed and a ≥ 1: c = Σ z^a β_z(b), with β_z(b) = tr(P_z D_i T^b X).
- (III) For a fixed and b ≥ 1: c = Σ z^b γ_z(a), with γ_z(a) = tr(P_z X T^a D_i).
- The dominant part of (I) is ν^{a+b} B(a mod 2, b mod 2), where B(p,q) = tr(X Q_p D_i Q_q), Q₀ = P_ν + P_{−ν} and Q₁ = P_ν − P_{−ν}.
- Only the parity classes (0,1) and (1,0) occur for a column edge, and (0,0) and (1,1) for a row edge.

**Step 4 (B ≠ 0, exactly).**
- Let y = ν² and g(x) = μ(x)/(x² − y), which is odd. Then:
  - Q₀ = T g(T)/(ν g(ν)) and Q₁ = g(T)/g(ν).
  - g(ν) = ν (y² + 10y + 5) F′(y).
- So every B is a Q(y)-combination of the integers c(k,l) with k, l ≤ 12, divided by y^ε ν^δ (y²+10y+5)² F′(y)². Reduce the numerator β modulo F (dominant_exact.py).
- Column edge, B(0,1) = −B(1,0) = β/ν:
  - i = 0, 1: β = (38y³ + 1034y² + 2435y + 920)/3875, B(0,1) ≈ 11.1808050974·i.
  - i = 2, 4: β = −(41y³ + 711y² + 1685y + 805)/3875, B(0,1) ≈ −29.2717277665·i.
  - i = 3: β = (6y³ − 646y² − 1500y − 230)/3875, B(0,1) ≈ 36.1818453383·i.
- Row edge:
  - i = 1: B(0,0) = β/y with β = (118y³ + 3560y² + 7390y + 2400)/3875, B(0,0) ≈ 3.2846425606. B(1,1) = (96y³ + 3242y² + 7000y + 2210)/3875 ≈ −3.2846425606. Row i = 4 gives the negatives.
  - i = 2: B(0,0) ≈ −5.3146633039 and B(1,1) ≈ 5.3146633039 (β in dominant_exact_output.txt). Row i = 3 gives the negatives.
- Each β is a nonzero polynomial of degree < 4 and F is irreducible of degree 4, so β(y) ≠ 0. These values match the independent ball computations.

**Step 5 (certified tail bounds).**
- Region I (a, b ≥ K): |c/ν^{a+b} − B| ≤ E_K := Σ over pairs (z,z′) not both dominant of |A_{zz′}| t_z^K t_{z′}^K. If E_K < |B|, then c ≠ 0 for all a, b ≥ K.
- Region II (b < K fixed): |c/ν^a − (β_ν(b) ± β_{−ν}(b))| ≤ Σ_{z≠±ν} |β_z(b)| t_z^a, which decreases in a. This gives a threshold a₀(b).
- Region III (a < K fixed): the same with γ, giving b₀(a).

| edge, row i | min abs(B) | K | E_K | a₀(b) = b₀(a), for 0..K−1 | leftover (a,b) |
|---|---|---|---|---|---|
| col, i = 0, 1 | 11.1808051 | 3 | 7.7184568 | 3, 2, 3 | (0,1), (1,0) [n = 3] |
| col, i = 2, 4 | 29.2717278 | 1 | 26.7913384 | 1 | none |
| col, i = 3 | 36.1818453 | 1 | 26.7913384 | 1 | none |
| row, i = 1, 4 | 3.2846426 | 2 | 2.6412125 | 4, 3 | (0,2), (1,1), (2,0) [n = 3] |
| row, i = 2, 3 | 5.3146633 | 2 | 2.6412125 | 2, 1 | none |

The script also confirms by enumeration that the three regions together cover every admissible (a,b) except the leftovers.

**Step 6 (exact leftovers).**
- Column edge, i = 0, 1: −9 and 9.
- Row edge, i = 1: −9, 18, −9. Row edge, i = 4: 9, −18, 9.
- All are nonzero, which completes the proof. ∎

**Growth.** In Region I, |c_w(n)| ≥ λ₁^{n−2}(|B| − E_K) for a column edge and λ₁^{n−1}(|B| − E_K) for a row edge.

## Evidence
All commands in odd-torus/ws-W4 with /home/sid/work/gt/odd-torus/env/bin/python.
- `tmlib.py`: library with exact Z[ω] matrices and the Step 1 formulas.
- `spectral.py`, command `python spectral.py`. Key lines:
  - (E1) to (E4) all print True.
  - `l1 in [5.62320763089573111160570889823 +/- 4.23e-30]`
  - `|other roots| <= 3.0776835371752534026`
  - `r <= 0.54731813925302337045`
  - `ranks [6, 2, ..., 2]`
- `prove_m5.py`, command `python prove_m5.py` (4 s), output `prove_m5_output.txt`. Key lines:
  - the table in Step 5
  - validation of the expansion against exact values: 42 (column) / 49 (row) pairs
  - `N_needed = 3`
- `dominant_exact.py` (1 s), output `dominant_exact_output.txt`: F irreducible over Q; every β mod F is nonzero.
- `exact_check.py 201` (21 s), output `exact_check_N201.txt`:
  - `TOTAL checked 91300, exact zeros: none`
  - `values that are not rational integers: none`
- `prove_gen.py 5`, output `prove_gen_m5_output.txt`: identical K, a₀ and leftovers, using an independent amplitude route (the exact moment matrix C[k,l] = c(k,l)).
- `prove_gen.py 7 2000` (290 s), output `prove_gen_m7_output.txt`:
  - Realified charpoly: x²⁸ (deg 24)⁴ (x²+12)⁴ (deg 18)⁴ (x⁶+21x⁴+35x²+7)⁸.
  - T q(T) = 0, so the nilpotent part is trivial.
  - λ₁ = 15.13415068159166935 (from the degree-24 factor); other moduli ≤ 10.5906683275 (from the degree-18 factor).
  - K and leftovers per case:
    - col i = 0, 1: K = 6, n ≤ 9
    - col i = 2, 6: K = 3, n ≤ 5
    - col i = 3, 4, 5: K = 2, n ≤ 3
    - row i = 1, 6: K = 4, n ≤ 7
    - row i = 2, 5: K = 3, n ≤ 5
    - row i = 3, 4: K = 2, n ≤ 3
  - Every leftover value is an exact nonzero integer.

## Cross-checks
- **Orchestrator's coeff_mod** (copied as `orch_exactp.py`: direct 243-state product mod p = 1000003), `crosscheck.py 5 3,5,7,9,11` → `crosscheck_output.txt`: 22, 40, 58, 76 and 94 positions agree, 0 disagreements, 0 zeros.
- **Direct expansion of ∏(x_u − x_v)**, a signed edge-endpoint DP with no colourings, `brute_dp.py`: exact agreement, sign included, with the transfer values for:
  - C₅ □ Cₙ, n = 3, 5, 7, 9, 11, 13: 22, 40, 58, 76, 94, 112 positions
  - C₇ □ C₃, C₇ □ C₅, C₇ □ C₇: 32, 58, 84 positions
  - C₃ □ C₅: 22 positions
- **Isomorphism:** C₃ □ C₅ and C₅ □ C₃ give the same multisets of abs(c_w), with column and row edges swapped.
- **Expansion vs exact:** the certified spectral sums contain the exact c(a,b) for all tested pairs (n ≤ 15 in prove_m5; n ≤ 25 in prove_gen, for both m = 5 and m = 7).
- **Rerun by the coordinating session:** spectral.py and dominant_exact.py reproduce the lines above; prove_m5.py reproduces prove_m5_output.txt exactly (apart from timing); crosscheck.py 5 5,7 gives 40/40 and 58/58 agreement with 0 zeros.

## Problems / disagreements
- No disagreements with the orchestrator's notes.
  - Each m = 5 eigenvalue has multiplicity 2 (for m = 7, multiplicity 2, or 4 for the tan(kπ/7) factor). T is diagonalisable, so this is harmless.
  - The dominant modulus is attained only by ±iλ₁, so there is no oscillation problem.
  - The nilpotent part is trivial, so the expansions hold for all exponents ≥ 1.
- n₀ is tiny (5 for m = 5, 11 for m = 7). The gap is large and the amplitudes are of moderate size.
- The story says the m = 3 edge-deletion theorem has "an exact formula (powers of 3)". For C₃ □ C₅ minus a column (triangle) edge, abs(c_w) ∈ {9, 15, 18, 30}; minus a row edge, abs(c_w) ∈ {9, 18}. Confirmed by the coordinating session with the orchestrator's own coeff.py. So c_w is not always ± a power of 3; check this against the partner's formula when [P] arrives (W6).
- Process note: the subagent harness refused to let the W4 agent write this file, so the coordinating session saved it from the agent's report.

## Next
1. Apply the same machinery to the m = 5 odd strip lemma (item C2). The trace becomes a bilinear form u_Sᵀ T^k v_S, so only a single-sided dominance argument is needed. The moment-matrix code carries over.
2. Look for the structure behind the spectrum. The roots ±i·tan(kπ/m) appear for m = 5 and m = 7. A symmetry decomposition (rotation, reflection, colour shift) might give a proof uniform in m.
3. Run m = 9 (510 states) only if a pattern in m is wanted. It is feasible.
