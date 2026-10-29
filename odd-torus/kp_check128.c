/* Kernel-perfectness checker for small digraphs (at most 127 vertices; 128-bit build of kp_check.c), used by kernel_torus.py.
 *
 * A kernel of D[S] is an independent K subset of S such that every vertex of S \ K has an
 * out-neighbour in K.  find_kernelless(n, out, maxsize) returns the bitmask of a smallest set S,
 * |S| <= maxsize, such that D[S] has no kernel, or 0 if every D[S] with |S| <= maxsize has one.
 * Only weakly connected S are examined: a disjoint union has a kernel iff every part has one.
 */
#include <stdint.h>

typedef unsigned __int128 u64;
static inline int ctz128(u64 x) {
    uint64_t lo = (uint64_t)x;
    return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(x >> 64));
}
static int N;
static u64 OUT[128], IN[128], NB[128];

/* Does D[S] have a kernel?  K = chosen, X = excluded (must be absorbed by K), U = undecided. */
static int solve(u64 S, u64 K, u64 X, u64 U) {
    for (;;) {
        int changed = 0;
        u64 x = X;
        while (x) {  /* excluded vertices not yet absorbed */
            int v = ctz128(x); x &= x - 1;
            if (OUT[v] & K) continue;
            u64 cand = OUT[v] & U;
            if (!cand) return 0;
            if (!(cand & (cand - 1))) {  /* exactly one candidate: force it into K */
                int y = ctz128(cand);
                if (NB[y] & K) return 0;
                K |= ((u64)1) << y; U &= ~(((u64)1) << y);
                u64 nb = NB[y] & U; U &= ~nb; X |= nb;
                changed = 1;
            }
        }
        u64 u = U;  /* an undecided vertex with no out-neighbour in K or U must go into K */
        while (u) {
            int v = ctz128(u); u &= u - 1;
            if (!(U >> v & 1)) continue;
            if (!(OUT[v] & S & (K | U))) {
                if (NB[v] & K) return 0;
                K |= ((u64)1) << v; U &= ~(((u64)1) << v);
                u64 nb = NB[v] & U; U &= ~nb; X |= nb;
                changed = 1;
            }
        }
        if (!changed) break;
    }
    if (!U) {
        u64 x = X;
        while (x) { int v = ctz128(x); x &= x - 1; if (!(OUT[v] & K)) return 0; }
        return 1;
    }
    int v = ctz128(U);
    u64 U2 = U & ~(((u64)1) << v);
    if (!(NB[v] & K)) {  /* v in K */
        u64 nb = NB[v] & U2;
        if (solve(S, K | (((u64)1) << v), X | nb, U2 & ~nb)) return 1;
    }
    return solve(S, K, X | (((u64)1) << v), U2);  /* v not in K */
}

static int has_kernel(u64 S) {
    u64 save[128];
    for (int v = 0; v < N; v++) { save[v] = OUT[v]; }
    for (int v = 0; v < N; v++) if (S >> v & 1) { OUT[v] = save[v] & S; }
    u64 nbs[128];
    for (int v = 0; v < N; v++) { nbs[v] = NB[v]; NB[v] = (OUT[v] | (IN[v] & S)) & S; }
    int r = solve(S, 0, 0, S);
    for (int v = 0; v < N; v++) { OUT[v] = save[v]; NB[v] = nbs[v]; }
    return r;
}

/* Enumerate connected subsets of size exactly k containing their minimum vertex, by the
 * standard "extension" scheme (each connected set generated once). */
static u64 found;
static void grow(u64 S, u64 ext, u64 forbidden, int k, int size) {
    if (found) return;
    if (size == k) { if (!has_kernel(S)) found = S; return; }
    while (ext) {
        int v = ctz128(ext);
        u64 bit = ((u64)1) << v;
        ext &= ~bit;
        u64 newext = ext | (NB[v] & ~S & ~forbidden & ~bit);
        newext &= ~forbidden;
        grow(S | bit, newext, forbidden | bit, k, size + 1);
        forbidden |= bit;
        if (found) return;
    }
}

void find_kernelless128(int n, const uint64_t *out2, int maxsize, uint64_t *res2) {
    N = n;
    for (int v = 0; v < n; v++) { OUT[v] = ((u64)out2[2*v+1] << 64) | out2[2*v]; IN[v] = 0; }
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++) if (OUT[v] >> w & 1) IN[w] |= ((u64)1) << v;
    for (int v = 0; v < n; v++) NB[v] = OUT[v] | IN[v];
    found = 0;
    for (int k = 1; k <= maxsize && k <= n; k++) {
        for (int r = 0; r < n && !found; r++) {
            u64 below = (r == 0) ? 0 : ((((u64)1) << r) - 1);  /* r is the minimum vertex of S */
            grow(((u64)1) << r, NB[r] & ~below & ~(((u64)1) << r), below | (((u64)1) << r), k, 1);
        }
        if (found) break;
    }
    res2[0] = (uint64_t)found; res2[1] = (uint64_t)(found >> 64);
}

