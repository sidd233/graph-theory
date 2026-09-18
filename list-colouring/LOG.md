# Thinking log, list-colouring via 2-d kernels

Brief entries. What was tried, what it showed, what it changed.

---

## 2026-09-11 - orientation session (no new research, scoping only)

**Why start at the proof rather than at 2-d kernels.** The 2-d kernel work so far is a
collection of existence results. Existence is not what the colouring proof consumes. So I
read the Bondy, Boppana, Siegel induction line by line to find which line touches the
kernel. Answer: exactly one, Step 5. Everything else is bookkeeping. That immediately
reduced the whole project to a single question, "what does Step 5 need", and made it clear
the bound halves for free once 1 becomes 2 there.

**Abstracting Step 5 first, before asking whether it holds.** I wrote the accounting lemma
with a general `f` instead of arguing about 2-d kernels directly. This was the useful move:
kernel and 2-d kernel are then the `f(d) = d+1` and `f(d) = ceil(d/2)+1` instances of one
statement, and any future relaxation is a choice of `f` rather than a new proof.

**Finding the weakest hypothesis, not the convenient one.** A 2-d kernel of `D[S]` demands
2-domination of every vertex of `S \ K`. But a vertex that is not adjacent to `K` loses no
colour, so it needs no compensation. Excusing those gives condition (star), strictly weaker.
I wanted the barrier tested against the weakest hypothesis so that a failure is conclusive
rather than an artefact of asking for too much.

**The barrier, found by shrinking rather than searching.** Rather than hunting for classes, I
asked for the smallest `S` that could break (star). Two vertices joined by an arc: any
nonempty independent `K` inside them is a single vertex, and one vertex cannot supply two
out-arcs. That is a two-line proof and it kills the hereditary plan outright. Exhaustive
check over all 4095 digraphs with an arc on at most 4 vertices agrees and, more usefully,
reports that the smallest failing `S` has size 2 **in every case**, which confirms the
two-vertex configuration is the whole obstruction and not merely one of many.

This also retro-explains `barrier.py`: E-B2 is this proposition, and E-B1's
"`t`-kernel-perfect forces `Delta+ <= t`" is the same argument with a threshold inserted.
Those two experiments were reporting one fact, not two.

**Calibrating the target before choosing an escape.** Before picking a way round, I checked
whether the goal is even true. With the best orientation, `chi <= ceil(Delta+/2) + 1` fails
for 121 of the 156 graphs on 6 vertices, starting with the triangle. So the naive halved
bound is far too strong to hold on any broad class. Reed's `ceil((Delta+1+omega)/2)` is the
same halving with `omega/2` of slack, and on the same 156 graphs it fails zero times while
the halved bound fails 26 times, so that slack is precisely what rescues `K_3`, `C_5`
and `K_4`. Working hypothesis, not yet tested: the `omega/2` is the price of the vertices
the barrier forces us to excuse.

**Where the escape should come from.** The barrier is a statement about one tiny `S`, not
about the graph. Quantifying over every `S` is therefore the assumption most likely to be
the wrong one, since in the actual induction we choose which colour to process and the
colour classes are coupled by `sum |L(v)|`. That is (B1), and it converts a hereditary
structural problem into a counting problem. Ranked ahead of fractional relaxation (B3),
which is the other natural candidate because fractional kernels always exist.

**Not done yet.** No attempt at (B1) to (B5). No literature check on the status of the list
version of Reed's conjecture. Both are the next session's work.

---

## 2026-09-11 - starting route (B1), the colour-choice route

**A correction found by checking an example, not by thinking.** I had defined a colour class
as bad when some vertex gets exactly one edge into the coloured set. Testing `P_4` by hand
showed that is wrong: the vertex there had degree 1, so its requirement dropped by one at
the same time, and the step was free. The real condition is parity. One edge suffices when
the vertex has odd degree, because `ceil(d/2)` only moves on odd `d`. Lesson: I derived the
condition abstractly and then checked a case only afterwards. Checking first would have
caught it immediately.

**Re-testing the barrier under the fixed condition.** Parity makes the condition strictly
weaker, so the earlier barrier had to be re-examined rather than assumed. It survives, and
in a sharper form: any graph containing a path on four vertices breaks the hereditary
demand, because the two middle vertices both have degree 2. Good, the earlier conclusion
stands, but now for a reason I can state in one line.

**Finding the exact stalling criterion instead of running the algorithm.** Rather than
simulate colouring against many list assignments, I asked when the adversary wins. Answer:
exactly when every vertex lies in some bad class, since the adversary can then hand each
vertex its own private colours drawn from bad classes only. That converts an open-ended
simulation into a finite check per graph, which is why the experiment was cheap enough to
run exhaustively.

