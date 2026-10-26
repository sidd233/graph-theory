"""Soundness tests for cegar2.py. Output: test_soundness.txt.

T1  Brute force vs search. Random small graphs, k in {2, 3}, small q. Brute force enumerates
    EVERY list assignment (all k-subsets of [q] per vertex) and decides by exhaustive colouring
    whether a bad one exists. The search must agree under every flag combination. (C) and (O)
    are only switched on when their hypothesis (G-v, resp. G-e, k-choosable for all v, e) was
    itself verified by brute force for that graph and palette.
T2  Symmetry breaking (S)+(G) on tori: every orbit (under the automorphisms of graphs.py and
    colour renaming) must have a representative satisfying the master's base CNF. Checked on
    ALL bad 2-list assignments of C3xC3 with q = 3 and q = 4 (complete), and on random 3-list
    assignments of C3xC3, C3xC5, C5xC5, C3xC7 (sampled). The base CNF is queried by SAT with
    the l-variables fixed by assumptions.
T3  The encoding of (G) agrees with a direct Python evaluation of the predicate (both
    directions) on random list assignments.
"""
import itertools
import random
import sys
import time

import networkx as nx
from pysat.solvers import Solver

from cegar2 import Search
from graphs import (adjacency, brute_force_colourable, colour_backtrack, torus,
                    torus_automorphisms, is_automorphism)

out = open("test_soundness.txt", "a")


def log(s):
    print(s, flush=True)
    out.write(s + "\n")
    out.flush()


def all_assignments(N, q, k):
    subs = list(itertools.combinations(range(q), k))
    return itertools.product(subs, repeat=N)


def exists_bad(N, E, q, k):
    for L in all_assignments(N, q, k):
        if not brute_force_colourable(N, E, L):
            return L
    return None


def choosable_minus(N, E, q, k, kind):
    """Brute force: is G - v (kind 'v') / G - e (kind 'e') k-choosable from palette q, for all
    v / e? Only used to decide whether (C) / (O) may be switched on in a test."""
    items = range(N) if kind == "v" else E
    for x in items:
        if kind == "v":
            keep = [u for u in range(N) if u != x]
            idx = {u: i for i, u in enumerate(keep)}
            E2 = [(idx[a], idx[b]) for a, b in E if x not in (a, b)]
            N2 = N - 1
        else:
            E2 = [e for e in E if e != x]
            N2 = N
        if exists_bad(N2, E2, q, k) is not None:
            return False
    return True


def quiet(s):
    pass


def T1(trials=400, seed=1):
    rng = random.Random(seed)
    combos = [dict(), dict(colsym=True), dict(fix0=True), dict(shrink=True),
              dict(shrink=True, glits=True, diverse=3), dict(colsym=True, shrink=True,
                                                             glits=True, diverse=3)]
    agree = disagree = 0
    nbad = ngood = ncrit = nover = 0
    t0 = time.time()
    for t in range(trials):
        k = rng.choice([2, 2, 3])
        n = rng.randint(3, 6) if k == 2 else rng.randint(4, 6)
        q = rng.randint(k + 1, k + 2) if k == 3 else rng.randint(k + 1, k + 2)
        if k == 3 and n == 6:
            q = 4
        G = nx.gnp_random_graph(n, rng.uniform(0.4, 0.9), seed=rng.randrange(10 ** 9))
        if not nx.is_connected(G):
            continue
        N, E = n, sorted((min(a, b), max(a, b)) for a, b in G.edges())
        bf = exists_bad(N, E, q, k) is not None
        nbad += bf
        ngood += not bf
        cv = choosable_minus(N, E, q, k, "v")
        ce = choosable_minus(N, E, q, k, "e")
        cs = list(combos)
        ncrit += cv
        nover += ce
        if cv:
            cs.append(dict(colsym=True, crit=True, shrink=True, glits=True, diverse=3))
        if ce:
            cs.append(dict(colsym=True, overlap=True, shrink=True, glits=True, diverse=3))
        for fl in cs:
            S = Search(N, E, q, k, log=quiet, seed=t, **fl)
            res, L = S.run(report=0)
            ok = (res == "found") == bf
            if res == "found":
                ok = ok and colour_backtrack(N, E, L) is None
            if ok:
                agree += 1
            else:
                disagree += 1
                log(f"T1 DISAGREE: n={n} k={k} q={q} E={E} flags={fl} bf_bad={bf} res={res}")
    log(f"T1 brute force vs search: {agree} agreements, {disagree} disagreements "
        f"({nbad} graphs with a bad assignment, {ngood} without; (C) tested on {ncrit} graphs, "
        f"(O) on {nover}) {time.time() - t0:.0f}s")


