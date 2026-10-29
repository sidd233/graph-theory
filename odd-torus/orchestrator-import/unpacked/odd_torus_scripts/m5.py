from coeff import coeff
import sys
m=int(sys.argv[1]); ns=[int(x) for x in sys.argv[2].split(',')]
for n in ns:
    for name,e in [('col',('col',0,0)),('row',('row',0,0))]:
        rows=[]
        for i in range(m):
            rows.append([round(abs(coeff(m,n,e,(i,j))),3) for j in range(n)])
        print(f"m={m} n={n} {name}-edge:")
        for i,r in enumerate(rows): print(f"  row {i}: {r}")