**The answer, and it is clean.** Under the halving target the surviving class is exactly
the forests, on all graphs up to 6 vertices, and the cycle half of that has a two-line
proof: a shortest cycle is induced, all its degrees are 2, so every edge of it is a bad
class. Forests have `ch = 2` and the method proves `ceil(Delta/2) + 1`, so the method
certifies nothing anywhere it runs. Halving is dead by this route too, and for a sharper
reason than before.

**Not stopping at the negative.** Before abandoning, I swept the target from `Delta + 1`
down to `Delta/2 + 1`. The method degrades gradually rather than falling off a cliff: 156,
145, 115, 63, 20 survivors at `lam = 1, 4/5, 3/4, 2/3, 1/2`. So the interesting question is
not whether halving works, it is how far below `Delta + 1` we can get. That is a better
question than the one we started with, and it is the one I would carry forward.

**Known weakness of today's sweep.** Six vertices means `Delta <= 5`, where a coarse `lam`
cannot be told apart from the greedy bound. The middle columns are not yet evidence. Rerun
at larger `Delta` before trusting them.

---

## 2026-09-11 - large-degree sweep

**Making the test cheap before making it big.** The old checker was exponential in a way
that stopped at 6 vertices. Two prunes fixed it: if no vertex has a bad degree the whole
graph is fine with no search, and a bad colour class must have every vertex adjacent inside
the class to a bad-degree vertex. I validated the fast version against the slow one on all
156 graphs at `n = 6` before using it, which was worth the extra step.

**A monotonicity assumption I should have checked earlier.** I had been taking the first
`lam` that survives as the best. Survival is not monotone in `lam`, because the bad-degree
sets for different fractions are not nested. Taking the best bound over all surviving `lam`
overturned section 4's claim that the method is worthless on forests: forests survive at
arbitrarily small `lam` and the bound is then `ch <= 2`, which is tight. So the earlier
negative was an artefact of fixing `lam = 1/2`, not a property of forests.

**Choosing the right opponent.** Beating `Delta + 1` is not an achievement, because the
degeneracy bound is free and usually much better. Benchmarking against `degen + 1` instead
is what made the result decisive, and it is the comparison I should have set up at the start.

**The hunt, designed to be cheap.** To beat degeneracy the method must survive at some `lam`
small enough that `ceil(lam*Delta) + 1 < degen + 1`. That is a short list of small `lam`, and
small `lam` fail fast. So the search over 1600 random graphs cost almost nothing. Zero
winners, on top of every structured family tested.

**The mistake worth recording.** All of this ran in the symmetric setting, where out-degree
equals degree. That is exactly the setting where the ordinary kernel method already collapses
to greedy, so it was never going to show a gain, for kernels or 2-d kernels. The kernel method's
power lives in orientations, where `min Delta+` is roughly half the degeneracy. I spent the
session measuring a room that has no headroom in it. The machinery all carries over, so the
cost is one session, but the lesson is that I should have checked where the slack was before
choosing the arena.

---

## 2026-09-11 - the oriented run, and the end of the programme

**Separating the refinement from the classical theorem.** The first oriented run showed wins
over degeneracy for `C_4`, `C_6`, `K_{3,3}` and the prism, which looked like success. It was
not. Reading the witnesses, every winning bound equalled `Delta+ + 1` for the chosen
orientation, and `lam = 1` is exactly the classical Bondy, Boppana and Siegel method. The
wins belonged to a 1987 theorem, not to us. Rerunning with the classical bound as an explicit
column, rather than degeneracy, turned a apparent success into a clean negative. Lesson:
benchmark against the strongest thing the method contains, not the weakest thing it beats.

**Noticing a pattern in the witnesses instead of collecting more data.** Every surviving
pair had `ceil(lam*Delta+) = Delta+`, meaning the refinement never actually rounded anything
down. That suggested the thresholds were linked, which turned out to be exactly true and to
have a three-line proof: the smallest degree where a rounding gain appears is the smallest
degree the method cannot handle. Checking the arithmetic was cheaper than running a larger
search, and it gave a reason rather than another data point.

**Confirming anyway.** 223 random graphs, every orientation of each, every `lam` with
denominator up to 9. Zero wins, as the lemma predicts.

**Verdict.** The 2-d kernel route to list colouring is closed, and the arithmetic says why
rather than merely that. The existing 2-d kernel results keep their value as combinatorics.
If the list-colouring problem stays the goal, Alon-Tarsi is the place to go, because it has
the kernel method's shape without the hereditary condition that killed every version of this.

---

## 2026-09-11 - Alon-Tarsi, and finding the floor before searching

**Looking for the ceiling before looking for a theorem.** The lesson of the last three
sessions is that I chased a target without first asking whether it was reachable. So with
Alon-Tarsi I asked that first. The answer took one paragraph: the graph polynomial has degree
`|E|`, the Nullstellensatz needs exponents summing to `|E|`, so the largest exponent is at
least `|E|/n`. No bound below about `mad/2 + 1` exists anywhere in this family. That single
observation would have saved the whole 2-d kernel detour had I made it in session one.

