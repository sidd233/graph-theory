/* W11: hill-climb for a counterexample to the WINDOW STATEMENT on C5 x Cn.
   An assignment "evades" if every cut is bad: for every trigger (r,j) with L(r,j) != L(r,j+1),
   the forward window (cols j+1, j+2) is bad for every alpha in L(r,j)\L(r,j+1), and the
   backward window (cols j, j-1) is bad for every alpha in L(r,j+1)\L(r,j). Window model and
   74 shapes exactly as ws-W8/window5g.c (alpha real: x_1, x_4 != alpha).
   Objective = number of triggers with at least one good cut (0 = evader). We search for an
   evader that is NOT row-constant, column-constant or one-free-row.
   Run: ./evade N PALETTE STEPS SEED                                                             */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int U;
#define NONE 31
static int nsh, sh0[100][5], sh3[100][5];
static U L1[5], L2[5]; static int ALPHA;
static int fill(const U*A,const U*B){
  int c[10]; int i=0; U cand[10]; cand[0]=A[0];
  for(;;){ if(cand[i]==0){ if(--i<0) return 0; continue; }
    int col=__builtin_ctz(cand[i]); cand[i]&=cand[i]-1; c[i]=col; i++; if(i==10) return 1;
    U L=i<5?A[i]:B[i-5]; U forb=0;
    if(i<5){forb|=1u<<c[i-1]; if(i==4) forb|=1u<<c[0];}
    else{int t=i-5; forb|=1u<<c[t]; if(t>0) forb|=1u<<c[i-1]; if(t==4) forb|=1u<<c[5];}
    cand[i]=L&~forb; }}
