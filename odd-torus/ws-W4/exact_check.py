# W4: exact finite check. For every odd n in [3, N] and every w off the cycle of e, compute
#   c(a,b) = tr(X T^a D_i T^b)  exactly in Z[omega]/3  (X = G for the column edge, H for the row edge)
# and report how many vanish. Exact integer arithmetic (flint fmpz_mat), no floating point.
# Usage: python exact_check.py N
import sys, time
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')
import flint
from fractions import Fraction as F
from tmlib import build, powers

N = int(sys.argv[1]) if len(sys.argv) > 1 else 101
t0 = time.time()
B = build(5)
L = N - 1                         # max exponent needed (row edge: a+b = n-1)
Tp = powers(B['T'], L)
n_st = 30
lines = []


def log(s):
    print(s, flush=True)
    lines.append(s)


def flat(M, transpose=False):
    out0, out1 = [], []
    for p in range(n_st):
        for q in range(n_st):
            i, j = (q, p) if transpose else (p, q)
            out0.append(M.A0[i, j]); out1.append(M.A1[i, j])
    return out0, out1


# V[(p,q), b] = T^b[q,p]
V0 = flint.fmpz_mat(n_st * n_st, L + 1)
V1 = flint.fmpz_mat(n_st * n_st, L + 1)
for b in range(L + 1):
    f0, f1 = flat(Tp[b], transpose=True)
    for k in range(n_st * n_st):
        V0[k, b] = f0[k]; V1[k, b] = f1[k]
log(f"built T^b for b <= {L}  ({time.time()-t0:.1f}s)")

cases = [('col', i) for i in range(5)] + [('row', i) for i in range(1, 5)]
total = 0
zeros = []
nonint = []
samples = {}
for et, i in cases:
    X = B['G'] if et == 'col' else B['H']
    den = X.den
    U0 = flint.fmpz_mat(L + 1, n_st * n_st)
    U1 = flint.fmpz_mat(L + 1, n_st * n_st)
    for a in range(L + 1):
        M = X @ Tp[a] @ B['D'][i]
        assert M.den == den
        f0, f1 = flat(M)
        for k in range(n_st * n_st):
            U0[a, k] = f0[k]; U1[a, k] = f1[k]
    P = U0 * V0
    Q = U1 * V1
    C0 = P - Q
    C1 = U0 * V1 + U1 * V0 - Q          # C[a,b] = den * c(a,b) = C0 + C1 w
    cnt = 0
    for n in range(3, N + 1, 2):
        s = n - 2 if et == 'col' else n - 1
        for a in range(s + 1):
            b = s - a
            z = (int(C0[a, b]), int(C1[a, b]))
            cnt += 1
            if z[1] != 0 or z[0] % den != 0:
                nonint.append((et, i, n, a, b))
            if z == (0, 0):
                zeros.append((et, i, n, a, b))
            if n in (3, 5, 7):
                samples.setdefault((et, i, n), []).append((a, F(z[0], den), F(z[1], den)))
    total += cnt
    log(f"{et} i={i}: checked {cnt} (n,j) pairs for odd n in [3,{N}], zeros: {sum(1 for zz in zeros if zz[:2]==(et,i))}  ({time.time()-t0:.1f}s)")
log(f"TOTAL checked {total}, exact zeros: {zeros if zeros else 'none'}")
log(f"values that are not rational integers (should be none, c_w is a coefficient of an integer polynomial): {nonint if nonint else 'none'}")
log("sample exact values c = x + y*w (n = 3, 5), j = a+1:")
for k, v in samples.items():
    if k[2] in (3, 5):
        log(f"  {k}: " + "; ".join(f"j={a+1}: {x} + {y}w" for a, x, y in v))
open(f'/home/sid/work/gt/odd-torus/ws-W4/exact_check_N{N}.txt', 'w').write("\n".join(lines) + "\n")