**Validating the implementation against known values first.** `AT(C_4) = 2`, `AT(C_5) = 3`,
`AT(K_4) = 4`, `AT(K_5) = 5`. All correct, and cheap to check, so the census that followed
could be trusted.

**Asking where the slack is rather than whether the method works.** Instead of trying to
improve `AT`, I measured the distance between `AT` and the floor, using `chi` as a witness
from below. Every graph tested fell into one of two clean cases: `AT` is already at the floor,
or `AT` sits above it and equals `chi`, meaning the floor was a false bound. Zero genuine
gaps at `n = 5` and `n = 6`. There is nothing to recover.

**Verdict on the goal.** Reducing the list-colouring bound below `mad/2 + 1` is not an open
problem within this family of methods, it is impossible within it. The remaining honest
options are to aim at the floor (for which classes does `AT` hit it?) or to leave the family
for probabilistic methods. Recommending the former, since the census hands us a conjecture
instead of a blank page.

---

## 2026-09-11 - status check on the List Colouring Conjecture

**Checking the literature before proposing work, for once.** The pattern of this project has
been to start computing and discover the obstruction afterwards. Here I looked up the status
first. It took four searches and changed the recommendation: the conjecture is open, but the
open part is concentrated (even-order complete graphs), and both of our tools are the two
that have actually produced results on it.

**The key realisation about the floor.** The `mad/2 + 1` floor from `05-alon-tarsi.md` sounded
like it closed off the polynomial method entirely. It does not apply here. On line graphs the
target `chi'` sits around `Delta`, which is above the floor, not below it. The conjecture asks
for **exactness**, not for a smaller bound, and that is a question these methods can answer.
So the floor rules out the halving we wanted, and rules out nothing about this problem.

**Setting expectations rather than overselling.** This is a fifty-year-old named conjecture
and the 2026 progress on it uses Pfaffian sign structure and Burnside reduction over signed
one-factorizations. Recording plainly that it is not a problem to expect to settle, and
proposing two proportionate entry points instead of a frontal attack.

---

## 2026-09-11 - the actual target, and where kernels stop

**Realigning after a drift I caused.** The user showed chapter 33 of *Proofs from THE BOOK*.
Its Lemma 1 is the kernel lemma this whole project rests on, and its closing conjecture, "does
`chi(H) = chi_ell(H)` for every line graph `H`", is the target. That is the List Colouring
Conjecture, which I had named without connecting it back to the chapter, and then compounded
the confusion by suggesting a change of goal. The lesson is to tie any literature name back
to the user's own source before building on it.

**Asking a definition-free question.** Rather than guess how "Galvin orientation" generalises
beyond bipartite, I asked the question the lemma actually needs: does `L(G)` have a
kernel-perfect orientation with `Delta+ <= chi'(G) - 1`? That is decidable by exhaustive
search, so no definitional guesswork was involved and the answer is certain.

**The answer, and it is sharp.** Bipartite cases pass, as Galvin guarantees. `C_5` and the
triangle pass via acyclic orientations. **`K_4` fails.** `L(K_4)` is the octahedron, 4-regular
on 6 vertices, so `Delta+ <= 2` forces every out-degree to be exactly 2; there are 38 such
orientations and all 38 contain a directed triangle, which has no kernel.

**Why this is the finding that matters.** `AT(L(K_4)) = 3`, computed earlier in the same
session, so Alon-Tarsi proves the `K_4` case that kernels provably cannot. The 2-d kernel
programme was therefore refining a tool that cannot reach the target problem even in
principle, and the three earlier negatives were symptoms of that, not separate facts. Had I
tested the base method against the actual target in session one, the whole detour would have
been unnecessary.

---

## 2026-09-11 - the two methods are incomparable

**A result that contradicted my own notes, so I checked it rather than reporting it.** The
census threw up `K_{3,3}` as a graph where `AT(L(G)) > chi'(G)`. That contradicted my earlier
claim that Alon-Tarsi is stronger than the kernel method, and `K_{3,3}` is bipartite, so
Galvin certainly proves it. Rather than trust either side, I built Galvin's own orientation of
`S_3` from the chapter's Latin square and ran both tests on that single object.

**The answer.** Galvin's orientation has all out-degrees 2 and is kernel-perfect, so Lemma 1
gives `chi_ell(S_3) <= 3`. Its `EE - EO` is zero, so Alon-Tarsi says nothing about it, and
exhaustively `AT(S_3) = 4`. My claim was wrong, and it was wrong in three files, now corrected.

