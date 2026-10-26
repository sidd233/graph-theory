# PROOF SCRIPT. For each of the 12 Latin-square orientations: compute the full set of pairs
# (product matrix, parity of number of 3-column blocks), closed under right multiplication by
# generators. Every induced subdigraph of the lift on C3 x C_{3k} is a product of k generators.
# Claim proved if no pair (X, odd) has zero trace: then for every odd k every induced subdigraph
# of the lift has a kernel.
from automaton import *
from latin_lift import *
allok=True
for t,L in enumerate(latin_squares()):
    Ms=[{U:trans(column_arcs(L[p]), row_arcs(L[(p-1)%3],L[p]), U) for U in subsets()} for p in range(3)]
    gens=set(mul(mul(A,B),C) for A in Ms[0].values() for B in Ms[1].values() for C in Ms[2].values())
    seen=set((g,1) for g in gens); stack=list(seen)
    while stack:
        X,par=stack.pop()
        for g in gens:
            Y=(mul(X,g),1-par)
            if Y not in seen: seen.add(Y); stack.append(Y)
    odd_bad=sum(1 for X,par in seen if par==1 and not trace(X))
    even_bad=sum(1 for X,par in seen if par==0 and not trace(X))
    allok &= odd_bad==0
    print(f"square #{t}: closure size {len(seen)}; zero-trace products with odd k: {odd_bad}; with even k: {even_bad}")
print("RESULT: lifts kernel-perfect on C3 x C_{3k} for every odd k:", allok)
