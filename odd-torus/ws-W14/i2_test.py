"""Test (I''): every failing hole is a local generalized sea or a local seam (lists constant along rows
on each side of one column boundary, inside the hole). Run: python i2_test.py FILES"""
import sys
from sea_test_lib import generalized_sea, parse
# hole vertex -> (row offset, column offset): block 0..5, border 6..15
pos={0:(-1,0),1:(0,0),2:(1,0),3:(-1,1),4:(0,1),5:(1,1),6:(-1,-1),7:(0,-1),8:(1,-1),9:(2,0),10:(3,0),11:(2,1),12:(3,1),13:(-1,2),14:(0,2),15:(1,2)}
def local_seam(lists):
    at={pos[v]:lists[v] for v in range(16)}
    rows={}
    for (r,c),L in at.items(): rows.setdefault(r,{})[c]=L
    for cut in (None,-1,0,1):          # seam between column cut and cut+1 (None: no seam, rows constant)
        ok=True
        for r,cs in rows.items():
            for c in cs:
                for d in cs:
                    same_side = cut is None or (c<=cut)==(d<=cut)
                    if same_side and cs[c]!=cs[d]: ok=False
        if ok: return cut
    return 'none'
H=[]
for f in sys.argv[1:]: H+=parse(open(f).read())
sea=seam=both=neither=0; bad=[]
for h in H:
    s=generalized_sea(h) is not None; m=local_seam(h)!='none'
    if s and m: both+=1
    elif s: sea+=1
    elif m: seam+=1
    else: neither+=1; bad.append(h)
print(f'failing holes: {len(H)}; sea only {sea}, seam only {seam}, both {both}, NEITHER {neither}')
for h in bad[:3]: print('  neither:', [''.join(map(str,sorted(x))) for x in h])
