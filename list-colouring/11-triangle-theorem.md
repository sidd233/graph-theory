# 13. Theorem: a triangle kills Lemma 1 on every cubic class-1 graph

> **Off target.** This note was written when `PROBLEM.md` wrongly named the line graph
> conjecture as this project's goal. The goal is improving the bound on list colouring,
> stated in `PROBLEM.md` section 1. The mathematics here stands, but it is not progress
> on the goal.

## Statement

> **Theorem.** Let `G` be 3-regular with `chi'(G) = 3`. If `G` contains a triangle, then
> `L(G)` has no kernel-perfect orientation with `Delta+ <= 2`. Consequently **Lemma 1 of
> chapter 33 cannot prove `ch'(G) = 3`**, whatever is true of `ch'(G)` itself.

## Proof

By the star lemma (`09`), a kernel-perfect orientation of `L(G)` induces a linear order on the
edges at each vertex. Write `M(u,v)` for the number of edges at `u` that `uv` points to, so
each row of `M` is a bijection onto `{0, 1, 2}` and `d+(uv) = M(u,v) + M(v,u)`.

`G` is 3-regular and class 1, so `|E(L(G))| = N * C(3,2) = 2 |E(G)|`, and the budget
`d+ <= chi' - 1 = 2` is **exactly** consumed. Hence

```
M(u,v) + M(v,u) = 2     for every edge uv.
```

Let `ijk` be a triangle of `G` and put `p = M(i,j)`, `q = M(j,k)`, `r = M(i,k)`, so
`M(j,i) = 2 - p`, `M(k,j) = 2 - q`, `M(k,i) = 2 - r`. Row `i` contains `p` and `r`, row `j`
contains `2-p` and `q`, row `k` contains `2-r` and `2-q`, and rows are injective, so

```
p != r,      p + q != 2,      q != r.
```

The three edges form a triangle in `L(G)`, oriented at their shared vertices:

```
ij -> jk  at j    iff   2 - p > q    iff   p + q < 2
jk -> ik  at k    iff   2 - q > 2 - r    iff   r > q
ik -> ij  at i    iff   r > p
```

so the triangle is cyclic exactly when `(p+q < 2 and r > p and r > q)` or
`(p+q > 2 and r < p and r < q)`. Enumerating all `(p,q,r)` in `{0,1,2}^3` subject to the three
row conditions leaves **no acyclic case**:

| `(p,q)` | forced `r` | outcome |
|---|---|---|
| `(0,0)` | acyclic needs `r <= 0`, but `r != p = 0` | impossible |
| `(0,1)` | acyclic needs `r <= 1`, and `r != 0`, so `r = 1 = q` | impossible |
| `(1,0)` | acyclic needs `r != 2`, and `r != 1`, so `r = 0 = q` | impossible |
| `(1,2)` | acyclic needs `r != 0`, and `r != 1`, so `r = 2 = q` | impossible |
| `(2,1)` | acyclic needs `r != 0`, and `r != 2`, so `r = 1 = q` | impossible |
| `(2,2)` | acyclic needs `r = 2 = p` | impossible |
| `(0,2)`, `(1,1)`, `(2,0)` | `p + q = 2` | excluded by row `j` |

Every surviving assignment makes the triangle a directed triangle, which has no kernel, as
chapter 33 notes for `{a, c, e}`. QED

Machine check in `triangle_thm.py`: for `s = Delta - 1 = 2` the count of acyclic triangles is
**0**, and `s = 2` is the only value above 1 for which that count vanishes.

## Scope, stated honestly

  - The theorem covers `K_4` and the prism `C_3 x K_2`, matching the exhaustive searches.
  - **It does not extend to larger `Delta`.** For `s >= 3` acyclic triangles exist locally,
    for instance `(p,q,r) = (0,2,1)`, with 6, 18, 42, 78 and 132 acyclic cases at
    `s = 3, 4, 5, 6, 7`. So the failures of `K_6`, `K_8` and `K_{2,2,2}` are **global**
    interactions between triangles, not a local obstruction, and need a different argument.

| `s = Delta - 1` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| acyclic triangles possible | 0 | **0** | 6 | 18 | 42 | 78 | 132 |

## Correction to `10`

Section `10` listed `C_5 x K_2` as passing. That was the triangle test only, which is vacuous
for a triangle-free graph. The full check has now run: the order found gives `Delta+ = 2`,
thin enough, but the resulting orientation is **not kernel-perfect**. That rules out one order,
not all of them, so `C_5 x K_2` is **undecided** and the joint census is enumerating the rest.

## What is still open here

Prove or refute: for `G` regular and class 1 with `Delta >= 4`, does a triangle still force
failure? `K_6`, `K_8` and `K_{2,2,2}` say yes in every case tested, but by a global argument
that is not yet identified. Finding it would extend the theorem to `K_{2n}` in general, which
would say that Lemma 1 can never prove the hard open case of the conjecture.
