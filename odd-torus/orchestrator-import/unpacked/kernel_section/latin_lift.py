# Orientation of C3 x C_{3k} lifted from a Latin square on {S,M,T}:
# column: S->M, S->T, M->T ; row: arc from higher to lower row-rank, T > M > S.
from itertools import permutations
from automaton import *
RANK={'S':0,'M':1,'T':2}
def latin_squares():
    out=[]
    for a in permutations('SMT'):
        for b in permutations('SMT'):
            for c in permutations('SMT'):
                rows=[(a[r],b[r],c[r]) for r in range(3)]
                if all(len(set(x))==3 for x in rows): out.append((a,b,c))   # columns a,b,c
    return out
def column_arcs(col):  # col[r] = type of row r
    arcs=set()
    for r in ROWS:
        for s in ROWS:
            if r!=s and RANK[col[r]]<RANK[col[s]]: arcs.add((r,s))  # S->M, S->T, M->T (lower col-rank first)
    return arcs
def row_arcs(colL,colR):
    return {r:(+1 if RANK[colL[r]]>RANK[colR[r]] else -1) for r in ROWS}
