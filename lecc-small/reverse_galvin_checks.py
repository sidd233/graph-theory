"""Brute-force checks for latex/galvin-converse-regular.tex (the reverse direction of Galvin).

For each small graph G with maximum degree k, this script
  1. lists every orientation D of the line graph L(G) with every out-degree at most k - 1,
  2. tests each D for kernel-perfectness directly, by searching every induced subdigraph for a
     kernel (independent set S such that every vertex outside S has an out-arc into S),
  3. counts the proper edge colourings of G with colours 0, ..., k - 1 by backtracking,
  4. for the bipartite regular graphs, checks the rigidity theorem: every certificate equals
     the Galvin orientation of the colouring c(ab) = r_a(b), a in A,
  5. for K_4 and the prism, repeats 1 and 2 with out-degree at most k (one more colour).

It uses none of the lemmas proved in the document: no star lemma, no tightness, no odd rings.
Pure Python, no dependencies.

Run: python3 reverse_galvin_checks.py > data/reverse_galvin_checks.out   (about 30 seconds)
"""
from itertools import combinations


# ---------------------------------------------------------------- graphs
def cycle(n):
    return n, [(i, (i + 1) % n) for i in range(n)]


def complete(n):
    return n, list(combinations(range(n), 2))


def complete_bipartite(p, q):
    return p + q, [(i, p + j) for i in range(p) for j in range(q)]


def prism(n):
    """C_n box K_2: outer cycle 0..n-1, inner cycle n..2n-1, spokes i -- n+i."""
    outer = [(i, (i + 1) % n) for i in range(n)]
    inner = [(n + i, n + (i + 1) % n) for i in range(n)]
    spokes = [(i, n + i) for i in range(n)]
    return 2 * n, outer + inner + spokes


def cube():
    return 8, [(u, u ^ (1 << b)) for u in range(8) for b in range(3) if u < u ^ (1 << b)]


def petersen():
    """Outer 5-cycle 0..4, inner pentagram 5..9, spokes i -- 5+i."""
    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    spokes = [(i, 5 + i) for i in range(5)]
    return 10, outer + inner + spokes


def octahedron():
    """K_{2,2,2}: all pairs except the three antipodal pairs {u, u+3}."""
    return 6, [(u, v) for u, v in combinations(range(6), 2) if v != u + 3]


def diamond():
    """K_4 minus the edge 2-3: degrees 3, 3, 2, 2."""
    return 4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]


GRAPHS = [
    ("C_4", cycle(4)),
    ("C_5", cycle(5)),
    ("C_6", cycle(6)),
    ("K_4", complete(4)),
    ("K_{3,3}", complete_bipartite(3, 3)),
    ("prism K_3 x K_2", prism(3)),
    ("cube Q_3", cube()),
    ("C_5 x K_2", prism(5)),
    ("Petersen", petersen()),
    ("K_5", complete(5)),
    ("octahedron", octahedron()),
    ("diamond K_4 - e", diamond()),
]


def degrees(n, edges):
    d = [0] * n
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d


