/* W14: general hole cut. Block (rows 1..3 x 2 columns) with ARBITRARY 3-lists, border lists arbitrary.
   Strategy = one of the 1256 proved placements (allowed_codes.txt) + colour choices from border lists
   (pin: any colour of the list; forbid: any colour of the list). Adversary: proper border colouring from
   border lists respecting the strategy. Fill: block from its lists minus outside-neighbour colours.
   Run: ./hole_general P N SEED  (random lists over a palette of P colours)                        */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
enum {P1,P2,P3,Q1,Q2,R1,R2,S1,S2,S3,NB};
static int bedge[8][2]={{P1,P2},{P2,P3},{Q1,Q2},{R1,R2},{Q1,R1},{Q2,R2},{S1,S2},{S2,S3}};
static int onb[6][2]={{P1,Q2},{P2,-1},{P3,Q1},{S1,R2},{S2,-1},{S3,R1}};
static int bblk[7][2]={{0,1},{1,2},{3,4},{4,5},{0,3},{1,4},{2,5}};
static unsigned BL[NB], KL[6]; static int P; static char allowed[59049];
static int fill(const int*bc){
  unsigned lst[6]; for(int k=0;k<6;k++){ lst[k]=KL[k]; for(int i=0;i<2;i++){ int v=onb[k][i]; if(v>=0) lst[k]&=~(1u<<bc[v]); } }
  int c[6]; int k=0; unsigned cand[6]; cand[0]=lst[0];
  for(;;){ if(cand[k]==0){ if(--k<0) return 0; continue; }
    c[k]=__builtin_ctz(cand[k]); cand[k]&=cand[k]-1; k++; if(k==6){ int ok=1; for(int e=0;e<7;e++) if(c[bblk[e][0]]==c[bblk[e][1]]) ok=0; if(ok) return 1; k=5; continue; }
    cand[k]=lst[k]; }
}
static int bad[2000000][NB]; static int nbad;
static void gen(int v,int*bc){
  if(v==NB){ for(int e=0;e<8;e++) if(bc[bedge[e][0]]==bc[bedge[e][1]]) return; if(!fill(bc)) memcpy(bad[nbad++],bc,NB*sizeof(int)); return; }
  for(int c=0;c<P;c++) if(BL[v]>>c&1){ bc[v]=c; gen(v+1,bc); } }
static int strategy(void){
  for(int sc=0;sc<59049;sc++){ if(!allowed[sc]) continue;
    int units[NB],z=sc; for(int v=0;v<NB;v++){ units[v]=z%3; z/=3; }
    int idx[NB],k=0; for(int v=0;v<NB;v++) if(units[v]) idx[k++]=v;
    int opts[NB][8],no[NB],ch[NB]; for(int i=0;i<k;i++){ no[i]=0; for(int c=0;c<P;c++) if(BL[idx[i]]>>c&1) opts[i][no[i]++]=c; ch[i]=0; }
    for(;;){ int works=1;
      for(int b=0;b<nbad&&works;b++){ int ex=0; for(int i=0;i<k&&!ex;i++){ int v=idx[i],x=bad[b][v],col=opts[i][ch[i]];
          if(units[v]==1&&x==col) ex=1; if(units[v]==2&&x!=col) ex=1; } if(!ex) works=0; }
      if(works) return 1;
      int i=0; while(i<k){ ch[i]++; if(ch[i]<no[i]) break; ch[i]=0; i++; } if(i==k) break; } }
  return 0; }
static unsigned r3(void){ unsigned s=0; while(__builtin_popcount(s)<3) s|=1u<<(rand()%P); return s; }
int main(int argc,char**argv){ P=atoi(argv[1]); int N=atoi(argv[2]); srand(atoi(argv[3]));
  FILE*f=fopen("allowed_codes.txt","r"); int na; fscanf(f,"%d",&na); for(int i=0;i<na;i++){int c; fscanf(f,"%d",&c); allowed[c]=1;} fclose(f);
  int good=0;
  int Kmax=atoi(argv[4]); long viol=0;
  for(int it=0;it<N;it++){
    unsigned X=7;
    for(int k=0;k<6;k++) KL[k]=X; for(int v=0;v<NB;v++) BL[v]=X;
    int K=1+rand()%Kmax; for(int c=0;c<K;c++){ int p=rand()%16; if(p<6) KL[p]=r3(); else BL[p-6]=r3(); }
    int alleq=1; for(int k=1;k<6;k++) if(KL[k]!=KL[0]) alleq=0;
    /* pattern (ii): top/bottom rows (aL,cL,aR,cR = 0,2,3,5) and all border equal one X */
    int pat=0; { unsigned Y=KL[0]; int ok=(KL[2]==Y&&KL[3]==Y&&KL[5]==Y); for(int v=0;v<NB;v++) if(BL[v]!=Y) ok=0; pat=ok; }
    nbad=0; int bc[NB]; gen(0,bc);
    if(nbad==0||strategy()) good++; else if(!alleq && !pat){ viol++; printf("VIOLATES H**:"); for(int k=0;k<6;k++) printf(" %x",KL[k]); printf(" |"); for(int v=0;v<NB;v++) printf(" %x",BL[v]); printf("\n"); fflush(stdout); } { } }
  printf("palette %d, up to %d changes: %d of %d have a strategy; violations of H** found: %ld\n",P,Kmax,good,N,viol); return 0; }