**What it means, which is more than a correction.** `K_4` is a case kernels cannot do and
Alon-Tarsi can. `K_{3,3}` is a case Alon-Tarsi cannot do and kernels can. The two methods are
**incomparable**, so the previous verdict that kernels are finished is withdrawn. This also
matches the history: Alon and Tarsi got Dinitz only for special `n`, Galvin got all `n`.

**The question this opens, which is better than the one we had.** Across all `G` with at most
6 edges, every single one is covered by at least one of the two methods, and no graph has yet
been found where both fail. So the target becomes a dichotomy: does every line graph admit
either a thin kernel-perfect orientation or a thin orientation with `EE != EO`? That is
concrete, checkable, and directly on the conjecture, rather than an attempt to improve one
method in isolation.

**Method note.** The useful move here was cross-checking a surprising computation against a
hand-built object from the source text, instead of collecting more data. The single `S_3`
calculation settled the question and caught an error that had propagated through three files.

---

## 2026-09-11 - what a kernel-perfect orientation of a line graph must look like

**Asking what the method forces, rather than searching harder.** The joint census was slow
because the kernel side searches all orientations of `L(G)`. Instead of optimising that search
I asked what kernel-perfectness implies. The edges at a vertex `v` of `G` form a clique in
`L(G)`; a clique's kernel is a sink; every subset needs one; and a tournament in which every
subset has a sink is transitive. So a kernel-perfect orientation is a **linear order at every
vertex of `G`**, full stop.

**Which explains Galvin's Latin square.** He orders each row and each column by the Latin
square entry. The lemma says that shape was forced: there are no other candidates. The Latin
square is not a trick, it is the general form.

**And it locates the real obstruction.** In the tight case, `Delta`-regular class 1 graphs
where the out-degree budget is exactly consumed, the requirement becomes
`M(u,v) + M(v,u) = Delta - 1` with each row a permutation. Bipartite graphs solve it with a
proper edge colouring, counting up on one side and down on the other, which is exactly where
the bipartition is used. For `K_4` the system **is** solvable, so counting is not what stops it;
the triangles are. And `K_{2n}`, the hard open case of the conjecture, sits in precisely this
tight regime.

This is the first result in the project that says something about the structure of the target
problem rather than about the limits of a method.

---

## 2026-09-11 - Lemma 1 fails on the hard open case

**Using the star lemma as a search reduction, not just as a fact.** The lemma says a
kernel-perfect orientation of `L(G)` is a linear order at every vertex of `G`. That replaces a
search over `2^|E(L(G))|` orientations with a search over orderings, and made `K_6` and `K_8`
reachable where they had been hopeless.

**Validating the reduction before trusting it.** `K_4` was already decided by exhaustive
search over all 4096 orientations of the octahedron in an earlier session. The new reduction
reproduces that answer, which is why the `K_6` and `K_8` results can be believed.

**The result.** No valid order exists for `K_4`, `K_6` or `K_8`. Since the search is
exhaustive over everything the star lemma permits, this is a proof that Lemma 1 cannot prove
the conjecture for the three smallest even complete graphs, which are the smallest instances of
the hard open case.

**A pattern, and the exception that sharpened it.** The prism and `K_{2,2,2}` also fail; all
the failures contain triangles. `C_5 x K_2` passes, and it is triangle-free, so the triangle
test is vacuous there and proves nothing. Noticing that the one pass was the one case the test
could not see stopped me from reporting a false pattern, and turned it into a sharper working
conjecture: in the tight regular class-1 regime, triangles are what kill the kernel method.

**Why this feels like the right altitude at last.** Every earlier session measured the limits
of a method against generic graphs. This one measures a method against the specific graphs the
conjecture is open on, and gets a definite answer about them.

---

## 2026-09-11 - a theorem, and the limits of it

**Working the smallest case by hand instead of computing more.** The tight system for cubic
class-1 graphs has `M(u,v) + M(v,u) = 2` with rows permutations of `{0,1,2}`, so a triangle has
only nine `(p,q)` pairs to consider. Three are excluded by a row condition and the other six
each force `r` into a value a row already uses. Every case dies, giving a complete proof that a
triangle kills Lemma 1 on any cubic class-1 graph. That covers `K_4` and the prism.

**Checking whether the argument generalises, and finding that it does not.** Running the same
enumeration for larger `s` shows acyclic triangles do exist from `s = 3` upward, 6 of them at
`s = 3` and 132 at `s = 7`. So `Delta = 3` is special, and the failures of `K_6`, `K_8` and
`K_{2,2,2}` are global interactions, not the local obstruction. Saying that explicitly matters:
without it the theorem would look like it settles `K_{2n}`, and it does not.

**A claim from the previous session withdrawn.** Section `10` listed `C_5 x K_2` as passing.
It only passed the triangle test, which is vacuous for a triangle-free graph. The full check
shows the order found is thin enough but not kernel-perfect. That kills one order, not all, so
the case is undecided and the census is enumerating the rest. Lesson: a test that cannot see a
case must be reported as silent, not as a pass.

