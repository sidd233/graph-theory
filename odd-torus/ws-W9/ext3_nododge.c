/* m = 3, Case 1 of the simplified proof. Row r = 0 pinned to alpha, alpha not in L1[0].
   Columns C1 (lists L1) and C2 (lists L2) are deleted. Adversary colours C0 (x0 = alpha,
   x1, x2 arbitrary) and C3 (y arbitrary proper, y_{r'} != beta). Claim: for r' in {1,2} and
   beta = the colour of L2[r'] \ L2[r''] when |L2[r'] & L2[r'']| = 2 (no constraint otherwise),
   the prism C1, C2 is always colourable. Lists are size 3 on palette P; colour index P = "outside". */
#include <stdio.h>
#include <stdlib.h>
static int P;
static int ok(int u0,int u1,int u2,int v0,int v1,int v2){
  for(int a=0;a<P;a++) if(u0>>a&1) for(int b=0;b<P;b++) if(b!=a&&(u1>>b&1)) for(int c=0;c<P;c++) if(c!=a&&c!=b&&(u2>>c&1))
   for(int d=0;d<P;d++) if(d!=a&&(v0>>d&1)) for(int e=0;e<P;e++) if(e!=b&&e!=d&&(v1>>e&1))
    for(int f=0;f<P;f++) if(f!=c&&f!=d&&f!=e&&(v2>>f&1)) return 1;
  return 0;}
int main(int argc,char**argv){
  P=atoi(argv[1]); int S[64],ns=0;
  for(int s=0;s<(1<<P);s++) if(__builtin_popcount(s)==3) S[ns++]=s;
  int U0=7; long cfg=0,fail=0;
  for(int i1=0;i1<ns;i1++)for(int i2=0;i2<ns;i2++)for(int j0=0;j0<ns;j0++)for(int j1=0;j1<ns;j1++)for(int j2=0;j2<ns;j2++){
    int L1[3]={U0,S[i1],S[i2]}, L2[3]={S[j0],S[j1],S[j2]};
    for(int rp=1;rp<=2;rp++){ int rq=3-rp; cfg++;
      int beta=P; int I=L2[rp]&L2[rq];
      if(0){int d=L2[rp]&~L2[rq]; beta=__builtin_ctz(d);}
      int bad=0;
      for(int x1=0;x1<=P&&!bad;x1++) for(int x2=0;x2<=P&&!bad;x2++){
        if(x1==x2&&x1<P) continue;
        int u1=L1[1]&~(1<<x1), u2=L1[2]&~(1<<x2);
        for(int y0=0;y0<=P&&!bad;y0++)for(int y1=0;y1<=P&&!bad;y1++)for(int y2=0;y2<=P&&!bad;y2++){
          int y[3]={y0,y1,y2};
          if((y0==y1&&y0<P)||(y0==y2&&y0<P)||(y1==y2&&y1<P)) continue;
          if(beta<P && y[rp]==beta) continue;
          if(!ok(L1[0],u1,u2,L2[0]&~(1<<y0),L2[1]&~(1<<y1),L2[2]&~(1<<y2))){bad=1;
            if(fail<5) printf("FAIL L1=%x %x %x L2=%x %x %x r'=%d x=%d %d y=%d %d %d\n",L1[0],L1[1],L1[2],L2[0],L2[1],L2[2],rp,x1,x2,y0,y1,y2);}
        }}
      fail+=bad; }}
  printf("palette %d: %ld (lists, r') cases, %ld failures\n",P,cfg,fail); return 0;}