static int xs[1024][5],ys[2048][5],nx,ny; static int F[300000][2],nf;
static void enumerate(void){
  int opt[5][5],no[5];
  for(int t=0;t<5;t++){no[t]=0;for(int c=0;c<31;c++) if(L1[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  nx=0; int x[5]; x[0]=NONE;
  for(int a=0;a<no[1];a++)for(int b=0;b<no[2];b++)for(int c=0;c<no[3];c++)for(int d=0;d<no[4];d++){
    x[1]=opt[1][a];x[2]=opt[2][b];x[3]=opt[3][c];x[4]=opt[4][d]; int ok=1;
    for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0;
    if(x[1]==ALPHA||x[4]==ALPHA) ok=0; if(ok) memcpy(xs[nx++],x,sizeof x);}
  for(int t=0;t<5;t++){no[t]=0;for(int c=0;c<31;c++) if(L2[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  ny=0; int y[5];
  for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++)for(int d=0;d<no[3];d++)for(int e=0;e<no[4];e++){
    y[0]=opt[0][a];y[1]=opt[1][b];y[2]=opt[2][c];y[3]=opt[3][d];y[4]=opt[4][e]; int ok=1;
    for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(ok) memcpy(ys[ny++],y,sizeof y);}
  nf=0;
  for(int i=0;i<nx;i++){U A[5]; for(int t=0;t<5;t++) A[t]=xs[i][t]==NONE?L1[t]:(L1[t]&~(1u<<xs[i][t]));
    for(int j=0;j<ny;j++){U B[5]; for(int t=0;t<5;t++) B[t]=ys[j][t]==NONE?L2[t]:(L2[t]&~(1u<<ys[j][t]));
      if(!fill(A,B)){F[nf][0]=i;F[nf][1]=j;nf++;}}}}
static int R[5],S[5],nr;
static int good_with(int depth,int*fc){
  if(depth==nr){ for(int f=0;f<nf;f++){ int hit=1;
      for(int i=0;i<nr&&hit;i++){ int v=S[i]?ys[F[f][1]][R[i]]:xs[F[f][0]][R[i]]; if(v==fc[i]) hit=0; }
      if(hit) return 0; } return 1; }
  U L=S[depth]?L2[R[depth]]:L1[R[depth]];
  for(int c=0;c<31;c++) if(L>>c&1){ fc[depth]=c; if(good_with(depth+1,fc)) return 1; }
  return 0;}
/* memo: window (pin row 0) + alpha -> good? */
#define HS (1<<22)
static unsigned long long hk[HS]; static signed char hv[HS];
static unsigned long long key(void){ unsigned long long k=ALPHA; for(int t=0;t<5;t++){k=k*1000003ULL+L1[t]; k=k*1000003ULL+L2[t];} return k|1ULL; }
static int window_good(void){
  unsigned long long k=key(); unsigned h=(unsigned)(k^(k>>29))&(HS-1);
  while(hk[h]){ if(hk[h]==k) return hv[h]; h=(h+1)&(HS-1); }
  if(L1[0]>>ALPHA&1){ /* alpha must be outside L1[0] */ hk[h]=k; hv[h]=1; return 1; }
  enumerate(); int good=(nf==0);
  for(int s=0;s<nsh&&!good;s++){ nr=0; for(int t=1;t<5;t++) if(sh0[s][t]){R[nr]=t;S[nr]=0;nr++;}
    for(int t=0;t<5;t++) if(sh3[s][t]){R[nr]=t;S[nr]=1;nr++;} int fc[5]; if(good_with(0,fc)) good=1; }
  hk[h]=k; hv[h]=good; return good; }

/* W11: hunt for a bad window violating Conjecture N' (no 3-set equals >= 7 of the 10 lists).
   Score = number of (shape, forbidden colours) strategies that succeed (0 = bad window).
   Run: ./hunt PALETTE STEPS SEED */
static long count_strats(int depth,int*fc){
  if(depth==nr){ for(int f=0;f<nf;f++){ int hit=1;
      for(int i=0;i<nr&&hit;i++){ int v=S[i]?ys[F[f][1]][R[i]]:xs[F[f][0]][R[i]]; if(v==fc[i]) hit=0; }
      if(hit) return 0; } return 1; }
  U L=S[depth]?L2[R[depth]]:L1[R[depth]]; long k=0;
  for(int c=0;c<31;c++) if(L>>c&1){ fc[depth]=c; k+=count_strats(depth+1,fc); }
  return k;}
static long score(void){
  if(L1[0]>>ALPHA&1) return 1000000;
  enumerate(); if(nf==0) return 1000000; long tot=0;
  for(int s=0;s<nsh;s++){ nr=0; for(int t=1;t<5;t++) if(sh0[s][t]){R[nr]=t;S[nr]=0;nr++;}
    for(int t=0;t<5;t++) if(sh3[s][t]){R[nr]=t;S[nr]=1;nr++;} int fc[5]; tot+=count_strats(0,fc); }
  return tot; }
static int maxeq(void){ int best=0; U all[10]; for(int t=0;t<5;t++){all[t]=L1[t];all[5+t]=L2[t];}
  for(int i=0;i<10;i++){ int k=0; for(int j=0;j<10;j++) if(all[j]==all[i]) k++; if(k>best) best=k; } return best; }
static U rnd3(int P){ U s=0; while(__builtin_popcount(s)<3) s|=1u<<(rand()%P); return s; }
int main(int argc,char**argv){
  int P=atoi(argv[1]); long steps=atol(argv[2]); srand(atoi(argv[3]));
  FILE*f=fopen("shapes5.txt","r"); fscanf(f,"%d",&nsh);
  for(int k=0;k<nsh;k++){char a[8],b[8]; fscanf(f,"%s %s",a,b); for(int t=0;t<5;t++){sh0[k][t]=a[t]-'0';sh3[k][t]=b[t]-'0';}}
  U X=7; for(int t=0;t<5;t++){L1[t]=X;L2[t]=X;}
  for(int k=0;k<4;k++){ int p=rand()%10; if(p<5) L1[p]=rnd3(P); else L2[p-5]=rnd3(P); }
  do ALPHA=rand()%(P+1); while(ALPHA<P && (L1[0]>>ALPHA&1)); if(ALPHA==P) ALPHA=NONE;
  long cur=score()+(maxeq()>=6?1000000:0), best=cur;
  for(long s=0;s<steps;s++){
    int p=rand()%11; U old=0; int olda=ALPHA;
    if(p<5){old=L1[p]; L1[p]=rnd3(P);} else if(p<10){old=L2[p-5]; L2[p-5]=rnd3(P);}
    else { ALPHA=rand()%(P+1); if(ALPHA==P) ALPHA=NONE; }
    long v=score()+(maxeq()>=6?1000000:0);
    if(v<=cur || rand()%30==0){ cur=v; if(v<best) best=v;
      if(v==0){ printf("BAD WINDOW WITH MAXEQ <= 5 at step %ld: alpha %d L1:",s,ALPHA);
        for(int t=0;t<5;t++) printf(" %03x",L1[t]); printf("  L2:"); for(int t=0;t<5;t++) printf(" %03x",L2[t]);
        printf("  maxeq %d\n",maxeq()); fflush(stdout); return 0; } }
    else { if(p<5) L1[p]=old; else if(p<10) L2[p-5]=old; else ALPHA=olda; }
    if(s%500==0){ printf("step %ld cur %ld best %ld\n",s,cur,best); fflush(stdout);} }
  printf("none found; best score %ld\n",best); return 0; }
