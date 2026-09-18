from fractions import Fraction
from sweep import classes, survives, make_f, acyclic
pc = int.bit_count

def props(adj, n):
    tri = any((adj[u] >> v) & 1 and adj[u] & adj[v] for u in range(n) for v in range(n) if u < v)
    col = [-1]*n; bip = True
    for s in range(n):
        if col[s] >= 0: continue
        col[s] = 0; st = [s]
        while st:
            v = st.pop(); m = adj[v]
            while m:
                b = m & -m; u = b.bit_length()-1
                if col[u] < 0: col[u] = 1-col[v]; st.append(u)
                elif col[u] == col[v]: bip = False
                m ^= b
    return tri, bip

n = 6
pool = list(classes(n))
for lam in [Fraction(3,4), Fraction(2,3), Fraction(1,2)]:
    f = make_f(lam)
    s = [a for a in pool if survives(a, n, f)]
    nb = [a for a in s if not props(a, n)[1]]
    nt = [a for a in s if props(a, n)[0]]
    fo = [a for a in s if acyclic(a, n)]
    mx = max((max(pc(x) for x in a) for a in s), default=0)
    print(f"lam={lam}: {len(s)} survive | forests {len(fo)} | non-bipartite {len(nb)}"
          f" | with a triangle {len(nt)} | max Delta among survivors {mx}")
    if nb:
        print("      non-bipartite survivors, degree sequences:",
              sorted(tuple(sorted(pc(x) for x in a)) for a in nb)[:6])
