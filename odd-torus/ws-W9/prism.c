/* Exhaustive check of the two-column lemma for the prism K3 x K2 (W9).
   Vertices u0,u1,u2 (triangle), v0,v1,v2 (triangle), edges u_t v_t.
   Lists: |A0| = 3, |A1| = |A2| = |B0| = |B1| = |B2| = 2.
   Every such assignment is, after renaming colours in order of first appearance
   (reading A0, A1, A2, B0, B1, B2), one where A0 = {0,1,2} and each later list uses old
   colours plus a prefix u, u+1 of fresh ones (u = number of colours used so far).
   We enumerate exactly those, so the check covers every list assignment.
   Checks:
     (L)  not colourable  =>  B1 == B2                      (the lemma used in the proof)
     (P)  not colourable  <=> (Z) or (W)                     (the prism lemma as stated in the notes)
   (Z): B0 == B1 == B2.  (W): A1 == A2 == D, A0 == D + {z}, B1 == B2 == E, B0 \ E == {z}.
   Run: ./prism                                                                      */
#include <stdio.h>
typedef unsigned int U;
static int col(U a0,U a1,U a2,U b0,U b1,U b2){
  for(int a=0;a<16;a++) if(a0>>a&1) for(int b=0;b<16;b++) if(b!=a&&(a1>>b&1))
   for(int c=0;c<16;c++) if(c!=a&&c!=b&&(a2>>c&1))
    for(int d=0;d<16;d++) if(d!=a&&(b0>>d&1)) for(int e=0;e<16;e++) if(e!=b&&e!=d&&(b1>>e&1))
     for(int f=0;f<16;f++) if(f!=c&&f!=d&&f!=e&&(b2>>f&1)) return 1;
  return 0;}
/* all 2-subsets of {0..u+1} that are canonical: fresh colours form a prefix u, u+1 */
static int pairs(int u,U*out){int n=0;
  for(int i=0;i<u+2;i++)for(int j=i+1;j<u+2;j++){
    if(j==u+1&&i!=u&&i>=u) continue;        /* never happens, kept for clarity */
    if(j==u+1&&i<u) continue;               /* uses u+1 without u */
    out[n++]=(1u<<i)|(1u<<j);}
  return n;}
static int used(U s){return 32-__builtin_clz(s);} /* colours are a prefix 0..k-1 */
int main(void){
  U A0=7, L[5][128]; long total=0,nonc=0,badL=0,badP=0;
  int n1=pairs(3,L[0]);
  for(int i1=0;i1<n1;i1++){U A1=L[0][i1]; int u1=used(A0|A1);
   int n2=pairs(u1,L[1]);
   for(int i2=0;i2<n2;i2++){U A2=L[1][i2]; int u2=used(A0|A1|A2);
    int n3=pairs(u2,L[2]);
    for(int i3=0;i3<n3;i3++){U B0=L[2][i3]; int u3=used(A0|A1|A2|B0);
     int n4=pairs(u3,L[3]);
     for(int i4=0;i4<n4;i4++){U B1=L[3][i4]; int u4=used(A0|A1|A2|B0|B1);
      int n5=pairs(u4,L[4]);
      for(int i5=0;i5<n5;i5++){U B2=L[4][i5]; total++;
       int ok=col(A0,A1,A2,B0,B1,B2);
       int Z=(B0==B1&&B1==B2);
       U zeta=A0&~A1;
       int W=(A1==A2&&(A1&A0)==A1&&B1==B2&&__builtin_popcount(zeta)==1&&(B0&~B1)==zeta);
       if(!ok){nonc++; if(B1!=B2) badL++;}
       if((!ok)!=(Z||W)){badP++; if(badP<5) printf("prism mismatch %x %x %x %x %x %x ok=%d\n",A0,A1,A2,B0,B1,B2,ok);}
  }}}}}
  printf("canonical assignments %ld, not colourable %ld\n",total,nonc);
  printf("(L) not colourable but B1 != B2: %ld\n",badL);
  printf("(P) mismatches with (Z) or (W): %ld\n",badP);
  return 0;}
