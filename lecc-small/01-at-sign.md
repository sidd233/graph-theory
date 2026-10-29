# 01. The Alon–Tarsi coefficient for line graphs of regular graphs

Let `G` be simple and `k`-regular on `N` vertices, with `N` even. Index the edges `e_1 < e_2 <
...` and form the graph polynomial of `L(G)`:

```
P(x) = product over pairs e_i, e_j sharing a vertex, i < j, of (x_{e_i} - x_{e_j}).
```

With lists of size `k`, the Combinatorial Nullstellensatz needs a monomial of degree `|E(L(G))|`
with every exponent at most `k - 1`. Since `|E(L(G))| = |E| (k-1)`, the only candidate is
`prod_e x_e^(k-1)`.

## Computing its coefficient

Use the interpolation formula, the Quantitative Nullstellensatz, with a colour set
`A = {a_0, ..., a_{k-1}}`:

```
coef = sum over c in A^E of P(c) / prod_e w(c_e),     w(j) = product over i != j of (a_j - a_i).
```

1. **Only proper colourings survive.** `P(c) = 0` unless `c` is a proper edge-colouring.
   Since `G` is `k`-regular and `|A| = k`, every vertex then sees all `k` colours.
2. **Each star contributes a sign times a Vandermonde.** Each pair of edges sharing a vertex
   shares exactly one, so `P` factors over the stars. At `v`, the factor is
   `prod over i<j at v of (a_{c(e_i)} - a_{c(e_j)})`, which is `sgn(pi_v)` times the Vandermonde
   `V(A)`. Here `pi_v` is the permutation sending the `i`-th edge at `v`, in index order, to its
   colour.
3. **The denominator is constant.** Each colour class is a perfect matching with `N/2` edges, so
   `prod_e w(c_e) = prod_j w(j)^(N/2)` is the same for every colouring.

Hence

```
coef = V(A)^N / prod_j w(j)^(N/2)  ·  S(G),    S(G) = sum over proper c of prod_v sgn(pi_v(c)).
```

The prefactor is nonzero, so **`coef != 0` if and only if `S(G) != 0`**.

## Normalising the colours

Permuting the colours by `sigma` multiplies every `pi_v` by `sigma`, so it multiplies the product
of signs by `sgn(sigma)^N = 1`. The sum over colourings with the colours at vertex 0 fixed is
therefore `S(G) / k!`. That restricted sum is what `at_sign.py` computes. Changing the reference
order at a vertex flips every term by the same sign, so whether `S(G)` is zero does not depend on
those choices.

This agrees with Schauz's sign of a 1-factorization (arXiv:1705.00484, Corollary 4) up to a
global sign. The census reproduces his counts exactly; see `RESULTS.md`.

## Validation

| graph | colourings with vertex 0 fixed | `S/k!` | expected |
|---|---:|---:|---|
| `K_4` | 1 | 1 | nonzero (Schauz, `K_{p+1}`) |
| `K_{3,3}` | 2 | 0 | zero (Schauz; note `08`) |
| `K_6` | 6 | -6 | nonzero |
| `K_8` | 6240 | 4320 | nonzero; 6240 is the known number of 1-factorizations of `K_8` |
| Petersen | 0 | 0 | class 2 |
