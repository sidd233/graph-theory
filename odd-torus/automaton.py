"""All n at once: for which n is the Galvin-type orientation D_n of C_3 x C_n kernel-perfect?

Level coordinates.  Column j of C_3 x C_n (3 | n) has the vertices a_j, b_j, c_j of colours
0, 1, 2.  The arcs are
    column:  c_j -> b_j,  b_j -> a_j,  c_j -> a_j            (towards the smaller colour)
    row:     a_j -> b_{j+1},  b_j -> c_{j+1},  a_{j+1} -> c_j  (towards the larger colour)
and they do not depend on j.  A set S is a word S_0 S_1 ... S_{n-1} over the 8 subsets of
{a, b, c}.  For a fixed S, the feasible partial kernels after column j are summarised by triples
(g, k_0, (k_j, U_j)): g is a guess for the kernel vertex of column n-1 (needed by column 0), k_0
the kernel vertex of column 0, k_j that of column j, and U_j the vertices of S_j outside K that
are not yet absorbed (only a right neighbour can still absorb them).  The set F_j of feasible
triples is a function of S_0 ... S_j, computed by a transition that does not depend on j.  So the
reachable sets F form a finite automaton, independent of n, and
    D_n is NOT kernel-perfect  <=>  some word of length n leads to a set F with no closing triple.
The sets X_t = {F reachable by words of length t} are eventually periodic in t, which gives
the answer for every n exactly.

Run: python3 automaton.py [--check N]   (--check compares with strip_dp for n = 3, 6, ..., N)
"""
import argparse
from itertools import product

LEVELS = (0, 1, 2)  # a, b, c
KOPTS = (None, 0, 1, 2)
LETTERS = [frozenset(x for x in LEVELS if m >> x & 1) for m in range(8)]


def col_arc(x, y):
    """x_j -> y_j inside a column: towards the smaller level."""
    return x > y


def right_arc(x):
    """Between x_j and its right neighbour (x+1)_{j+1}: True iff x_j -> (x+1)_{j+1}."""
    return x in (0, 1)  # a -> b, b -> c; for x = c the arc is a_{j+1} -> c_j


def column_profile(S, k, kprev):
    """Unabsorbed vertices of a column (given its kernel vertex k and the previous one kprev),
    or None if k is not allowed."""
    if k is not None and k not in S:
        return None
    if k is not None and kprev is not None and k == (kprev + 1) % 3:
        return None  # kprev_{j-1} and k_j are row neighbours, both in K
    U = []
    for y in S:
        if y == k:
            continue
        if k is not None and col_arc(y, k):
            continue  # absorbed by the column mate
        if y == 0 and kprev == 2:
            continue  # a_j -> c_{j-1} = left neighbour, in K
        U.append(y)
    return frozenset(U)


def step(F, S):
    G = set()
    for g, k0, (k, U) in F:
        for kn in KOPTS:
            if any(not (right_arc(x) and kn == (x + 1) % 3) for x in U):
                continue
            Un = column_profile(S, kn, k)
            if Un is not None:
                G.add((g, k0, (kn, Un)))
    return frozenset(G)


def initial(S):
    F = set()
    for g in KOPTS:
        for k0 in KOPTS:
            U = column_profile(S, k0, g)
            if U is not None:
                F.add((g, k0, (k0, U)))
    return frozenset(F)


def closes(F):
    for g, k0, (k, U) in F:
        if k == g and all(right_arc(x) and k0 == (x + 1) % 3 for x in U):
            return True
    return False


def explore():
    """Reachable states and transitions."""
    init = {initial(S) for S in LETTERS}
    states = set(init)
    frontier = list(init)
    succ = {}
    while frontier:
        F = frontier.pop()
        succ[F] = {step(F, S) for S in LETTERS}
        for G in succ[F]:
            if G not in states:
                states.add(G)
                frontier.append(G)
    return init, states, succ


def length_profile(init, succ, bad):
    """X_t = set of states reachable by words of length t (t >= 1).  Returns the lengths t at
    which X_t meets a bad state, as (prefix list, periodic part) once X_t repeats."""
    seen = {}
    X = frozenset(init)
    t = 1
    hits = []
    while X not in seen:
        seen[X] = t
        hits.append(any(F in bad for F in X))
        X = frozenset(G for F in X for G in succ[F])
        t += 1
    start = seen[X]
    period = t - start
    return hits, start, period


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", type=int, default=0)
    a = ap.parse_args()
    init, states, succ = explore()
    bad = {F for F in states if not closes(F)}
    print(f"reachable states: {len(states)}, bad (no closing triple): {len(bad)}")
    hits, start, period = length_profile(init, succ, bad)
    print(f"X_t is periodic from t = {start} with period {period}")
    bad_n = [t for t in range(1, len(hits) + 1) if hits[t - 1]]
    print(f"bad lengths n among 1..{len(hits)}: {bad_n}")
    per = [t for t in range(start, start + period) if hits[t - 1]]
    print(f"for n >= {start}: D_n is not kernel-perfect iff n mod {period} in "
          f"{sorted(set(t % period for t in per))}")
    if a.check:
        import strip_dp
        for n in range(3, a.check + 1, 3):
            X = frozenset(init)
            for _ in range(n - 1):
                X = frozenset(G for F in X for G in succ[F])
            auto_bad = any(F in bad for F in X)
            dp_bad = strip_dp.find_kernelless(n, strip_dp.galvin_arc(n)) is not None
            assert auto_bad == dp_bad, n
        print(f"agrees with strip_dp for n = 3, 6, ..., {a.check}")


if __name__ == "__main__":
    main()
