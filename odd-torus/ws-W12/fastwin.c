/* W12: fast window judge (same model as ws-W8/window5g.c: pin row 0, alpha real, 74 shapes).
   Speed-up: a fill exists for (x, y) iff some proper colouring b of the C2 cycle from B - y is
   compatible with some proper colouring a of the C1 cycle from A - x. Enumerate all proper
   colourings of the C2 cycle from the FULL lists (at most 3^5); Mx = bitset of those compatible
   with some colouring of C1 from A - x; Ny = bitset of those using only B - y. (x,y) fails iff
   Mx & Ny == 0.
   Library use: int judge(U L1[5], U L2[5], int alpha)  -> 1 good, 0 bad.                     */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int U; typedef unsigned long long W;
#define NONE 31
int nsh, sh0[100][5], sh3[100][5];
static int vb[256][5], nvb;                 /* proper colourings of C2 from full lists */
static int nx, ny, xs[1024][5], ys[1024][5];
static W Mx[1024][4], Ny[1024][4];
static int F[300000][2], nf;
static void cyc_cols(const U*L, int (*out)[5], int*n){
  *n=0; int o[5][3],no[5];
  for(int t=0;t<5;t++){no[t]=0; for(int c=0;c<31;c++) if(L[t]>>c&1) o[t][no[t]++]=c;}
  for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++)for(int d=0;d<no[3];d++)for(int e=0;e<no[4];e++){
    int z[5]={o[0][a],o[1][b],o[2][c],o[3][d],o[4][e]}; int ok=1;
    for(int t=0;t<5;t++) if(z[t]==z[(t+1)%5]) ok=0;
    if(ok){ memcpy(out[*n],z,sizeof z); (*n)++; } } }
