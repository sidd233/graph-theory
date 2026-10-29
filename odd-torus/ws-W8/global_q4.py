"""W8: is there a 3-list assignment of C5 x Cn (palette 4) that is neither row-constant nor column-constant and in which
EVERY cut is bad? A cut is a trigger (r, j) with L(r,j) != L(r,j+1); its forward window is
(col j+1, col j+2) with the pin at row r, its backward window (col j, col j-1) with the pin at row r
(the backward cut uses alpha' in L(r,j+1) \\ L(r,j); with 4 colours alpha is forced).
Bad windows (pin at row 0, real alpha, all 74 shapes tried): all_q4_stillbad_real.txt.
Pin at row r: rotate rows so that r becomes 0. Run: python global_q4.py"""
import sys
W = set()
for l in open('all_q4_stillbad_real.txt'):
    w = l.split(); W.add((tuple(int(h, 16) for h in w[1:6]), tuple(int(h, 16) for h in w[7:12])))
rot = lambda c, r: tuple(c[(t + r) % 5] for t in range(5))
def bad(a, b, r): return (rot(a, r), rot(b, r)) in W
dom = sorted({rot(c, r) for a, b in W for c in (a, b) for r in range(5)})
print('bad windows', len(W), '; columns that can occur next to a cut:', len(dom))
def trig_ok(cm1, c0, c1, c2):
    # every trigger between c0 and c1 must have both cuts bad
    return all(c0[r] == c1[r] or (bad(c1, c2, r) and bad(c0, cm1, r)) for r in range(5))
def search(n):
    found = []
    seq = []
    def go():
        if len(seq) == n:
            if all(trig_ok(seq[(j - 1) % n], seq[j], seq[(j + 1) % n], seq[(j + 2) % n]) for j in range(n)) \
               and len(set(seq)) > 1 and not all(len(set(c)) == 1 for c in seq):
                found.append(list(seq)); return True
            return False
        for c in dom:
            seq.append(c)
            k = len(seq)
            ok = k < 4 or trig_ok(seq[k - 4], seq[k - 3], seq[k - 2], seq[k - 1])
            if ok and go(): return True
            seq.pop()
        return False
    go(); return found
for n in (5, 7, 9):
    f = search(n)
    print(f'n = {n}:', 'EVADING ASSIGNMENT FOUND' if f else 'none (every assignment that is not row- or column-constant has a good cut)')
    if f: print('  columns (hex lists, rows 0..4):', [[format(x, 'x') for x in c] for c in f[0]])
