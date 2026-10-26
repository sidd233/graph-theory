# odd-torus workstream status

Updated 2026-10-26. One line per workstream: state, headline result, blocking issue.

- W1 (strip-lemma formula): DONE. c_S = −(g/9)·μ_k^(m−1)·(ω^s + (−1)^m ω^(2s)) PROVED for all m ≥ 2 (μ_3 = 0), 3 exact methods agree for m from 2 to 11; odd m, k ∈ {1,2}, s ≢ 0 gives c_S = ±3^((m−1)/2) ≠ 0 for every S. Blocking: none. Caution: Case A needs r' ≠ r (s ≡ r' − r).
- W2 (bad 3-list assignment search): RUNNING. No result yet. Blocking: none.
- W3 (2-d kernels in tori): RUNNING. No result yet. Blocking: none.
- W4 (edge deletion, m = 5, all odd n): RUNNING. No result yet. Blocking: none.
- W5 (reconcile old odd-torus code): DONE. All orientation counts (148, 2116, 33028, 525316; 143224) and kernel-perfect counts (12, 0, 0, 12; 0) reproduced by independent code; the 12 for C₃ □ C₉ are exactly the Latin lifts. Correction: Latin lifts on C₃ □ C_{3k} fail exactly for k ≡ 2 (mod 4), not for all even k (C₃ □ C₁₂ is kernel-perfect). Two lines of old bounded_13.out are invalid (N > 127 overflow). Blocking: none.
- W6 (verify [P]): WAITING. Blocking: [P] is not yet in references/papers/.
