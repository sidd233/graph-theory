"""Compare exact strip coefficients (strip_coeff_m2-11.txt, method A/B, and direct_expand_m2-11.txt)
with the closed form  c_S = -(g/9) mu_k^(m-1) (w^s + (-1)^m w^(2s)),  g = 3 sqrt3 i,
mu_1 = w^2 - w, mu_2 = w - w^2, mu_0 = 0, and the extension mu_k = w^(2k) - w^k (so mu_3 = 0).
All comparisons exact in Q(omega)."""
import sys
from collections import defaultdict
from fractions import Fraction as Fr
from zomega import Z, wpow, ISQ3

G = Z(3) * ISQ3  # 3 sqrt3 i


def mu(k):
    return wpow(2 * k) - wpow(k)


def formula(m, k, s):
    return -(G * Z(Fr(1, 9))) * mu(k) ** (m - 1) * (wpow(s) + Z((-1) ** m) * wpow(2 * s))


def load(fn):
    rows = []
    for line in open(fn):
        if line.startswith("#") or not line.strip():
            continue
        a, rest = line.split("[", 1)
        key, val = rest.split("]")
        m, k, s = map(int, a.split())
        mu_ = {}
        for tok in key.split():
            rc, x = tok.split(":")
            r, c = map(int, rc.split(","))
            mu_[(r, c)] = int(x)
        rows.append((m, k, s, frozenset(mu_.items()), int(val)))
    return rows


def main():
    A = load(sys.argv[1])
    B = load(sys.argv[2])
    dA = {(m, S): v for m, k, s, S, v in A}
    dB = {(m, S): v for m, k, s, S, v in B}
    assert dA.keys() == dB.keys()
    nd = sum(dA[x] != dB[x] for x in dA)
    print(f"entries: {len(dA)}; transfer (method A, B) vs direct expansion disagreements: {nd}")
    # check the stated mu_0, mu_1, mu_2
    assert mu(0) == Z(0) and mu(1) == wpow(2) - wpow(1) and mu(2) == wpow(1) - wpow(2) and mu(3) == Z(0)
    assert mu(1) == -ISQ3 and mu(2) == ISQ3
    bad = 0
    byms = defaultdict(set)
    for m, k, s, S, v in A:
        f = formula(m, k, s)
        if not (f == Z(v)):
            bad += 1
            print("FORMULA MISMATCH", m, k, s, sorted(S), v, f)
        byms[(m, k, s)].add(v)
    print(f"signed mismatches with formula (mu_k = w^2k - w^k, k = 0..3): {bad} of {len(A)}")
    multi = {x: vs for x, vs in byms.items() if len(vs) > 1}
    print(f"(m,k,s) classes with more than one value of c_S: {len(multi)}")
    # symmetries
    sym_bad = 0
    for m, k, s, S, v in A:
        Sc = frozenset((((r, m + 1 - c)), x) for (r, c), x in S)      # column reflection
        Sr = frozenset((((-r) % 3, c), x) for (r, c), x in S)         # row reflection r -> -r
        Ss = frozenset((((r + 1) % 3, c), x) for (r, c), x in S)      # row shift r -> r+1
        if dA[(m, Sc)] != (-1) ** (m - 1) * v: sym_bad += 1
        if dA[(m, Sr)] != (-1) ** m * v: sym_bad += 1
        if dA[(m, Ss)] != v: sym_bad += 1
    print(f"symmetry violations (col reflection sign (-1)^(m-1), row reflection (-1)^m, row shift +1): {sym_bad}")
    # table by (k, s, m parity)
    print("\nTable: c_S by k, s (rows) and m (columns); every S in a class has the same value")
    ms = sorted({m for m, *_ in A})
    for par, name in ((1, "m odd"), (0, "m even")):
        mm = [m for m in ms if m % 2 == par]
        print(f"\n{name}: m = {mm}")
        print(f"{'k':>2} {'s':>2} | " + " ".join(f"{m:>7}" for m in mm) + " | formula")
        for k in range(4):
            for s in range(3):
                vals = []
                for m in mm:
                    vs = byms.get((m, k, s))
                    vals.append(f"{vs.pop() if vs and len(vs)==1 else '-':>7}" if vs else f"{'n/a':>7}")
                    if vs is not None:
                        byms[(m, k, s)] = {int(vals[-1])} if vals[-1].strip() not in ('-', 'n/a') else vs
                if par == 1:
                    cf = "0" if (k in (0, 3) or s == 0) else ("(-3)^((m-1)/2)" if s == 1 else "-(-3)^((m-1)/2)")
                else:
                    if k in (0, 3):
                        cf = "0"
                    else:
                        sg = 1 if k == 1 else -1
                        br = 2 if s == 0 else -1
                        cf = f"{sg*br:+d} * (-3)^(m/2)/3"
                print(f"{k:>2} {s:>2} | " + " ".join(vals) + f" | {cf}")
    # proof requirement
    print("\nRequirement: m odd, k in {1,2}, s != 0 mod 3  =>  c_S != 0, every S individually")
    cnt = viol = 0
    for m, k, s, S, v in A:
        if m % 2 == 1 and k in (1, 2) and s % 3:
            cnt += 1
            viol += v == 0
    print(f"  checked {cnt} end multisets (m odd in {[m for m in ms if m%2]}), zero coefficients: {viol}")
    zeros = defaultdict(int)
    tot = defaultdict(int)
    for m, k, s, S, v in A:
        cat = ("odd" if m % 2 else "even", "k in {0,3}" if k in (0, 3) else "k in {1,2}", "s=0" if s == 0 else "s!=0")
        tot[cat] += 1
        zeros[cat] += v == 0
    print("\nVanishing by class (m parity, k, s): zeros / total")
    for cat in sorted(tot):
        print(f"  {cat}: {zeros[cat]} / {tot[cat]}")


if __name__ == "__main__":
    main()
