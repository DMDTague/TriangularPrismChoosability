"""Validate the 71-variable model of Proposition 4.7 against brute-force house counts.

For random house assignments with |A1|=|A3|=|R|=k-1, |L2|=|L4|=k, L2 != L4:
  (a) brute-force h equals formula (4) (Lemma 4.3) computed with the true |I|;
  (b) h - target >= F0(v), where v is the 71-variable encoding (Lemma 4.4 substitution);
  (c) F0(v) > 0 (Proposition 4.7, k >= 6).
F0 is the polynomial built by a1_certificate.py. Exact integer arithmetic throughout.
"""
import itertools, pickle, random, sys
import sympy as sp

data = pickle.load(open(sys.argv[1], 'rb'))
k = sp.Symbol('k')
F0 = data['F0']; names = data['order']
syms = [sp.Symbol(n) for n in names]

def house_brute(A1, A3, L2, L4, R):
    # vertices b1,b3,s2,s4,rho; edges b1b3, b1s2, b3s4, s2s4, s2rho, s4rho
    cnt = 0
    for c2 in L2:
        for c4 in L4:
            if c2 == c4: continue
            nr = sum(1 for r in R if r != c2 and r != c4)
            if nr == 0: continue
            nb = sum(1 for a in A1 if a != c2 for c in A3 if c != c4 and c != a)
            cnt += nr * nb
    return cnt

def house_fully_brute(A1, A3, L2, L4, R):
    return sum(1 for a in A1 for c in A3 for s in L2 for t in L4 for r in R
               if a != c and a != s and c != t and s != t and s != r and t != r)

def formula4(A1, A3, L2, L4, R, kk):
    I = A1 & A3
    tot = 0
    for c2 in L2:
        for c4 in L4:
            if c2 == c4: continue
            tot += (kk - 1 - (c2 in R) - (c4 in R)) * ((kk - 1 - (c2 in A1)) * (kk - 1 - (c4 in A3))
                    - len(I) + (c2 in I) + (c4 in I))
    return tot

def encode(A1, A3, L2, L4, R):
    typ = lambda c: f'{int(c in R)}{int(c in A1)}{int(c in A3)}'
    v = {n: 0 for n in names}
    for c in L2 & L4:
        t = typ(c)
        if t != '111': v[f'D_{t}'] += 1
    P = sorted(L2 - L4); Q = sorted(L4 - L2)
    for p, q in zip(P, Q):
        v[f'Z_{typ(p)}_{typ(q)}'] += 1
    return v

random.seed(20261123)
stats = {}
for kk in (6, 7):
    target = (kk - 1) * (kk - 2) * (kk**3 - 6*kk**2 + 14*kk - 13)
    F0k = sp.lambdify(syms, F0.subs(k, kk), 'math')
    n = worst = 0; minF = None
    for trial in range(3000):
        N = random.randint(kk + 1, 3 * kk)
        U = list(range(N))
        L2 = set(random.sample(U, kk)); L4 = set(random.sample(U, kk))
        if L2 == L4: continue
        A1 = set(random.sample(U, kk - 1)); A3 = set(random.sample(U, kk - 1)); R = set(random.sample(U, kk - 1))
        h = house_brute(A1, A3, L2, L4, R)
        assert h == formula4(A1, A3, L2, L4, R, kk), 'formula (4) mismatch'
        if trial < 40:
            assert h == house_fully_brute(A1, A3, L2, L4, R), 'brute mismatch'
        v = encode(A1, A3, L2, L4, R)
        f = F0k(*[v[nm] for nm in names])
        assert float(h - target) >= f - 1e-6, ('model not a lower bound', h - target, f)
        assert f > 0, ('Prop 4.7 violated', f)
        n += 1; minF = f if minF is None else min(minF, f)
    stats[kk] = (n, minF)
    print(f'k={kk}: {n} random unequal-shoulder assignments; formula (4) = brute force; '
          f'h - target >= F0(v) > 0 in all; min F0(v) = {minF:.0f}')
print('All model-validation checks passed.')
