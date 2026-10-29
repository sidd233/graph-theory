# Local obstructions. For a linear word w (consecutive columns), w is LOCALLY BAD if some induced
# subdigraph H using only these columns has no kernel. Columns outside H are empty, so the run
# starts at state (None, {}) and must end with no pending vertex.
# R-sets: for each choice of present rows, the set of reachable automaton states.
import sys, itertools
from words import *
LI=range(len(LETTERS)); SUBS=subsets()
ADJ={(a,b):rowarc(LETTERS[a],LETTERS[b]) is not None for a in LI for b in LI}
START=1<<IDX[(None,frozenset())]
OKEND=0
for i,(K,P) in enumerate(STATES):
    if not P: OKEND|=1<<i
# first column of a window: no K, no pending to the left, so row arcs from the left are irrelevant;
# use any consistent predecessor letter (result does not depend on it from START).
def post(R,M):
    out=0; x=R
    while x:
        i=(x&-x).bit_length()-1; x&=x-1; out|=M[i]
    return out
MAT={(a,b):[colmat(LETTERS[a],LETTERS[b],U) for U in SUBS] for a in LI for b in LI if ADJ[(a,b)]}
pred={b:next(a for a in LI if ADJ[(a,b)]) for b in LI}
def latin_periodic(w):
    for i in range(len(w)-2):
        tps=[LETTERS[w[i+j]][0] for j in range(3)]
        if any(len({tps[j][r] for j in range(3)})<3 for r in ROWS): return False
    return all(w[i]==w[i+3] for i in range(len(w)-3))
L=int(sys.argv[1])
# BFS over linear words, tracking the set of reachable R's
frontier={}
for b in LI:
    Rs=frozenset(post(START,M) for M in MAT[(pred[b],b)])
    frontier[(b,)]=Rs
bad_words=0
for length in range(1,L+1):
    nb=sum(1 for w,Rs in frontier.items() if any((R&OKEND)==0 for R in Rs))
    good=[w for w,Rs in frontier.items() if all((R&OKEND)!=0 for R in Rs)]
    nonlatin=[w for w in good if not latin_periodic(w)]
    print(f"length {length}: words {len(frontier)}, locally bad {nb}, not bad {len(good)}, not bad AND not Latin-periodic {len(nonlatin)}",flush=True)
    if length==L: 
        if nonlatin: print("  e.g.", [LETTERS[x] for x in nonlatin[0]])
        break
    nf={}
    for w,Rs in frontier.items():
        if any((R&OKEND)==0 for R in Rs): continue       # already bad: extensions are bad too
        a=w[-1]
        for b in LI:
            if not ADJ[(a,b)]: continue
            nRs=set()
            for R in Rs:
                for M in MAT[(a,b)]: nRs.add(post(R,M))
            # also a fresh start inside the window (H may begin here): post(START, M)
            for M in MAT[(a,b)]: nRs.add(post(START,M))
            nf[w+(b,)]=frozenset(nRs)
    frontier=nf
