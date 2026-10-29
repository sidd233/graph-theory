import sys
from kp import torus, eulerian_orientations, build, kernel_perfect
from indcyc import find_induced_odd_dicycle

def lift(base_arcs, m, nb, n):
    # base: C_m x C_nb with idx r*nb+c ; lift to C_m x C_n (nb | n) via c -> c mod nb
    barc=set(base_arcs)
    N,E=torus(m,n); arcs=[]
    for a,b in E:
        ra,ca=divmod(a,n); rb,cb=divmod(b,n)
        A=ra*nb+ca%nb; B=rb*nb+cb%nb
        arcs.append((a,b) if (A,B) in barc else (b,a))
    return arcs

m=3
N3,E3=torus(3,3)
kp33=[]
for arcs in eulerian_orientations(N3,E3):
    out,adj=build(N3,arcs)
    if kernel_perfect(N3,out,adj)[0]: kp33.append(arcs)
print("C3xC3 kernel-perfect orientations:",len(kp33))
for n in (9,15,21):
    N,E=torus(3,n); good=0
    for b in kp33:
        arcs=lift(b,3,3,n); out,adj=build(N,arcs)
        assert all(bin(o).count('1')==2 for o in out)
        if find_induced_odd_dicycle(N,out,adj) is None: good+=1
    print(f"lifts to C3xC{n}: {good}/12 have no induced odd directed cycle")
# also lifts to C9 x C9? (both coordinates)
