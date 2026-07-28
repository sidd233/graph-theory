# LaTeX Guide

This document explains how to use the Graph Theory LaTeX template and serves as a quick reference while writing notes.

---

# Philosophy

Use Markdown for

- Concept notes
- Paper summaries
- Research journal
- Reading notes
- Questions

Use LaTeX for

- Long proofs
- Mathematical derivations
- Lecture notes
- Assignments
- Drafts of research papers

---

# Basic Structure

Every note starts with

```latex
\section{Topic}
```

Within a section, use any of the following environments.

---

# Definitions

```latex
\begin{definition}[Graph]
A graph is an ordered pair $G=(V,E)$.
\end{definition}
```

Produces

> **Definition (Graph)**

---

# Examples

```latex
\begin{example}
Every tree is connected.
\end{example}
```

---

# Exercises

```latex
\begin{exercise}
Show that every tree has exactly $n-1$ edges.
\end{exercise}
```

---

# Theorems

```latex
\begin{theorem}[Hall's Marriage Theorem]
Statement...
\end{theorem}
```

---

# Lemmas

```latex
\begin{lemma}
...
\end{lemma}
```

---

# Corollaries

```latex
\begin{corollary}
...
\end{corollary}
```

---

# Conjectures

```latex
\begin{conjecture}
...
\end{conjecture}
```

---

# Remarks

Use remarks for intuition.

```latex
\begin{remark}
This theorem fails for directed graphs.
\end{remark}
```

---

# Notes

```latex
\begin{note}
Remember this for Petersen's theorem.
\end{note}
```

Unlike remarks, notes are not numbered.

---

# Proofs

```latex
\begin{proof}

...

\end{proof}
```

If the last line is an equation

```latex
\qedhere
```

places the □ correctly.

---

# Mathematics

Inline

```latex
$G=(V,E)$
```

Display

```latex
\[
G=(V,E)
\]
```

Multiple equations

```latex
\begin{align}
a+b &= c\\
x+y &= z
\end{align}
```

Never use

```latex
$$...$$
```

Prefer

```latex
\[
...
\]
```

---

# Common Symbols

## Greek

```latex
\alpha
\beta
\gamma
\delta
\epsilon
\lambda
\mu
\phi
\psi
\omega
```

---

## Logic

```latex
\forall
\exists
\implies
\iff
\therefore
\because
```

---

## Sets

```latex
\in
\notin
\subseteq
\supseteq
\cup
\cap
\setminus
```

---

## Relations

```latex
=
\neq
<
>
\le
\ge
```

---

## Arrows

```latex
\rightarrow

\Rightarrow

\leftrightarrow

\mapsto
```

---

# Graph Theory Macros

Instead of writing

```latex
\operatorname{girth}(G)
```

write

```latex
\girth(G)
```

Available macros

## Vertex set

```latex
\V
```

Produces

$$
V
$$

---

## Edge set

```latex
\E
```

---

## Neighbourhood

```latex
\N(v)
```

---

## Complete Graph

```latex
\Kn{5}
```

Produces

$$
K_5
$$

---

## Complete Bipartite Graph

```latex
\Kmn{3}{4}
```

Produces

$$
K_{3,4}
$$

---

## Path

```latex
\Pn{7}
```

---

## Cycle

```latex
\Cn{8}
```

---

## Degree

```latex
\dg(v)
```

---

## Girth

```latex
\girth(G)
```

---

## Diameter

```latex
\diam(G)
```

---

## Chromatic Number

```latex
\chr(G)
```

---

## Automorphism Group

```latex
\Aut(G)
```

---

# Lists

Bullet list

```latex
\begin{itemize}

\item

\item

\end{itemize}
```

Numbered list

```latex
\begin{enumerate}

\item

\item

\end{enumerate}
```

---

# Figures

The template already loads TikZ.

Example

```latex
\begin{center}
\begin{tikzpicture}

...

\end{tikzpicture}
\end{center}
```

Prefer TikZ over screenshots whenever possible.

---

# Hyperlinks

Website

```latex
\url{https://graph.org}
```

Text

```latex
\href{https://graph.org}{Graph Theory}
```

---

# References

Later

```latex
\cite{diestel}
```

---

# Recommended Note Structure

```latex
\section{Name}

Definition

Example

Remark

Theorem

Proof

Example

Remark
```

or

```latex
\section{Matching}

Definition

Examples

Properties

Theorems

Applications
```

---

# Writing Style

Good

- Short sentences.
- One idea per paragraph.
- Explain intuition before proof.
- State assumptions clearly.
- Label important equations.

Avoid

- Huge paragraphs.
- Screenshots of mathematics.
- Undefined notation.
- Skipping proof ideas.

---

# VS Code Shortcuts

Build

```
Ctrl + Shift + B
```

Open PDF

```
Ctrl + Alt + V
```

Split Editor

```
Ctrl + \
```

Command Palette

```
Ctrl + Shift + P
```

---

# Workflow

```
Read paper

↓

Understand concept

↓

Write rough notes

↓

Write polished LaTeX note

↓

Compile

↓

Commit

↓

Push
```

---

# General Tips

- Keep one concept per document.
- Use theorem environments instead of bold text.
- Use display equations only when necessary.
- Prefer `align` over multiple `equation` environments.
- Reuse the provided graph-theory macros instead of writing raw notation repeatedly.
- Keep figures simple and readable.

---

# Useful Resources

- The Not So Short Introduction to LaTeX2ε
- Overleaf Documentation
- Detexify (draw a symbol to find its LaTeX command)
- TikZ Example Gallery