# 6. The oriented setting, and the verdict on the whole programme

## Setting

`D` is a digon-free orientation of `G`. A vertex `u` loses the colour when **any**
neighbour in `K` is coloured, but pays out-degree only for its **out**-neighbours in `K`.
With `a = |N+(u) cap K|` and `f(d) = ceil(lam*d) + 1`, a vertex `u` in `S \ K` adjacent to
`K` needs `f(d+(u)) - f(d+(u) - a) >= 1`. That forces `a >= 1`, which is ordinary
kernel-perfectness, and asks for more when `d+(u)` sits at a bad degree. The bound proved is
`f(Delta+(D))`, so a thin orientation is what buys the gain over degeneracy.

Note `lam = 1` **is** the classical Bondy, Boppana and Siegel method: the condition reduces
to `a >= 1` and the bound to `Delta+ + 1`. Everything with `lam < 1` is our refinement. Note
also that surviving at `lam < 1` implies surviving at `lam = 1`, since the condition is
strictly stronger, so the refinement can only ever pick orientations the classical method
already accepts.

## The classical method does beat degeneracy

Searching all orientations and all `lam`:

| graph | `degen+1` | kernel bound (`lam=1`) | best with any `lam` |
|---|---:|---:|---:|
| `C_4` | 3 | **2** | 2 |
| `C_6` | 3 | **2** | 2 |
| `K_{3,3}` | 4 | **3** | 3 |
| prism | 4 | **3** | 3 |
| `L(K_{2,3})` | 4 | **3** | 3 |
| `K_4` | 4 | 4 | 4 |
| `K_5` | 5 | 5 | 5 |
| `K_{2,4}` | 3 | 3 | 3 |
| `P_6`, `K_{1,5}` | 2 | 2 | 2 |

So orientations really do have the headroom the symmetric setting lacked, and the classical
kernel method collects it. **The refinement collects nothing on top, in every case.**

Broad hunt: 223 random graphs on 5 and 6 vertices, every orientation of each, every `lam`
with denominator up to 9. **Zero wins.**

## Why the refinement cannot win

**Lemma.** Fix `lam` in `(0,1)` and let `d0 = min{d >= 1 : ceil(lam*d) < d}`, the smallest
out-degree at which the refinement improves on the greedy count at all. Then `d0` is also the
smallest **bad** degree, that is the smallest `d` with `ceil(lam*d) = ceil(lam*(d-1))`.

*Proof.* For `d < d0` we have `ceil(lam*d) = d` and `ceil(lam*(d-1)) = d-1`, which differ by
1, so no `d < d0` is bad. At `d0` we have `ceil(lam*d0) <= d0 - 1`, and `ceil` is
non-decreasing so `ceil(lam*d0) >= ceil(lam*(d0-1)) = d0 - 1`. Hence
`ceil(lam*d0) = ceil(lam*(d0-1))` and `d0` is bad. QED

Verified for every `lam` with denominator up to 9: the two thresholds agree exactly, always.

**Corollary (the mechanism).** Suppose the bound `ceil(lam*Delta+) + 1` is any better than
`Delta+ + 1`. Then `Delta+ >= d0`, so some vertex `u` has out-degree at least `d0`. Delete
out-neighbours of `u` until its out-degree is exactly `d0`. In that induced subdigraph `u`
sits at a bad degree and still has an out-neighbour `v`, and the colour class `S = {u, v}` is
unusable: digon-freeness rules out `K = {u}`, since `v` would need an out-arc into `u`; and
`K = {v}` leaves `u` with one out-arc into `K` at a bad degree.

**The gain and the obstruction switch on at exactly the same threshold.** The configuration
that would let the refinement pay less is precisely the configuration it cannot handle. That
is not an accident of small cases, it is arithmetic.

## Verdict on the 2-d kernel programme

Closed, as a route to list colouring. It failed in four independent ways, and the last one
explains the other three:

  1. Hereditarily, a single arc defeats it.
  2. With the parity correction, a path on four vertices defeats it.
  3. With free colour choice in the symmetric setting, it never beats degeneracy, and the
     symmetric setting had no headroom in it anyway.
  4. With free colour choice on orientations, where the headroom is real and the classical
     kernel method does collect it, the refinement adds exactly nothing, for the arithmetic
     reason above.

What survives is worth keeping. The existing 2-d kernel results (the census, the chordal and
acyclic theorems, the structural work in `latex/2-d-kernels-structural-theorems.tex`) stand on
their own as combinatorics. They are simply not a tool for bounding `ch`.

## If the list-colouring problem is still the goal

Go to **Alon-Tarsi**, for the reason given in `02-other-routes.md`: it has the same shape as
the kernel method, an orientation with small out-degree, but imposes no hereditary condition,
so none of the four obstructions above applies to it. It is also strictly stronger than the
kernel method, so it starts from a better place than the one we have spent this project
trying to improve.
