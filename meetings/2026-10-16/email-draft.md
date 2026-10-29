To: Prof. T. K. Mishra
Subject: Formal proof: Galvin's kernel method on regular graphs works only for bipartite graphs

Dear Sir,

As discussed in our meeting on 9 October, I am attaching a formal proof of the converse
direction of Galvin's bound for regular graphs.

**Theorem.** Let G be a simple k-regular graph. The line graph L(G) has a kernel-perfect
orientation with every out-degree at most k - 1 if and only if G is bipartite.

The "if" direction is Galvin's theorem. The proof of the "only if" direction is in eight short
steps: every vertex ranks its edges; the out-degree budget is used exactly; there is no odd ring;
this gives an orientation of G itself; its directed cycles are rings; it has no odd directed
closed walk; every arc can be walked back in an odd number of steps; and so every cycle of G is
even. I have also checked the statement by computer on 1923 regular graphs; a kernel-perfect
orientation exists in exactly the 29 bipartite ones.

A consequence is that the kernel method cannot prove the List Edge Colouring Conjecture for any
non-bipartite regular graph. I have not found this result in the literature (Borodin, Kostochka
and Woodall 1998; McDonald 2015). I would be grateful to know if you have seen it before.

As you suggested, I am now working mainly on the torus problem,
chi_l(C_{2m+1} □ C_{2n+1}) = 3. [STATUS: one or two lines on where the torus work stands.]

Thank you for your time.

Regards,
Siddharth Mishra