def bipartition(n, edges):
    """Return a 0/1 colouring if G is bipartite, else None (breadth-first search)."""
    nbr = [[] for _ in range(n)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    col = [None] * n
    for s in range(n):
        if col[s] is not None:
            continue
        col[s] = 0
        queue = [s]
        while queue:
            x = queue.pop()
            for y in nbr[x]:
                if col[y] is None:
                    col[y] = 1 - col[x]
                    queue.append(y)
                elif col[y] == col[x]:
                    return None
    return col


# ---------------------------------------------------------------- line graph
def line_graph(edges):
    """Pairs (i, j), i < j, of edges of G sharing an end, with the shared end."""
    pairs = []
    for i, j in combinations(range(len(edges)), 2):
        common = set(edges[i]) & set(edges[j])
        assert len(common) <= 1, "graph is not simple"
        if common:
            pairs.append((i, j, common.pop()))
    return pairs


def orientations(m, pairs, cap):
    """Every orientation of L(G) with all out-degrees <= cap, as a list of out-masks."""
    out = [0] * m
    deg = [0] * m
    found = []

    def go(t):
        if t == len(pairs):
            found.append(tuple(out))
            return
        i, j, _ = pairs[t]
        for a, b in ((i, j), (j, i)):
            if deg[a] < cap:
                deg[a] += 1
                out[a] |= 1 << b
                go(t + 1)
                out[a] &= ~(1 << b)
                deg[a] -= 1

    go(0)
    return found


def has_kernel(S, out, adj):
    """Does the subdigraph induced by the bitmask S have a kernel?"""
    K = S
    while True:  # enumerate submasks K of S, including the empty set last
        ok = True
        x = K
        while x:  # independence
            v = (x & -x).bit_length() - 1
            if adj[v] & K:
                ok = False
                break
            x &= x - 1
        if ok:
            x = S & ~K
            while x:  # every vertex outside K has an out-arc into K
                v = (x & -x).bit_length() - 1
                if not out[v] & K:
                    ok = False
                    break
                x &= x - 1
        if ok:
            return True
        if K == 0:
            return False
        K = (K - 1) & S


def kernel_perfect(m, out, adj, by_size):
    return all(has_kernel(S, out, adj) for S in by_size)


# ---------------------------------------------------------------- colourings
def proper_colourings(n, edges, k):
    """Every proper edge colouring with colours 0..k-1, as a tuple indexed like edges."""
    used = [set() for _ in range(n)]
    col = [None] * len(edges)
    found = []

    def go(t):
        if t == len(edges):
            found.append(tuple(col))
            return
        u, v = edges[t]
        for c in range(k):
            if c not in used[u] and c not in used[v]:
                used[u].add(c)
                used[v].add(c)
                col[t] = c
                go(t + 1)
                used[u].discard(c)
                used[v].discard(c)

    go(0)
    return found


def galvin_orientation(edges, pairs, side, c):
    """D_{c,A}: at a common end in A point to the smaller colour, in B to the larger."""
    out = [0] * len(edges)
    for i, j, w in pairs:
        if side[w] == 0:  # w in A
            a, b = (i, j) if c[i] > c[j] else (j, i)
        else:
            a, b = (i, j) if c[i] < c[j] else (j, i)
        out[a] |= 1 << b
    return tuple(out)


# ---------------------------------------------------------------- main
def main():
    print(f"{'graph':18} {'k':>2} {'reg':>4} {'bip':>4} {'#orient':>8} {'#out=k-1':>8} "
          f"{'#kp':>5} {'#col':>5}  rigidity")
    for name, (n, edges) in GRAPHS:
        d = degrees(n, edges)
        k = max(d)
        regular = min(d) == k
        side = bipartition(n, edges)
        m = len(edges)
        pairs = line_graph(edges)
        adj = [0] * m
        for i, j, _ in pairs:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
        by_size = sorted(range(1, 1 << m), key=lambda S: bin(S).count("1"))
        ors = orientations(m, pairs, k - 1)
        exact = sum(all(bin(o).count("1") == k - 1 for o in out) for out in ors)
        certs = [out for out in ors if kernel_perfect(m, out, adj, by_size)]
        cols = proper_colourings(n, edges, k)
        rig = "-"
        if regular and side is not None:
            galvin = {galvin_orientation(edges, pairs, side, c) for c in cols}
            rig = "ok" if set(certs) == galvin and len(galvin) == len(cols) else "FAIL"
        print(f"{name:18} {k:>2} {str(regular):>4} {str(side is not None):>4} {len(ors):>8} "
              f"{exact:>8} {len(certs):>5} {len(cols):>5}  {rig}")

    # One more colour: budget k + 1, that is out-degree at most k.
    print()
    print("out-degree at most k (lists of size k + 1):")
    for name, (n, edges) in [("K_4", complete(4)), ("prism K_3 x K_2", prism(3))]:
        k = max(degrees(n, edges))
        m = len(edges)
        pairs = line_graph(edges)
        adj = [0] * m
        for i, j, _ in pairs:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
        by_size = sorted(range(1, 1 << m), key=lambda S: bin(S).count("1"))
        ors = orientations(m, pairs, k)
        kp = sum(kernel_perfect(m, out, adj, by_size) for out in ors)
        print(f"{name:18} {k:>2}  #orient {len(ors)}  #kp {kp}")


if __name__ == "__main__":
    main()
