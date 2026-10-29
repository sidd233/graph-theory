// Kernel-perfectness checker: every induced subdigraph has a kernel
// (independent S, every v in U\S has an out-arc into S). N <= 32.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef uint32_t M;
int N; M out[32], adj[32];
static int pc(M x){return __builtin_popcount(x);}
static int rec(M U, M S, M O){
  for(;;){
    M und=U&~S&~O; int ch=0;
    for(M x=und;x;x&=x-1){int v=__builtin_ctz(x);
      if((out[v]&U&~O)==0){ if(adj[v]&S) return 0; S|=1u<<v; O|=adj[v]&U&~S; ch=1; break; } }
    if(!ch) break;
  }
  for(M y=O;y;y&=y-1){int v=__builtin_ctz(y); if((out[v]&U&~O)==0) return 0;}
  M und=U&~S&~O;
  if(!und){ for(M y=O;y;y&=y-1){int v=__builtin_ctz(y); if(!(out[v]&S)) return 0;} return 1; }
  int v=__builtin_ctz(und);
  if(!(adj[v]&S) && rec(U,S|1u<<v,O|(adj[v]&U&~S))) return 1;
  return rec(U,S,O|1u<<v);
}
int main(){
  int A; if(scanf("%d %d",&N,&A)!=2) return 1;
  for(int i=0;i<A;i++){int u,v; scanf("%d %d",&u,&v); out[u]|=1u<<v; adj[u]|=1u<<v; adj[v]|=1u<<u;}
  uint64_t tot=(N==32)?0xffffffffull:((1ull<<N)-1);
  for(uint64_t U=1;U<=tot;U++){
    if(!rec((M)U,0,0)){ printf("NOT kernel-perfect; kernel-less U=%llu size=%d\n",(unsigned long long)U,pc((M)U)); return 0; }
    if((U&((1ull<<26)-1))==0){fprintf(stderr,"progress %llu/%llu\n",(unsigned long long)U,(unsigned long long)tot);}
  }
  printf("KERNEL-PERFECT (all %llu induced subdigraphs have a kernel)\n",(unsigned long long)tot);
  return 0;
}
