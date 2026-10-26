"""Improved CEGAR search for a bad k-list assignment (default k = 3) with palette {0..q-1}.

Master SAT: variables l(v,a) = "colour a is in L(v)". It proposes L. Checker SAT colours L.
Each colouring is turned into a cut (a clause over the l variables) that is a valid fact
about ALL list assignments, not just the current one. Master UNSAT => no bad assignment
satisfying the chosen hypotheses exists with this palette.

Constraints (each switchable, see REPORT.md for the proofs):
  (L)  |L(v)| = k for all v.                                   always on
  (S)  colour value precedence along vertex order 0, 1, ...     --colsym
  (F)  L(0) = {0..k-1} only (orchestrator's colour fix)         --fix0 (weaker than (S))
  (G)  torus symmetry breaking at vertex 0 = (0,0)              --gsym (torus only)
  (C)  criticality: a in L(v) => a in L(u) for a neighbour u    --crit (hypothesis: G-v k-choosable)
  (O)  overlap: L(u) & L(v) nonempty on every edge              --overlap (hypothesis: G-e k-choosable)
Cuts from a colouring c of L:
  plain    : OR_v not l(v, c(v))                                 (orchestrator's cut)
  --shrink : OR_{v in S} not l(v, c(v)), where V - S is peelable (degenerate) for the
             worst-case residual list sizes k - |c(N(w) & S)|.
  --glits  : also literals "|L(w) & X_w| >= t" for peeled vertices w, X_w = c(N(w) & S),
             which raise the guaranteed residual of w to k - t + 1. See verify_cuts.py.

Run:  python cegar2.py torus M N Q [options]     or    python cegar2.py kab A B Q [options]
"""
import argparse
import itertools
import json
import math
import os
import random
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

from verify_cuts import cut_holds, verify_cut
from graphs import (adjacency, colour_backtrack, complete_bipartite, is_proper_list_colouring,
                    peelable, torus)


# ----------------------------------------------------------------------------- encoding helpers
_TOT = itertools.count()


def unary_count(lits, pool, out):
    """Totalizer with both directions. Returns O with O[t-1] <-> (sum of lits >= t)."""
    if len(lits) == 1:
        return [lits[0]]
    h = len(lits) // 2
    A = unary_count(lits[:h], pool, out)
    B = unary_count(lits[h:], pool, out)
    na, nb = len(A), len(B)
    O = [pool.id(("tot", next(_TOT), t)) for t in range(na + nb)]
    a = lambda t: A[t - 1]
    b = lambda t: B[t - 1]
    o = lambda t: O[t - 1]
    for i in range(na + 1):
        for j in range(nb + 1):
            if i + j >= 1:
                cl = [o(i + j)]
                if i:
                    cl.append(-a(i))
                if j:
                    cl.append(-b(j))
                out.append(cl)
            if i + j + 1 <= na + nb:
                cl = [-o(i + j + 1)]
                if i + 1 <= na:
                    cl.append(a(i + 1))
                if j + 1 <= nb:
                    cl.append(b(j + 1))
                out.append(cl)
    return O


def geq(Ox, Oy):
    """Clauses for count(x) >= count(y), from unary outputs."""
    cl = []
    for t in range(len(Oy)):
        if t < len(Ox):
            cl.append([-Oy[t], Ox[t]])
        else:
            cl.append([-Oy[t]])
    return cl


