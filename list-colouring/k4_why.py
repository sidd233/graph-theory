"""Why K_4 blocks the kernel method.

L(K_4) is the octahedron: 6 vertices, 12 edges, 4-regular.  chi'(K_4) = 3, so the
kernel method needs Delta+ <= 2.  With 12 arcs on 6 vertices the average out-degree
is exactly 2, so EVERY vertex must have out-degree exactly 2.  A directed triangle
has no kernel, so every triangle must come out transitive.
"""
from itertools import combinations
from galvin import line_graph, kernel_perfect, has_kernel
pc = int.bit_count

edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
adj, m = line_graph(edges, 4)
pairs = [(i, j) for i in range(m) for j in range(i + 1, m) if (adj[i] >> j) & 1]
tris = [(a, b, c) for a, b, c in combinations(range(m), 3)
        if (adj[a] >> b) & 1 and (adj[b] >> c) & 1 and (adj[a] >> c) & 1]
print(f"L(K_4): {m} vertices, {len(pairs)} edges, {len(tris)} triangles, "
      f"degrees {[pc(a) for a in adj]}")

thin = cyclic_tri = kp = 0
for code in range(1 << len(pairs)):
    out = [0] * m
    for t, (i, j) in enumerate(pairs):
        if (code >> t) & 1: out[i] |= 1 << j
        else:               out[j] |= 1 << i
    if max(pc(x) for x in out) > 2:
        continue
    thin += 1
    bad = any(((out[a] >> b) & 1 and (out[b] >> c) & 1 and (out[c] >> a) & 1) or
              ((out[a] >> c) & 1 and (out[c] >> b) & 1 and (out[b] >> a) & 1)
              for a, b, c in tris)
    if bad:
        cyclic_tri += 1
    elif kernel_perfect(out, adj, m):
        kp += 1
print(f"orientations with Delta+ <= 2: {thin}")
print(f"   of those, containing a directed triangle (so no kernel): {cyclic_tri}")
print(f"   of those, kernel-perfect: {kp}")
print(f"\nevery thin orientation of L(K_4) contains a directed triangle: "
      f"{cyclic_tri == thin}")
