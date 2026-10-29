# Check the plan's "midpoint rule" against W7's exact strip data for m = 5:
# shape = pin one row (mu=2) at one end, mu=1 at every row of the other end except p, q.
from collections import defaultdict
D=defaultdict(dict)
for line in open('/home/sid/work/gt/odd-torus/ws-W7/strip5_A_l2-27.txt'):
    if line.startswith('#'): continue
    l,a,b,v=line.split(); D[(a,b)][int(l)]=int(v)
m=5; bad=0; n=0
for (a,b),d in D.items():
    for pin,dele in ((a,b),(b,a)):
        if sorted(pin)!=['0']*4+['2'] or sorted(dele)!=['0','0','1','1','1']: continue
        r=pin.index('2'); p,q=[i for i in range(m) if dele[i]=='0']
        for l,v in d.items():
            pred_zero = (l%2==1) and (2*r-p-q)%m==0
            n+=1
            if (v==0)!=pred_zero: bad+=1; print('MISMATCH',l,a,b,v)
print(f'checked {n} (shape, l) pairs, l = 2..27, mismatches {bad}')
