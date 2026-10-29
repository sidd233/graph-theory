"""Profile failing holes that are local seas but not local seams: majority set X, defect positions,
defect count, whether defects touch (adjacent in the hole graph), outside-colour counts."""
import sys
from collections import Counter
from sea_test_lib import parse, adj
from i2_test import local_seam
names = ['aL','bL','cL','aR','bR','cR','p1','p2','p3','q1','q2','r1','r2','s1','s2','s3']
H = []
for f in ('failing_holes.txt', 'copy_out.txt', 'copy_out2.txt'): H += parse(open(f).read())
seaonly = [h for h in H if local_seam(h) == 'none']
print('sea-only failing holes:', len(seaonly))
cnt = Counter(); pos = Counter(); touch = 0; ocount = Counter(); inblock = 0
for h in seaonly:
    X = Counter(h).most_common(1)[0][0]
    D = [v for v in range(16) if h[v] != X]
    cnt[len(D)] += 1
    for v in D: pos[names[v]] += 1; ocount[len(h[v] - X)] += 1
    if any(w in D for v in D for w in adj[v]): touch += 1
    if any(v < 6 for v in D): inblock += 1
print('defects per hole:', sorted(cnt.items()))
print('defect positions:', pos.most_common())
print('holes with two adjacent defects:', touch, '; holes with a defect inside the block:', inblock)
print('outside colours per defect:', sorted(ocount.items()))
