# Explicit construction (the proof): rule A, then at the first c with
# p_c,p_{c+1},p_{c+2} distinct and p_{c+3} = p_{c+1}, set b_c = p_{c+1}.
from winding import proper_colourings, latin, orient
from verify_winding import check_cycle
from gadget import third
def construct(p):
    n=len(p); b=[third(p[i],p[(i+1)%n]) for i in range(n)]
    for c in range(n):
        if len({p[c],p[(c+1)%n],p[(c+2)%n]})==3 and p[(c+3)%n]==p[(c+1)%n]:
            b[c]=p[(c+1)%n]; return tuple(b)
    return None
for n in (5,7,9,11,13,15,17):
    tot=ok=0
    for p in proper_colourings(n):
        if latin(p): continue
        tot+=1; b=construct(p)
        if b is not None and check_cycle(p,b): ok+=1
    print(f"n={n}: non-Latin proper colourings {tot}; explicit cycle is an induced odd directed cycle in the real digraph: {ok}",flush=True)
