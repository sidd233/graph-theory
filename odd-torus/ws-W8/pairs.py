# Can the forward cut (delete j+1, j+2) and the backward cut (delete j, j-1) both be bad?
# A window is (L1, L2) = (column next to the pin, column after it), pin at row 0.
# Forward: L1 = col j+1, L2 = col j+2, alpha in L(0,j) \ L(0,j+1).
# Backward: L1' = col j, L2' = col j-1, alpha' in L(0,j+1) \ L(0,j).
# Both bad needs (colj+1, colj+2) and (colj, colj-1) in the still-bad set, with L(0,j) != L(0,j+1).
# Rows: the backward window is the mirror image; rows keep their indices, so the same set applies.
bad = [tuple(l.split()[1:6]) + tuple(l.split()[7:12]) for l in open('all_q4_stillbad.txt')]
B = {(w[:5], w[5:]) for w in bad}
L1s = {}
for a, b in B: L1s.setdefault(a, []).append(b)
hits = 0
for a, b in B:            # a = col j+1, b = col j+2
    for c, d in B:        # c = col j,   d = col j-1
        if c[0] != a[0]: hits += 1; ex = (d, c, a, b)
print('bad windows', len(B), '; forward+backward both bad (rows 0 differ):', hits)
if hits: print('example cols j-1, j, j+1, j+2:', ex)
