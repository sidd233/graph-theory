/* W12: every window (10 lists of size 3) with at most 5 colours, up to renaming colours
   (restricted growth: each list = old colours + a prefix of fresh ones; L1[0] = {0,1,2}),
   and every pinned colour alpha in {0..4} not in L1[0] (colours unused by the window are all
   equivalent, so one representative). Prints every BAD (alpha, window).
   Run: ./enum5 WORKER NWORKERS > out                                                          */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned int U;
extern int judge_core(const U*L1,const U*L2,int alpha);
extern void load_shapes(const char*fn);
#define PAL 4
static U L[10]; static int worker, nworkers; static long combo=0, nwin=0, nbad=0;
static int used_of(U s){ return s?32-__builtin_clz(s):0; }
static int sets(int u, U*out){ int n=0;
  for(U s=0;s<(1u<<PAL);s++){ if(__builtin_popcount(s)!=3) continue;
    U fresh=s>>u; if(fresh&(fresh+1)) continue;      /* fresh colours must be a prefix u, u+1, ... */
    if(used_of(s)>PAL) continue; out[n++]=s; } return n; }
static void rec(int k, U usedmask){
  if(k==3){ long c=combo++; if(c%nworkers!=worker) return; }
  if(k==10){
    int u=used_of(usedmask); U L1[5]={L[0],L[1],L[2],L[3],L[4]}, L2[5]={L[5],L[6],L[7],L[8],L[9]};
    for(int a=0;a<=u && a<PAL;a++){ if(L1[0]>>a&1) continue; nwin++;
      if(!judge_core(L1,L2,a)){ nbad++; printf("%d L1: %03x %03x %03x %03x %03x L2: %03x %03x %03x %03x %03x\n",a,L1[0],L1[1],L1[2],L1[3],L1[4],L2[0],L2[1],L2[2],L2[3],L2[4]); } }
    return; }
  U opts[64]; int n=sets(used_of(usedmask),opts);
  for(int i=0;i<n;i++){ L[k]=opts[i]; rec(k+1, usedmask|opts[i]); } }
int main(int argc,char**argv){ worker=atoi(argv[1]); nworkers=atoi(argv[2]); load_shapes("shapes5.txt");
  L[0]=7; rec(1,7); fprintf(stderr,"worker %d: %ld (window, alpha) judged, %ld bad\n",worker,nwin,nbad); fflush(stdout); return 0; }
