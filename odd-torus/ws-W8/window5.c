/* W8: does the plan's cut shape work for m = 5?
   Window = lists on columns C1 (L1[t]) and C2 (L2[t]), t in Z5, all of size 3.
   Row 0 of C0 is pinned to a fresh colour alpha (so alpha is in no list; this is the hardest
   case for us, since alpha then restricts nothing). The adversary picks any proper colouring x
   of the C0 cycle and y of the C3 cycle; colours outside a list act as "remove nothing".
   Shape (plan): rows {p,q} with p+q != 0 (mod 5) of C3 keep their full list; every other row t
   of C3 forbids one colour beta_t (we may take beta_t in L2[t]).
   The window is GOOD if some shape makes the C5 x K2 fill colourable for every admissible x, y.
   Modes:  ./window5 rand Q SAMPLES SEED   random lists from a palette of Q colours
           ./window5 all3 LO HI             windows with code in [LO,HI) from a palette of 4 colours (lists = complements)  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int U;
#define NONE 31
static U L1[5],L2[5];
static int fill(const U*A,const U*B){ /* colour u0..u4 then v0..v4 */
  int c[10]; int i=0; U cand[10]; cand[0]=A[0];
  for(;;){
    if(i==10) return 1;
    if(cand[i]==0){ if(--i<0) return 0; continue; }
    int col=__builtin_ctz(cand[i]); cand[i]&=cand[i]-1; c[i]=col;
    i++; if(i==10) return 1;
    U L = i<5 ? A[i] : B[i-5];
    U forb=0;
    if(i<5){ forb|=1u<<c[i-1]; if(i==4) forb|=1u<<c[0]; }
    else { int t=i-5; forb|=1u<<c[t]; if(t>0) forb|=1u<<c[i-1]; if(t==4) forb|=1u<<c[5]; }
    cand[i]=L&~forb;
  }}
static U Avec[1024][5], Bvec[2048][5]; static int ys[2048][5];
int window_good(int verbose){
  int na=0, nb=0;
  /* x: x0 = alpha fresh; x_t in L1[t] or NONE, proper on cycle */
  int opt[5][4], no[5];
  for(int t=0;t<5;t++){no[t]=0; for(int c=0;c<31;c++) if(L1[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  int x[5]; x[0]=NONE;
  for(int a=0;a<no[1];a++)for(int b=0;b<no[2];b++)for(int c=0;c<no[3];c++)for(int d=0;d<no[4];d++){
    x[1]=opt[1][a];x[2]=opt[2][b];x[3]=opt[3][c];x[4]=opt[4][d];
    int ok=1; for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0; if(!ok) continue;
    U A[5]; for(int t=0;t<5;t++) A[t]= x[t]==NONE?L1[t]:(L1[t]&~(1u<<x[t]));
    int dup=0; for(int k=0;k<na&&!dup;k++) if(!memcmp(Avec[k],A,sizeof A)) dup=1;
    if(!dup) memcpy(Avec[na++],A,sizeof A);}
  for(int t=0;t<5;t++){no[t]=0; for(int c=0;c<31;c++) if(L2[t]>>c&1) opt[t][no[t]++]=c; opt[t][no[t]++]=NONE;}
  int y[5];
  for(int a=0;a<no[0];a++)for(int b=0;b<no[1];b++)for(int c=0;c<no[2];c++)for(int d=0;d<no[3];d++)for(int e=0;e<no[4];e++){
    y[0]=opt[0][a];y[1]=opt[1][b];y[2]=opt[2][c];y[3]=opt[3][d];y[4]=opt[4][e];
    int ok=1; for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok=0; if(!ok) continue;
    for(int t=0;t<5;t++) Bvec[nb][t]= y[t]==NONE?L2[t]:(L2[t]&~(1u<<y[t]));
    memcpy(ys[nb],y,sizeof y); nb++;}
  /* failing y's: those for which some x makes the fill fail */
  static int fy[2048]; int nf=0;
  for(int k=0;k<nb;k++){ int f=0; for(int j=0;j<na&&!f;j++) if(!fill(Avec[j],Bvec[k])) f=1; if(f) fy[nf++]=k; }
  if(nf==0) return 1;
  for(int p=0;p<5;p++)for(int q=p+1;q<5;q++){ if((p+q)%5==0) continue;
    int T[3],nt=0; for(int t=0;t<5;t++) if(t!=p&&t!=q) T[nt++]=t;
    int bo[3][3],nbo[3]; for(int i=0;i<3;i++){nbo[i]=0; for(int c=0;c<31;c++) if(L2[T[i]]>>c&1) bo[i][nbo[i]++]=c;}
    for(int i=0;i<nbo[0];i++)for(int j=0;j<nbo[1];j++)for(int k=0;k<nbo[2];k++){
      int beta[3]={bo[0][i],bo[1][j],bo[2][k]}; int dodged=1;
      for(int f=0;f<nf&&dodged;f++){ int*yy=ys[fy[f]];
        if(yy[T[0]]!=beta[0]&&yy[T[1]]!=beta[1]&&yy[T[2]]!=beta[2]) dodged=0; }
      if(dodged){ if(verbose) printf("  good: p=%d q=%d beta=%d %d %d\n",p,q,beta[0],beta[1],beta[2]); return 1; }
    }}
  return 0;}
static void show(void){printf("L1:");for(int t=0;t<5;t++)printf(" %03x",L1[t]);printf("  L2:");for(int t=0;t<5;t++)printf(" %03x",L2[t]);printf("\n");}
static U rnd3(int Q){U s;do{s=0;while(__builtin_popcount(s)<3)s|=1u<<(rand()%Q);}while(0);return s;}
int main(int argc,char**argv){
  if(!strcmp(argv[1],"stdin")){ char line[512]; long bad=0,tot=0;
    while(fgets(line,sizeof line,stdin)){ if(sscanf(line,"%x %x %x %x %x %x %x %x %x %x",&L1[0],&L1[1],&L1[2],&L1[3],&L1[4],&L2[0],&L2[1],&L2[2],&L2[3],&L2[4])!=10) continue;
      tot++; if(!window_good(0)){bad++; printf("BAD ");show();}}
    printf("stdin: %ld windows, %ld bad\n",tot,bad); return 0;}
  if(!strcmp(argv[1],"rand")){int Q=atoi(argv[2]);long S=atol(argv[3]);srand(atoi(argv[4]));long bad=0;
    for(long s=0;s<S;s++){for(int t=0;t<5;t++){L1[t]=rnd3(Q);L2[t]=rnd3(Q);}
      if(!window_good(0)){bad++; printf("BAD ");show();}}
    printf("palette %d: %ld random windows, %ld bad\n",Q,S,bad);}
  else { /* all windows from palette 4: each list = complement of one colour */
    long bad=0,tot=0;
    int lo=atoi(argv[2]),hi=atoi(argv[3]);
    for(int code=lo;code<hi;code++){int c=code;
      for(int t=0;t<5;t++){L1[t]=15&~(1u<<(c&3));c>>=2;} for(int t=0;t<5;t++){L2[t]=15&~(1u<<(c&3));c>>=2;}
      tot++; if(!window_good(0)){bad++; printf("BAD ");show();}}
    printf("palette 4, %ld windows: %ld bad\n",tot,bad);}
  return 0;}