def canon_colours(L, order):
    """Relabel colours by first appearance along order (ties: increasing old label)."""
    ren = {}
    for v in order:
        for a in sorted(L[v]):
            if a not in ren:
                ren[a] = len(ren)
    return [sorted(ren[a] for a in L[v]) for v in range(len(L))]


def representative_ok(S, L, auts, q):
    """Is there sigma in auts such that the colour-canonical form of L o sigma^-1 satisfies the
    base CNF of S (queried by SAT with assumptions)?"""
    N = len(L)
    for p in auts:
        L2 = [None] * N
        for v in range(N):
            L2[p[v]] = L[v]           # (sigma L)(sigma v) = L(v)
        L3 = canon_colours(L2, range(N))
        if max(max(x) for x in L3) >= q:
            continue
        ass = [S.l[v, a] if a in L3[v] else -S.l[v, a] for v in range(N) for a in range(q)]
        if S.master.solve(assumptions=ass):
            return True
    return False


def T2():
    t0 = time.time()
    for (m, n, q, k, mode, cnt) in [(3, 3, 3, 2, "allbad", None), (3, 3, 4, 2, "randombad", 300),
                                    (3, 5, 3, 2, "randombad", 200),
                                    (3, 3, 4, 3, "random", 300), (3, 5, 5, 3, "random", 200),
                                    (5, 5, 4, 3, "random", 100), (5, 5, 6, 3, "random", 100),
                                    (3, 7, 5, 3, "random", 60)]:
        N, E = torus(m, n)
        auts = torus_automorphisms(m, n)
        assert all(is_automorphism(p, E) for p in auts)
        S = Search(N, E, q, k, colsym=True, gsym=(m, n), log=quiet)
        rng = random.Random(m * 100 + n * 10 + q)
        tested = fails = 0
        if mode == "allbad":
            Ls = (L for L in all_assignments(N, q, k) if not brute_force_colourable(N, E, L))
        elif mode == "randombad":
            subs = list(itertools.combinations(range(q), k))

            def gen():
                got = 0
                while got < cnt:
                    L = [rng.choice(subs) for _ in range(N)]
                    if colour_backtrack(N, E, L) is None:
                        got += 1
                        yield L
            Ls = gen()
        else:
            subs = list(itertools.combinations(range(q), k))
            Ls = ([rng.choice(subs) for _ in range(N)] for _ in range(cnt))
        for L in Ls:
            tested += 1
            if not representative_ok(S, L, auts, q):
                fails += 1
                log(f"T2 FAIL: C{m}xC{n} q={q} k={k} L={L}")
        log(f"T2 orbit representatives C{m}xC{n} q={q} k={k} {mode}: {tested} tested, "
            f"{fails} without a representative, |auts|={len(auts)} {time.time() - t0:.0f}s")


def gsym_predicate(L, m, n):
    N = m * n
    adj = adjacency(*torus(m, n))
    g = [sum(len(set(L[v]) & set(L[u])) for u in adj[v]) for v in range(N)]
    e = lambda x: len(set(L[0]) & set(L[x]))
    R, Lf, D, U = 1 % n, n - 1, n % N, (m - 1) * n
    ok = all(g[0] >= g[v] for v in range(N)) and e(R) >= e(Lf) and e(D) >= e(U)
    if m == n:
        ok = ok and e(R) >= e(D)
    return ok


def T3():
    for (m, n, q) in [(3, 5, 5), (5, 5, 4), (5, 5, 6)]:
        N, E = torus(m, n)
        S = Search(N, E, q, 3, gsym=(m, n), log=quiet)
        rng = random.Random(7)
        subs = list(itertools.combinations(range(q), 3))
        agree = dis = npos = 0
        auts = torus_automorphisms(m, n)
        for it in range(300):
            L = [rng.choice(subs) for _ in range(N)]
            if it % 2:   # half the samples: an automorphic image satisfying the predicate
                for p in auts:
                    L2 = [None] * N
                    for v in range(N):
                        L2[p[v]] = L[v]
                    if gsym_predicate(L2, m, n):
                        L = L2
                        break
            ass = [S.l[v, a] if a in L[v] else -S.l[v, a] for v in range(N) for a in range(q)]
            sat = S.master.solve(assumptions=ass)
            pr = gsym_predicate(L, m, n)
            npos += pr
            if sat == pr:
                agree += 1
            else:
                dis += 1
                log(f"T3 DISAGREE C{m}xC{n} q={q}: sat={sat} predicate={pr} L={L}")
        log(f"T3 (G) encoding vs predicate C{m}xC{n} q={q}: {agree} agree, {dis} disagree, "
            f"{npos} satisfy the predicate")


if __name__ == "__main__":
    which = sys.argv[1:] or ["T1", "T2", "T3"]
    for w in which:
        globals()[w]()
