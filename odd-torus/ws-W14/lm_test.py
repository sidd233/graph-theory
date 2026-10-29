"""Conjecture LM: a failing hole has a 3-colourable colour graph (colours adjacent iff they share a list
among the 16 hole lists). Test on every failing hole printed by the hole hunts. Run: python lm_test.py"""
import glob, itertools, re
def colour_graph_3col(lists):
    cols = sorted(set().union(*lists)); idx = {c: i for i, c in enumerate(cols)}
    adj = {c: set() for c in cols}
    for L in lists:
        for a, b in itertools.combinations(L, 2): adj[a].add(b); adj[b].add(a)
    col = {}
    def go(k):
        if k == len(cols): return True
        c = cols[k]
        for v in range(3):
            if all(col.get(d) != v for d in adj[c]):
                col[c] = v
                if go(k + 1): return True
                del col[c]
        return False
    return go(0)
holes = []
for f in glob.glob('*.txt') + glob.glob('*.out'):
    pass
import subprocess
out = subprocess.run(['bash', '-c', 'cat /tmp/claude-1000/-home-sid-work-gt/cde30492-dd50-44c8-ab73-c6c935f33432/tasks/*.output 2>/dev/null'], capture_output=True, text=True).stdout
for line in out.split('\n'):
    m = re.search(r'(?:VIOLATES H\*\*:|NO STRATEGY: block)\s*([0-9a-f ]+)\s*(?:\||border)\s*([0-9a-f ]+)', line)
    if m:
        bl = [int(h, 16) for h in m.group(1).split()]; br = [int(h, 16) for h in m.group(2).split()]
        if len(bl) == 6 and len(br) == 10:
            holes.append([frozenset(c for c in range(16) if x >> c & 1) for x in bl + br])
holes = list({tuple(h): h for h in holes}.values())
ok = sum(colour_graph_3col(h) for h in holes)
print(f'failing holes found in the logs: {len(holes)}; with 3-colourable colour graph: {ok}')
for h in holes:
    if not colour_graph_3col(h): print('  COUNTEREXAMPLE TO LM:', [sorted(x) for x in h])
