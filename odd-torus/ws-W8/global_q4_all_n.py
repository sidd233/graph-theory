"""Enumerate ALL evading assignments of C5 x Cn, n = (palette 4) from global_q4.py and summarise
their structure: how many rows are non-constant, and whether the constant rows share one list.
Run: python global_q4_all.py"""
from collections import Counter
exec(open('global_q4.py').read().split('def search(n):')[0])
import sys; n = int(sys.argv[1]) if len(sys.argv) > 1 else 5; sols = []
seq = []
def go():
    if len(seq) == n:
        if all(trig_ok(seq[(j-1) % n], seq[j], seq[(j+1) % n], seq[(j+2) % n]) for j in range(n)) \
           and len(set(seq)) > 1 and not all(len(set(c)) == 1 for c in seq):
            sols.append(tuple(seq))
        return
    for c in dom:
        seq.append(c); k = len(seq)
        if k < 4 or trig_ok(seq[k-4], seq[k-3], seq[k-2], seq[k-1]): go()
        seq.pop()
go()
print('evading assignments of C5 x Cn, n = ', n, '(palette 4):', len(sols))
def shape(s):
    rows = [tuple(c[r] for c in s) for r in range(5)]
    nonconst = [r for r in range(5) if len(set(rows[r])) > 1]
    constlists = {rows[r][0] for r in range(5) if r not in nonconst}
    return (len(nonconst), len(constlists))
print('(non-constant rows, distinct lists on constant rows):', Counter(shape(s) for s in sols))
