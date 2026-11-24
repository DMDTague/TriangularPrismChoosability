/* Independent complete check of Theorem 1.1 for small k:
   every assignment of k-element lists to the six edges of K_{2,3} has at least c_k
   proper list edge-colourings.

   A colour's type is its membership vector in the six lists (63 nonzero types).  Up to
   renaming colours, an assignment is a count vector n_t with sum over types containing
   edge i of n_t equal to k, for each i.  This enumerates ALL such count vectors, so it
   covers every colour universe.

   The number of proper colourings is computed by inclusion-exclusion over the 9 edges of
   the line graph (the prism):  N = sum_{S subset of E(prism)} (-1)^{|S|} prod_{components C
   of (V,S)} (number of colours lying in every list of C).
   Validated against direct brute force in a6_validate.py.
   Optional second argument caps the total number of colours (universe size).
   Usage: ./a5_prism_census k [maxcolours]                                                   */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
static int K;
/* K_{2,3}: e0=ua e1=av e2=ub e3=bv e4=uw e5=wv (0-based) */
static const int ends[6][2] = {{0,2},{2,1},{0,3},{3,1},{0,4},{4,1}}; /* u=0 v=1 a=2 b=3 w=4 */
static int ladj[9][2]; static int nle = 0;
static int nsub = 512;
static int compmask[512][6]; static int ncomp[512]; static int sgn[512];
static int cnt[64];
static ll sup[64];
static ll ncfg = 0, minN = 1LL << 62, nbelow = 0;

static int find(int *p, int x) { while (p[x] != x) x = p[x] = p[p[x]]; return x; }

static void prepare(void) {
    for (int i = 0; i < 6; i++) for (int j = i + 1; j < 6; j++) {
        int sh = 0;
        for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) if (ends[i][a] == ends[j][b]) sh = 1;
        if (sh) { ladj[nle][0] = i; ladj[nle][1] = j; nle++; }
    }
    if (nle != 9) { printf("line graph edge count %d != 9\n", nle); exit(1); }
    for (int S = 0; S < nsub; S++) {
        int p[6]; for (int i = 0; i < 6; i++) p[i] = i;
        int bits = 0;
        for (int e = 0; e < 9; e++) if (S >> e & 1) { bits++; p[find(p, ladj[e][0])] = find(p, ladj[e][1]); }
        sgn[S] = (bits & 1) ? -1 : 1;
        int m[6] = {0}; int nc = 0;
        for (int i = 0; i < 6; i++) m[find(p, i)] |= 1 << i;
        for (int i = 0; i < 6; i++) if (m[i]) compmask[S][nc++] = m[i];
        ncomp[S] = nc;
    }
}

static void evaluate(void) {
    for (int M = 0; M < 64; M++) {            /* sup[M] = #colours whose type contains M */
        ll s = 0;
        for (int t = 1; t < 64; t++) if ((t & M) == M) s += cnt[t];
        sup[M] = s;
    }
    ll N = 0;
    for (int S = 0; S < nsub; S++) {
        ll pr = 1;
        for (int c = 0; c < ncomp[S]; c++) { pr *= sup[compmask[S][c]]; if (!pr) break; }
        N += sgn[S] * pr;
    }
    ncfg++;
    if (N < minN) minN = N;
    ll ck = (ll)K*(K-1)*(K-2)*((ll)K*K*K - 6LL*K*K + 14LL*K - 13);
    if (N < ck) { nbelow++; printf("BELOW c_k: N=%lld\n", N); }
}

static int cap[6]; static int UMAX = 1000, used = 0;
static void rec(int t) {
    if (t == 64) { for (int i = 0; i < 6; i++) if (cap[i]) return; evaluate(); return; }
    { int need = 0; for (int i = 0; i < 6; i++) if (cap[i] > need) need = cap[i];
      if (need > UMAX - used) return; }   /* each colour adds at most 1 to a list */
    int mx = 1 << 30;
    for (int i = 0; i < 6; i++) if ((t >> i & 1) && cap[i] < mx) mx = cap[i];
    /* prune: remaining types t..63 must be able to fill every capacity (always true by
       singleton types 1,2,4,...: a list can always be filled by private colours) */
    if (mx > UMAX - used) mx = UMAX - used;
    for (int m = 0; m <= mx; m++) {
        cnt[t] = m; used += m;
        for (int i = 0; i < 6; i++) if (t >> i & 1) cap[i] -= m;
        rec(t + 1);
        for (int i = 0; i < 6; i++) if (t >> i & 1) cap[i] += m;
        used -= m;
    }
    cnt[t] = 0;
}

int main(int argc, char **argv) {
    K = atoi(argv[1]);
    if (argc > 2) UMAX = atoi(argv[2]);
    prepare();
    for (int i = 0; i < 6; i++) cap[i] = K;
    rec(1);
    ll ck = (ll)K*(K-1)*(K-2)*((ll)K*K*K - 6LL*K*K + 14LL*K - 13);
    printf("k=%d, at most %d colours: count vectors=%lld  min N=%lld  c_k=%lld  below c_k=%lld\n", K, UMAX, ncfg, minN, ck, nbelow);
    return 0;
}
