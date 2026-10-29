/* W11: Lemma S, case "no cut at w". C3 x Cn, w = (0, C0) with L(w) = {0,1}, and
   L(w) contained in A0 = L(0, C1); WLOG A0 = {0,1,2}. Strategy space (chosen before the strip is
   coloured): pin p0 in {0,1} at w, forbidden row r' in {1,2} of C3, forbidden colour beta (any
   colour, or none). Adversary: x1, x2 (C0 rows 1,2) proper with x0 = p0; y (C3) proper with
   y_{r'} != beta. Fill the prism C1, C2 with A_t minus x_t, B_t minus y_t.
   Claim tested: for every A1, A2, B0, B1, B2 some strategy works.  Run: ./lemmaS_ext P      */
#include <stdio.h>
#include <stdlib.h>
static int P;
static int ok(int u0,int u1,int u2,int v0,int v1,int v2){
  for(int a=0;a<P;a++) if(u0>>a&1) for(int b=0;b<P;b++) if(b!=a&&(u1>>b&1))
   for(int c=0;c<P;c++) if(c!=a&&c!=b&&(u2>>c&1))
    for(int d=0;d<P;d++) if(d!=a&&(v0>>d&1)) for(int e=0;e<P;e++) if(e!=b&&e!=d&&(v1>>e&1))
     for(int f=0;f<P;f++) if(f!=c&&f!=d&&f!=e&&(v2>>f&1)) return 1;
  return 0;}
int main(int argc,char**argv){
  P=atoi(argv[1]); int S[64],ns=0; for(int s=0;s<(1<<P);s++) if(__builtin_popcount(s)==3) S[ns++]=s;
  int A0=7; long cfg=0,fail=0;
  for(int i1=0;i1<ns;i1++)for(int i2=0;i2<ns;i2++)for(int j0=0;j0<ns;j0++)for(int j1=0;j1<ns;j1++)for(int j2=0;j2<ns;j2++){
    int A[3]={A0,S[i1],S[i2]}, B[3]={S[j0],S[j1],S[j2]}; cfg++; int found=0;
    for(int p0=0;p0<2&&!found;p0++) for(int rp=1;rp<=2&&!found;rp++) for(int beta=0;beta<=P&&!found;beta++){
      int good=1;
      for(int x1=0;x1<=P&&good;x1++) for(int x2=0;x2<=P&&good;x2++){
        if(x1==p0||x2==p0) continue; if(x1==x2&&x1<P) continue;
        int u0=A[0]&~(1<<p0), u1=A[1]&~(1<<x1), u2=A[2]&~(1<<x2);
        for(int y0=0;y0<=P&&good;y0++)for(int y1=0;y1<=P&&good;y1++)for(int y2=0;y2<=P&&good;y2++){
          int y[3]={y0,y1,y2};
          if((y0==y1&&y0<P)||(y0==y2&&y0<P)||(y1==y2&&y1<P)) continue;
          if(beta<P&&y[rp]==beta) continue;
          if(!ok(u0,u1,u2,B[0]&~(1<<y0),B[1]&~(1<<y1),B[2]&~(1<<y2))) good=0; }}
      if(good) found=1; }
    if(!found){ fail++; if(fail<=5) printf("NO STRATEGY: A=%x %x %x B=%x %x %x\n",A[0],A[1],A[2],B[0],B[1],B[2]); } }
  printf("palette %d: %ld configurations, %ld without a strategy\n",P,cfg,fail); return 0;}
