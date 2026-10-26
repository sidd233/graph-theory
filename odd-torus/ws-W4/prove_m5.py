# W4: certified dominance argument for c_w(n) != 0, G = C_5 x C_n minus an edge, n odd.
#
#   column edge e = (0,0)-(1,0), w = (i, j), j != 0:  c(a,b) = tr(G T^a D_i T^b), a = j-1, b = n-1-j, a+b = n-2 odd
#   row edge    e = (0,0)-(0,1), w = (i, j), i != 0:  c(a,b) = tr(H T^a D_i T^b), a = j-1, b = n-j (j=n is column 0), a+b = n-1 even
#
# T diagonalisable (spectral.py), T^a = sum_{z != 0} z^a P_z for a >= 1.  nu = i*l1 dominant, t_z = |z|/l1.
# Region I  (a >= K, b >= K): c/nu^{a+b} = B(a mod 2, b mod 2) + sum_{(z,z') not both dominant} A_{z z'} (z/nu)^a (z'/nu)^b,
#            A_{z z'} = tr(X P_z D P_z'),  B(p,q) = sum_{s,t = +-1} s^p t^q A_{s nu, t nu}.
#            Certified if |B| > sum |A_{zz'}| t_z^K t_z'^K.
# Region II (b < K fixed, a >= 1): c = sum_z z^a beta_z(b), beta_z(b) = tr(P_z D T^b X); certified for a >= a0(b).
# Region III(a < K fixed, b >= 1): c = sum_z z^b gamma_z(a), gamma_z(a) = tr(P_z X T^a D); certified for b >= b0(a).
# Everything else is a finite set of (a,b), i.e. n <= N_needed, checked exactly by exact_check.py.
import sys, time
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')
import flint
from flint import acb, arb, acb_mat
from tmlib import build, powers
from spectral import exact_checks, certified_spectrum, projectors, check_projectors

PREC = 300
out_lines = []


def log(s=""):
    print(s, flush=True)
    out_lines.append(s)


