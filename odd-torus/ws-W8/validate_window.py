"""Independent re-check of window5.c verdicts (plan shape, m = 5) by plain brute force.
Same model: alpha fresh at row 0 of C0; adversary x on C0 (x0 = alpha), y on C3, proper on the
5-cycles; colours outside a list remove nothing. Run: python validate_window.py"""
import itertools, random, subprocess
NONE = None
def colourable(A, B):
    # u_t: lists A[t], v_t: lists B[t]; edges: u-cycle, v-cycle, u_t v_t
    order = [('u', t) for t in range(5)] + [('v', t) for t in range(5)]
    col = {}
    def nbrs(s, t):
        o = 'v' if s == 'u' else 'u'
        return [(s, (t + 1) % 5), (s, (t - 1) % 5), (o, t)]
    def go(i):
        if i == 10: return True
        s, t = order[i]
        for c in sorted((A if s == 'u' else B)[t]):
            if all(col.get(w) != c for w in nbrs(s, t)):
                col[(s, t)] = c
                if go(i + 1): return True
                del col[(s, t)]
        return False
    return go(0)
def proper(z):
    return all(z[t] is None or z[t] != z[(t + 1) % 5] for t in range(5))
def verdict(L1, L2):
    X = [x for x in itertools.product([None], *[list(L1[t]) + [None] for t in range(1, 5)]) if proper(x)]
    Y = [y for y in itertools.product(*[list(L2[t]) + [None] for t in range(5)]) if proper(y)]
    rm = lambda L, c: L - {c}
    Afam = {tuple(frozenset(rm(L1[t], x[t])) for t in range(5)) for x in X}
    fail_y = [y for y in Y if any(not colourable(A, [rm(L2[t], y[t]) for t in range(5)]) for A in Afam)]
    for p, q in itertools.combinations(range(5), 2):
        if (p + q) % 5 == 0: continue
        T = [t for t in range(5) if t not in (p, q)]
        for beta in itertools.product(*[sorted(L2[t]) for t in T]):
            if all(any(y[t] == b for t, b in zip(T, beta)) for y in fail_y): return True
    return False
def parse(h): return [{c for c in range(5) if int(h, 16) >> c & 1}]
lines = open('rand_bad.txt').read().split('\n')[:3]
random.seed(5); cases = []
for ln in lines:
    w = ln.split(); cases.append(([parse(h)[0] for h in w[2:7]], [parse(h)[0] for h in w[8:13]], False))
for _ in range(3):
    L1 = [set(random.sample(range(4), 3)) for _ in range(5)]; L2 = [set(random.sample(range(4), 3)) for _ in range(5)]
    cases.append((L1, L2, None))
for L1, L2, expect in cases:
    v = verdict(L1, L2)
    print('python verdict:', 'GOOD' if v else 'BAD', '| C verdict:', 'BAD' if expect is False else 'see C')
