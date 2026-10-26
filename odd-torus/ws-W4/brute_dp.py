# W4 cross-check 3: direct expansion of P_{G-e} = prod_{arcs u->v, != e} (x_u - x_v), G = C_m x C_n.
# The coefficient of prod x_v^{t_v} is the signed number of ways to pick one endpoint per edge with
# vertex v picked t_v times (tail picked: +1, head picked: -1). Computed by a DP over edges with a frontier
# of active vertices (a vertex retires after its last edge, with count forced to t_v).
# No colourings, no roots of unity, no transfer matrices.  Usage: python brute_dp.py m n
import sys
sys.path.insert(0, '/home/sid/work/gt/odd-torus/ws-W4')


def coeff_dp(m, n, e, w):
    V = [(r, c) for c in range(n) for r in range(m)]
    edges = []
    for c in range(n):
        for r in range(m):
            if ('col', r, c) != e:
                edges.append(((r, c), ((r + 1) % m, c)))
        for r in range(m):
            if ('row', r, c) != e:
                edges.append(((r, c), (r, (c + 1) % n)))
    target = {v: 2 for v in V}
    target[w] = 1
    last = {}
    for k, (u, v) in enumerate(edges):
        last[u] = k; last[v] = k
    active = []           # ordered list of active vertices
    states = {(): 1}
    for k, (u, v) in enumerate(edges):
        for x in (u, v):
            if x not in active:
                active.append(x)
                states = {s + (0,): val for s, val in states.items()}
        iu, iv = active.index(u), active.index(v)
        new = {}
        for s, val in states.items():
            if s[iu] < target[u]:
                t = list(s); t[iu] += 1; t = tuple(t)
                new[t] = new.get(t, 0) + val
            if s[iv] < target[v]:
                t = list(s); t[iv] += 1; t = tuple(t)
                new[t] = new.get(t, 0) - val
        states = new
        for x in (u, v):
            if last[x] == k:
                ix = active.index(x)
                states2 = {}
                for s, val in states.items():
                    if s[ix] == target[x]:
                        t = s[:ix] + s[ix + 1:]
                        states2[t] = states2.get(t, 0) + val
                states = states2
                active.pop(ix)
        states = {s: val for s, val in states.items() if val != 0}
    assert active == []
    return states.get((), 0)


if __name__ == '__main__':
    from fractions import Fraction as F
    from tmlib import build, powers, c_col, c_row
    m, n = int(sys.argv[1]), int(sys.argv[2])
    B = build(m)
    Tp = powers(B['T'], n)
    agree = dis = 0
    for i in range(m):
        for j in range(1, n):
            d = coeff_dp(m, n, ('col', 0, 0), (i, j))
            t = c_col(B, i, j - 1, n - 1 - j, Tp)
            ok = (t == (F(d), F(0))); agree += ok; dis += not ok
            print(f"col e, w=({i},{j}): DP {d}, transfer {t[0]}+{t[1]}w {'OK' if ok else 'MISMATCH'}", flush=True)
    for i in range(1, m):
        for j in range(n):
            jj = j if j > 0 else n
            d = coeff_dp(m, n, ('row', 0, 0), (i, j))
            t = c_row(B, i, jj - 1, n - jj, Tp)
            ok = (t == (F(d), F(0))); agree += ok; dis += not ok
            print(f"row e, w=({i},{j}): DP {d}, transfer {t[0]}+{t[1]}w {'OK' if ok else 'MISMATCH'}", flush=True)
    print(f"C{m}xC{n}: agree {agree}, disagree {dis}")