int judge_core(const U*L1,const U*L2,int alpha){
  cyc_cols(L2,vb,&nvb);
  int ox[5][4],nox[5]; for(int t=0;t<5;t++){nox[t]=0; for(int c=0;c<31;c++) if(L1[t]>>c&1) ox[t][nox[t]++]=c; ox[t][nox[t]++]=NONE;}
  nx=0; int x[5]; x[0]=NONE;
  for(int a=0;a<nox[1];a++)for(int b=0;b<nox[2];b++)for(int c=0;c<nox[3];c++)for(int d=0;d<nox[4];d++){
    x[1]=ox[1][a];x[2]=ox[2][b];x[3]=ox[3][c];x[4]=ox[4][d]; int ok=1;
    for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0;
    if(x[1]==alpha||x[4]==alpha) ok=0; if(!ok) continue;
    U A[5]; for(int t=0;t<5;t++) A[t]= x[t]==NONE?L1[t]:(L1[t]&~(1u<<x[t]));
    static int ac[256][5]; int na; cyc_cols(A,ac,&na);
    memset(Mx[nx],0,sizeof Mx[nx]);
    for(int i=0;i<nvb;i++){ for(int k=0;k<na;k++){ int ok2=1; for(int t=0;t<5;t++) if(ac[k][t]==vb[i][t]){ok2=0;break;}
        if(ok2){ Mx[nx][i>>6]|=1ULL<<(i&63); break; } } }
    memcpy(xs[nx],x,sizeof x); nx++; }
  int oy[5][4],noy[5]; for(int t=0;t<5;t++){noy[t]=0; for(int c=0;c<31;c++) if(L2[t]>>c&1) oy[t][noy[t]++]=c; oy[t][noy[t]++]=NONE;}
  ny=0; int y[5];
  for(int a=0;a<noy[0];a++)for(int b=0;b<noy[1];b++)for(int c=0;c<noy[2];c++)for(int d=0;d<noy[3];d++)for(int e=0;e<noy[4];e++){
    y[0]=oy[0][a];y[1]=oy[1][b];y[2]=oy[2][c];y[3]=oy[3][d];y[4]=oy[4][e]; int ok=1;
    for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(!ok) continue;
    memset(Ny[ny],0,sizeof Ny[ny]);
    for(int i=0;i<nvb;i++){ int ok2=1; for(int t=0;t<5;t++) if(y[t]==vb[i][t]){ok2=0;break;} if(ok2) Ny[ny][i>>6]|=1ULL<<(i&63); }
    memcpy(ys[ny],y,sizeof y); ny++; }
  { /* quick test on inclusion-minimal sets: if no failing pair among them, none at all */
    static int mi[1024], mj[1024]; int nmi=0, nmj=0;
    for(int i=0;i<nx;i++){ int dom=0; for(int k=0;k<nx&&!dom;k++){ if(k==i) continue;
        int sub=1, eq=1; for(int w=0;w<4;w++){ if(Mx[k][w]&~Mx[i][w]) sub=0; if(Mx[k][w]!=Mx[i][w]) eq=0; }
        if(sub && (!eq || k<i)) dom=1; } if(!dom) mi[nmi++]=i; }
    for(int j=0;j<ny;j++){ int dom=0; for(int k=0;k<ny&&!dom;k++){ if(k==j) continue;
        int sub=1, eq=1; for(int w=0;w<4;w++){ if(Ny[k][w]&~Ny[j][w]) sub=0; if(Ny[k][w]!=Ny[j][w]) eq=0; }
        if(sub && (!eq || k<j)) dom=1; } if(!dom) mj[nmj++]=j; }
    int anyfail=0;
    for(int a=0;a<nmi&&!anyfail;a++) for(int b=0;b<nmj&&!anyfail;b++){ int i=mi[a], j=mj[b];
      if(!((Mx[i][0]&Ny[j][0])|(Mx[i][1]&Ny[j][1])|(Mx[i][2]&Ny[j][2])|(Mx[i][3]&Ny[j][3]))) anyfail=1; }
    if(!anyfail) return 1; }
  nf=0;
  for(int i=0;i<nx;i++) for(int j=0;j<ny;j++){
    if(!((Mx[i][0]&Ny[j][0])|(Mx[i][1]&Ny[j][1])|(Mx[i][2]&Ny[j][2])|(Mx[i][3]&Ny[j][3]))){ F[nf][0]=i;F[nf][1]=j;nf++; } }
  if(nf==0) return 1;
  static U L1s[5],L2s[5]; memcpy(L1s,L1,sizeof L1s); memcpy(L2s,L2,sizeof L2s);
  for(int s=0;s<nsh;s++){
    int R[5],S[5],nr=0; for(int t=1;t<5;t++) if(sh0[s][t]){R[nr]=t;S[nr]=0;nr++;} for(int t=0;t<5;t++) if(sh3[s][t]){R[nr]=t;S[nr]=1;nr++;}
    int o[3][3],no[3]; for(int k=0;k<3;k++){ U L=S[k]?L2s[R[k]]:L1s[R[k]]; no[k]=0; for(int c=0;c<31;c++) if(L>>c&1) o[k][no[k]++]=c; }
    for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++){
      int fc[3]={o[0][a],o[1][b],o[2][c]}; int good=1;
      for(int f=0;f<nf&&good;f++){ int hit=1; for(int k=0;k<3&&hit;k++){ int v=S[k]?ys[F[f][1]][R[k]]:xs[F[f][0]][R[k]]; if(v==fc[k]) hit=0; } if(hit) good=0; }
      if(good) return 1; } }
  return 0; }
void load_shapes(const char*fn){ FILE*f=fopen(fn,"r"); fscanf(f,"%d",&nsh);
  for(int k=0;k<nsh;k++){char a[8],b[8]; fscanf(f,"%s %s",a,b); for(int t=0;t<5;t++){sh0[k][t]=a[t]-'0';sh3[k][t]=b[t]-'0';}} fclose(f); }
#ifdef TESTMAIN
int main(void){ load_shapes("shapes5.txt"); char line[512]; long n=0,g=0;
  while(fgets(line,sizeof line,stdin)){ U L1[5],L2[5]; int a;
    if(sscanf(line,"%d L1: %x %x %x %x %x L2: %x %x %x %x %x",&a,&L1[0],&L1[1],&L1[2],&L1[3],&L1[4],&L2[0],&L2[1],&L2[2],&L2[3],&L2[4])!=11) continue;
    n++; int r=judge_core(L1,L2,a); g+=r; printf("%d\n",r); }
  fprintf(stderr,"%ld windows, %ld good\n",n,g); return 0; }
#endif
