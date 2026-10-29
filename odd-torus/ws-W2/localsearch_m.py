"""Cross-check for q = 4 by a different method (orchestrator's item 1).

Encode a 3-list assignment from palette {0,1,2,3} by its missing colour m(v): L(v) = [4] - {m(v)}.
L is bad iff count(m) = 0, where count(m) = number of proper 4-colourings c with c(v) != m(v).

count(m) is computed EXACTLY by a column transfer matrix: states = proper q-colourings of one
column C_rows; count = trace(prod_c D_c A), D_c = diagonal 0/1 mask of states avoiding m on
column c, A[s,s'] = 1 iff s(r) != s'(r) for all rows r. Integer arithmetic (int64 is enough:
every entry of a partial product is at most the number of partial colourings, < 4^N <= 2^50).

Validation: count(m) equals brute-force enumeration on C3xC3 and C3xC5 for random m, and
count(m) > 0 iff graphs.colour_backtrack finds a colouring, on random m for C5xC5.

Search: steepest-descent with random restarts and random-walk kicks on m, minimising count(m).
Run: python localsearch_m.py ROWS COLS SECONDS [seed]       (output localsearch_m_*.txt)
"""
import itertools
import random
import sys
import time

import numpy as np

from graphs import colour_backtrack, torus

Q = 4


def column_states(rows):
    st = []
    for s in itertools.product(range(Q), repeat=rows):
        if all(s[r] != s[(r + 1) % rows] for r in range(rows)) or rows == 1:
            st.append(s)
    return st


class Counter:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.st = column_states(rows)
        S = np.array(self.st)
        self.A = np.all(S[:, None, :] != S[None, :, :], axis=2).astype(np.int64)
        self.S = S

    def mask(self, mc):
        """mc: tuple of missing colours on one column (rows entries)."""
        return np.all(self.S != np.array(mc)[None, :], axis=1).astype(np.int64)

    def count(self, m):
        """m[r][c] -> missing colour. Exact count of proper colourings avoiding m."""
        M = None
        for c in range(self.cols):
            d = self.mask([m[r][c] for r in range(self.rows)])
            T = d[:, None] * self.A
            M = T if M is None else M @ T
        return int(np.trace(M))


def brute_count(rows, cols, m):
    N, E = torus(rows, cols)
    cnt = 0
    for c in itertools.product(range(Q), repeat=N):
        if all(c[v] != m[v // cols][v % cols] for v in range(N)) and all(c[a] != c[b] for a, b in E):
            cnt += 1
    return cnt


def validate(log):
    rng = random.Random(1)
    for rows, cols, trials in [(3, 3, 30), (3, 5, 4)]:
        C = Counter(rows, cols)
        ok = 0
        for _ in range(trials):
            m = [[rng.randrange(Q) for _ in range(cols)] for _ in range(rows)]
            ok += C.count(m) == brute_count(rows, cols, m)
        log(f"validate C{rows}xC{cols}: transfer count == brute force on {ok}/{trials} random m")
    C = Counter(5, 5)
    N, E = torus(5, 5)
    ok = 0
    for _ in range(200):
        m = [[rng.randrange(Q) for _ in range(5)] for _ in range(5)]
        L = [[a for a in range(Q) if a != m[v // 5][v % 5]] for v in range(N)]
        ok += (C.count(m) > 0) == (colour_backtrack(N, E, L) is not None)
    log(f"validate C5xC5: (count > 0) == backtracking colourable on {ok}/200 random m")


def search(rows, cols, seconds, seed, log):
    C = Counter(rows, cols)
    rng = random.Random(seed)
    t0 = time.time()
    best_overall, best_m, restarts, evals = None, None, 0, 0
    while time.time() - t0 < seconds:
        restarts += 1
        m = [[rng.randrange(Q) for _ in range(cols)] for _ in range(rows)]
        cur = C.count(m)
        evals += 1
        stall = 0
        while time.time() - t0 < seconds and stall < 3:
            best_move, best_val = None, cur
            for r in range(rows):
                for c in range(cols):
                    old = m[r][c]
                    for a in range(Q):
                        if a == old:
                            continue
                        m[r][c] = a
                        v = C.count(m)
                        evals += 1
                        if v < best_val:
                            best_move, best_val = (r, c, a), v
                    m[r][c] = old
            if best_move is None:
                stall += 1     # local minimum: random kick of 2 vertices
                for _ in range(2):
                    m[rng.randrange(rows)][rng.randrange(cols)] = rng.randrange(Q)
                cur = C.count(m)
                evals += 1
                continue
            r, c, a = best_move
            m[r][c] = a
            cur = best_val
            if best_overall is None or cur < best_overall:
                best_overall, best_m = cur, [row[:] for row in m]
                log(f"  t={time.time() - t0:.0f}s restart {restarts}: new minimum count = {cur}")
            if cur == 0:
                log(f"BAD ASSIGNMENT (count 0): m = {m}")
                return 0, m, restarts, evals
    return best_overall, best_m, restarts, evals


def main():
    rows, cols, seconds = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    out = open(f"localsearch_m_C{rows}xC{cols}.txt", "w")

    def log(s):
        print(s, flush=True)
        out.write(s + "\n")
        out.flush()

    validate(log)
    C = Counter(rows, cols)
    rng = random.Random(9)
    tot = [C.count([[rng.randrange(Q) for _ in range(cols)] for _ in range(rows)])
           for _ in range(100)]
    log(f"C{rows}xC{cols}: {len(C.st)} column states; count over 100 random m: "
        f"min {min(tot)} median {sorted(tot)[50]} max {max(tot)}")
    best, m, restarts, evals = search(rows, cols, seconds, seed, log)
    log(f"C{rows}xC{cols} q=4 local search, {seconds:.0f}s: minimum count found = {best} "
        f"({restarts} restarts, {evals} exact counts); best m (rows) = {m}")
    if best:
        N, E = torus(rows, cols)
        L = [[a for a in range(Q) if a != m[v // cols][v % cols]] for v in range(N)]
        log(f"backtracking confirms best m is colourable: {colour_backtrack(N, E, L) is not None}")


if __name__ == "__main__":
    main()
