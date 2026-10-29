/* W11: test an explicit strategy for windows with NO rigid row (A_t != B_t for all t), m = 5.
   Strategy(q): pin row 0 (alpha fresh), free rows {0, q}, forbid at C3 rows t not in {0,q}:
   beta_t = the unique colour of B_t \ A_t if that set has size 1 (otherwise no constraint).
   Reports, over all 4-colour windows with no rigid row: how many are good for
     (a) q chosen as a row with |B_q \ A_q| >= 2 (if one exists), else
     (b) some q in 1..4 works,  (c) no q works.
   Run: ./r0_strategy                                                                          */
#include <stdio.h>
#include <string.h>
typedef unsigned int U;
#define NONE 31
static U L1[5],L2[5];
static int fill(const U*A,const U*B){
  int c[10]; int i=0; U cand[10]; cand[0]=A[0];
  for(;;){ if(cand[i]==0){ if(--i<0) return 0; continue; }
    int col=__builtin_ctz(cand[i]); cand[i]&=cand[i]-1; c[i]=col; i++; if(i==10) return 1;
    U L=i<5?A[i]:B[i-5]; U forb=0;
    if(i<5){forb|=1u<<c[i-1]; if(i==4) forb|=1u<<c[0];}
    else{int t=i-5; forb|=1u<<c[t]; if(t>0) forb|=1u<<c[i-1]; if(t==4) forb|=1u<<c[5];}
    cand[i]=L&~forb; }}
static int good_q(int q){
  int beta[5]; for(int t=0;t<5;t++){ beta[t]=NONE; U e=L2[t]&~L1[t]; if(t!=0&&t!=q&&__builtin_popcount(e)==1) beta[t]=__builtin_ctz(e); }
  int ox[5][5],nox[5],oy[5][5],noy[5];
  for(int t=0;t<5;t++){nox[t]=0; for(int c=0;c<31;c++) if(L1[t]>>c&1) ox[t][nox[t]++]=c; ox[t][nox[t]++]=NONE;
                       noy[t]=0; for(int c=0;c<31;c++) if(L2[t]>>c&1 && c!=beta[t]) oy[t][noy[t]++]=c; oy[t][noy[t]++]=NONE;}
  int x[5]; x[0]=NONE;
  for(int a=0;a<nox[1];a++)for(int b=0;b<nox[2];b++)for(int c=0;c<nox[3];c++)for(int d=0;d<nox[4];d++){
    x[1]=ox[1][a];x[2]=ox[2][b];x[3]=ox[3][c];x[4]=ox[4][d];
    int ok=1; for(int t=1;t<4;t++) if(x[t]!=NONE&&x[t]==x[t+1]) ok=0; if(!ok) continue;
    U A[5]; for(int t=0;t<5;t++) A[t]= x[t]==NONE?L1[t]:(L1[t]&~(1u<<x[t]));
    int y[5];
    for(int e0=0;e0<noy[0];e0++)for(int e1=0;e1<noy[1];e1++)for(int e2=0;e2<noy[2];e2++)for(int e3=0;e3<noy[3];e3++)for(int e4=0;e4<noy[4];e4++){
      y[0]=oy[0][e0];y[1]=oy[1][e1];y[2]=oy[2][e2];y[3]=oy[3][e3];y[4]=oy[4][e4];
      int ok2=1; for(int t=0;t<5;t++) if(y[t]!=NONE&&y[t]==y[(t+1)%5]) ok2=0; if(!ok2) continue;
      U B[5]; for(int t=0;t<5;t++) B[t]= y[t]==NONE?L2[t]:(L2[t]&~(1u<<y[t]));
      if(!fill(A,B)) return 0; }}
  return 1; }
int main(void){
  long tot=0,ga=0,gb=0,none=0; long perq[5]={0};
  for(int code=0;code<(1<<20);code++){ int c=code;
    for(int t=0;t<5;t++){L1[t]=15&~(1u<<(c&3));c>>=2;} for(int t=0;t<5;t++){L2[t]=15&~(1u<<(c&3));c>>=2;}
    int rig=0; for(int t=0;t<5;t++) if(L1[t]==L2[t]) rig=1; if(rig) continue;
    tot++;
    int qa=-1; for(int t=1;t<5;t++) if(__builtin_popcount(L2[t]&~L1[t])>=2){qa=t;break;}
    if(qa>0 && good_q(qa)){ ga++; continue; }
    int any=0; for(int q=1;q<5;q++) if(good_q(q)){ any=1; perq[q]++; break; }
    if(any) gb++; else { none++; if(none<=5){ printf("NO q WORKS: L1"); for(int t=0;t<5;t++) printf(" %x",L1[t]); printf(" L2"); for(int t=0;t<5;t++) printf(" %x",L2[t]); printf("\n"); } }
  }
  printf("4-colour windows with no rigid row: %ld\n  good via a row with |B\\A|>=2: %ld\n  good via some q: %ld (first working q: 1:%ld 2:%ld 3:%ld 4:%ld)\n  no q works: %ld\n",tot,ga,gb,perq[1],perq[2],perq[3],perq[4],none);
  return 0; }
