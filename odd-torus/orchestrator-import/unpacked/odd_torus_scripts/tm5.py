import numpy as np, itertools
w=np.exp(2j*np.pi/3); R=[1,w,w*w]
for m in (3,5,7):
    S=[s for s in itertools.product(range(3),repeat=m) if all(s[r]!=s[(r+1)%m] for r in range(m))]
    X=np.array([[R[i] for i in s] for s in S])
    W=np.prod(X,axis=1)/3**m
    for r in range(m): W=W*(X[:,r]-X[:,(r+1)%m])
    Rm=np.ones((len(S),len(S)),dtype=complex)
    for r in range(m): Rm*=X[:,r][:,None]-X[:,r][None,:]
    T=W[:,None]*Rm
    ev=np.linalg.eigvals(T)
    vals=sorted(set((round(z.real,6),round(z.imag,6)) for z in ev))
    print(f"m={m}: {len(S)} column states; nonzero rank {np.linalg.matrix_rank(T,tol=1e-8)}; distinct eigenvalues ({len(vals)}):")
    print("   ",vals[:24], "..." if len(vals)>24 else "")
    print("    |eigenvalues|:",sorted(set(round(abs(complex(a,b)),6) for a,b in vals)))
