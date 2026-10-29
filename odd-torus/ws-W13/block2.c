/* W13: Block Lemma, fill step. Block = rows a,b,c (= t-1, t, t+1) x columns L (= j), R (= j+1),
   all lists X = {0,1,2}. Border (10 vertices): p1 p2 p3 = (t-1..t+1, j-1); q1 = (t+2, j), q2 = (t+3, j);
   r1 = (t+2, j+1), r2 = (t+3, j+1); s1 s2 s3 = (t-1..t+1, j+2).
   Block vertex -> outside neighbours: aL: p1,q2  bL: p2  cL: p3,q1  aR: s1,r2  bR: s2  cR: s3,r1.
   Border edges (adversary must be proper on them): p1p2 p2p3 q1q2 r1r2 q1r1 q2r2 s1s2 s2s3.
   Border lists = X too (hardest case). Adversary picks border colours in X (or a colour outside X = "none").
   Strategy: spend 5 units on border vertices: pin (2 units) = choose the colour; forbid (1 unit) = exclude
   one colour. Find all strategies under which the block can always be filled.                    */
#include <stdio.h>
#include <string.h>
enum {P1,P2,P3,Q1,Q2,R1,R2,S1,S2,S3,NB};
static const char*nm[NB]={"p1","p2","p3","q1","q2","r1","r2","s1","s2","s3"};
static int bedge[8][2]={{P1,P2},{P2,P3},{Q1,Q2},{R1,R2},{Q1,R1},{Q2,R2},{S1,S2},{S2,S3}};
/* block vertices 0..5 = aL bL cL aR bR cR ; outside neighbours */
static int onb[6][2]={{P1,Q2},{P2,-1},{P3,Q1},{S1,R2},{S2,-1},{S3,R1}};
static int bblk[7][2]={{0,1},{1,2},{3,4},{4,5},{0,3},{1,4},{2,5}};
static int fillable(const int*bc){ /* bc[v] in 0..3 (3 = outside X) */
  int lst[6]; for(int k=0;k<6;k++){ lst[k]=7; for(int i=0;i<2;i++){ int v=onb[k][i]; if(v>=0&&bc[v]<3) lst[k]&=~(1<<bc[v]); } }
  int c[6];
  for(c[0]=0;c[0]<3;c[0]++) if(lst[0]>>c[0]&1) for(c[1]=0;c[1]<3;c[1]++) if(lst[1]>>c[1]&1)
  for(c[2]=0;c[2]<3;c[2]++) if(lst[2]>>c[2]&1) for(c[3]=0;c[3]<3;c[3]++) if(lst[3]>>c[3]&1)
  for(c[4]=0;c[4]<3;c[4]++) if(lst[4]>>c[4]&1) for(c[5]=0;c[5]<3;c[5]++) if(lst[5]>>c[5]&1){
    int ok=1; for(int e=0;e<7;e++) if(c[bblk[e][0]]==c[bblk[e][1]]) ok=0; if(ok) return 1; }
  return 0; }
static int badset[60000][NB], nbad;
int main(void){
  int bc[NB]; long tot=0;
  for(int code=0;code<1048576;code++){ int z=code; for(int v=0;v<NB;v++){ bc[v]=z&3; z>>=2; }
    int ok=1; for(int e=0;e<8;e++){ int u=bc[bedge[e][0]], w=bc[bedge[e][1]]; if(u<3&&u==w) ok=0; } if(!ok) continue;
    tot++; if(!fillable(bc)){ memcpy(badset[nbad++],bc,sizeof bc); } }
  printf("proper border colourings (colours in X or outside): %ld, block not fillable: %d\n",tot,nbad);
  /* strategies: each border vertex gets 0, 1 (forbid colour f) or 2 (pin colour f) units; total 5.
     pin to "outside X" (value 3) allowed only if the border list has a colour outside X: here lists = X, so no. */
  long nstrat=0, nwork=0;
  int units[NB];
  for(int code=0;code<59049;code++){ int z=code,sum=0; for(int v=0;v<NB;v++){ units[v]=z%3; z/=3; sum+=units[v]; } if(sum!=5) continue;
    int adjpin=0; for(int e=0;e<8;e++) if(units[bedge[e][0]]==2&&units[bedge[e][1]]==2) adjpin=1; if(adjpin) continue;
    int idx[NB],k=0; for(int v=0;v<NB;v++) if(units[v]) idx[k++]=v;
    int ncol=1; for(int i=0;i<k;i++) ncol*=3;
    for(int cc=0;cc<ncol;cc++){ int col[NB],zz=cc; for(int i=0;i<k;i++){ col[idx[i]]=zz%3; zz/=3; }
      nstrat++; int works=1;
      for(int b=0;b<nbad&&works;b++){ int excluded=0;
        for(int i=0;i<k&&!excluded;i++){ int v=idx[i]; int x=badset[b][v];
          if(units[v]==1 && x==col[v]) excluded=1;      /* forbid */
          if(units[v]==2 && x!=col[v]) excluded=1; }    /* pin */
        if(!excluded) works=0; }
      if(works){ nwork++; if(nwork<=40){ printf("WORKS:"); for(int i=0;i<k;i++){int v=idx[i]; printf(" %s%s%d",nm[v],units[v]==2?"=":"!=",col[v]);} printf("\n"); } } } }
  printf("strategies tried %ld, working %ld\n",nstrat,nwork);
  return 0; }
