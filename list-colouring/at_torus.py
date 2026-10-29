"""Alon-Tarsi coefficient of the toroidal grid T(m,n) = C_m x C_n.

T(m,n) is 4-regular, so AT <= 3 needs an orientation with every out-degree exactly 2
(an Eulerian orientation), and then EE - EO is, up to sign, the coefficient of
prod_v x_v^2 in the graph polynomial.  Orient D: vertical arcs (i,j) -> (i+1,j),
horizontal arcs (i,j) -> (i,j+1).

Coefficient by the Quantitative Nullstellensatz with colour set A = {1, w, w^2}
(w a primitive cube root of unity).  There phi(a) = prod_{b != a} (a - b) = 3a^2,
so 1/phi(a) = a/3 and

    coef = 3^(-mn) * sum over a in A^V of  prod_v a_v * prod_{(u,v) in D} (a_u - a_v).

The sum is a trace of a column transfer matrix, computed exactly in Z[w].

Prediction (reflection argument): coef = 0 whenever m and n are both odd.
"""
from itertools import product
import sys

W = [(1, 0), (0, 1), (-1, -1)]          # w^k as (a, b) meaning a + b*w, with w^2 = -1 - w


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def diff(e, f):
    return sub(W[e], W[f])


def coefficient(m, n):
    cols = [s for s in product(range(3), repeat=m)
            if all(s[i] != s[(i + 1) % m] for i in range(m))]     # proper column colourings
    weight = []
    for s in cols:                                                  # prod a_v * vertical arcs
        x = (1, 0)
        for i in range(m):
            x = mul(x, W[s[i]])
            x = mul(x, diff(s[i], s[(i + 1) % m]))
        weight.append(x)
    k = len(cols)
    M = [[(0, 0)] * k for _ in range(k)]                            # M[s][t] = weight(s) * horizontal arcs s -> t
    for p, s in enumerate(cols):
        for q, t in enumerate(cols):
            x = weight[p]
            for i in range(m):
                x = mul(x, diff(s[i], t[i]))
            M[p][q] = x
    P = [[(1, 0) if p == q else (0, 0) for q in range(k)] for p in range(k)]
    for _ in range(n):
        P = [[_dot(P[p], M, q, k) for q in range(k)] for p in range(k)]
    tr = (0, 0)
    for p in range(k):
        tr = add(tr, P[p][p])
    assert tr[1] == 0, tr                                           # the sum is rational
    c, r = divmod(tr[0], 3 ** (m * n))
    assert r == 0
    return c


def _dot(row, M, q, k):
    x = (0, 0)
    for r in range(k):
        if row[r] != (0, 0) and M[r][q] != (0, 0):
            x = add(x, mul(row[r], M[r][q]))
    return x


if __name__ == "__main__":
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print(" m  n   coef(prod x_v^2)   both odd")
    for m in range(3, top + 1):
        for n in range(m, top + 1):
            c = coefficient(m, n)
            print(f"{m:2d} {n:2d}   {c:16d}   {'yes' if m % 2 and n % 2 else ''}")
