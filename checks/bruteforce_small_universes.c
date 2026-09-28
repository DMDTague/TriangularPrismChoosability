// Brute force: (1) N_L(K_{2,3}) >= c_k over all k-assignments from a colour universe of size U,
// with L(e5) fixed to {0..k-1} by colour symmetry. (2) House lemma over base lists of size k-1,
// shoulders k, roof k-1 from universe U, with L2 fixed to {0..k-1}.
#include <stdio.h>
#include <stdlib.h>
typedef unsigned int u32;
static int subsets[4096], ns;
static void gen(int U, int r) { ns = 0; for (int s = 0; s < (1 << U); s++) if (__builtin_popcount(s) == r) subsets[ns++] = s; }
static int elems[4096][16], cnt[4096];
static void prep(int U) { for (int i = 0; i < ns; i++) { cnt[i] = 0; for (int c = 0; c < U; c++) if (subsets[i] >> c & 1) elems[i][cnt[i]++] = c; } }

int main(int argc, char **argv) {
  int mode = atoi(argv[1]), k = atoi(argv[2]), U = atoi(argv[3]);
  if (mode == 1) {
    long ck = (long)k*(k-1)*(k-2)*((long)k*k*k - 6*k*k + 14*k - 13);
    gen(U, k); prep(U);
    int L5 = (1 << k) - 1, i5 = -1; for (int i = 0; i < ns; i++) if (subsets[i] == L5) i5 = i;
    long minN = -1, configs = 0, below = 0;
    for (int i1 = 0; i1 < ns; i1++) for (int i2 = 0; i2 < ns; i2++) for (int i3 = 0; i3 < ns; i3++)
    for (int i4 = 0; i4 < ns; i4++) for (int i6 = 0; i6 < ns; i6++) {
      long N = 0;
      for (int a = 0; a < k; a++) { int c1 = elems[i1][a];
       for (int b = 0; b < k; b++) { int c3 = elems[i3][b]; if (c3 == c1) continue;
        for (int c = 0; c < k; c++) { int c5 = elems[i5][c]; if (c5 == c1 || c5 == c3) continue;
         for (int d = 0; d < k; d++) { int c2 = elems[i2][d]; if (c2 == c1) continue;
          for (int e = 0; e < k; e++) { int c4 = elems[i4][e]; if (c4 == c3 || c4 == c2) continue;
           for (int f = 0; f < k; f++) { int c6 = elems[i6][f]; if (c6 == c5 || c6 == c2 || c6 == c4) continue; N++; }}}}}}
      configs++; if (minN < 0 || N < minN) minN = N; if (N < ck) below++;
    }
    printf("K23 k=%d U=%d: assignments=%ld  min N=%ld  c_k=%ld  below c_k=%ld\n", k, U, configs, minN, ck, below);
  } else {
    long o = (long)(k-2)*((long)k*k*k - 6*k*k + 14*k - 13), target = (k-1)*o;
    int nb, nk; static int B[4096], S[4096];
    gen(U, k-1); prep(U); nb = ns; int eb[4096][16]; for (int i = 0; i < nb; i++) { B[i] = subsets[i]; for (int t = 0; t < k-1; t++) eb[i][t] = elems[i][t]; }
    gen(U, k); prep(U); nk = ns;
    int L2 = (1 << k) - 1; long configs = 0, below = 0, minD = 1L<<60;
    for (int i4 = 0; i4 < nk; i4++) for (int ia = 0; ia < nb; ia++) for (int ic = 0; ic < nb; ic++) for (int ir = 0; ir < nb; ir++) {
      int L4 = subsets[i4];
      long h = 0;
      for (int c2 = 0; c2 < k; c2++) for (int t = 0; t < k; t++) { int c4 = elems[i4][t]; if (c4 == c2) continue;
        int roof = k - 1 - ((B[ir] >> c2) & 1) - ((B[ir] >> c4) & 1);
        long pairs = 0;
        for (int x = 0; x < k-1; x++) { int a1 = eb[ia][x]; if (a1 == c2) continue;
          for (int y = 0; y < k-1; y++) { int a3 = eb[ic][y]; if (a3 == c4 || a3 == a1) continue; pairs++; } }
        h += roof * pairs; }
      configs++; long d = h - target; if (d < minD) minD = d;
      if (d < 0) { below++;
        int A1 = B[ia], A3 = B[ic], R = B[ir];
        int isDelta = (A1 == A3) && (L2 == L4) && __builtin_popcount(A1 & L2) == k-1;
        int gamma = L2 & ~A1;
        isDelta = isDelta && (R & gamma) && __builtin_popcount(R & A1) == k-2;
        if (!isDelta) printf("NON-DELTA deficit config: L4=%x A1=%x A3=%x R=%x d=%ld\n", L4, A1, A3, R, d); }
    }
    printf("House k=%d U=%d: configs=%ld  min(h-target)=%ld  sigma_k=%d  configs below target=%ld (all Delta unless flagged)\n", k, U, configs, minD, 2*(k-2)*(k-3), below);
  }
  return 0;
}
