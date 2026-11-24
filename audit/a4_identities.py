"""Independent checks of the displayed identities in
'The triangular prism is enumeratively chromatic-choosable'.
Written from the manuscript. Exact integer / sympy arithmetic; brute force where possible."""
import itertools, random
import sympy as sp

k, r = sp.symbols('k r')
out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
def ok(name, cond):
    say(('PASS ' if cond else 'FAIL ') + name); assert cond, name

# K_{2,3}: u, v degree 3; a, b, w degree 2. e1=ua e2=av e3=ub e4=bv e5=uw e6=wv
EDGES = [('u','a'),('a','v'),('u','b'),('b','v'),('u','w'),('w','v')]
ADJ = [(i, j) for i in range(6) for j in range(i+1, 6) if set(EDGES[i]) & set(EDGES[j])]
def N_brute(L):
    return sum(1 for col in itertools.product(*L) if all(col[i] != col[j] for i, j in ADJ))

c_k = k*(k-1)*(k-2)*(k**3-6*k**2+14*k-13)
o_k = (k-2)*(k**3-6*k**2+14*k-13)
d_k = (k-1)*(k-2)*(k**2-5*k+7)
s_k = 2*(k-2)*(k-3)
target = (k-1)*o_k

# Lemma 2.1
ok('Lemma 2.1: c_k equals brute-force proper k-edge-colourings of K_{2,3}, k=3..6',
   all(N_brute([list(range(kk))]*6) == c_k.subs(k, kk) for kk in range(3, 7)))
ok('o_k - d_k = sigma_k', sp.expand(o_k - d_k - s_k) == 0)
ok('d_k = (k-2)^4 + (k-2) = P(C4, k-1)', sp.expand(d_k - ((k-2)**4 + (k-2))) == 0)
def P_C4(m): return (m-1)**4 + (m-1)
ok('d_3 = o_3 = 2', d_k.subs(k, 3) == 2 and o_k.subs(k, 3) == 2)

# Lemma 3.1 (gluing) on random list assignments
def F(L, x, y):
    # colourings of Q = e1..e4 avoiding x on e1,e3 and y on e2,e4
    L1 = [c for c in L[0] if c != x]; L3 = [c for c in L[2] if c != x]
    L2 = [c for c in L[1] if c != y]; L4 = [c for c in L[3] if c != y]
    # Q: e1-e2 share a, e3-e4 share b, e1-e3 share u, e2-e4 share v
    return sum(1 for a1 in L1 for a3 in L3 if a1 != a3 for a2 in L2 if a2 != a1
               for a4 in L4 if a4 != a3 and a4 != a2)
def S(L, x): return sum(F(L, x, y) for y in L[5] if y != x)
random.seed(7)
good = True
for _ in range(300):
    kk = random.choice([3, 4, 5]); U = list(range(random.randint(kk, 2*kk+1)))
    L = [random.sample(U, kk) for _ in range(6)]
    good &= N_brute(L) == sum(S(L, x) for x in L[4])
ok('Lemma 3.1: N_L = sum_{x in A} S(x) on 300 random assignments', good)

# Corollary 3.3(ii) identity
ok('Cor 3.3(ii): k d_k - (k-1) o_k = (k-1)(k-2)(k^2-7k+13)',
   sp.expand(k*d_k - (k-1)*o_k - (k-1)*(k-2)*(k**2-7*k+13)) == 0)

# House counts: brute force vs formula with general base sizes (used by a3_house_census.c)
def h_brute(A1, A3, L2, L4, R):
    return sum(1 for a in A1 for c in A3 for s in L2 for t in L4 for q in R
               if a != c and a != s and c != t and s != t and s != q and t != q)
def h_formula(A1, A3, L2, L4, R):
    I = A1 & A3; tot = 0
    for c2 in L2:
        for c4 in L4:
            if c2 == c4: continue
            tot += (len(R) - (c2 in R) - (c4 in R)) * ((len(A1) - (c2 in A1)) * (len(A3) - (c4 in A3))
                    - (len(I) - (c2 in I) - (c4 in I)))
    return tot
