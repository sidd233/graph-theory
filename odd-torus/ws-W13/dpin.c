/* W13: double-pinned two-column window. u-side pin at row 0 of C0 (alpha fresh, so u_0 keeps all of A_0);
   v-side pin at row s of C3 (delta fresh, so v_s keeps all of B_s). Remaining unit: one forbidden colour,
   at a C0 row (x_t != gamma) or a C3 row (y_t != beta), as allowed by the 40 double-pin shapes.
   Adversary: x_1..x_4 (C0), y_t for t != s (C3), proper on the 5-cycles; colours outside lists remove nothing.
   GOOD(s) if some shape with C3 pin at s and some forbidden colour make every fill succeed.
   Run: ./dpin MODE P N SEED   (MODE 0 random lists, MODE 1 nearly constant: base {0,1,2} + K changes) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int U;
#define NONE 31
static U A[5],B[5];
static int fill(const U*Au,const U*Bv){
  int c[10]; int i=0; U cand[10]; cand[0]=Au[0];
  for(;;){ if(cand[i]==0){ if(--i<0) return 0; continue; }
    int col=__builtin_ctz(cand[i]); cand[i]&=cand[i]-1; c[i]=col; i++; if(i==10) return 1;
    U L=i<5?Au[i]:Bv[i-5]; U forb=0;
    if(i<5){forb|=1u<<c[i-1]; if(i==4) forb|=1u<<c[0];}
    else{int t=i-5; forb|=1u<<c[t]; if(t>0) forb|=1u<<c[i-1]; if(t==4) forb|=1u<<c[5];}
    cand[i]=L&~forb; }}
static int xs[512][5],ys[2048][5],nx,ny,F[600000][2],nf;
static void enumerate(int s){
  int o[5][5],no[5];
  for(int t=0;t<5;t++){no[t]=0; for(int c=0;c<31;c++) if(A[t]>>c&1) o[t][no[t]++]=c; o[t][no[t]++]=NONE;}
  nx=0; int x[5]; x[0]=NONE;
  for(int a=0;a<no[1];a++)for(int b=0;b<no[2];b++)for(int c=0;c<no[3];c++)for(int d=0;d<no[4];d++){
    x[1]=o[1][a];x[2]=o[2][b];x[3]=o[3][c];x[4]=o[4][d]; int ok=1;
    for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0; if(ok) memcpy(xs[nx++],x,sizeof x); }
  for(int t=0;t<5;t++){no[t]=0; if(t!=s) for(int c=0;c<31;c++) if(B[t]>>c&1) o[t][no[t]++]=c; o[t][no[t]++]=NONE;}
  ny=0; int y[5];
  for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++)for(int d=0;d<no[3];d++)for(int e=0;e<no[4];e++){
    y[0]=o[0][a];y[1]=o[1][b];y[2]=o[2][c];y[3]=o[3][d];y[4]=o[4][e]; int ok=1;
    for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(ok) memcpy(ys[ny++],y,sizeof y); }
  nf=0;
  for(int i=0;i<nx;i++){ U Au[5]; for(int t=0;t<5;t++) Au[t]= xs[i][t]==NONE?A[t]:(A[t]&~(1u<<xs[i][t]));
    for(int j=0;j<ny;j++){ U Bv[5]; for(int t=0;t<5;t++) Bv[t]= ys[j][t]==NONE?B[t]:(B[t]&~(1u<<ys[j][t]));
      if(!fill(Au,Bv)){F[nf][0]=i;F[nf][1]=j;nf++;}}}}
/* extra unit positions allowed with C3 pin at s (from the 40 shapes): C0 rows 1..4 (any s), or C3 row t != s */
static int good_s(int s){
  enumerate(s); if(nf==0) return 1;
  for(int side=0;side<2;side++) for(int t=0;t<5;t++){
    if(side==0 && t==0) continue; if(side==1 && t==s) continue;
    U L= side? B[t]:A[t];
    for(int c=0;c<31;c++) if(L>>c&1){ int ok=1;
      for(int f=0;f<nf&&ok;f++){ int v= side? ys[F[f][1]][t] : xs[F[f][0]][t]; if(v!=c) ok=0; }
      if(ok) return 1; } }
  return 0; }
static U r3(int P){ U s=0; while(__builtin_popcount(s)<3) s|=1u<<(rand()%P); return s; }
int main(int argc,char**argv){
  int mode=atoi(argv[1]),P=atoi(argv[2]); long N=atol(argv[3]); srand(atoi(argv[4]));
  long tot=0, badany=0, badall=0;
  for(long it=0;it<N;it++){
    if(mode==0){ for(int t=0;t<5;t++){A[t]=r3(P);B[t]=r3(P);} }
    else { for(int t=0;t<5;t++){A[t]=7;B[t]=7;} int K=1+rand()%3; for(int k=0;k<K;k++){int p=rand()%10; if(p<5)A[p]=r3(P); else B[p-5]=r3(P);} }
    tot++; int g=0, gall=1;
    for(int s=0;s<5;s++){ int r=good_s(s); if(r) g=1; else gall=0; }
    if(!g){ badany++; if(badany<=4){printf("BAD for every s: A"); for(int t=0;t<5;t++) printf(" %x",A[t]); printf(" B"); for(int t=0;t<5;t++) printf(" %x",B[t]); printf("\n");} }
    if(!gall) badall++; }
  printf("mode %d palette %d: %ld windows; bad for EVERY right-pin row s: %ld; bad for SOME s: %ld\n",mode,P,tot,badany,badall);
  return 0; }
