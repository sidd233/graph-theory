/* Independent, deliberately naive kernel-perfectness check (shares no code with kp_check.c).
 * Input on stdin: n, then n lines "v w1 w2 ..." listing out-neighbours.  Checks EVERY nonempty
 * subset S (no connectivity shortcut); for each S searches for a kernel by plain backtracking
 * over the vertices of S in index order.  Prints KERNEL-PERFECT or the first kernel-less S. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int n;
static uint64_t out_[64], adj[64];

/* place vertices of list[pos..] ; K = chosen so far ; S = current subset */
static int search(const int *list, int len, int pos, uint64_t S, uint64_t K) {
    if (pos == len) {
        for (int t = 0; t < len; t++) {
            int v = list[t];
            if (!(K >> v & 1) && !(out_[v] & K)) return 0;
        }
        return 1;
    }
    int v = list[pos];
    /* prune: any earlier vertex not in K whose out-neighbours in S are all earlier and none in K */
    for (int t = 0; t < pos; t++) {
        int x = list[t];
        if (K >> x & 1) continue;
        if (out_[x] & K) continue;
        uint64_t later = 0;
        for (int s = pos; s < len; s++) later |= 1ULL << list[s];
        if (!(out_[x] & S & later)) return 0;
    }
    if (!(adj[v] & K) && search(list, len, pos + 1, S, K | (1ULL << v))) return 1;
    return search(list, len, pos + 1, S, K);
}

int main(void) {
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++) {
        int v, d; scanf("%d %d", &v, &d);
        for (int k = 0; k < d; k++) { int w; scanf("%d", &w); out_[v] |= 1ULL << w; }
    }
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++)
        if (out_[v] >> w & 1) { adj[v] |= 1ULL << w; adj[w] |= 1ULL << v; }
    uint64_t total = 1ULL << n;
    int list[64];
    for (uint64_t S = 1; S < total; S++) {
        int len = 0;
        for (int v = 0; v < n; v++) if (S >> v & 1) list[len++] = v;
        if (!search(list, len, 0, S, 0)) { printf("KERNEL-LESS S = %llx\n", (unsigned long long)S); return 0; }
        if ((S & 0xFFFFFF) == 0) { fprintf(stderr, "progress %llu/%llu\n", (unsigned long long)(S >> 24), (unsigned long long)(total >> 24)); }
    }
    printf("KERNEL-PERFECT (all %llu nonempty subsets have a kernel)\n", (unsigned long long)(total - 1));
    return 0;
}
