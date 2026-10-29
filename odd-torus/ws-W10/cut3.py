"""W10: three-column cut for m = 5. Delete columns C1, C2, C3; the strip C4 ... C0 has even
length n - 3. Pin (0, C0) = alpha (fresh, alpha not in L(0, C1)). Adversary colours C0 (x, x0 = alpha)
and C4 (y), each a proper colouring of a 5-cycle; colours outside a list remove nothing.
Fill: C1 lists A_t minus x_t (A_0 full), C2 lists B_t (full), C3 lists D_t minus y_t.
Window is GOOD (pin only, no forbidden colours) if every (x, y) leaves the C5 x P3 fill colourable.
Fast test: MX(x) = middle colourings m compatible with some colouring of C1; MY(y) likewise;
(x, y) is fine iff MX(x) and MY(y) intersect.
Run: python cut3.py"""
import itertools, random
NONE = None
def cyc_cols(lists):
    out = []
    for c in itertools.product(*[sorted(l) for l in lists]):
        if all(c[t] != c[(t + 1) % 5] for t in range(5)): out.append(c)
    return out
def window_bad_pairs(A, B, D, stop_first=True):
    M = cyc_cols(B)
    if not M: return None
    idx = {m: i for i, m in enumerate(M)}
    def mask_for(cols):
        mk = 0
        for i, m in enumerate(M):
            if any(all(m[t] != a[t] for t in range(5)) for a in cols): mk |= 1 << i
        return mk
    def adv(lists, fixed0):
        opts = [[NONE]] if fixed0 else [sorted(lists[0]) + [NONE]]
        opts += [sorted(lists[t]) + [NONE] for t in range(1, 5)]
        seen = {}
        for z in itertools.product(*opts):
            if any(z[t] is not None and z[t] == z[(t + 1) % 5] for t in range(5)): continue
            red = tuple(frozenset(lists[t] - {z[t]}) if z[t] is not None else frozenset(lists[t]) for t in range(5))
            if red not in seen: seen[red] = z
        return seen
    XA = adv(A, True)                       # x0 = alpha: row 0 of C1 keeps its full list
    YD = adv(D, False)
    MX = {r: mask_for(cyc_cols(r)) for r in XA}
    MY = {r: mask_for(cyc_cols(r)) for r in YD}
    bad = []
    for rx, mx in MX.items():
        for ry, my in MY.items():
            if mx & my == 0:
                bad.append((XA[rx], YD[ry]))
                if stop_first: return bad
    return bad
if __name__ == '__main__':
    random.seed(1)
    const = frozenset({0, 1, 2})
    print('all 15 lists = {0,1,2}: bad pairs:', len(window_bad_pairs([const]*5, [const]*5, [const]*5, stop_first=False)))
    for P in (3, 4, 5, 6):
        nb = 0; N = 400
        for _ in range(N):
            A = [frozenset(random.sample(range(P), 3)) for _ in range(5)]
            B = [frozenset(random.sample(range(P), 3)) for _ in range(5)]
            D = [frozenset(random.sample(range(P), 3)) for _ in range(5)]
            if window_bad_pairs(A, B, D): nb += 1
        print(f'palette {P}: {nb} of {N} random three-column windows bad (pin only, no forbidden colours)')
