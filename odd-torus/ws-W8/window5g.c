/* W8: generalised cut shapes for m = 5. Same window model as window5.c (alpha fresh at row 0 of
   C0; adversary picks proper x on C0 and y on C3). A shape (from shapes5.txt) forbids one colour
   gamma_t at each row t of C0 with weight 1 and one colour beta_t at each row t of C3 with
   weight 1. Window is GOOD if some shape and some choice of forbidden colours (taken from L1[t],
   resp. L2[t]) leaves no failing (x, y).
   Run: ./window5g < windows.txt   (lines "BAD L1: a b c d e  L2: a b c d e", hex)            */
#include <stdio.h>
#include <string.h>
typedef unsigned int U;
#define NONE 31
static U L1[5],L2[5]; static int ALPHA=NONE; /* real alpha: x1, x4 != alpha */
static int fill(const U*A,const U*B){
  int c[10]; int i=0; U cand[10]; cand[0]=A[0];
  for(;;){ if(cand[i]==0){ if(--i<0) return 0; continue; }
    int col=__builtin_ctz(cand[i]); cand[i]&=cand[i]-1; c[i]=col; i++; if(i==10) return 1;
    U L=i<5?A[i]:B[i-5]; U forb=0;
    if(i<5){forb|=1u<<c[i-1]; if(i==4) forb|=1u<<c[0];}
    else{int t=i-5; forb|=1u<<c[t]; if(t>0) forb|=1u<<c[i-1]; if(t==4) forb|=1u<<c[5];}
    cand[i]=L&~forb; }}
static int xs[1024][5],ys[2048][5],nx,ny; static int F[300000][2],nf;
static int sh0[100][5],sh3[100][5],nsh;
static void enumerate(void){
  int opt[5][5],no[5];
  for(int t=0;t<5;t++){no[t]=0;for(int c=0;c<31;c++) if(L1[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  nx=0; int x[5]; x[0]=NONE;
  for(int a=0;a<no[1];a++)for(int b=0;b<no[2];b++)for(int c=0;c<no[3];c++)for(int d=0;d<no[4];d++){
    x[1]=opt[1][a];x[2]=opt[2][b];x[3]=opt[3][c];x[4]=opt[4][d]; int ok=1;
    for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0;
    if(ALPHA!=NONE&&(x[1]==ALPHA||x[4]==ALPHA)) ok=0; if(ok) memcpy(xs[nx++],x,sizeof x);}
  for(int t=0;t<5;t++){no[t]=0;for(int c=0;c<31;c++) if(L2[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  ny=0; int y[5];
  for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++)for(int d=0;d<no[3];d++)for(int e=0;e<no[4];e++){
    y[0]=opt[0][a];y[1]=opt[1][b];y[2]=opt[2][c];y[3]=opt[3][d];y[4]=opt[4][e]; int ok=1;
    for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(ok) memcpy(ys[ny++],y,sizeof y);}
  nf=0;
  for(int i=0;i<nx;i++){U A[5]; for(int t=0;t<5;t++) A[t]=xs[i][t]==NONE?L1[t]:(L1[t]&~(1u<<xs[i][t]));
    for(int j=0;j<ny;j++){U B[5]; for(int t=0;t<5;t++) B[t]=ys[j][t]==NONE?L2[t]:(L2[t]&~(1u<<ys[j][t]));
      if(!fill(A,B)){F[nf][0]=i;F[nf][1]=j;nf++;}}}}
/* try shape k: rows R (side 0 = C0 via x, side 1 = C3 via y), choose forbidden colour per row */
static int R[5],S[5],nr; static int good_with(int depth,int*fc){
  if(depth==nr){ for(int f=0;f<nf;f++){ int hit=1;
      for(int i=0;i<nr&&hit;i++){ int v=S[i]?ys[F[f][1]][R[i]]:xs[F[f][0]][R[i]]; if(v==fc[i]) hit=0; }
      if(hit) return 0; } return 1; }
  U L=S[depth]?L2[R[depth]]:L1[R[depth]];
  for(int c=0;c<31;c++) if(L>>c&1){ fc[depth]=c; if(good_with(depth+1,fc)) return 1; }
  return 0;}
int main(int argc,char**argv){ int realalpha=argc>1; int peralpha=argc>1&&!strcmp(argv[1],"peralpha");
  FILE*f=fopen("shapes5.txt","r"); int n; fscanf(f,"%d",&n); nsh=0;
  for(int k=0;k<n;k++){char a[8],b[8]; fscanf(f,"%s %s",a,b); for(int t=0;t<5;t++){sh0[k][t]=a[t]-'0';sh3[k][t]=b[t]-'0';} nsh++;}
  char line[512]; long tot=0,still=0;
  while(fgets(line,sizeof line,stdin)){
    if(strncmp(line,"BAD",3)) continue;
    if(sscanf(line,"BAD L1: %x %x %x %x %x L2: %x %x %x %x %x",&L1[0],&L1[1],&L1[2],&L1[3],&L1[4],&L2[0],&L2[1],&L2[2],&L2[3],&L2[4])!=10) continue;
    tot++;
    if(peralpha){ /* every alpha in 0..5 not in L1[0], plus fresh (6 = NONE stands for fresh) */
      for(int a=0;a<=6;a++){ if(a<6&&(L1[0]>>a&1)) continue; ALPHA= a==6?NONE:a; enumerate();
        int good=0; for(int k=0;k<nsh&&!good;k++){ nr=0; for(int t=1;t<5;t++) if(sh0[k][t]){R[nr]=t;S[nr]=0;nr++;}
          for(int t=0;t<5;t++) if(sh3[k][t]){R[nr]=t;S[nr]=1;nr++;} int fc[5]; if(good_with(0,fc)) good=1; }
        if(!good) printf("BADA %d %s",a,line+4); }
      continue; }
    ALPHA=NONE; if(realalpha){ U m=15&~L1[0]; ALPHA=__builtin_ctz(m);} enumerate(); int good=0,which=-1;
    for(int k=0;k<nsh&&!good;k++){ nr=0; for(int t=1;t<5;t++) if(sh0[k][t]){R[nr]=t;S[nr]=0;nr++;}
      for(int t=0;t<5;t++) if(sh3[k][t]){R[nr]=t;S[nr]=1;nr++;}
      int fc[5]; if(good_with(0,fc)){good=1;which=k;} }
    if(!good){ still++; printf("STILL BAD (failing pairs %d): %s",nf,line+4); }
  }
  printf("%ld windows bad for the plan's shape; %ld still bad with all 74 shapes\n",tot,still);
  return 0;}