good = True
for _ in range(400):
    kk = random.choice([4, 5]); U = list(range(random.randint(kk, 3*kk)))
    A1 = set(random.sample(U, random.choice([kk-1, kk]))); A3 = set(random.sample(U, random.choice([kk-1, kk])))
    L2 = set(random.sample(U, kk)); L4 = set(random.sample(U, kk)); R = set(random.sample(U, kk-1))
    good &= h_brute(A1, A3, L2, L4, R) == h_formula(A1, A3, L2, L4, R)
ok('House count formula (general base sizes) = brute force, 400 random cases, k=4,5', good)

# Lemma 3.4 (rows in B are house counts) on random prism assignments
good = True
for _ in range(200):
    kk = random.choice([4, 5]); U = list(range(random.randint(kk, 2*kk)))
    L = [random.sample(U, kk) for _ in range(6)]
    for x in set(L[4]) & set(L[5]):
        good &= S(L, x) == h_brute(set(L[0]) - {x}, set(L[2]) - {x}, set(L[1]), set(L[3]), set(L[5]) - {x})
ok('Lemma 3.4: S(x) = house count, 200 random assignments', good)

# Proposition 4.5 (equal pairs): f-values, D(r), Delta value
p, q, t = sp.symbols('p q t')
fexpr = p*(p-1)*q*(q-1) - 2*t*(p-1)*(q-1) + t*(t-1)
fC = fexpr.subs({p: k-1, q: k-1, t: r-1}); fV = fexpr.subs({p: k-1, q: k-1, t: r}); fO = fexpr.subs({p: k-1, q: k, t: r})
ok('f_C as displayed', sp.expand(fC - ((k-1)**2*(k-2)**2 - 2*(r-1)*(k-2)**2 + (r-1)*(r-2))) == 0)
ok('f_V as displayed', sp.expand(fV - ((k-1)**2*(k-2)**2 - 2*r*(k-2)**2 + r*(r-1))) == 0)
ok('f_O as displayed', sp.expand(fO - (k*(k-1)**2*(k-2) - 2*r*(k-1)*(k-2) + r*(r-1))) == 0)
# brute-force the per-roof-colour counts on a concrete instance
good = True
for kk in (4, 5, 6):
    for rr in range(0, kk):
        A = set(range(kk-1)); V = set(range(kk-1-rr, 2*kk-1-rr))   # |A n V| = rr
        assert len(A & V) == rr and len(V) == kk
        def f_of(y):
            return h_brute(A, A, V, V, {y})
        yC = next(iter(A & V), None); yV = next(iter(V - A)); yO = 10*kk
        if yC is not None: good &= f_of(yC) == fC.subs({k: kk, r: rr})
        good &= f_of(yV) == fV.subs({k: kk, r: rr}) and f_of(yO) == fO.subs({k: kk, r: rr})
ok('f_C, f_V, f_O match brute force, k=4..6, all r', good)
D = sp.expand(target - ((k-r)*fV + (r-1)*fC))
ok('D(r) quadratic in r with leading coefficient 3-k', sp.expand(sp.Poly(D, r).LC() - (3-k)) == 0 and sp.Poly(D, r).degree() == 2)
ok("D'(k-1) = (k-3)(2k^2-8k+9)", sp.expand(sp.diff(D, r).subs(r, k-1) - (k-3)*(2*k**2-8*k+9)) == 0)
ok('D(k-1) = sigma_k', sp.expand(D.subs(r, k-1) - s_k) == 0)
ok('D(k-2) = -2(k-3)(k^2-5k+7)', sp.expand(D.subs(r, k-2) + 2*(k-3)*(k**2-5*k+7)) == 0)
ok('r=0 value = -(k-1)(k-2)(2k^2-9k+11)', sp.expand(target - (k-1)*fV.subs(r, 0) + (k-1)*(k-2)*(2*k**2-9*k+11)) == 0)
ok('f_O - f_C at r=k-1 = 2(k-2)(k^2-4k+5)', sp.expand((fO-fC).subs(r, k-1) - 2*(k-2)*(k**2-4*k+5)) == 0)
ok('2(k-2)(k^2-4k+5) > sigma_k for k>=4', all(2*(kk-2)*(kk**2-4*kk+5) > 2*(kk-2)*(kk-3) for kk in range(4, 50))
   and sp.Poly(sp.expand(2*(k-2)*(k**2-4*k+5) - s_k).subs(k, k+4), k).all_coeffs() == [c for c in sp.Poly(sp.expand(2*(k-2)*(k**2-4*k+5) - s_k).subs(k, k+4), k).all_coeffs()])
