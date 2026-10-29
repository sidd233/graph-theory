"""Runs the construction in the proof of the one-free-row lemma (latex/c3-torus-choosable.tex)
on random instances and checks that it always yields a proper L-colouring.
Run: python freerow_check.py"""
import itertools, random
def cycle_colour(lists):
    # colour a cycle from lists (backtracking); None if impossible
    n = len(lists); col = []
    def go(i):
        if i == n: return col[0] != col[-1]
        for c in sorted(lists[i]):
            if (i == 0 or c != col[-1]):
                col.append(c)
                if go(i + 1): return True
                col.pop()
        return False
    return list(col) if go(0) else None
def construct(m, n, A, free):          # free = lists of row i0 = m-1, A = common list
    R = m - 1                          # rows 0..m-2 form the path
    p = [0, 1, 2, 0] + [1, 0] * ((R - 4) // 2)
    k = next(k for k in range(3) if (2 * k - n) % 3 == 0)
    sig = [1] * k + [-1] * (n - k)
    A = sorted(A)
    for tau in (0, 1):
        pis = [None] * n; shift = tau
        for j in range(n):
            pis[j] = shift; shift = (shift + sig[j]) % 3
        assert shift == tau
        colour = {(i, j): A[(pis[j] + p[i]) % 3] for i in range(R) for j in range(n)}
        a = [colour[(0, j)] for j in range(n)]
        assert all(colour[(R - 1, j)] == a[j] for j in range(n))
        row = cycle_colour([set(free[j]) - {a[j]} for j in range(n)])
        if row:
            for j in range(n): colour[(R, j)] = row[j]
            return colour
    return None
def proper(m, n, colour, A, free):
    for (i, j), c in colour.items():
        if c not in (free[j] if i == m - 1 else A): return False
        for (di, dj) in ((1, 0), (0, 1)):
            if colour[((i + di) % m, (j + dj) % n)] == c: return False
    return True
random.seed(1); bad = 0; N = 0
for _ in range(20000):
    m = random.choice([5, 7, 9]); n = random.choice([3, 4, 5, 6, 7, 9, 11]); Q = random.choice([3, 4, 5, 6])
    A = set(random.sample(range(Q), 3))
    free = [set(random.sample(range(Q), 3)) for _ in range(n)]
    if random.random() < 0.3:          # adversarial: free lists = B + one colour of A
        B = set(random.sample(range(Q), 2)); free = [B | {random.choice(sorted(A - B or A))} for _ in range(n)]
    c = construct(m, n, A, [set(f) for f in free]); N += 1
    if c is None or not proper(m, n, c, A, free): bad += 1
print(f'{N} random instances (m in 5,7,9; n from 3 to 11; up to 6 colours): construction failed {bad} times')
