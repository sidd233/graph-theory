# 1. The standard kernel proof of the list-colouring bound

## Setting

`G` is a simple graph. A **list assignment** `L` gives each `v` a set `L(v)` of colours.
An **`L`-colouring** is a proper colouring with `phi(v) in L(v)`. `ch(G)` is the least `k`
with `G` `L`-colourable for every `L` having `|L(v)| >= k` everywhere.

`D` is a digraph whose underlying graph is `G`. Write `d+(v)` for the out-degree in `D`
and `N+(v)` for the out-neighbourhood.

A **kernel** of `D` is an independent set `K` such that every `v` outside `K` has at least
one out-neighbour in `K`. `D` is **kernel-perfect** if every induced subdigraph of `D` has
a kernel.

A **2-d kernel** (our definition) is an independent set `K` such that every `v` outside `K`
has at least two out-neighbours in `K`.

## Theorem (Bondy, Boppana, Siegel 1987)

Let `D` be kernel-perfect. Then `G` is `L`-colourable for every `L` with
`|L(v)| >= d+(v) + 1`. In particular `ch(G) <= Delta+(D) + 1`.

## Proof, in steps

Induction on `|V(D)|`. The empty case is trivial.

**Step 1 (pick a colour).** Every list is nonempty since `|L(v)| >= d+(v)+1 >= 1`. Fix any
colour `c` appearing in some list and set `S = {v : c in L(v)}`, which is nonempty.

**Step 2 (find the independent set).** `D[S]` is an induced subdigraph, so it has a kernel
`K`. `K` is nonempty: a vertex of `S` outside an empty `K` would need an out-neighbour in
the empty set.

**Step 3 (colour it).** Give colour `c` to every vertex of `K`. `K` is independent in `D`,
hence in `G`, so this much is proper.

**Step 4 (delete and trim).** Put `D' = D - K`, and `L'(v) = L(v) \ {c}` for `v in S`,
`L'(v) = L(v)` otherwise. This is enough for properness later: if `v` survives and is
adjacent to `K`, then either `c` was never in `L(v)`, or `v in S` and `c` has just been
removed. Either way `c` is not in `L'(v)`.

**Step 5 (the hypothesis survives).** This is the only step that uses the kernel property.
  - `v in S \ K`. Its list shrank by exactly one. Because `K` is a kernel of `D[S]`, `v`
    has at least one out-neighbour in `K`, so `d+` drops by at least one. Hence
    `|L'(v)| = |L(v)| - 1 >= d+_D(v) >= d+_{D'}(v) + 1`.
  - `v` outside `S`. Its list is unchanged and `d+` can only drop.

**Step 6 (recurse).** Induced subdigraphs of `D'` are induced subdigraphs of `D`, so `D'`
is kernel-perfect. Apply induction to `(D', L')` and add the class coloured `c`. QED

## What the proof is actually doing

Steps 1, 3, 4 and 6 are bookkeeping. **All the strength sits in Step 5**, and it is one
exchange rate:

> losing one colour from a list must be paid for by losing at least one unit of out-degree.

## The accounting lemma

Let `f` be non-decreasing with `f(0) >= 1`. Suppose that for every `W` and every `S` inside
`W` there is a nonempty independent `K` inside `S` such that every `u` in `S \ K` with a
neighbour in `K` satisfies

```
f(d+(u)) - f(d+(u) - |N+(u) cap K|) >= 1        (all degrees taken in D[W])
```

Then `G` is `L`-colourable whenever `|L(v)| >= f(d+_D(v))`. The proof is Steps 1 to 6 verbatim.

  - Kernel: guarantees `|N+(u) cap K| >= 1`, needs `f(d) - f(d-1) >= 1`, so `f(d) = d+1`.
    Bound `Delta+ + 1`.
  - **2-d kernel**: guarantees `|N+(u) cap K| >= 2`, needs `f(d) - f(d-2) >= 1`, so
    `f(d) = ceil(d/2) + 1`. Bound `ceil(Delta+/2) + 1`.

So the whole hope of the 2-d kernel route is a single substitution of 2 for 1 in Step 5, and
a halving of the bound falls out. Nothing else in the proof has to change.
