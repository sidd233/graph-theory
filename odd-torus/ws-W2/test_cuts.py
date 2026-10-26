"""Direct test of cut validity, independent of verify_cuts.py's proof.

For every cut stored in a checkpoint (and for each of a few random images under the symmetry
maps), sample list assignments L that FALSIFY the cut, uniformly-ish (premise lists are built
to contain the fixed colour, literal vertices get lists violating their literal), and check by
plain backtracking (graphs.colour_backtrack) that each sampled L is colourable. One failure
means the cut generation is unsound.

Exhaustive mode (C3xC3 etc.): enumerate ALL falsifying L of each cut.

Run: python test_cuts.py torus M N Q CKPT [samples] [--exhaustive]
"""
import itertools
import json
import random
import sys

from graphs import colour_backtrack, torus, torus_automorphisms

kind, m, n, q, ck = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
samples = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6].isdigit() else 200
exhaustive = "--exhaustive" in sys.argv
k = 3
N, E = torus(m, n)
cuts = json.load(open(ck))["cuts"]
auts = torus_automorphisms(m, n)
rng = random.Random(5)
subs = [frozenset(s) for s in itertools.combinations(range(q), k)]


def options(cut):
    """For each vertex, the k-lists compatible with the cut being false."""
    opt = {v: list(subs) for v in range(N)}
    for x in cut:
        if x[0] == "n":
            opt[x[1]] = [s for s in opt[x[1]] if x[2] in s]
        else:
            opt[x[1]] = [s for s in opt[x[1]] if len(s & set(x[2])) < x[3]]
    return opt


tested = bad = 0
lens = []
for ci, cut in enumerate(cuts):
    lens.append(len(cut))
    imgs = [cut]
    for p in rng.sample(auts, 3):
        cperm = list(range(q))
        rng.shuffle(cperm)
        imgs.append([("n", p[x[1]], cperm[x[2]]) if x[0] == "n"
                     else ("y", p[x[1]], sorted(cperm[a] for a in x[2]), x[3]) for x in cut])
    for img in imgs:
        opt = options(img)
        if exhaustive:
            Ls = itertools.product(*[opt[v] for v in range(N)])
        else:
            Ls = ([rng.choice(opt[v]) for v in range(N)] for _ in range(samples))
        for L in Ls:
            tested += 1
            if colour_backtrack(N, E, [sorted(s) for s in L]) is None:
                bad += 1
                print("INVALID CUT", cut, "L=", [sorted(s) for s in L], flush=True)
                break
print(f"test_cuts {kind} {m} {n} q={q} {ck}: {len(cuts)} cuts (x4 images), cut length "
      f"min/avg/max {min(lens)}/{sum(lens) / len(lens):.2f}/{max(lens)}, {tested} falsifying "
      f"assignments tested{' (exhaustive)' if exhaustive else ''}, {bad} not colourable")
