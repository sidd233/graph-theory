# TikZ figure: C3 x C7 orientation for a non-Latin p, with the explicit odd induced cycle.
from core3 import construct
from core3 import third
p=(0,1,2,0,1,0,2); n=len(p)   # non-Latin
b=construct(p); A=[third(p[i],p[(i+1)%n]) for i in range(n)]
gad=[c for c in range(n) if b[c]!=A[c]][0]
X=1.45; Y=1.25
def pos(r,c): return (c*X, -r*Y)
cyc=set(); arcs_c=[]
for c in range(n):
    a=b[(c-1)%n]; x=b[c]
    cyc.add((a,c)); cyc.add((x,c))
    if a!=x: arcs_c.append(((a,c),(x,c)))
L=[r"\begin{tikzpicture}[>=Stealth,v/.style={circle,draw,inner sep=1.2pt,minimum size=15pt,font=\scriptsize}]"]
for c in range(n):
    T,S=p[(c-1)%n],p[c]; M=3-T-S; role={T:'T',S:'S',M:'M'}
    for r in range(3):
        x,y=pos(r,c); hl=(r,c) in cyc
        L.append(rf"\node[v{',fill=red!15,draw=red!70!black,thick' if hl else ''}] (v{r}{c}) at ({x:.2f},{y:.2f}) {{{role[r]}}};")
    L.append(rf"\node[font=\scriptsize] at ({c*X:.2f},0.7) {{$c={c}$}};")
    L.append(rf"\node[font=\scriptsize,text=blue!60!black] at ({(c+0.5)*X:.2f},{-2*Y-0.75:.2f}) {{$p_{c}={p[c]}$}};")
# column arcs (S->M, S->T, M->T)
for c in range(n):
    T,S=p[(c-1)%n],p[c]; M=3-T-S
    for u,v in ((S,M),(S,T),(M,T)):
        used=((u,c),(v,c)) in arcs_c
        style="red!70!black,very thick" if used else "gray!60"
        bend="" if abs(u-v)==1 else (",bend left=40" )
        L.append(rf"\draw[->,{style}{bend}] (v{u}{c}) to (v{v}{c});")
# row arcs
for c in range(n):
    for r in range(3):
        right = (r!=p[c])
        used = (b[c]==r)
        style="red!70!black,very thick" if used else "gray!60"
        if c<n-1:
            s,t=(f"v{r}{c}",f"v{r}{c+1}") if right else (f"v{r}{c+1}",f"v{r}{c}")
            L.append(rf"\draw[->,{style}] ({s}) -- ({t});")
        else:
            # wrap-around edge to column 0: draw stubs
            x,y=pos(r,c)
            if right:
                L.append(rf"\draw[->,{style}] (v{r}{c}) -- ({x+0.75*X:.2f},{y:.2f}) node[right,font=\tiny]{{to $c\!=\!0$}};")
            else:
                L.append(rf"\draw[<-,{style}] (v{r}{c}) -- ({x+0.75*X:.2f},{y:.2f}) node[right,font=\tiny]{{from $c\!=\!0$}};")
for r in range(3):
    L.append(rf"\node[font=\scriptsize] at ({-0.9:.2f},{-r*Y:.2f}) {{row {r}}};")
L.append(r"\end{tikzpicture}")
open('fig_cycle.tex','w').write("\n".join(L))
steps=sum(1 for c in range(n) if b[(c-1)%n]!=b[c])
print("p=",p,"rule A b=",A,"constructed b=",b,"gadget at c=",gad,"cycle length",n+steps)
