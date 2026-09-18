"""Theorem: a triangle kills Lemma 1 on any cubic class-1 graph.

Tight regime (Delta-regular, class 1): M(u,v) + M(v,u) = s = Delta - 1, and each row
of M is a permutation, so within a triangle ijk with p = M(i,j), q = M(j,k),
r = M(i,k) the row conditions force
        p != r      (rows i),      p + q != s   (row j),      q != r   (row k).
The triangle of L(G) is cyclic, hence kernelless, exactly when
        (p + q < s and r > p and r > q)  or  (p + q > s and r < p and r < q).
Enumerate every (p, q, r) for each s and see when an acyclic triangle is possible.
"""
print(f"{'s = Delta-1':>12} {'Delta':>6} {'acyclic triangles possible':>28}   witness")
for s in range(1, 8):
    good = []
    for p in range(s + 1):
        for q in range(s + 1):
            if p + q == s:
                continue
            for r in range(s + 1):
                if r == p or r == q:
                    continue
                cyc = ((p + q < s and r > p and r > q) or
                       (p + q > s and r < p and r < q))
                if not cyc:
                    good.append((p, q, r))
    w = f"(p,q,r) = {good[0]}" if good else "-- none, every triangle is cyclic --"
    print(f"{s:>12} {s+1:>6} {len(good):>28}   {w}")
print()
print("s = 2, i.e. Delta = 3, is the only case with NO acyclic triangle.")
print("So: G cubic and class 1 and containing a triangle  =>  Lemma 1 cannot prove it.")
print("Covers K_4 and the prism.  For Delta >= 4 a single triangle is locally fine,")
print("so the failures of K_6, K_8 and K_2,2,2 are global, not local.")
