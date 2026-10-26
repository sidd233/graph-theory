# Number of orientations of C_m x C_n with every out-degree exactly 2 ("admissible"), by a
# transfer matrix. Independent of the backtracking enumerator eulerian_orientations() in
# orch/kp.py, which produced the orchestrator's counts.
# State between columns c and c+1: bit r = 1 iff the row arc is (r,c) -> (r,c+1).
# T[a][b] = number of orientations of the column cycle C_m (column c, left boundary a,
# right boundary b) with out-degree of (r,c) equal to 2 - [b_r = 1] - [a_r = 0].
# Count = trace(T^n), exact integers.
# Run: ../env/bin/python count_orient.py   (from odd-torus/ws-W5)
from itertools import product

def transfer(m):
    T = [[0] * (1 << m) for _ in range(1 << m)]
    cyc = list(product((0, 1), repeat=m))   # bit r = 1 iff column arc (r) -> (r+1)
    colout = []
    for o in cyc:
        d = [0] * m
        for r in range(m):
            d[r if o[r] else (r + 1) % m] += 1
        colout.append(tuple(d))
    for a in range(1 << m):
        for b in range(1 << m):
            need = tuple(2 - ((b >> r) & 1) - (1 - ((a >> r) & 1)) for r in range(m))
            T[a][b] = sum(1 for d in colout if d == need)
    return T

def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def count(m, n):
    T = transfer(m)
    P = T
    for _ in range(n - 1):
        P = mat_mul(P, T)
    return sum(P[i][i] for i in range(len(P)))

orch = {(3, 3): 148, (3, 5): 2116, (3, 7): 33028, (3, 9): 525316, (5, 5): 143224}
for (m, n), claimed in orch.items():
    c = count(m, n)
    print(f"C{m} x C{n}: transfer-matrix count {c}, orchestrator {claimed}: {'agree' if c == claimed else 'DISAGREE'}")
# symmetry sanity check: C_m x C_n and C_n x C_m must give the same count
for m, n in [(3, 4), (3, 5), (4, 5), (3, 7)]:
    print(f"symmetry C{m} x C{n} = {count(m, n)}, C{n} x C{m} = {count(n, m)}")