# ----------------------------------------------------------------------------- the solver
class Search:
    def __init__(self, N, E, q, k=3, colsym=False, fix0=False, gsym=None, crit=False,
                 overlap=False, shrink=False, glits=False, diverse=1, tries=8, seed=0,
                 solver="cadical153", log=print):
        self.N, self.E, self.q, self.k = N, E, q, k
        self.adj = adjacency(N, E)
        self.shrink, self.glits, self.diverse, self.tries = shrink, glits, diverse, tries
        self.wneg = -math.log(k / q)
        self._yc, self.yvar = {}, {}
        self.rng = random.Random(seed)
        self.log = log
        self.pool = IDPool()
        self.l = {(v, a): self.pool.id(("l", v, a)) for v in range(N) for a in range(q)}
        cls = []
        for v in range(N):  # (L)
            cls += CardEnc.equals([self.l[v, a] for a in range(q)], bound=k, vpool=self.pool,
                                  encoding=EncType.seqcounter).clauses
        if colsym:  # (S)
            for i in range(N):
                for a in range(1, q):
                    cls.append([-self.l[i, a]] + [self.l[j, a - 1] for j in range(i + 1)])
        if fix0:  # (F)
            for a in range(k):
                cls.append([self.l[0, a]])
        if crit:  # (C)
            for v in range(N):
                for a in range(q):
                    cls.append([-self.l[v, a]] + [self.l[u, a] for u in self.adj[v]])
        p = {}
        if overlap or gsym:
            for u, v in E:
                for a in range(q):
                    z = self.pool.id(("p", u, v, a))
                    p[u, v, a] = p[v, u, a] = z
                    cls += [[-z, self.l[u, a]], [-z, self.l[v, a]],
                            [z, -self.l[u, a], -self.l[v, a]]]
        if overlap:  # (O)
            for u, v in E:
                cls.append([p[u, v, a] for a in range(q)])
        if gsym:  # (G)
            m, n = gsym
            cls += self.gsym_clauses(m, n, p)
        self.base = cls
        self.master = Solver(name=solver, bootstrap_with=cls)
        self.cuts = []
        self.stats = {"iters": 0, "cuts": 0, "lits": 0}

    def gsym_clauses(self, m, n, p):
        """(G): g(0) >= g(v) for all v, where g(v) = sum over edges vu of |L(v) & L(u)|;
        at vertex 0: e(R) >= e(L), e(D) >= e(U), and e(R) >= e(D) if m == n, where e(X) is
        |L(0) & L(X)| for the right/left/down/up neighbour X."""
        out = []
        q = self.q
        G = {}
        for v in range(self.N):
            lits = [p[v, u, a] for u in sorted(self.adj[v]) for a in range(q)]
            G[v] = unary_count(lits, self.pool, out)
        for v in range(1, self.N):
            out += geq(G[0], G[v])
        R, Lf, D, U = 1 % n, (n - 1) % n, (1 % m) * n, ((m - 1) % m) * n
        e = {x: unary_count([p[0, x, a] for a in range(q)], self.pool, out)
             for x in {R, Lf, D, U}}
        out += geq(e[R], e[Lf]) + geq(e[D], e[U])
        if m == n:
            out += geq(e[R], e[D])
        return out

    # ------------------------------------------------------------------ checker and cuts
    def colourings(self, L, K):
        N, q = self.N, self.q
        x = lambda v, a: v * q + a + 1
        cls = []
        for v in range(N):
            cls.append([x(v, a) for a in L[v]])
            for a in range(q):
                if a not in L[v]:
                    cls.append([-x(v, a)])
            for i, a in enumerate(L[v]):
                for b in L[v][i + 1:]:
                    cls.append([-x(v, a), -x(v, b)])
        for u, v in self.E:
            for a in set(L[u]) & set(L[v]):
                cls.append([-x(u, a), -x(v, a)])
        out = []
        with Solver(name="minisat22", bootstrap_with=cls) as s:
            for i in range(K):
                if i:
                    s.set_phases([x(v, a) if self.rng.random() < 0.4 else -x(v, a)
                                  for v in range(N) for a in L[v]])
                if not s.solve():
                    break
                mod = set(t for t in s.get_model() if t > 0)
                c = [next(a for a in L[v] if x(v, a) in mod) for v in range(N)]
                out.append(c)
                s.add_clause([-x(v, c[v]) for v in range(N)])
        return out

    def cut_from(self, L, c):
        """A cut (list of literals) valid for every list assignment and false on L.

        Literal forms: ("n", v, a) means "a not in L(v)"; ("y", w, X, t) means
        "|L(w) & X| >= t". The cut says: NOT( c(v) in L(v) for v in S and |L(w) & X_w| < t_w
        for the literal vertices w ), and its validity is certified by peeling V - S."""
        if not self.shrink:
            return [("n", v, c[v]) for v in range(self.N)]
        best, bestw = None, math.inf
        for t in range(self.tries):
            order = list(range(self.N))
            self.rng.shuffle(order)
            S = set(range(self.N))
            cost, lits = len(S) * self.wneg, []
            for v in order:
                S2 = S - {v}
                ok, cost2, lits2 = self.peel_cost(L, c, S2)
                if ok and cost2 + len(S2) * self.wneg < cost:
                    S, cost, lits = S2, cost2 + len(S2) * self.wneg, lits2
            if cost < bestw:
                bestw = cost
                best = [("n", v, c[v]) for v in sorted(S)] + lits
        return best

    def ycost(self, X, t):
        """-log P(|L & X| < t) for a uniform random k-subset L of [q], |X| = X."""
        key = (X, t)
        if key not in self._yc:
            q, k = self.q, self.k
            p = sum(math.comb(X, j) * math.comb(q - X, k - j) for j in range(t)) / math.comb(q, k)
            self._yc[key] = -math.log(p) if p > 0 else math.inf
        return self._yc[key]

    def peel_cost(self, L, c, S):
        k, adj = self.k, self.adj
        D = set(range(self.N)) - S
        X = {w: frozenset(c[u] for u in adj[w] if u in S) for w in D}
        deg = {w: len(adj[w] & D) for w in D}
        rem, cost, lits = set(D), 0.0, []
        while rem:
            w = next((w for w in rem if k - len(X[w]) >= deg[w] + 1), None)
            if w is None:
                if not self.glits:
                    return False, None, None
                cand = [(self.ycost(len(X[w]), k - deg[w]), w) for w in rem
                        if deg[w] <= k - 1 and len(set(L[w]) - X[w]) >= deg[w] + 1]
                if not cand:
                    return False, None, None
                cw, w = min(cand)
                cost += cw
                lits.append(("y", w, sorted(X[w]), k - deg[w]))
            rem.discard(w)
            for u in adj[w]:
                if u in rem:
                    deg[u] -= 1
        return True, cost, lits

    def lit(self, x):
        if x[0] == "n":
            return -self.l[x[1], x[2]]
        _, w, X, t = x
        X = tuple(X)
        if len(X) == 1 and t == 1:
            return self.l[w, X[0]]
        key = ("y", w, X, t)
        if key not in self.yvar:
            y = self.yvar[key] = self.pool.id(key)
            # y -> |L(w) & X| >= t : every (|X|-t+1)-subset of X meets L(w)
            for Y in itertools.combinations(X, len(X) - t + 1):
                self.master.add_clause([-y] + [self.l[w, a] for a in Y])
        return self.yvar[key]

    def add_cut(self, cl):
        self.master.add_clause([self.lit(x) for x in cl])
        self.cuts.append(cl)
        self.stats["cuts"] += 1
        self.stats["lits"] += len(cl)

    # ------------------------------------------------------------------ main loop
    def run(self, time_limit=None, ckpt=None, every=2000, report=1000):
        t0 = time.time()
        N, q = self.N, self.q
        while True:
            if time_limit and time.time() - t0 > time_limit:
                self.log(f"UNFINISHED: time limit, iters={self.stats['iters']} "
                         f"cuts={self.stats['cuts']} t={time.time() - t0:.0f}s")
                self.dump(ckpt)
                return "unfinished", None
            if not self.master.solve():
                self.log(f"NONE: master UNSAT after iters={self.stats['iters']} "
                         f"cuts={self.stats['cuts']} t={time.time() - t0:.1f}s")
                self.dump(ckpt)
                return "none", None
            mod = set(t for t in self.master.get_model() if t > 0)
            L = [[a for a in range(q) if self.l[v, a] in mod] for v in range(N)]
            self.stats["iters"] += 1
            cs = self.colourings(L, self.diverse)
            if not cs:
                self.log(f"FOUND candidate bad assignment after iters={self.stats['iters']} "
                         f"t={time.time() - t0:.1f}s: {L}")
                return "found", L
            for c in cs:
                assert is_proper_list_colouring(N, self.E, L, c)
                cl = self.cut_from(L, c)
                assert verify_cut(self.N, self.E, self.k, cl), cl
                assert not cut_holds(cl, L), "cut does not exclude current L"
                self.add_cut(cl)
            it = self.stats["iters"]
            if report and it % report == 0:
                self.log(f"  iters={it} cuts={self.stats['cuts']} avg_cut_len="
                         f"{self.stats['lits'] / self.stats['cuts']:.2f} t={time.time() - t0:.0f}s")
            if ckpt and it % every == 0:
                self.dump(ckpt)

    def dump(self, ckpt):
        if not ckpt:
            return
        tmp = ckpt + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"stats": self.stats, "cuts": self.cuts}, f)
        os.replace(tmp, ckpt)

    def load(self, ckpt):
        with open(ckpt) as f:
            d = json.load(f)
        for cl in d["cuts"]:
            self.add_cut([tuple(x) for x in cl])
        self.stats["iters"] = d["stats"]["iters"]
        self.log(f"resumed {len(d['cuts'])} cuts from {ckpt}")


