# Graph

## Status

- [ ] Read
- [ ] Understood
- [ ] Revised
- [ ] Can explain without notes

## Definition

A **graph** is an ordered pair

$$
G = (V, E)
$$

where

- $V$ is a finite set of **vertices** (or **nodes**).
- $E$ is a set of **edges** connecting pairs of vertices.

Depending on the type of graph, edges may be

- unordered pairs (undirected graphs),
- ordered pairs (directed graphs),
- or allow multiple edges and loops (multigraphs).

---

## Intuition

A graph models **relationships** between objects.

Think of

- cities connected by roads,
- people connected by friendships,
- computers connected by cables,
- webpages connected by hyperlinks.

Vertices represent the objects.

Edges represent the relationships.

---

## Visual Example

```text
A ----- B
|       |
|       |
C ----- D
```

Vertices

$$
V=\{A,B,C,D\}
$$

Edges

$$
E=\{
(A,B),
(B,D),
(D,C),
(C,A)
\}
$$

---

## Formal Notation

Usually

$$
V(G)
$$

denotes the vertex set.

$$
E(G)
$$

denotes the edge set.

Number of vertices

$$
|V(G)|
$$

Number of edges

$$
|E(G)|
$$

Order of graph

$$
|V(G)|
$$

Size of graph

$$
|E(G)|
$$

---

## Terminology

Know these terms.

- Vertex
- Edge
- Adjacent vertices
- Incident edge
- Neighbor
- Degree
- Order
- Size

---

## Types of Graphs

- [ ] Simple Graph
- [ ] Multigraph
- [ ] Pseudograph
- [ ] Directed Graph (Digraph)
- [ ] Weighted Graph
- [ ] Complete Graph
- [ ] Bipartite Graph
- [ ] Complete Bipartite Graph
- [ ] Regular Graph
- [ ] Tree
- [ ] Forest

---

## Common Notation

| Symbol | Meaning |
|---------|---------|
| $G$ | Graph |
| $V(G)$ | Vertex set |
| $E(G)$ | Edge set |
| $u,v$ | Vertices |
| $uv$ | Edge |
| $\deg(v)$ | Degree of vertex |
| $\Delta(G)$ | Maximum degree |
| $\delta(G)$ | Minimum degree |
| $n$ | Number of vertices |
| $m$ | Number of edges |

---

## Basic Properties

For a simple graph

$$
0 \le |E(G)| \le \binom{|V(G)|}{2}
$$

Maximum possible edges

$$
\binom{n}{2}
=
\frac{n(n-1)}{2}
$$

---

## Immediate Consequences

Every graph has

- vertices
- edges
- adjacency
- degrees

Everything else in graph theory is built from these.

---

## Related Concepts

- [[vertex]]
- [[edge]]
- [[degree]]
- [[path]]
- [[walk]]
- [[cycle]]
- [[tree]]
- [[subgraph]]
- [[connected graph]]

---

## Used In

Graphs are the foundation for

- Matchings
- Factors
- Graph Coloring
- Network Flows
- Graph Decomposition
- Arboricity
- Spectral Graph Theory
- Extremal Graph Theory
- Probabilistic Graph Theory

---

## Classical Theorems Built on Graphs

- [ ] Handshaking Lemma
- [ ] Euler's Theorem
- [ ] Hall's Marriage Theorem
- [ ] Menger's Theorem
- [ ] Petersen's 2-Factor Theorem
- [ ] Vizing's Theorem
- [ ] Nash-Williams Arboricity Theorem

---

## Algorithms That Operate on Graphs

- [ ] BFS
- [ ] DFS
- [ ] Kruskal
- [ ] Prim
- [ ] Dijkstra
- [ ] Bellman-Ford
- [ ] Floyd-Warshall
- [ ] Ford-Fulkerson
- [ ] Hopcroft-Karp

---

## Research Connections

This concept appears in nearly every paper in graph theory.

When reading a paper, pay attention to

- What class of graphs is being studied?
- What assumptions are made?
- Is the graph simple?
- Is it regular?
- Is it planar?
- Is it bipartite?
- Is it directed?
- Is it weighted?

These assumptions often determine which theorems and techniques can be used.

---

## Questions

- Why do graph theorists usually assume graphs are finite?
- Why are loops often excluded?
- Why distinguish multigraphs from simple graphs?
- When is a directed graph more appropriate than an undirected graph?

---

## References

### Primary

- Diestel — *Graph Theory* (Chapter 1)

### Secondary

- West — *Introduction to Graph Theory*

### Reference

- Bondy & Murty — *Graph Theory*

---

## Revision Checklist

### Level 1 — Recognition

- [ ] I know what a graph is.
- [ ] I know the notation $G=(V,E)$.
- [ ] I know what vertices and edges represent.

### Level 2 — Understanding

- [ ] I can explain graphs to someone else.
- [ ] I know the difference between vertices and edges.
- [ ] I know the common graph types.

### Level 3 — Application

- [ ] I can model a real-world problem as a graph.
- [ ] I can determine $V(G)$ and $E(G)$ from a diagram.
- [ ] I understand the notation used in graph theory papers.

### Level 4 — Research

- [ ] I immediately recognize what assumptions a paper makes about its graphs.
- [ ] I understand why those assumptions matter.