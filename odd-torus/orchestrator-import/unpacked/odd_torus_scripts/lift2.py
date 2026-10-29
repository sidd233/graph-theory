from kp import torus, eulerian_orientations, build, kernel_perfect
def lift2(base_arcs, mb, nb, m, n):
    barc=set(base_arcs); N,E=torus(m,n); arcs=[]
    for a,b in E:
        ra,ca=divmod(a,n); rb,cb=divmod(b,n)
        A=(ra%mb)*nb+ca%nb; B=(rb%mb)*nb+cb%nb
        arcs.append((a,b) if (A,B) in barc else (b,a))
    return N,arcs
def kp33():
    N3,E3=torus(3,3)
    return [a for a in eulerian_orientations(N3,E3) if kernel_perfect(N3,*build(N3,a))[0]]
if __name__=='__main__':
    K=kp33()
    # describe the rule: f(r,c)=(r+c)%3 or (r-c)%3 ?
    for a in K[:12]:
        rowarcs=[(u,v) for u,v in a if u//3==v//3]; colarcs=[(u,v) for u,v in a if u%3==v%3]
        print("row arcs:",sorted(rowarcs),"| col arcs:",sorted(colarcs))
