/* Block Lemma (a), palette-free check. Each border vertex v has type S_v = L(v) & X (|S_v| <= 2), plus at
   least one colour outside X, all of which act the same on the block ("o"). Conservative adversary: picks
   b_v in S_v + {o}, ignoring properness between border vertices (only makes it stronger). Strategy: 5 units,
   no two adjacent pins; pin v to a colour of S_v or to o; forbid a colour of S_v.
   Checks ALL 7^10 type assignments (up to nothing): does a strategy always exist? Run: ./block_types W NW  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
enum {P1,P2,P3,Q1,Q2,R1,R2,S1,S2,S3,NB};
static int bedge[8][2]={{P1,P2},{P2,P3},{Q1,Q2},{R1,R2},{Q1,R1},{Q2,R2},{S1,S2},{S2,S3}};
static int onb[6][2]={{P1,Q2},{P2,-1},{P3,Q1},{S1,R2},{S2,-1},{S3,R1}};
static int bblk[7][2]={{0,1},{1,2},{3,4},{4,5},{0,3},{1,4},{2,5}};
static int typemask[7]={0,1,2,4,3,5,6};       /* subsets of X of size <= 2 */
static int S[NB];
static int fill_ok[1<<20];                      /* indexed by border colouring code (base 4: 0..2 in X, 3 = o) */
static int bad[1100000], nbad;
int main(int argc,char**argv){ int W=atoi(argv[1]), NW=atoi(argv[2]);
  /* precompute fillability for every border colouring (values 0,1,2,3) */
  for(int code=0;code<(1<<20);code++){ int bc[NB],z=code; for(int v=0;v<NB;v++){ bc[v]=z&3; z>>=2; }
    int lst[6]; for(int k=0;k<6;k++){ lst[k]=7; for(int i=0;i<2;i++){ int v=onb[k][i]; if(v>=0&&bc[v]<3) lst[k]&=~(1<<bc[v]); } }
    int ok=0, c[6];
    for(c[0]=0;c[0]<3&&!ok;c[0]++) if(lst[0]>>c[0]&1) for(c[1]=0;c[1]<3&&!ok;c[1]++) if(lst[1]>>c[1]&1)
    for(c[2]=0;c[2]<3&&!ok;c[2]++) if(lst[2]>>c[2]&1) for(c[3]=0;c[3]<3&&!ok;c[3]++) if(lst[3]>>c[3]&1)
    for(c[4]=0;c[4]<3&&!ok;c[4]++) if(lst[4]>>c[4]&1) for(c[5]=0;c[5]<3&&!ok;c[5]++) if(lst[5]>>c[5]&1){
      int g=1; for(int e=0;e<7;e++) if(c[bblk[e][0]]==c[bblk[e][1]]) g=0; if(g) ok=1; }
    fill_ok[code]=ok; }
  long tot=0, nostrat=0;
  for(long tc=0;tc<282475249L;tc++){ if(tc%NW!=W) continue;
    long z=tc; for(int v=0;v<NB;v++){ S[v]=typemask[z%7]; z/=7; }
    tot++;
    /* enumerate adversary colourings (b_v in S_v + {3}); collect unfillable ones */
    nbad=0; int bc[NB]; int opt[NB][3],no[NB];
    for(int v=0;v<NB;v++){ no[v]=0; for(int c=0;c<3;c++) if(S[v]>>c&1) opt[v][no[v]++]=c; opt[v][no[v]++]=3; }
    int ix[NB]; memset(ix,0,sizeof ix);
    for(;;){ int code=0; for(int v=NB-1;v>=0;v--) code=code*4+opt[v][ix[v]];
      if(!fill_ok[code]) bad[nbad++]=code;
      int v=0; while(v<NB){ ix[v]++; if(ix[v]<no[v]) break; ix[v]=0; v++; } if(v==NB) break; }
    if(nbad==0) continue;
    /* strategies */
    int found=0, units[NB];
    for(int sc=0;sc<59049&&!found;sc++){ int zz=sc,sum=0; for(int v=0;v<NB;v++){ units[v]=zz%3; zz/=3; sum+=units[v]; } if(sum!=5) continue;
      int adj=0; for(int e=0;e<8;e++) if(units[bedge[e][0]]==2&&units[bedge[e][1]]==2) adj=1; if(adj) continue;
      int idx[NB],k=0; for(int v=0;v<NB;v++) if(units[v]) idx[k++]=v;
      int ch[NB],nch[NB],cv[NB][4];
      int feasible=1; for(int i=0;i<k;i++){ int v=idx[i]; nch[i]=0;
        if(units[v]==2){ for(int c=0;c<3;c++) if(S[v]>>c&1) cv[i][nch[i]++]=c; cv[i][nch[i]++]=3; }
        else { for(int c=0;c<3;c++) if(S[v]>>c&1) cv[i][nch[i]++]=c; if(nch[i]==0) feasible=0; } ch[i]=0; }
      if(!feasible) continue;
      for(;;){ int works=1;
        for(int b=0;b<nbad&&works;b++){ int code=bad[b], ex=0;
          for(int i=0;i<k&&!ex;i++){ int v=idx[i]; int x=(code>>(2*v))&3; int col=cv[i][ch[i]];
            if(units[v]==1&&x==col) ex=1; if(units[v]==2&&x!=col) ex=1; }
          if(!ex) works=0; }
        if(works){ found=1; break; }
        int i=0; while(i<k){ ch[i]++; if(ch[i]<nch[i]) break; ch[i]=0; i++; } if(i==k) break; } }
    if(!found){ nostrat++; if(nostrat<=5){ printf("NO STRATEGY types:"); for(int v=0;v<NB;v++) printf(" %d",S[v]); printf("\n"); fflush(stdout);} } }
  fprintf(stderr,"worker %d: %ld type assignments, %ld without strategy\n",W,tot,nostrat); return 0; }
