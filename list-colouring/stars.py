"""Lemma: kernel-perfectness forces a LINEAR ORDER at each vertex of G.

The edges at a vertex v of G form a clique in L(G).  In a clique, a kernel must be
a single vertex with no out-arc inside the clique, i.e. a SINK.  Kernel-perfectness
asks every induced subgraph to have a kernel, so EVERY SUBSET of that clique must
have a sink.  A tournament in which every subset has a sink is exactly a transitive
tournament.  Hence the orientation restricted to the edges at v is a linear order.

That is precisely the shape of Galvin's construction (order by Latin square entry),
so his choice was not a convenience: any kernel-perfect orientation must look like
that at every vertex.  Verified on all tournaments up to 6 vertices.
"""
from itertools import combinations, permutations
pc = int.bit_count

def every_subset_has_sink(out, k):
    for S in range(1, 1 << k):
        ok = False
        m = S
        while m:
            b = m & -m
            if not (out[b.bit_length() - 1] & S):
                ok = True; break
            m ^= b
        if not ok:
            return False
    return True

def transitive(out, k):
    for a in range(k):
        for b in range(k):
            for c in range(k):
                if (out[a] >> b) & 1 and (out[b] >> c) & 1 and not (out[a] >> c) & 1:
                    return False
    return True

print("tournaments: does 'every subset has a sink' coincide with 'transitive'?")
for k in range(2, 7):
    pairs = list(combinations(range(k), 2))
    same = tot = 0
    for code in range(1 << len(pairs)):
        out = [0] * k
        for t, (i, j) in enumerate(pairs):
            if (code >> t) & 1: out[i] |= 1 << j
            else:               out[j] |= 1 << i
        tot += 1
        if every_subset_has_sink(out, k) == transitive(out, k):
            same += 1
    print(f"  k={k}: {same}/{tot} agree  "
          f"{'(identical)' if same == tot else '(DIFFER)'}")
