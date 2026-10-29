import numpy as np, itertools, sys
w3 = np.exp(2j*np.pi/3); R = [1, w3, w3**2]

def coeff(m, n, e, w):
    """c_w = coeff of x_w * prod_{v!=w} x_v^2 in P_{G-e}, G = C_m [] C_n, via
    Lason/Karasev-Petrov formula with A_v = cube roots of unity (Lemma 2.2/2.3).
    Vertex (r,c): row r in Z_m, column c in Z_n. Column edges (r,c)-(r+1,c), row edges (r,c)-(r,c+1).
    e = ('col', r, c) or ('row', r, c). Independent of the paper's transfer-matrix derivation."""
    S = list(itertools.product(range(3), repeat=m))          # column assignments, indices into R
    X = np.array([[R[i] for i in s] for s in S])               # |S| x m
    base = np.prod(X, axis=1) / 3**m                           # prod 1/N(a) = prod a/3
    def colw(c):
        wv = base.copy()
        for r in range(m):
            if e == ('col', r, c): continue
            wv = wv * (X[:, r] - X[:, (r+1) % m])
        if w[1] == c: wv = wv * X[:, w[0]]
        return wv
    def rowm(c):
        M = np.ones((len(S), len(S)), dtype=complex)
        for r in range(m):
            if e == ('row', r, c): continue
            M *= X[:, r][:, None] - X[:, r][None, :]
        return M
    P = np.eye(len(S), dtype=complex)
    for c in range(n):
        P = P @ (colw(c)[:, None] * rowm(c))
    return np.trace(P)

if __name__ == '__main__':
    m = int(sys.argv[1]); ns = [int(x) for x in sys.argv[2].split(',')]
    for n in ns:
        print(f"--- m={m}, n={n} ---")
        # column edge e={(0,0),(1,0)}
        res = {}
        for i in range(m):
            for j in range(n):
                res[(i,j)] = abs(coeff(m, n, ('col',0,0), (i,j)))
        print("col edge |c_w| by row i (columns 0..n-1):")
        for i in range(m): print(f"  row {i}:", [round(res[(i,j)],4) for j in range(n)])
        res = {}
        for i in range(m):
            for j in range(n):
                res[(i,j)] = abs(coeff(m, n, ('row',0,0), (i,j)))
        print("row edge |c_w| by row i:")
        for i in range(m): print(f"  row {i}:", [round(res[(i,j)],4) for j in range(n)])