def build(kind, a, b):
    if kind == "torus":
        return torus(a, b)
    if kind == "kab":
        return complete_bipartite(a, b)
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["torus", "kab"])
    ap.add_argument("a", type=int)
    ap.add_argument("b", type=int)
    ap.add_argument("q", type=int)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--colsym", action="store_true")
    ap.add_argument("--fix0", action="store_true")
    ap.add_argument("--gsym", action="store_true")
    ap.add_argument("--crit", action="store_true")
    ap.add_argument("--overlap", action="store_true")
    ap.add_argument("--shrink", action="store_true")
    ap.add_argument("--glits", action="store_true")
    ap.add_argument("--diverse", type=int, default=1)
    ap.add_argument("--tries", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--time-limit", type=float)
    ap.add_argument("--ckpt")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--report", type=int, default=1000)
    ap.add_argument("--log")
    A = ap.parse_args()
    N, E = build(A.kind, A.a, A.b)
    f = open(A.log, "a") if A.log else None

    def log(s):
        print(s, flush=True)
        if f:
            f.write(s + "\n")
            f.flush()

    log(f"=== {' '.join(sys.argv[1:])}")
    log(f"graph {A.kind} {A.a} {A.b}: N={N} |E|={len(E)} q={A.q} k={A.k}")
    gs = (A.a, A.b) if (A.gsym and A.kind == "torus") else None
    S = Search(N, E, A.q, A.k, A.colsym, A.fix0, gs, A.crit, A.overlap, A.shrink, A.glits,
               A.diverse, A.tries, A.seed, log=log)
    if A.resume and A.ckpt and os.path.exists(A.ckpt):
        S.load(A.ckpt)
    res, L = S.run(A.time_limit, A.ckpt, report=A.report)
    if res == "found":
        c = colour_backtrack(N, E, L)
        log(f"independent backtracking check: {'COLOURABLE (bug!)' if c else 'NOT colourable'}")
        log(f"lists sizes ok: {all(len(set(x)) == A.k for x in L)}")
    log(f"RESULT {res} iters={S.stats['iters']} cuts={S.stats['cuts']}")


if __name__ == "__main__":
    main()
