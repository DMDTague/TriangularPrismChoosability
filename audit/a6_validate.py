"""(1) Cross-check the inclusion-exclusion count used in a5_prism_census.c against brute force.
(2) Exhaustive check of fact (F2) for C4 = L(C4) at m = 2..5: every assignment of m-lists to
    the four vertices of C4 has at least (m-1)^4 + (m-1) proper colourings (all colour universes,
    via membership-type count vectors).  The proof cites this as a known theorem."""
import itertools, random
EDGES = [(0,2),(2,1),(0,3),(3,1),(0,4),(4,1)]
LADJ = [(i, j) for i in range(6) for j in range(i+1, 6) if set(EDGES[i]) & set(EDGES[j])]
assert len(LADJ) == 9
def brute(L):
    return sum(1 for c in itertools.product(*L) if all(c[i] != c[j] for i, j in LADJ))
def ie(L):
    tot = 0
    for S in range(512):
        p = list(range(6))
        def f(x):
            while p[x] != x: x = p[x]
            return x
        bits = 0
        for e in range(9):
            if S >> e & 1: bits += 1; p[f(LADJ[e][0])] = f(LADJ[e][1])
        comps = {}
        for i in range(6): comps.setdefault(f(i), []).append(i)
        pr = 1
        for cs in comps.values(): pr *= len(set.intersection(*[set(L[i]) for i in cs]))
        tot += (-1) ** bits * pr
    return tot
random.seed(11)
for _ in range(150):
    kk = random.choice([3, 4]); U = list(range(random.randint(kk, 2*kk+2)))
    L = [random.sample(U, kk) for _ in range(6)]
    assert brute(L) == ie(L)
print('inclusion-exclusion count = brute force on 150 random K_{2,3} assignments (k=3,4)')

# (2) C4 with vertices 0-1-2-3-0
def c4_count(counts, m):
    # counts: dict type(4-bit mask) -> number of colours; IE over the 4 cycle edges
    sup = {M: sum(n for t, n in counts.items() if t & M == M) for M in range(16)}
    E = [(0,1),(1,2),(2,3),(3,0)]; tot = 0
    for S in range(16):
        p = list(range(4))
        def f(x):
            while p[x] != x: x = p[x]
            return x
        for e in range(4):
            if S >> e & 1: p[f(E[e][0])] = f(E[e][1])
        comps = {}
        for i in range(4): comps.setdefault(f(i), 0); comps[f(i)] |= 1 << i
        pr = 1
        for M in comps.values(): pr *= sup[M]
        tot += (-1) ** bin(S).count('1') * pr
    return tot
for m in range(2, 6):
    types = list(range(1, 16)); best = None; nvec = 0
    def rec(i, cap, cnt):
        global best, nvec
        if i == len(types):
            if any(cap): return
            nvec += 1; v = c4_count(cnt, m)
            best = v if best is None else min(best, v); return
        t = types[i]; mx = min(cap[j] for j in range(4) if t >> j & 1)
        for c in range(mx + 1):
            cnt[t] = c
            rec(i + 1, [cap[j] - (c if t >> j & 1 else 0) for j in range(4)], cnt)
        cnt[t] = 0
    rec(0, [m]*4, {})
    target = (m-1)**4 + (m-1)
    print(f'C4, m={m}: {nvec} count vectors, min colourings = {best}, P(C4,m) = {target}, ok = {best == target}')
    assert best == target
