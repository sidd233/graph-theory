"""Fall 3-colourings of C_b x C_c: proper 3-colourings in which every vertex sees both other
colours among its neighbours (equivalently, a partition into 3 independent dominating sets).

By the K_3 reduction proved in REPORT.md, C_3 x C_b x C_c has a 2-d kernel iff C_b x C_c
has a fall 3-colouring. This is an independent SAT check of that statement against
torus3d_upto9.txt, and a test of the conjecture 'fall 3-colourable iff 3 | b or 3 | c'.

Run: python fall3.py cmax
"""
import sys

from pysat.solvers import Cadical153

from common import torus


def fall3(b, c):
    verts, idx, adj = torus((b, c))
    var = lambda v, k: 3 * v + k + 1
    cls = []
    for v in range(len(verts)):
        cls.append([var(v, k) for k in range(3)])
        for k in range(3):
            for l in range(k + 1, 3):
                cls.append([-var(v, k), -var(v, l)])
            for w in adj[v]:
                if v < w:
                    cls.append([-var(v, k), -var(w, k)])
            # if v has colour k, then for each other colour l some neighbour has colour l
            for l in range(3):
                if l != k:
                    cls.append([-var(v, k)] + [var(w, l) for w in adj[v]])
    with Cadical153(bootstrap_with=cls) as s:
        return s.solve()


def main():
    cmax = int(sys.argv[1])
    sat3d = {}
    try:
        for line in open("torus3d_upto9.txt"):
            p = line.split()
            if len(p) > 4 and p[0] == "3":
                sat3d[(int(p[1]), int(p[2]))] = "YES" in line
    except FileNotFoundError:
        pass
    bad_conj = bad_3d = 0
    for b in range(3, cmax + 1):
        row = []
        for c in range(3, cmax + 1):
            f = fall3(b, c)
            conj = (b % 3 == 0) or (c % 3 == 0)
            bad_conj += f != conj
            if (b, c) in sat3d:
                bad_3d += f != sat3d[(b, c)]
            row.append("Y" if f else ".")
        print(f"b={b:2d}: " + "".join(row))
    print(f"(columns c = 3..{cmax}; Y = fall 3-colourable)")
    print(f"disagreements with 'iff 3|b or 3|c': {bad_conj}")
    print(f"disagreements with 3D SAT for C_3 x C_b x C_c (b, c <= 9): {bad_3d}")


if __name__ == "__main__":
    main()
