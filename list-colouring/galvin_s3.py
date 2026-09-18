"""Cross-check: build Galvin's own orientation of S_3 and test both methods on it.

S_3 = L(K_{3,3}) is the Dinitz graph for n = 3.  Galvin's theorem gives
chi_ell(S_3) = 3, via an orientation with d+ = 2 everywhere that is kernel-perfect.
So if AT(S_3) = 4, the claim "kernel-perfect implies EE != EO" that I put in the
notes must be wrong.  Settle it by computing both on the same orientation.
"""
from alontarsi import euler_diff
from galvin import has_kernel
pc = int.bit_count

L = [[1, 2, 3],
     [3, 1, 2],
     [2, 3, 1]]
idx = {(i, j): 3 * i + j for i in range(3) for j in range(3)}
n = 9
out = [0] * n
adj = [0] * n
for i in range(3):
    for j in range(3):
        v = idx[(i, j)]
        for j2 in range(3):                       # same row
            if j2 == j: continue
            u = idx[(i, j2)]
            adj[v] |= 1 << u
            if L[i][j] < L[i][j2]:                # row: smaller points to larger
                out[v] |= 1 << u
        for i2 in range(3):                       # same column
            if i2 == i: continue
            u = idx[(i2, j)]
            adj[v] |= 1 << u
            if L[i][j] > L[i2][j]:                # column: the other way around
                out[v] |= 1 << u

print("Galvin's orientation of S_3:")
print("  out-degrees:", [pc(x) for x in out], " (Lemma 1 needs all = 2)")
print("  degrees:    ", [pc(x) for x in adj])
kp = all(has_kernel(out, adj, S) for S in range(1, 1 << n))
print(f"  kernel-perfect: {kp}   -> Lemma 1 gives chi_ell(S_3) <= 3")
d = euler_diff(out, n)
print(f"  EE - EO = {d}   -> Alon-Tarsi {'applies' if d else 'says NOTHING'}")
print()
print("conclusion:",
      "kernel-perfect does NOT imply EE != EO; the two methods are incomparable"
      if kp and d == 0 else "the two agree here, so AT(S_3)=4 needs re-checking")
