# 7. Alon-Tarsi, and the hard floor under this whole family of methods

## The method

**Theorem (Alon, Tarsi 1992).** Let `D` be an orientation of `G`. Call a set `A` of arcs
*Eulerian* if every vertex has equal in-degree and out-degree inside `A`. Let `EE` and `EO`
count the Eulerian arc sets of even and odd size. If `EE != EO`, then `G` is `L`-colourable
whenever `|L(v)| >= d+(v) + 1`. Write

```
AT(G) = min { Delta+(D) + 1 : D an orientation of G with EE(D) != EO(D) },   ch(G) <= AT(G).
```

It asks **nothing** about induced subgraphs, so none of the four obstructions in sections 1
to 6 applies. That is why it was the right next place to look.
**Correction (see `08`): it is NOT stronger than the kernel method.** A kernel-perfect
orientation can have `EE = EO`; Galvin's orientation of `S_3` is one, and `AT(S_3) = 4`
while `chi_ell(S_3) = 3`. The two methods are incomparable.

Implementation in `alontarsi.py`: `EE - EO` by a signed walk over the arcs tracking each
vertex's out-minus-in imbalance. Validated against known values: `AT(C_4) = 2`, `AT(C_5) = 3`,
`AT(K_4) = 4`, `AT(K_5) = 5`, all equal to the true `ch`.

## The hard floor

Alon-Tarsi is the combinatorial face of the Combinatorial Nullstellensatz applied to the
graph polynomial `prod over edges of (x_u - x_v)`, whose degree is `|E|`. The method needs a
nonzero coefficient of `prod x_v^{t_v}` with `sum of t_v = |E|`, and then yields
`L`-colourability for `|L(v)| >= t_v + 1`.

**Since the `t_v` sum to `|E|`, the largest of them is at least `|E| / n`.** Hence

```
any bound from this method is at least  ceil(|E| / n) + 1,
```

roughly half the average degree, plus one. For the orientation form the floor is
`min Delta+ + 1`, which by Hakimi equals `max over subgraphs H of ceil(|E(H)|/|V(H)|) + 1`,
and is at least the above.

**Consequence.** The halving we spent this project chasing is impossible for Alon-Tarsi too,
and for the same kind of reason it was impossible for 2-d kernels: not a missing idea, but
arithmetic. Kernels, 2-d kernels, Alon-Tarsi and the Nullstellensatz all bottom out at about
`mad/2 + 1`. **There is no route below that anywhere in this family.**

## How much room is left above the floor

For every graph on 5 and 6 vertices with at most 10 edges, comparing `AT` against the floor
`min Delta+ + 1` and against `chi` from below (`chi <= ch <= AT`):

| n | `AT` = floor | `AT` above floor but `= chi` | genuine gap |
|---|---:|---:|---:|
| 5 | 21 | 12 | **0** |
| 6 | 97 | 40 | **0** |

Every single graph falls into one of two cases. Either `AT` already achieves the best any
method in this family could achieve, or `AT` sits above the floor and equals `chi` exactly,
which means the floor was a **false** bound and `AT` is tight. Examples of the second kind
are `C_5` (floor 2, `AT = chi = 3`), `K_4` (floor 3, `AT = chi = 4`) and `K_5` (floor 3,
`AT = chi = 5`).

**There is no slack to recover.** Not "we could not find any": there is none, on everything
tested.

Caveat worth stating: edges were capped at 10, so the densest graphs on 6 vertices were not
covered, and graphs with `AT > ch` are known to exist at larger sizes. The census says the
gap is empty here, not that it is empty everywhere.

## Where this leaves the goal

The goal was to reduce the bound on list colouring by finding the right class of graphs. The
honest landscape after this session:

  - **Below `mad/2 + 1` is unreachable** by kernels, 2-d kernels, Alon-Tarsi or the
    Nullstellensatz. That is settled, not merely unsolved.
  - **At `mad/2 + 1`, Alon-Tarsi is already essentially optimal**, with no measurable slack on
    small graphs.
  - The truth is often far lower. Triangle-free graphs satisfy
    `ch <= (1 + o(1)) Delta / ln Delta` (Johansson, Molloy), which is far below `mad/2`. No
    method in this family can see that, because of the floor above.

So there are two honest ways forward, and they are different projects:

  1. **Stay structural, and aim at the floor rather than below it.** The open question our
     census points at is: *for which classes does `AT(G)` equal the Hakimi floor?* Our data
     says "nearly always, for small graphs". Proving it for an infinite class would be a real
     theorem, and it is live territory: Zhu proved `AT <= 5` for planar graphs in 2019, and
     Alon and Tarsi proved `AT <= 3` for planar bipartite graphs.
  2. **Go probabilistic** if the aim is genuinely to beat `mad/2 + 1`. That means the Local
     Lemma, entropy compression, or the hard-core counting method of Davies, Kang, Pirot and
     Sereni. Those are the only tools that get below the floor, and they are what the current
     records are made of.

My recommendation is (1): it uses the structural taste this project already has, it has a
concrete and checkable target, and the census gives us a strong working conjecture to attack
rather than a blank page.
