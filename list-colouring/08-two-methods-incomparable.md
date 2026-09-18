# 10. The two methods are incomparable, and that is the opening

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## The error being corrected

Earlier notes in this project claimed that every kernel-perfect orientation satisfies the
Alon-Tarsi condition `EE != EO`, and therefore that Alon-Tarsi is strictly stronger than
Lemma 1 of chapter 33. **That is false**, and the counterexample is Galvin's own construction.

## The counterexample: `S_3 = L(K_{3,3})`

Take the Latin square of chapter 33 and build Galvin's orientation of `S_3`: horizontally
from the smaller entry to the larger, vertically the other way. Computed directly
(`galvin_s3.py`):

```
out-degrees:      2 2 2 2 2 2 2 2 2      so Lemma 1 needs lists of size 3
kernel-perfect:   True                   so Lemma 1 gives chi_ell(S_3) <= 3
EE - EO:          0                      so Alon-Tarsi says NOTHING about it
```

And exhaustively, `AT(S_3) = 4`: **no** orientation of `S_3` with `Delta+ = 2` has
`EE != EO`. Since `chi_ell(S_3) = 3` by Galvin, Alon-Tarsi overshoots the truth here.

This matches the history. Alon and Tarsi could prove the Dinitz conjecture only for special
`n`; Galvin's kernel argument got all `n`. The obstruction for odd `n` is the Alon-Tarsi
conjecture on even and odd Latin squares, still open.

## The two results side by side

| `G` | `chi'(G)` | Lemma 1 (kernels) | Alon-Tarsi |
|---|---:|---|---|
| `K_4` | 3 | **fails**: all 38 thin orientations of the octahedron contain a directed triangle | **works**: `AT = 3` |
| `K_{3,3}` | 3 | **works**: Galvin's orientation is kernel-perfect | **fails**: `AT(S_3) = 4` |

**Neither method dominates the other.** Each proves a case the other provably cannot.

## Joint census, all `G` with at most 6 edges

|  | Alon-Tarsi works | Alon-Tarsi fails |
|---|---:|---:|
| **kernel works** | 52 | 0 |
| **kernel fails** | 1 (`K_4`) | 0 |

Every graph in range is covered by at least one of the two, and `K_{3,3}` at 9 edges is the
first graph covered by the kernel method alone. **No graph yet found where both fail.**

## Why this reopens the project

The previous conclusion, that kernels are finished and Alon-Tarsi is the live method, was
built on the false claim above and is withdrawn. The correct picture:

  - Both methods are partial, in different directions.
  - Their **union** covers everything tested so far.
  - The conjecture would follow from showing the union covers everything, or from finding a
    single method that subsumes both.

So the sharp question for this project is no longer "improve one method" but:

> **Is there a graph `G` for which neither Lemma 1 nor Alon-Tarsi proves `ch'(G) = chi'(G)`?**

If no such `G` exists, the conjecture reduces to a dichotomy: every line graph admits either a
thin kernel-perfect orientation or a thin orientation with `EE != EO`. That is a concrete,
checkable statement about orientations of line graphs, and it is exactly the kind of question
the census machinery in this repository was built to answer.

If such a `G` does exist, finding it is itself valuable: it would mark the precise boundary
where both known methods run out, and say what any future method has to handle.

## Next step

Push the joint census up in size, since the interesting cell is empty so far. The cost is the
kernel side, which searches all orientations of `L(G)`; that needs pruning by out-degree
before the kernel-perfectness test, and the Boros and Gurvich criterion (a clique-acyclic
orientation of a perfect graph is kernel-perfect) may replace the search entirely on the line
graphs that happen to be perfect.
