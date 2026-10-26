"""SAT and brute-force cross-checks for 2-d kernels of C_m x C_n.

Parts (choose with the first argument):
  exist  m_max n_max : SAT existence for 3 <= m <= m_max, 3 <= n <= n_max; compare with
                       gcd(m, n) > 1; every model is re-checked by the definition and
                       tested to be 'diagonal' (theorem in REPORT.md).
  count  m_max n_max : enumerate all 2-d kernels by SAT with blocking clauses; compare the
                       count with the formula from the classification theorem
                       (0 if d = 1, 2 P(d) - 2 if d even, 2 P(d) if d odd, d = gcd(m, n),
                       P = Perrin numbers) and check every one is diagonal.
  brute  max_vertices: independent brute force (backtracking, no SAT) counting 2-d kernels
                       for all 3 <= m <= n with m * n <= max_vertices.
"""
import sys
from math import gcd

from pysat.solvers import Cadical153

from common import torus, is_2d_kernel, kernel_clauses


def perrin(k):
    P = [3, 0, 2]
    while len(P) <= k:
        P.append(P[-2] + P[-3])
    return P[k]


def formula_count(m, n):
    d = gcd(m, n)
    if d == 1:
        return 0
    return 2 * perrin(d) - (2 if d % 2 == 0 else 0)


def is_diagonal(m, n, S):
    """S (set of (r, c)) is {(r, c) : c - s r in K} for s = +1 or -1, i.e. row r+1 equals
    row r shifted by s, for every r, with one fixed s."""
    rows = [frozenset(c for (r, c) in S if r == rr) for rr in range(m)]
    for s in (1, -1):
        if all(rows[(r + 1) % m] == frozenset((c + s) % n for c in rows[r]) for r in range(m)):
            return True
    return False


def part_exist(mmax, nmax):
    bad = 0
    for m in range(3, mmax + 1):
        line = []
        for n in range(3, nmax + 1):
            verts, idx, adj = torus((m, n))
            with Cadical153(bootstrap_with=kernel_clauses(adj)) as s:
                sat = s.solve()
                model = s.get_model() if sat else None
            if sat:
                S = [v - 1 for v in model if v > 0]
                assert is_2d_kernel(adj, S)
                assert is_diagonal(m, n, {verts[v] for v in S})
            ok = sat == (gcd(m, n) > 1)
            bad += not ok
            line.append("Y" if sat else ".")
        print(f"m={m:2d}: " + "".join(line))
    print(f"(columns n = 3..{nmax}; Y = SAT, . = UNSAT)  disagreements with gcd>1: {bad}")


def part_count(mmax, nmax):
    bad = 0
    for m in range(3, mmax + 1):
        for n in range(m, nmax + 1):
            verts, idx, adj = torus((m, n))
            cnt = 0
            alldiag = True
            with Cadical153(bootstrap_with=kernel_clauses(adj)) as s:
                while s.solve():
                    model = s.get_model()
                    S = [v - 1 for v in model if v > 0]
                    assert is_2d_kernel(adj, S)
                    alldiag &= is_diagonal(m, n, {verts[v] for v in S})
                    cnt += 1
                    s.add_clause([-v for v in model[: m * n]])
            f = formula_count(m, n)
            bad += (cnt != f) or not alldiag
            print(f"m={m} n={n} gcd={gcd(m, n)} count_SAT={cnt} formula={f} "
                  f"all_diagonal={alldiag}")
    print(f"disagreements: {bad}")


def brute_count(m, n):
    """Count 2-d kernels by row-by-row backtracking with the full definition checked at
    the end of each completed neighbourhood. Independent of SAT and of the theorem."""
    verts, idx, adj = torus((m, n))
    N = m * n
    x = [0] * N
    count = 0

    def ok_vertex(v):
        if x[v]:
            return all(not x[w] for w in adj[v])
        return sum(x[w] for w in adj[v]) >= 2

    # vertex v's neighbourhood is fully decided once all of its neighbours and itself have
    # index <= current; precompute for each position the vertices that become decided.
    last = [max([v] + adj[v]) for v in range(N)]
    decided_at = [[] for _ in range(N)]
    for v in range(N):
        decided_at[last[v]].append(v)

    def rec(i):
        nonlocal count
        if i == N:
            count += 1
            return
        for val in (0, 1):
            x[i] = val
            if val == 1 and any(x[w] for w in adj[i] if w < i):
                continue
            if all(ok_vertex(v) for v in decided_at[i]):
                rec(i + 1)
        x[i] = 0

    rec(0)
    return count


def part_brute(maxv):
    bad = 0
    for m in range(3, 13):
        for n in range(m, 40):
            if m * n > maxv:
                continue
            c = brute_count(m, n)
            f = formula_count(m, n)
            bad += c != f
            print(f"m={m} n={n} brute_count={c} formula={f}")
            sys.stdout.flush()
    print(f"disagreements: {bad}")


if __name__ == "__main__":
    part = sys.argv[1]
    if part == "exist":
        part_exist(int(sys.argv[2]), int(sys.argv[3]))
    elif part == "count":
        part_count(int(sys.argv[2]), int(sys.argv[3]))
    elif part == "brute":
        part_brute(int(sys.argv[2]))
