/* Independent census for the House Lemma (Theorem 4.1) of
   "The triangular prism is enumeratively chromatic-choosable".

   Written from the manuscript, not from checks/house_type_enumeration.cpp.

   A colour's type is its membership vector in (L2, L4, A1, A3, R); 31 nonzero types.
   A house assignment is determined, up to renaming colours, by the number n_t of colours
   of each type.  We enumerate ALL count vectors with |L2| = |L4| = k, |R| = k-1 and
   |A1|, |A3| in {k-1, k}  (so Lemma 4.2's size reduction is checked, not assumed).

   The house count is computed exactly by conditioning on the shoulder colours (c2, c4):
     roof choices  = |R| - [c2 in R] - [c4 in R]
     base choices  = (|A1| - [c2 in A1]) (|A3| - [c4 in A3]) - (|I| - [c2 in I] - [c4 in I])
   where I = A1 n A3.  This is formula (4) with general base sizes; it is checked against
   direct brute force by a4_identities.py.

   Output: number of count vectors, min(h - target), and every count vector with h < target,
   which must be exactly the configuration Delta with h = target - sigma_k.
   Usage: ./a3_house_census k                                             */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long ll;
static int K, NT = 31;
static int ty[31][5];          /* bits: 0=L2 1=L4 2=A1 3=A3 4=R */
static int cnt[31];
static ll ncfg = 0, nbelow = 0, nbelow_nondelta = 0;
static ll minv = 1LL << 60;
static ll target, sigma;

static int is_delta(void) {
    /* Delta: (1,1,1,1,1) x (k-2), (1,1,1,1,0) x 1, (1,1,0,0,1) x 1, nothing else */
    for (int i = 0; i < NT; i++) {
        int *b = ty[i]; int want = 0;
        if (b[0]&&b[1]&&b[2]&&b[3]&&b[4]) want = K - 2;
        else if (b[0]&&b[1]&&b[2]&&b[3]&&!b[4]) want = 1;
        else if (b[0]&&b[1]&&!b[2]&&!b[3]&&b[4]) want = 1;
        if (cnt[i] != want) return 0;
    }
    return 1;
}

static void evaluate(void) {
    ll sz[5] = {0,0,0,0,0}, I = 0;
    for (int i = 0; i < NT; i++) {
        for (int j = 0; j < 5; j++) sz[j] += (ll)cnt[i] * ty[i][j];
        I += (ll)cnt[i] * (ty[i][2] & ty[i][3]);
    }
    ll h = 0;
    for (int a = 0; a < NT; a++) {            /* type of c2 (must be in L2) */
        if (!ty[a][0] || !cnt[a]) continue;
        for (int c = 0; c < NT; c++) {        /* type of c4 (must be in L4) */
            if (!ty[c][1] || !cnt[c]) continue;
            ll pairs = (ll)cnt[a] * cnt[c] - (a == c ? cnt[a] : 0);   /* c2 != c4 */
            if (!pairs) continue;
            ll roof = sz[4] - ty[a][4] - ty[c][4];
            ll inIa = ty[a][2] & ty[a][3], inIc = ty[c][2] & ty[c][3];
            ll base = (sz[2] - ty[a][2]) * (sz[3] - ty[c][3]) - (I - inIa - inIc);
            if (a == c) { /* same colour type but distinct colours: formula unchanged */ }
            h += pairs * roof * base;
        }
    }
    ncfg++;
    ll d = h - target;
    if (d < minv) minv = d;
    if (d < 0) {
        nbelow++;
        int bad = !(is_delta() && d == -sigma && sz[2] == K - 1 && sz[3] == K - 1);
        if (bad) {
            nbelow_nondelta++;
            printf("  NON-DELTA deficit config: d=%lld sizes A1=%lld A3=%lld\n", d, sz[2], sz[3]);
        }
    }
}

/* recursive enumeration with remaining capacities */
static int cap[5];
static int baseA1, baseA3;
static void rec(int i) {
    if (i == NT) {
        for (int j = 0; j < 5; j++) if (cap[j]) return;
        evaluate(); return;
    }
    /* max copies of type i allowed by remaining capacities */
    int mx = 1 << 30;
    for (int j = 0; j < 5; j++) if (ty[i][j] && cap[j] < mx) mx = cap[j];
    for (int m = 0; m <= mx; m++) {
        cnt[i] = m;
        for (int j = 0; j < 5; j++) if (ty[i][j]) cap[j] -= m;
        rec(i + 1);
        for (int j = 0; j < 5; j++) if (ty[i][j]) cap[j] += m;
    }
    cnt[i] = 0;
}

int main(int argc, char **argv) {
    K = atoi(argv[1]);
    ll o = (ll)(K - 2) * ((ll)K*K*K - 6LL*K*K + 14LL*K - 13);
    target = (ll)(K - 1) * o;
    sigma = 2LL * (K - 2) * (K - 3);
    int t = 0;
    for (int m = 1; m < 32; m++) { for (int j = 0; j < 5; j++) ty[t][j] = (m >> j) & 1; t++; }
    ll tot = 0, totbelow = 0;
    for (baseA1 = K - 1; baseA1 <= K; baseA1++)
        for (baseA3 = K - 1; baseA3 <= K; baseA3++) {
            ll c0 = ncfg, b0 = nbelow;
            cap[0] = K; cap[1] = K; cap[2] = baseA1; cap[3] = baseA3; cap[4] = K - 1;
            rec(0);
            printf("k=%d |A1|=%d |A3|=%d: count vectors=%lld, below target=%lld\n",
                   K, baseA1, baseA3, ncfg - c0, nbelow - b0);
        }
    printf("k=%d TOTAL count vectors=%lld  min(h-target)=%lld  -sigma_k=%lld  below target=%lld  non-Delta below target=%lld\n",
           K, ncfg, minv, -sigma, nbelow, nbelow_nondelta);
    return 0;
}
