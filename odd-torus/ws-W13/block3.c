/* Block Lemma fill step, border lists != X (each contains a colour outside X). Random border lists over a
   palette of P colours (X = {0,1,2}). Strategy: 5 units, no two adjacent pins; a pin may use any colour of
   the border list (a colour outside X then does not touch the block). Adversary: proper border colouring from
   the lists respecting the strategy. Reports how many random border-list configurations have a strategy.  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
enum {P1,P2,P3,Q1,Q2,R1,R2,S1,S2,S3,NB};
static int bedge[8][2]={{P1,P2},{P2,P3},{Q1,Q2},{R1,R2},{Q1,R1},{Q2,R2},{S1,S2},{S2,S3}};
static int onb[6][2]={{P1,Q2},{P2,-1},{P3,Q1},{S1,R2},{S2,-1},{S3,R1}};
static int bblk[7][2]={{0,1},{1,2},{3,4},{4,5},{0,3},{1,4},{2,5}};
static unsigned BL[NB]; static int P;
static int fillable(const int*bc){
  int lst[6]; for(int k=0;k<6;k++){ lst[k]=7; for(int i=0;i<2;i++){ int v=onb[k][i]; if(v>=0&&bc[v]<3) lst[k]&=~(1<<bc[v]); } }
  int c[6];
  for(c[0]=0;c[0]<3;c[0]++) if(lst[0]>>c[0]&1) for(c[1]=0;c[1]<3;c[1]++) if(lst[1]>>c[1]&1)
  for(c[2]=0;c[2]<3;c[2]++) if(lst[2]>>c[2]&1) for(c[3]=0;c[3]<3;c[3]++) if(lst[3]>>c[3]&1)
  for(c[4]=0;c[4]<3;c[4]++) if(lst[4]>>c[4]&1) for(c[5]=0;c[5]<3;c[5]++) if(lst[5]>>c[5]&1){
    int ok=1; for(int e=0;e<7;e++) if(c[bblk[e][0]]==c[bblk[e][1]]) ok=0; if(ok) return 1; }
  return 0; }
static int bad[300000][NB], nbad;
static void gen(int v,int*bc){
  if(v==NB){ for(int e=0;e<8;e++) if(bc[bedge[e][0]]==bc[bedge[e][1]]) return; if(!fillable(bc)) memcpy(bad[nbad++],bc,NB*sizeof(int)); return; }
  for(int c=0;c<P;c++) if(BL[v]>>c&1){ bc[v]=c; gen(v+1,bc); } }
static int strategy_exists(void){
  int units[NB];
  for(int code=0;code<59049;code++){ int z=code,sum=0; for(int v=0;v<NB;v++){ units[v]=z%3; z/=3; sum+=units[v]; } if(sum!=5) continue;
    int adj=0; for(int e=0;e<8;e++) if(units[bedge[e][0]]==2&&units[bedge[e][1]]==2) adj=1; if(adj) continue;
    int idx[NB],k=0; for(int v=0;v<NB;v++) if(units[v]) idx[k++]=v;
    int opts[NB][8],no[NB]; for(int i=0;i<k;i++){ no[i]=0; for(int c=0;c<P;c++) if(BL[idx[i]]>>c&1) opts[i][no[i]++]=c; }
    int ch[NB]; memset(ch,0,sizeof ch);
    for(;;){ int works=1;
      for(int b=0;b<nbad&&works;b++){ int ex=0;
        for(int i=0;i<k&&!ex;i++){ int v=idx[i], col=opts[i][ch[i]], x=bad[b][v];
          if(units[v]==1&&x==col) ex=1; if(units[v]==2&&x!=col) ex=1; }
        if(!ex) works=0; }
      if(works) return 1;
      int i=0; while(i<k){ ch[i]++; if(ch[i]<no[i]) break; ch[i]=0; i++; } if(i==k) break; } }
  return 0; }
int main(int argc,char**argv){ P=atoi(argv[1]); int N=atoi(argv[2]); srand(atoi(argv[3])); int ok=0;
  for(int it=0;it<N;it++){
    for(int v=0;v<NB;v++){ unsigned s; do{ s=0; while(__builtin_popcount(s)<3) s|=1u<<(rand()%P); } while((s&~7u)==0); BL[v]=s; }
    nbad=0; int bc[NB]; gen(0,bc);
    if(strategy_exists()) ok++; else { printf("NO STRATEGY, border lists:"); for(int v=0;v<NB;v++) printf(" %x",BL[v]); printf("\n"); } }
  printf("palette %d: %d of %d random border configurations have a strategy\n",P,ok,N); return 0; }