**Census so far.** Through 6 vertices and 9 edges: 114 graphs covered by both methods, 1 by
kernels alone, 7 by Alon-Tarsi alone, and **still none covered by neither**.

---

## 2026-09-11 - the theorem for all even complete graphs

**Why the local approach was never going to work, and what replaced it.** Section `11` showed
a single triangle is satisfiable once `Delta >= 4`, so `K_6` could not be killed triangle by
triangle. The move that worked was to stop looking at triangles in isolation and fix an
extreme instead: take the neighbour `j` with `M(i,j) = 0`, which forces `M(j,i) = s`, the
largest value in row `j`. Two of the three arcs of every triangle through `ij` are then
determined for free, and the third gives a single inequality `M(i,k) < M(j,k)` that holds for
**every** `k`. Summing over `k` contradicts the row totals, because row `i` lost its `0` and
row `j` lost its `s`.

**The result.** For every even `m >= 4`, `L(K_m)` has no kernel-perfect orientation with
`Delta+ <= m - 2`, so Lemma 1 cannot prove `ch'(K_m) = chi'(K_m)`. That is the entire hard open
case of the conjecture, closed to the chapter's own method, for all `m` at once rather than
case by case.

**Consistency.** The computations already in hand agree: exhaustive order search finds nothing
for `K_4`, `K_6`, `K_8`, and for `K_4` the independent scan of all 4096 orientations of the
octahedron agrees too. Three routes to the same answer.

**Method note worth keeping.** The two sessions of computation were not wasted, but the proof
did not come from more of them. It came from asking which configuration the constraints pin
down for free, and then counting. The computations said where to look, `K_4` first and then
`K_6` and `K_8`, and the counting said why.

---

## 2026-09-11 - the write-up, and what the literature check changed

**Checking the literature before writing, not after.** McDonald's paper would not extract
through the fetch tool, so I read the saved PDF directly. Her Theorem 5 states that
`L(K_n)` has no proper **Galvin** orientation with respect to `chi'(K_n)` for `n >= 4`. That
is close enough to our result that writing up without having read it would have been
careless.

**The distinction that survives.** A Galvin orientation is built from one global edge
colouring plus a `U`/`D` split of the vertices, so every vertex orders its edges by the
**same** colouring and only chooses a direction. The star lemma gives each vertex an
arbitrary linear order. Recovering a global colouring from a rank function would need each
vertex to play one role for all its edges, which is a bipartition, so on `K_m` our family is
strictly larger. Her theorem says Galvin's construction does not reach cliques; ours says the
kernel lemma does not, however the orientation is built. That is worth writing down, and the
paper says plainly that novelty in this generality is unconfirmed pending two specific
references.

**Also learned from the check.** `ch'(K_8) = 7` and `ch'(K_10) = 9` are known, by Rabern, via
signed one-factorization counts (`K_8` has 5280 positive and 960 negative, certificate 4320).
So the speculation that `K_8` might be open was wrong; the smallest uncovered even complete
graphs look to be around `K_20`.

**Draft state.** `latex/kernel-orientations-of-line-graphs.tex`, 7 pages, compiles clean with
no warnings or undefined references. Contains the star lemma with a four-step proof, the
budget lemma, the main theorem in nine steps, the cubic sharpness proposition with its case
table, two remarks delimiting scope, the computational verification section, and the
comparison with McDonald.

---

## 2026-09-11 - novelty check completed

**Both named references consulted.** Borodin, Kostochka and Woodall, *On kernel-perfect
orientations of line graphs*, Discrete Math. 191 (1998) 45 to 49, proves only the
characterisation: an orientation of a line graph is kernel-perfect iff every clique has a
kernel and every directed odd cycle has a chord or pseudochord. Its abstract makes no claim
about complete graphs or out-degree bounds. McDonald's theorem is about Galvin orientations,
a strictly smaller family for non-bipartite `G`. Neither contains our theorem.

**An attribution I owed, now paid.** The star lemma is not new in content: the necessity of
the clique half of the BKW characterisation, applied to every subset of `E(v)`, gives it
immediately. The paper now says so in a remark, keeps the direct proof for self-containedness,
and notes that the value added is the reformulation as a linear order, which is what makes the
rank function available. Writing "our lemma" without that would have been misleading.

