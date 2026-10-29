"""Neighbourhood of the 184 real-alpha bad windows (palette 4): change one or two of the ten lists
to any 3-subset of a 6-colour palette. Writes candidate windows (hex, L1 then L2), deduplicated.
Run: python nbhd.py K  (K = 1 or 2 changed lists)"""
import itertools, sys
K = int(sys.argv[1])
base = [[int(h, 16) for h in l.split()[1:6] + l.split()[7:12]] for l in open('all_q4_stillbad_real.txt')]
subsets = [sum(1 << c for c in t) for t in itertools.combinations(range(6), 3)]
seen = set()
for w in base:
    for pos in itertools.combinations(range(10), K):
        for vals in itertools.product(subsets, repeat=K):
            v = list(w)
            for p, x in zip(pos, vals): v[p] = x
            t = tuple(v)
            if t in seen: continue
            seen.add(t)
            if bin(sum(1 << i for i in range(6) if any(x >> i & 1 for x in t))).count('1') >= 5:
                print(' '.join(format(x, 'x') for x in t))
