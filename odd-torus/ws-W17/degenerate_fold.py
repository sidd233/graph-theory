"""Degenerate case of the column-fold lemma. Block lists A_r = E + {x_r}, E = {e1, e2}, x a proper colouring
of the 5-cycle with x_r not in E. Neighbour columns U, V of the folded column satisfy U_r != x_r, V_r != x_r.
Only the TYPE of U_r matters: 'e1', 'e2' or 'o' (a colour not in A_r). Question: are there columns c1, c2, c3,
each a proper colouring of C5 with c_r in A_r, such that U ~ c1 ~ c2 ~ c3 ~ V (~ = different in every row)?
Exhaustive over all type vectors for U and V (U, V proper: no two adjacent rows both e1 or both e2).
Colours: e1 = 'E1', e2 = 'E2', x_r = ('x', r); 'o' never equals anything in A_r. Run: python degenerate_fold.py"""
import itertools
rows = range(5)
A = [['E1', 'E2', ('x', r)] for r in rows]
S = [c for c in itertools.product(*A) if all(c[r] != c[(r + 1) % 5] for r in rows)]
def compat_type(u, c): return all(not (u[r] != 'o' and u[r] == c[r]) for r in rows)
compat = lambda a, b: all(a[r] != b[r] for r in rows)
types = [t for t in itertools.product(['E1', 'E2', 'o'], repeat=5)
         if all(not (t[r] != 'o' and t[r] == t[(r + 1) % 5]) for r in rows)]
adj = {i: [j for j in range(len(S)) if compat(S[i], S[j])] for i in range(len(S))}
bad = 0
for U in types:
    C1 = [i for i in range(len(S)) if compat_type(U, S[i])]
    for V in types:
        C3 = set(i for i in range(len(S)) if compat_type(V, S[i]))
        ok = any(any(any(k in C3 for k in adj[j]) for j in adj[i]) for i in C1)
        if not ok:
            bad += 1
            if bad <= 3: print('NO PATH: U', U, 'V', V)
print(f'patterns in S: {len(S)}; U/V type pairs: {len(types)**2}; with no path U~c1~c2~c3~V: {bad}')