def main(K_max=40, a_max=2000):
    t0 = time.time()
    B = build(5)
    exact_checks(B, log)
    roots = certified_spectrum(B, PREC, log)
    Z, P = projectors(B, roots, PREC)
    ranks = check_projectors(B, Z, P, log)
    flint.ctx.prec = PREC
    Zn, Pn = Z[1:], P[1:]                 # nonzero roots; Zn[0] = nu = i l1, Zn[1] = -nu
    l1 = Zn[0].imag
    t = [arb(1), arb(1)] + [abs(z) / l1 for z in Zn[2:]]
    t = [x.upper() if k >= 2 else x for k, x in enumerate(t)]
    for k in range(2, 12):
        assert t[k] < 1
    Tex = powers(B['T'], K_max)
    Tacb = [M.to_acb() for M in Tex]
    D = [M.to_acb() for M in B['D']]
    cases = [('col', i) for i in range(5)] + [('row', i) for i in range(1, 5)]
    summary = []
    for (et, i) in cases:
        X = (B['G'] if et == 'col' else B['H']).to_acb()
        Di = D[i]
        par_sum = 1 if et == 'col' else 0          # a+b mod 2
        nfun = (lambda a, b: a + b + 2) if et == 'col' else (lambda a, b: a + b + 1)
        log(f"\n=== edge {et}, w row i={i}  (a+b = n-{2 if et=='col' else 1}, a+b = {par_sum} mod 2) ===")
        # ---- Region I amplitudes
        XP = [X * Pz for Pz in Pn]
        DP = [Di * Pz for Pz in Pn]
        A = [[(XP[z] * DP[zz]).trace() for zz in range(12)] for z in range(12)]
        Bd = {}
        for p in (0, 1):
            q = (par_sum - p) % 2
            s = A[0][0] + (-1) ** q * A[0][1] + (-1) ** p * A[1][0] + (-1) ** (p + q) * A[1][1]
            Bd[(p, q)] = s
            log(f"  dominant amplitude B(a={p} mod 2, b={q} mod 2) = {s.str(15, radius=True)}  |B| >= {s.abs_lower().str(10)}")
            assert not s.contains(0), "dominant amplitude not certified nonzero"
        K = None
        for KK in range(1, K_max + 1):
            err = arb(0)
            for z in range(12):
                for zz in range(12):
                    if z < 2 and zz < 2:
                        continue
                    err += A[z][zz].abs_upper() * t[z] ** KK * t[zz] ** KK
            if all(Bd[k].abs_lower() > err for k in Bd):
                K = KK
                log(f"  Region I certified with K = {K}: error bound {err.upper().str(10)} < min|B| = {min(Bd[k].abs_lower() for k in Bd).str(10)}")
                break
        assert K is not None, "Region I failed"
        # ---- Region II: b < K
        need = 0
        a0s = []
        for b in range(K):
            M = Di * Tacb[b] * X
            beta = [(Pz * M).trace() for Pz in Pn]
            # a parity is fixed: a = par_sum - b mod 2; take smallest a >= 1 of that parity
            pa = (par_sum - b) % 2
            dom = beta[0] + (-1) ** pa * beta[1]
            assert not dom.contains(0), f"Region II dominant amplitude zero-ish at b={b}"
            a = pa if pa >= 1 else 2
            while True:
                err = sum((beta[z].abs_upper() * t[z] ** a for z in range(2, 12)), arb(0))
                if dom.abs_lower() > err:
                    break
                a += 2
                assert a < a_max
            a0s.append(a)
            # uncovered: (a', b) with a' < a, a' of parity pa  -> n = nfun(a', b)
            if a - 2 >= 0:
                need = max(need, nfun(a - 2, b))
        log(f"  Region II (b<K): a0(b) for b=0..{K-1}: {a0s}")
        b0s = []
        for a in range(K):
            M = X * Tacb[a] * Di
            gamma = [(Pz * M).trace() for Pz in Pn]
            pb = (par_sum - a) % 2
            dom = gamma[0] + (-1) ** pb * gamma[1]
            assert not dom.contains(0), f"Region III dominant amplitude zero-ish at a={a}"
            b = pb if pb >= 1 else 2
            while True:
                err = sum((gamma[z].abs_upper() * t[z] ** b for z in range(2, 12)), arb(0))
                if dom.abs_lower() > err:
                    break
                b += 2
                assert b < a_max
            b0s.append(b)
            if b - 2 >= 0:
                need = max(need, nfun(a, b - 2))
        log(f"  Region III (a<K): b0(a) for a=0..{K-1}: {b0s}")
        # sanity: does the union of regions cover every (a,b) with n > need?  brute check up to a big n
        def covered(a, b):
            if a >= K and b >= K:
                return True
            if b < K and a >= a0s[b]:
                return True
            if a < K and b >= b0s[a]:
                return True
            return False
        unc = [(a, nb - a) for nb in range(0, 4 * (K + max(a0s + b0s)) + 10) for a in range(nb + 1)
               if (nb % 2 == par_sum) and nfun(a, nb - a) >= 3 and not covered(a, nb - a)]
        nmax = max(nfun(a, b) for a, b in unc) if unc else 0
        log(f"  uncovered (a,b) count {len(unc)}, largest n among them: {nmax}")
        summary.append((et, i, K, nmax, min(Bd[k].abs_lower() for k in Bd)))
    log("\n=== summary ===")
    for et, i, K, nmax, bmin in summary:
        log(f"  {et} i={i}: K={K}, exact check needed for odd n <= {nmax}, min|B| >= {bmin.str(8)}")
    N = max(s[3] for s in summary)
    log(f"N_needed (exact check of all odd n <= N_needed suffices) = {N}")
    log(f"time {time.time()-t0:.1f}s")
    open('/home/sid/work/gt/odd-torus/ws-W4/prove_m5_output.txt', 'w').write("\n".join(out_lines) + "\n")


if __name__ == '__main__':
    main()
