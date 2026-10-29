from coeff import coeff
import sys
# minimum |c_w| over all w off the cycle of e, for col and row edges
for m,n in [(5,7),(5,9),(5,11),(7,5),(7,7)]:
    out=[]
    for name,e in [('col',('col',0,0)),('row',('row',0,0))]:
        vals=[]
        for i in range(m):
            for j in range(n):
                on = (j==0) if name=='col' else (i==0)
                if on: continue
                if m==7 and n==7 and (i,j) not in [(1,1),(2,3),(3,3),(3,1),(6,4)]: continue
                vals.append(abs(coeff(m,n,e,(i,j))))
        out.append(f"{name}: min|c_w|={min(vals):.1f} over {len(vals)} w")
    print(f"C{m} x C{n}:", "; ".join(out), flush=True)
