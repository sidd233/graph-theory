/* As prism.c, but every list except A0 may have 2 or 3 colours (A0 has 3).
   Checks (L'): not colourable => |B1| = |B2| = 2 and B1 == B2.
   Same canonical enumeration: each list = old colours + a prefix of fresh ones.     */
#include <stdio.h>
typedef unsigned int U;
static int col(U a0,U a1,U a2,U b0,U b1,U b2){
  for(int a=0;a<20;a++) if(a0>>a&1) for(int b=0;b<20;b++) if(b!=a&&(a1>>b&1))
   for(int c=0;c<20;c++) if(c!=a&&c!=b&&(a2>>c&1))
    for(int d=0;d<20;d++) if(d!=a&&(b0>>d&1)) for(int e=0;e<20;e++) if(e!=b&&e!=d&&(b1>>e&1))
     for(int f=0;f<20;f++) if(f!=c&&f!=d&&f!=e&&(b2>>f&1)) return 1;
  return 0;}
static int sets(int u,U*out){int n=0;              /* 2- and 3-subsets, fresh = prefix of u,u+1,u+2 */
  for(U s=1;s<(1u<<(u+3));s++){int p=__builtin_popcount(s); if(p<2||p>3) continue;
    U fresh=s>>u; if(fresh&(fresh+1)) continue;     /* fresh bits must be 0b0, 0b1, 0b11, 0b111 */
    out[n++]=s;} return n;}
static int used(U s){return 32-__builtin_clz(s);}
int main(void){
  static U L[5][1400]; U A0=7; long total=0,nonc=0,bad=0;
  int n1=sets(3,L[0]);
  for(int i1=0;i1<n1;i1++){U A1=L[0][i1]; int n2=sets(used(A0|A1),L[1]);
   for(int i2=0;i2<n2;i2++){U A2=L[1][i2]; U s2=A0|A1|A2; int n3=sets(used(s2),L[2]);
    for(int i3=0;i3<n3;i3++){U B0=L[2][i3]; U s3=s2|B0; int n4=sets(used(s3),L[3]);
     for(int i4=0;i4<n4;i4++){U B1=L[3][i4]; U s4=s3|B1; int n5=sets(used(s4),L[4]);
      for(int i5=0;i5<n5;i5++){U B2=L[4][i5]; total++;
       if(!col(A0,A1,A2,B0,B1,B2)){nonc++;
         if(!(B1==B2&&__builtin_popcount(B1)==2)) bad++;}}}}}}
  printf("canonical assignments (outer lists of size 2 or 3) %ld, not colourable %ld\n",total,nonc);
  printf("(L') not colourable but not (|B1|=|B2|=2 and B1 == B2): %ld\n",bad);
  return 0;}
