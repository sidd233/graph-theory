# W1: Strip-lemma formula verification

## Results
- [PROVED, every m ≥ 2, every end multiset S] c_S = −(g/9)·μ_k^(m−1)·(ω^s + (−1)^m ω^(2s)), with μ_k = ω^(2k) − ω^k. This gives μ_0 = 0, μ_1 = −i√3 and μ_2 = i√3, as in the note, and also μ_3 = 0. The formula is exactly right, signed, for the stated orientation.
- [COMPUTER-VERIFIED, m from 2 to 11, all 50 S per m, 500 coefficients] The signed formula has 0 mismatches against three independent exact computations, all in exact Q(ω) arithmetic with no floating point.
- [PROVED] c_S depends only on (m, k, s).
  - m odd, k ∈ {1,2}: c_S is (−3)^((m−1)/2) for s = 1, −(−3)^((m−1)/2) for s = 2, and 0 for s = 0.
  - m even, k = 1: c_S = −(−3)^((m−2)/2)·(ω^s + ω^(2s)). That is −2·(−3)^((m−2)/2) for s = 0 and (−3)^((m−2)/2) for s ≠ 0. For k = 2 the value is minus the k = 1 value.
  - k ∈ {0,3}: c_S = 0.
- [PROVED] What the m = 3 proof needs holds for **every** S of that type individually, for every odd m ≥ 3: if k ∈ {1,2} and s ≢ 0 then c_S = ±3^((m−1)/2) ≠ 0.
- [PROVED] c_S = 0 exactly when k ∈ {0,3} (any m), or m is odd and s ≡ 0. For m even and k ∈ {1,2}, nothing vanishes, including s ≡ 0.
- [PROVED, and COMPUTER-VERIFIED for m from 2 to 11] Symmetries:
  - Column reflection c ↦ m+1−c maps k ↦ 3−k, keeps s, and gives c_{S'} = (−1)^(m−1)·c_S, because the 3(m−1) row edges reverse. This explains why k = 3 behaves like k = 0 and k = 2 like k = 1.
  - The vanishing at k = 0 does not come from the symmetry. It comes from Σ_d χ(d) = 0 (step 5 of the proof), which makes μ_0 = 0.
  - Row reflection r ↦ −r gives the sign (−1)^m and sends s ↦ −s. A row shift leaves c_S unchanged.

### Comparison table (exact c_S; every S in a class has the same value)

m odd:

| k | s | m=3 | m=5 | m=7 | m=9 | m=11 |
|---|---|---:|---:|---:|---:|---:|
| 0 | any | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | −3 | 9 | −27 | 81 | −243 |
| 1 | 2 | 3 | −9 | 27 | −81 | 243 |
| 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | −3 | 9 | −27 | 81 | −243 |
| 2 | 2 | 3 | −9 | 27 | −81 | 243 |
| 3 | any | 0 | 0 | 0 | 0 | 0 |

m even:

| k | s | m=2 | m=4 | m=6 | m=8 | m=10 |
|---|---|---:|---:|---:|---:|---:|
| 0 | any | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | −2 | 6 | −18 | 54 | −162 |
| 1 | 1, 2 | 1 | −3 | 9 | −27 | 81 |
| 2 | 0 | 2 | −6 | 18 | −54 | 162 |
| 2 | 1, 2 | −1 | 3 | −9 | 27 | −81 |
| 3 | any | 0 | 0 | 0 | 0 | 0 |

### Proof (PROVED)
0. **Reduction.** H_m has 3m column edges and 3(m−1) row edges, so deg P = 6m−3 = Σ t_v. Put Q = P·∏x^μ. Then [∏x^t]P = [∏x²]Q and deg Q = 6m. Use the Lasoń / Karasev–Petrov formula with every A_v = {1, ω, ω²}. Then N_v(a) = 3a² = 3/a, so c_S = 3^(−3m)·Σ_φ P(φ)·∏_v φ(v)^(1+μ(v)).
1. **Column states.** Only colourings that are proper on each column triangle contribute. These are φ(r,c) = ω^(a_c + ε_c·r), with a ∈ Z₃ and ε = ±1: the 6 affine bijections of Z₃.
2. **Column edges.** The product over a column is (1−ω^ε)³ = −ε·g, using (1−ω)² = −3ω, so (1−ω)³ = −g.
3. **Row edges.** If ε_c ≠ ε_(c+1), the maps a+εr and b−εr agree at r ≡ 2ε(b−a). Some row edge then has equal colours at its ends, so the product is 0, and ε is constant along the strip. If ε is the same in both columns, the product is (1−ω^(b−a))³ = g·χ(b−a), with χ(0) = 0, χ(1) = −1, χ(2) = +1.
4. **Vertex weights.** Column c contributes ω^(a·M_c + ε·R_c), where M_c = Σ_r μ(r,c) and R_c = Σ_r r·μ(r,c). Here M_1 = 3−k, M_m = k, every other M_c is 0, and R_1 + R_m ≡ s.
5. **Summation.**
   - c_S = 3^(−3m)·Σ_ε (−εg)^m·g^(m−1)·ω^(εs)·Σ_a ω^(k(a_m−a_1))·∏ χ(a_(c+1) − a_c).
   - Put d_c = a_(c+1) − a_c. The sum over a is 3·(Σ_d χ(d)·ω^(kd))^(m−1) = 3·μ_k^(m−1).
   - The sum over ε is (−1)^m·g^m·(ω^s + (−1)^m·ω^(2s)).
   - With g² = −27, the scalar 3^(1−3m)·(−1)^m·g^(2m−1) equals −g/9. ∎
6. **Integer form.** For k ∈ {1,2}, μ_k² = −3. Also −(g/9)(ω^s − ω^(2s)) = ±1 for s = 1, 2, and −(g/9)·μ_1 = −1. These give the integer values above.

## Evidence
All commands run in odd-torus/ws-W1 with /home/sid/work/gt/odd-torus/env/bin/python.
- script: zomega.py (exact Q(ω) arithmetic), command: `python zomega.py`, output: `zomega self-test ok`
- script: strip_coeff.py, command: `python strip_coeff.py 2 11 3 > strip_coeff_m2-11.txt`, output: 500 integer c_S, and `# method A vs method B mismatches: 0`.
  - Method A: the formula with |A_v| = 3 and the extra factor φ(v)^μ(v).
  - Method B: the formula with |A_v| = t_v + 1, using subsets of the cube roots, 3 random draws per S.
  - Both are 27-state transfers over the columns with open ends.
- script: direct_expand.py, command: `python direct_expand.py 2,3,4,5,6,7,8,9,10,11 > direct_expand_m2-11.txt`, output: 500 lines and `# m=2: sympy expansion agrees with dict expansion on all 50 S`.
  - It expands P with integer dict polynomials and drops monomials with an exponent above 2. This is exact, since multiplying never lowers an exponent.
  - At most 252 monomials survive, so the whole range from 2 to 11 was cheap.
- script: compare.py, command: `python compare.py strip_coeff_m2-11.txt direct_expand_m2-11.txt > compare_m2-11.txt`, output:
  - `transfer (method A, B) vs direct expansion disagreements: 0`
  - `signed mismatches with formula (mu_k = w^2k - w^k, k = 0..3): 0 of 500`
  - `(m,k,s) classes with more than one value of c_S: 0`
  - `symmetry violations ...: 0`
  - `checked 120 end multisets (m odd in [3, 5, 7, 9, 11]), zero coefficients: 0`
- script: proof_checks.py, command: `python proof_checks.py > proof_checks.txt`, output: `all proof step checks passed` (proof steps 1 to 5 checked exactly).

## Cross-checks
- Method B agrees with method A on all 500 cases.
- Direct expansion agrees with method A on all 500 cases, and sympy agrees at m = 2. Direct expansion does not use the coefficient formula at all.
- The proved closed form matches all three computations, signed.
- Rerun by the coordinating session (compare.py on the committed outputs): zero coefficients occur exactly in the classes k ∈ {0,3} (all m) and m odd, k ∈ {1,2}, s ≡ 0.

## Problems / disagreements
- No disagreement with the formula.
- The brief leaves μ_3 undefined. The natural value is μ_3 = ω⁶ − ω³ = 0, which gives c_S = 0 for k = 3, as the data show.
- The sign of c_S depends on the orientation convention. Whether c_S is nonzero does not.
- A caution for the gluing step, Case A of toroidal_grid_story.tex. The strip runs from C₃ (column 1) around to C₀ (column m), so S = {(r,C₀),(r,C₀),(r',C₃)} has k = 2 and s ≡ 2r + r' ≡ r' − r. This is nonzero only if r' ≠ r, so the argument must make sure r' ≠ r. When s ≡ 0 and m is odd, c_S = 0 for every such S.
- Process note: the subagent harness refused to let the W1 agent write this file, so the coordinating session saved it from the agent's report.

## Next
1. Record that the strip lemma (Step 2, [P, Theorem 4]) is now independently PROVED. The remaining unchecked input of the m = 3 proof is [P, Lemma 3.5] (propagation).
2. Check that Case A guarantees r' ≠ r, and that it uses the same orientation and indexing of S as here.
3. For m = 5 (C₅ □ P_m), adapt strip_coeff.py and direct_expand.py. The 6-state affine collapse no longer applies, so a real transfer matrix is needed.
