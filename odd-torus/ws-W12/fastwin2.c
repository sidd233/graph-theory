/* W12: faster window judge, same model and same verdicts as fastwin.c / ws-W8/window5g.c.
   colsA = proper colourings a of the C1 cycle from the full lists (a_0 from L1[0]);
   colsB = proper colourings b of the C2 cycle from the full lists; compat[k] = {b : b_t != a_k,t}.
   Adversary x: Mx = OR of compat[k] over a_k avoiding x (a_k,t != x_t). Adversary y: Ny = {b avoiding y}.
   (x, y) fails iff Mx & Ny = 0. Distinct Mx / Ny are deduplicated before the pair test.        */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int U; typedef unsigned long long W;
#define NONE 31
int nsh, sh0[100][5], sh3[100][5];
static int ca[256][5], cb[256][5], nca, ncb;
static W compat[256][4];
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
static int cmpW(const void*p,const void*q){ return memcmp(p,q,4*sizeof(W)); }
int judge_core(const U*L1,const U*L2,int alpha){
  cyc_cols(L1,ca,&nca); cyc_cols(L2,cb,&ncb);
  for(int k=0;k<nca;k++){ memset(compat[k],0,sizeof compat[k]);
    for(int i=0;i<ncb;i++){ int ok=1; for(int t=0;t<5;t++) if(ca[k][t]==cb[i][t]){ok=0;break;} if(ok) compat[k][i>>6]|=1ULL<<(i&63); } }
  int ox[5][4],nox[5]; for(int t=0;t<5;t++){nox[t]=0; for(int c=0;c<31;c++) if(L1[t]>>c&1) ox[t][nox[t]++]=c; ox[t][nox[t]++]=NONE;}
  nx=0; int x[5]; x[0]=NONE;
  for(int a=0;a<nox[1];a++)for(int b=0;b<nox[2];b++)for(int c=0;c<nox[3];c++)for(int d=0;d<nox[4];d++){
    x[1]=ox[1][a];x[2]=ox[2][b];x[3]=ox[3][c];x[4]=ox[4][d]; int ok=1;
    for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0;
    if(x[1]==alpha||x[4]==alpha) ok=0; if(!ok) continue;
    W m[4]={0,0,0,0};
    for(int k=0;k<nca;k++){ int av=1; for(int t=1;t<5;t++) if(ca[k][t]==x[t]){av=0;break;} if(av) for(int w=0;w<4;w++) m[w]|=compat[k][w]; }
    memcpy(Mx[nx],m,sizeof m); memcpy(xs[nx],x,sizeof x); nx++; }
  int oy[5][4],noy[5]; for(int t=0;t<5;t++){noy[t]=0; for(int c=0;c<31;c++) if(L2[t]>>c&1) oy[t][noy[t]++]=c; oy[t][noy[t]++]=NONE;}
  ny=0; int y[5];
  for(int a=0;a<noy[0];a++)for(int b=0;b<noy[1];b++)for(int c=0;c<noy[2];c++)for(int d=0;d<noy[3];d++)for(int e=0;e<noy[4];e++){
    y[0]=oy[0][a];y[1]=oy[1][b];y[2]=oy[2][c];y[3]=oy[3][d];y[4]=oy[4][e]; int ok=1;
    for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(!ok) continue;
    W m[4]={0,0,0,0};
    for(int i=0;i<ncb;i++){ int av=1; for(int t=0;t<5;t++) if(cb[i][t]==y[t]){av=0;break;} if(av) m[i>>6]|=1ULL<<(i&63); }
    memcpy(Ny[ny],m,sizeof m); memcpy(ys[ny],y,sizeof y); ny++; }
  /* dedupe copies for the quick test */
  static W dx[1024][4], dy[1024][4]; memcpy(dx,Mx,nx*sizeof dx[0]); memcpy(dy,Ny,ny*sizeof dy[0]);
  qsort(dx,nx,sizeof dx[0],cmpW); qsort(dy,ny,sizeof dy[0],cmpW);
  int ux=0; for(int i=0;i<nx;i++) if(ux==0||memcmp(dx[ux-1],dx[i],sizeof dx[0])) memcpy(dx[ux++],dx[i],sizeof dx[0]);
  int uy=0; for(int i=0;i<ny;i++) if(uy==0||memcmp(dy[uy-1],dy[i],sizeof dy[0])) memcpy(dy[uy++],dy[i],sizeof dy[0]);
  int anyfail=0;
  for(int i=0;i<ux&&!anyfail;i++) for(int j=0;j<uy;j++)
    if(!((dx[i][0]&dy[j][0])|(dx[i][1]&dy[j][1])|(dx[i][2]&dy[j][2])|(dx[i][3]&dy[j][3]))){anyfail=1;break;}
  if(!anyfail) return 1;
  nf=0;
  for(int i=0;i<nx;i++) for(int j=0;j<ny;j++)
    if(!((Mx[i][0]&Ny[j][0])|(Mx[i][1]&Ny[j][1])|(Mx[i][2]&Ny[j][2])|(Mx[i][3]&Ny[j][3]))){ F[nf][0]=i;F[nf][1]=j;nf++; }
  for(int s=0;s<nsh;s++){
    int R[5],S[5],nr=0; for(int t=1;t<5;t++) if(sh0[s][t]){R[nr]=t;S[nr]=0;nr++;} for(int t=0;t<5;t++) if(sh3[s][t]){R[nr]=t;S[nr]=1;nr++;}
    int o[3][3],no[3]; for(int k=0;k<3;k++){ U L=S[k]?L2[R[k]]:L1[R[k]]; no[k]=0; for(int c=0;c<31;c++) if(L>>c&1) o[k][no[k]++]=c; }
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
