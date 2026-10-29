# exploration: orbits of the zero classes under D5 (rows) x column reflection
from collections import defaultdict
D=defaultdict(dict)
for line in open('/home/sid/work/gt/odd-torus/ws-W7/strip5_A_l2-27.txt'):
    if line.startswith('#'): continue
    l,a,b,v=line.split(); D[(a,b)][int(l)]=int(v)
def rot(s,k): return s[k:]+s[:k]
def refl(s): return ''.join(s[(-r)%5] for r in range(5))
def images(S):
    a,b=S; out=set()
    for k in range(5):
        for f in (lambda x:x, refl):
            A,B=f(rot(a,k)),f(rot(b,k))
            out.add((A,B)); out.add((B,A))
    return out
def trivial(S):
    a,b=S
    k=sum(map(int,b))
    if k in (0,5): return 'k0/5'
    for s in (a,b):
        for r in range(5):
            if s[r]=='2' and s[(r+1)%5]=='2': return 'adj22'
    return None
for name,ls in (('odd',range(3,28,2)),('even',range(4,28,2))):
    Z={S for S,d in D.items() if all(d[l]==0 for l in ls)}
    inv=all(images(S)<=Z for S in Z)
    print(f"== {name}: |Z|={len(Z)}, G-invariant: {inv}")
    seen=set(); reps=defaultdict(list)
    for S in sorted(Z):
        if S in seen: continue
        orb=images(S); seen|=orb
        reps[trivial(S)].append((S,len(orb)))
    for t,L in reps.items():
        print(f"  {t}: {len(L)} orbits, {sum(n for _,n in L)} S")
        if t is None:
            for S,n in L: print("     ",S,'k=',sum(map(int,S[1])),'orbit',n)
