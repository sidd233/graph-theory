/* Gap 2b test: windows where every row has |A_t & B_t| = 1. Pin only (alpha fresh, NO forbidden
   colours at all). Is the fill always possible against every adversary? Random over palettes 5..8.
   Run: ./vg_test P N SEED                                                                         */
#include <stdio.h>
#include <stdlib.h>
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
static int good(void){
  int ox[5][5],nox[5],oy[5][5],noy[5];
  for(int t=0;t<5;t++){nox[t]=0; for(int c=0;c<31;c++) if(L1[t]>>c&1) ox[t][nox[t]++]=c; ox[t][nox[t]++]=NONE;
                       noy[t]=0; for(int c=0;c<31;c++) if(L2[t]>>c&1) oy[t][noy[t]++]=c; oy[t][noy[t]++]=NONE;}
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
static U r3(int P){ U s=0; while(__builtin_popcount(s)<3) s|=1u<<(rand()%P); return s; }
int main(int argc,char**argv){
  int P=atoi(argv[1]); long N=atol(argv[2]); srand(atoi(argv[3])); long bad=0,tot=0;
  while(tot<N){
    for(int t=0;t<5;t++){ do{ L1[t]=r3(P); L2[t]=r3(P);} while(__builtin_popcount(L1[t]&L2[t])!=1); }
    tot++;
    if(!good()){ bad++; if(bad<=5){ printf("BAD L1:"); for(int t=0;t<5;t++) printf(" %02x",L1[t]); printf(" L2:"); for(int t=0;t<5;t++) printf(" %02x",L2[t]); printf("\n"); } } }
  printf("palette %d: %ld windows with |A&B|=1 in every row, %ld bad with pin only\n",P,tot,bad); return 0; }
