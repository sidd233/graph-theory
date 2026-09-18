"""Check the fast test against the definition on everything small."""
from itertools import combinations
from bkw import kernel_perfect_bkw
from galvin import kernel_perfect, line_graph
import random
pc = int.bit_count

rng = random.Random(7)
bad = 0; n_checked = 0
for trial in range(4000):
    m = rng.randint(3, 7)
    adj = [0]*m
    for i in range(m):
        for j in range(i+1, m):
            if rng.random() < 0.55:
                adj[i] |= 1 << j; adj[j] |= 1 << i
    out = [0]*m
    for i in range(m):
        for j in range(i+1, m):
            if (adj[i] >> j) & 1:
                if rng.random() < 0.5: out[i] |= 1 << j
                else:                  out[j] |= 1 << i
    n_checked += 1
    if kernel_perfect_bkw(out, adj, m) != kernel_perfect(out, adj, m):
        bad += 1
        if bad <= 3:
            print("  MISMATCH adj=", adj, "out=", out)
print(f"{n_checked} random digraphs: {bad} mismatches between the fast test and the definition")
print("NOTE: BKW applies to LINE graphs; random digraphs are a stress test of the code,")
print("      not of the theorem, so a mismatch here would flag a coding error.")
