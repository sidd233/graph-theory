# census-tool

Census tooling for **2-d kernels** — the `(2-d)`-kernel of Włoch (*Australas. J. Combin.*
**53** (2012) 273–284) — in graphs and digraphs.

A 2-d kernel of a digraph `D = (V, A)` is a set `S ⊆ V` such that:

1. **independence** — no arc of `A` has both ends in `S`;
2. **2-domination** — every `v ∉ S` has `|N⁺(v) ∩ S| ≥ 2`.

An undirected graph is treated as its symmetric digraph, so one engine covers both cases.
Existence is NP-complete, so this tool is about exhaustively (or, past feasible size,
exponential-but-fast and sampled) computing 2-d kernel data across many graph/digraph
families, storing it, and querying it — not a polynomial-time solver.

See `PLAN.md` for design rationale and interpretation decisions, and `FINDINGS.md` for the
results (E1–E8) this tool has produced.

## Setup

```
python -m venv env
env/bin/pip install networkx pytest
```

Requires Python ≥ 3.12 (developed against 3.14). `env/` is gitignored — recreate it rather
than committing it. All commands below assume you are in the project root (`census-tool/`)
so that `python -m twokernel...` can find the package; the project is not pip-installed.

`pynauty` is used for exact canonical labelling at any graph size, if it's importable in
your environment; otherwise a built-in fallback (1-WL refinement + brute-force minimisation)
is used, capped at 7 vertices. Everything works without pynauty, just at smaller scale.

Run the test suite with:

```
env/bin/python -m pytest
```

## Library (`twokernel/`)

| module | contents |
|---|---|
| `core.py` | bitmask `Digraph`, `is_2kernel` verifier, maximal-independent-set enumeration, reference solver, forcing-closure propagation (`forced_set`, `forcing_closure`), DPLL solver (`solve_dpll`) |
| `canon.py` | graph6/digraph6 codec (`encode`/`decode`), canonical labelling and keys (pynauty or fallback) |
| `classes.py` | boolean recognizers (chordal, split, cograph, claw-free, …) and numeric invariants (α, ω, girth, degeneracy, …) |
| `generators.py` | the graph atlas, named families, structured exhaustive generators, seeded random families |
| `census.py` | the sqlite-backed census: family generation, storage, and the CLI (see below) |
| `experiments.py` | standalone experiments (E5, E6) that are proofs/structural checks rather than plain SQL queries |

Import from these directly if you want to explore a graph interactively, e.g.:

```python
from twokernel.generators import petersen
from twokernel.core import all_2kernels

D = petersen()
print(len(all_2kernels(D)))
```

## Tool 1: `python -m twokernel.census` — build and query the database

Populates `census.sqlite3` (one row per isomorphism class, keyed by its canonical
graph6/digraph6 string) with structural invariants and 2-d kernel data, then lets you run
canned reports against it.

```
# list the known families (exhaustive vs. sampled)
env/bin/python -m twokernel.census families

# populate one or more families (repeatable, dedups by canonical key)
env/bin/python -m twokernel.census run --family atlas7
env/bin/python -m twokernel.census run --family digraphs6sample --limit 5000

# run a canned query
env/bin/python -m twokernel.census query summary
env/bin/python -m twokernel.census query classes --family atlas7
env/bin/python -m twokernel.census query forcing --family dags7

# fill in a column added after some rows already existed
env/bin/python -m twokernel.census backfill degeneracy
```

Available `query` reports: `summary`, `classes`, `forcing`, `digraphs`, `cubic`, `dags`,
`degeneracy`. Available families (see `families` for the live list): `atlas7`, `graphs8`,
`graphs9`, `named`, `oriented6`, `digraphs5`, `digraphs6`, `digraphs6sample`, `dags7`,
`dags8sample`, `cubic`, `cubic_trianglefree`, `cubic_girth5`.

### Browsing the database directly

The database has two tables: `graphs` (one row per graph, ~40 columns of invariants plus
2-d kernel results) and `membership` (`key → family`). With the `sqlite3` CLI installed:

```
sqlite3 census.sqlite3 -header -column "SELECT key, n, m, has_2kernel, count_2kernels FROM graphs LIMIT 10;"
```

or interactively:

```
sqlite3 census.sqlite3
sqlite> .headers on
sqlite> .mode column
sqlite> .schema graphs
sqlite> SELECT * FROM graphs LIMIT 10;
```

Without the `sqlite3` CLI, Python's built-in `sqlite3` module works the same way:

```python
import sqlite3
conn = sqlite3.connect("census.sqlite3")
for row in conn.execute("SELECT * FROM graphs LIMIT 10"):
    print(row)
```

## Tool 2: `python -m twokernel.experiments` — standalone experiments

Runs the two experiments that are structural checks/proofs rather than SQL queries over
the census: **E5** (every atlas graph's vertex set is a 2-d kernel of its subdivision) and
**E6** (structure of 2-d kernels in DAGs). Prints results directly; doesn't touch the
database.

```
env/bin/python -m twokernel.experiments e5
env/bin/python -m twokernel.experiments e6
env/bin/python -m twokernel.experiments all
```