**Honest status recorded in the paper.** Remark 7.3 now says the check was done, names what
was and was not read (abstract and McDonald's quotation of it, not the full 1998 text), and
states that a literature search cannot establish a negative. Novelty is likely but
unconfirmed, and the document says exactly that rather than either claiming or hedging vaguely.

**Census.** Still running at 7 vertices. Through 6 vertices and 9 edges: 114 covered by both
methods, 1 by kernels alone, 7 by Alon-Tarsi alone, none by neither.

---

## 2026-09-16 - realignment, and the terminology fix

**The goal was wrong in the repository, not just in my head.** The user's target is improving
the bound on list colouring. An earlier session saw them share chapter 33 of *Proofs from THE
BOOK*, inferred that the one-sentence line graph conjecture closing it on page 226 was the
target, and wrote that inference into `PROBLEM.md` and `CLAUDE.md` as settled fact. Every
session after that read it as established and worked on the wrong problem. The user corrected
it by pointing out the obvious thing, that chapter 33 is a chapter about list colouring. The
lesson is that an unconfirmed inference written into an alignment document is much harder to
detect later than one left in conversation, because it stops looking like an inference.

**What that costs and what it does not.** Notes `06` to `12` and the LaTeX paper are off
target and now say so in a banner. The star lemma and the even-complete-graph theorem are
still correct mathematics, so nothing is discarded. Notes `00` to `05` were on target all
along and are the live work.

**Terminology.** Independent plus 2-dominating sets are now **2-d kernels** everywhere, 318
occurrences across 22 documents, so they are never confused with the distance-based
`(k,l)`-kernel of the literature. Code identifiers (`twokernel`, `is_2kernel`) are untouched
and are a separate decision.

**The problem restated as three constraints, which is the user's framing and a better one.**
Have a 2-d kernel; still have one after removal, on every induced subdigraph, the way the
Dinitz proof gets a kernel for every induced subgraph out of a stable matching; and have the
list colouring problem map onto the class. These are (R1), (R2) and (R3) of note `01`, which
already had them, so the framing and the notes agree. The core difficulty is that all three
must hold at once.

**What to check first, and why that one.** The two-vertex barrier says no digraph with an arc
satisfies (star), which kills (R2) as literally stated. Before accepting that, the honest move
is to re-derive the `mad/2 + 1` floor of note `05` independently, because that floor is the
claim that decides whether the target is reachable at all, and it was written in one paragraph
by a session that was moving fast. Check the obstruction before running the experiment. This
is the mistake this project has now made three times.

## 2026-09-16 - the non-heredity theorem, written up

**The user's question was the right one and it has an exact answer.** They asked whether some
class of digraphs could inherit 2-d kernels the way "no odd directed cycle" inherits kernels
under Richardson. The answer is a clean iff: a class closed under induced subdigraphs has
2-d kernels throughout precisely when it is arcless. So there is no such class, and the
question is closed rather than open.

**Why it comes out so short.** The whole proof is one observation. A 2-d kernel needs two
distinct heads for the two arcs out of any excluded vertex, so it has at least two elements
whenever anything is outside it. An ordinary kernel has no such floor, a single vertex will
do. Heredity drags you down to two-vertex subdigraphs, and that is below the floor. Stating
it as a size lemma first made the rest fall out in three lines, where the earlier note `01`
version argued the two-vertex case directly and looked like a special-case trick.

**The part worth keeping beyond this project.** The obstruction is a single arc, which is
acyclic, so no condition on directed cycles can exclude it. That is why the Richardson
analogy cannot be repaired by choosing a better forbidden structure: any forbidding condition
is hereditary, so the theorem applies to it, and the thing it would have to forbid is the arc.
Recorded as a remark rather than left implicit, because "we did not find the right class" and
"there is no class" are very different statements.

**Draft.** `scratch.tex`, 4 pages, compiles with no warnings. Definitions from first
principles, size lemma, two-vertex lemma, the iff, the corollary that the 2-d form of Lemma 1
is vacuous, and the contrast with Richardson. Awaiting `./done.sh` to file it.

**Review pass, same day.** Two defects found in the draft, both in the commentary rather than
in the proof. First, Remark 4.3 wrote that the conclusion "forces $\mathcal{F}$ to exclude"
the single-arc digraph, with $\mathcal{F}$ the *forbidden* family, so the quantifier pointed
the wrong way. Second, and only visible once the first was being fixed, the same sentence
assumed every digraph with an arc contains the single-arc digraph as an *induced*
subdigraph. That is false here because the definitions admit digons, and the digon's only
two-vertex induced subdigraph is itself. The theorem was never at risk, since Lemma 2.2 is
stated for two vertices and at least one arc, but the remark's final clause was wrong. Fixed
by dropping the clause entirely: the content is that forbidding is hereditary, so the theorem
applies, and that is enough. A one-line note after Lemma 2.2 now records that both two-vertex
digraphs with an arc are covered, since that is the point the remark tripped over.

Section 5 was also overstated. It asserted the $\lceil d^{+}/2 \rceil + 1$ bound with no
proof and then leaned on it. The valid argument does not need it: whatever conclusion a
2-d version of Lemma 1 might draw, its hypothesis holds only for arcless digraphs, where the
colouring is immediate. Rewritten that way, with the halving demoted to a remark that is
explicitly labelled as motivation and not used. **Lesson: the error was in the part of the
document that was explaining rather than proving, which is where it was least likely to be
checked.**

**Filed.** Titled *Hereditary Classes of Digraphs with 2-d Kernels Are Arcless*, since the
title states the theorem rather than describing the topic. Authored to S. N. Mishra
(123CS0189). Definition 1.5 now says explicitly that this is the notion written 2-kernel in
the capstone research plan, so the supervisor can connect the two names without being told
separately. Filed as `latex/hereditary-2-d-kernels-are-arcless.tex` and
`notes/hereditary-2-d-kernels-are-arcless.pdf`, following the convention `done.sh` uses;
`scratch.tex` reset. Not committed.

## 2026-09-16 - raising the floor to three vertices, and why it closes

**The user's idea, and why it was the right shape.** After the arcless theorem the user asked
whether the induction could be cut off above two vertices instead: define the smallest
structure that can carry a 2-d kernel, insist on it only down to there, and pay separately for
whatever finite remainder is left. Three is the correct floor, since a 2-d kernel needs two
vertices inside and at least one outside. The move is legitimate. The arcless proof drags you
to two vertices and cannot reach a hypothesis that stops at three, and the out-star witnesses
that the resulting class is not empty. So this is not the old question in new clothes.

**Why the census went first.** Two things were worth doing, the census of the new class and
the accounting lemma with a general remainder term. The census went first because it can
close the route outright and the lemma cannot, and because a cheap decisive check before a
piece of theory is the standing instruction in this project that has been skipped three times.

**The answer is a classification, and it came out of the same lemma twice.** Working out when
a three-vertex digraph has a 2-d kernel at all takes four lines and leaves exactly two cases:
no arcs, or two non-adjacent vertices with the third pointing at both. Applying that to a
triangle kills triangles. Applying it to a path on three vertices makes non-adjacency
transitive. Transitive non-adjacency plus triangle-free is complete bipartite, and that is the
whole theorem. The orientations then pin down too: bidirected `K_{a,b}` for `a, b >= 2`, or a
star whose centre points at everything, with the back-arcs free.

**Verdict: closed, and for a sharper reason than "the class is small".** Every member has
chromatic number 2, which already makes a colouring theorem there uninteresting. The stronger
point is that the bound is not just redundant but exponentially wrong: Theorem 13.4 leaves no
choice of orientation, so on `K_{a,b}` we are stuck with `Delta+ = max(a, b)` and a bound of
about `max(a,b)/2`, where the truth is `O(log max(a,b))`. Orienting more cleverly leaves the
class. That is worth more than the count, because a small class with a good bound would still
have been interesting.

**What the census did not close, and the planning correction.** Raising the floor does not
touch the real failure mode, and thinking it through was the useful part. The induction never
asks for a 2-d kernel of an arbitrary induced subdigraph. It asks for one of `D[A(c)]`, the
vertices whose list still contains the colour being processed. `A(c)` can be tiny while `D` is
huge, so the obstruction appears on the *first* step of a large instance and no base case can
absorb it. The fix has to be a choice rule at every step, which is route (B1), not a floor.
Recorded in note `13` so the next session does not re-propose the floor.

**Tooling defect found on the way.** `twokernel.canon.certificate` falls back to a
Weisfeiler-Leman canonical form capped at `CANON_MAX_N = 7` when pynauty is absent, and above
the cap returns a key that is not canonical rather than failing. The first run reported 148
members on 8 vertices instead of 12. Caught only because 148 stars contradicted the shape of
the answer, not by any warning. `three_hereditary.py` now carries its own exact certificate
and agrees with the capped one for `n <= 7`. Anything in this repository that enumerates above
7 vertices without pynauty should be treated as suspect.

**Cutoff `k = 4`, checked because the obvious next question is "so raise it further".** The
`k = 3` verdict does not transfer. Without the three-vertex lemma triangles are no longer
excluded and they appear, the class grows to 192 members on 7 vertices, and `chi` reaches 3.
More to the point the halved bound is not vacuous there: it beats greedy on about 15 per cent
of members. But the gain is 1 or 2 colours and is not growing, and a genuine halving should
gain proportionally to `Delta`. Recorded in the appendix of note `13` as an observation on
`n <= 7`, explicitly not a theorem, with the two questions that would settle it. Comparing
against greedy rather than counting the class was the move that made this informative; the
count alone would have read as encouraging.

## 2026-09-16 - the remainder term, and a correction to the barrier

**Why the remainder lemma was worth writing even though note `00` already had the general
`f`.** Note `00` assumes the induction reaches the empty digraph. Carrying the leftover
explicitly costs four lines and turns "pay for the remainder somehow" into `f(Delta+) + r - 1`,
and then into the criterion `r <= floor(Delta+/2)`. Having a number to aim at is the whole
value; the route had been discussed for several sessions without one.

**The step that made the proof work.** The invariant survives only because a vertex with no
neighbour in `K` is allowed to *keep* the colour. Note `01` had already observed this for
(star) but note `00`'s Step 4 removes the colour from all of `S`, which would break the
accounting the moment the remainder slack is introduced. Worth knowing the two notes differed.

**The correction, which is the real result of the day.** The two-vertex barrier has been
treated since note `01` as fatal to (R2), and the arcless theorem was built on it. It is not
fatal. (star) demands two out-neighbours in `K`; the accounting lemma only demands that `f`
drop by one, and `ceil(d/2)` drops on a single out-neighbour whenever `d+` is odd. The single
arc `u -> v` passes. So the barrier kills the 2-d kernel demand, not the requirement the proof
consumes, and everything downstream of it was answering a stronger question than necessary.

**What the corrected (R2) is worth.** Censused it. The class of parity-processable digraphs is
emphatically not arcless: 154 of 155 members on 6 vertices carry an arc. But it is sparse, with
at most `n` edges and degeneracy at most 2 throughout `n <= 7`, and always bipartite. Digons
are the reason: an out-degree counting both arcs of a digon destroys the parity the escape
depends on, so bidirected `C4`, `C6` and `K3` all fail while directed `C4` passes. So (R2) for
all `S` is closed on merit rather than by the barrier.

**Order of work, and why this order.** Lemma before census, unusually. Normally the cheap
decisive check goes first, but here the census could not be *specified* until the lemma
identified what condition to enumerate, and enumerating (star) again would have reproduced the
arcless theorem. Writing the general statement first is what exposed the parity gap.

**Where the project now stands.** One sharp question, in note `15`: bound `r` for a class that
excludes strongly connected tournaments. Route (B1) is the only live line, and it is now a
question about the base case of Theorem 14.4, not about 2-d kernels.

**Cutoff `k = 5`, and a pattern worth a name.** Max chromatic number of the `k`-hereditary
class came out 2, 3, 4 for `k = 3, 4, 5`, that is `k - 1`, at every size computed. Combined
with Theorem 14.4 that is a conservation law in the making: cutting off at `k` leaves a
remainder of `k - 1`, so the bound is `ceil(Delta+/2) + (k - 1)` while the class it applies to
has chromatic number at most `k - 1`. You pay exactly what the enrichment is worth and the
halving never appears as a gain. Suggestive only, since the bound is about `chi_ell` and the
observation is about `chi`, but it is cheap to settle and would close the whole cutoff family
in one stroke. Recorded in the appendix of note `13` as a conjecture with its data.

## 2026-09-16 - the floor, finally measured

**Why it could be done now and not before.** The floor has been the stated first task for
several sessions and was skipped every time, including twice by me today. The reason it kept
sliding is that it was unmeasurable as written: "the family bottoms out at `mad/2 + 1`" names
no quantity to compute. Theorem 14.4 supplies one. Once the bound is
`ceil(Delta+/2) + max(1, r)`, the floor is a statement about `r` and can be checked by
enumeration. The lesson is that a vague obstruction is not checked by trying harder, it is
checked by first finding the lemma that turns it into a number.

**The trick that made it computable.** `r(D)` is defined through list assignments, and
enumerating those is hopeless. Lemma 16.1 removes them: a digraph stalls exactly when its bad
colour classes cover the vertex set, because a bad set can be repeated across as many colours
as a list needs. That collapses an exponential search over assignments into one pass over
subsets.

**Result: the floor holds.** Over all 207 graphs to 6 vertices, minimising over every
orientation, none beats `D* + 1`. 47 meet it exactly, 160 do worse. So the halving never once
converts into a bound below what the ordinary kernel method already floors at.

**The three obstructions are one.** This is the part worth carrying forward. The two-vertex
barrier says you cannot always get two out-arcs into `K`. The parity escape of 14.6 says one
out-arc suffices when `d+` is odd, which is why (R2) is not arcless after all. Lemma 16.2 says
the escape can never be hereditary, because deleting an out-neighbour of `u` flips the parity
at `u`. So "sometimes one is enough" cannot be upgraded, and the floor is what you measure when
all three are in force. Three notes had been treating these as separate findings.

**Consequence for the goal, which is the user's call and not mine.** `ceil(Delta+/2) + 1` looks
unreachable by this family. The Reed-shaped target `ceil((Delta + 1 + omega)/2)` survives, and
note `14` reduces it to one bounded question: can the remainder be paid at `omega/2` instead of
`omega` by reusing colours the induction already spent. Flagged rather than written into the
goal, because changing the stated aim of the project is not a change to make unilaterally.