good = True
for kk in range(4, 8):
    C = set(range(kk-1)); g = 100
    h = h_brute(C, C, C | {g}, C | {g}, (C - {0}) | {g})
    good &= h == (target - s_k).subs(k, kk)
ok('Delta attains target - sigma_k (brute force, k=4..7)', good)

# Proposition 4.6: equality example (A1, A3, R = V minus three distinct colours)
q_k = k**3 - 8*k**2 + 24*k - 25
good = True
for kk in range(4, 8):
    V = set(range(kk))
    good &= h_brute(V - {0}, V - {1}, V, V, V - {2}) == (target + q_k).subs(k, kk)
ok('Prop 4.6 equality example attains target + q_k (k=4..7)', good)
ok('q_k > 0 for k >= 4 (coefficients after k=4+m)', all(c > 0 for c in sp.Poly(sp.expand(q_k.subs(k, k+4)), k).all_coeffs()))

# Lemma 5.2 (compensation): deltas computed by brute force on the prism configuration
good = True
for kk in range(4, 8):
    C = list(range(1, kk)); x = 0; g = 100; c0 = C[0]
    P = C + [x]; V = C + [g]; B = [x, g] + [c for c in C if c != c0]
    A = [x] + random.sample(range(200, 300), kk - 1)   # L(e5): only its rows matter via deltas
    L = [P, V, P, V, A, B]
    delta = lambda col: (kk-1)*o_k.subs(k, kk) - S(L, col)
    good &= delta(x) == s_k.subs(k, kk)
    good &= delta(g) == -2*(kk**4-5*kk**3+10*kk**2-8*kk+1)
    good &= all(delta(c) == -2*(2*kk**3-13*kk**2+31*kk-27) for c in C if c != c0)
ok('Lemma 5.2: delta_x = sigma_k, delta_gamma, delta_c match brute force (k=4..7)', good)
e1 = sp.expand(s_k - 2*(k**4-5*k**3+10*k**2-8*k+1)); e2 = sp.expand(s_k - 2*(2*k**3-13*k**2+31*k-27))
ok('delta_x + delta_gamma = -2(k^4-5k^3+9k^2-3k-5)', sp.expand(e1 + 2*(k**4-5*k**3+9*k**2-3*k-5)) == 0)
ok('delta_x + delta_c = -2(2k^3-14k^2+36k-33)', sp.expand(e2 + 2*(2*k**3-14*k**2+36*k-33)) == 0)
ok('both brackets have positive coefficients after k=4+m',
   all(c > 0 for c in sp.Poly(sp.expand((k**4-5*k**3+9*k**2-3*k-5).subs(k, k+4)), k).all_coeffs()) and
   all(c > 0 for c in sp.Poly(sp.expand((2*k**3-14*k**2+36*k-33).subs(k, k+4)), k).all_coeffs()))

# Section 6, case q = 1
expr = sp.expand((k-1)*(k-2)*(k**2-7*k+13) - s_k)
ok('q=1: (k-1)(k-2)(k^2-7k+13) - sigma_k = (k-2)(k^3-8k^2+18k-7)', sp.expand(expr - (k-2)*(k**3-8*k**2+18*k-7)) == 0)
vals = [(k**3-8*k**2+18*k-7).subs(k, kk) for kk in range(4, 8)]
say('  k^3-8k^2+18k-7 at k=4..7:', vals, '| after k=4+m:', sp.Poly(sp.expand((k**3-8*k**2+18*k-7).subs(k, k+4)), k).all_coeffs())

