"""Checks for Prop 4.5, Prop 4.6 (Table 1, minimal patterns, Case B), Lemma 5.2, Cor 3.3 and Sec 6."""
import itertools, sympy as sp
from pathlib import Path
_cert = Path(__file__).with_name('certificate_rebuild.py')
exec(_cert.read_text().split("o = (k - 2)")[0])  # reuse the exact type-count model
m = sp.symbols('m')
o = (k - 2) * (k**3 - 6*k**2 + 14*k - 13)
target = (k - 1) * o
qk = k**3 - 8*k**2 + 24*k - 25
sig = 2*(k-2)*(k-3)
zero = {z: 0 for z in Zv.values()}
F = sp.expand(h.subs(zero) - target - qk)
Fm = sp.expand(F.subs(k, 4 + m))
vars7 = [Dv[t] for t in free]
pF = sp.Poly(Fm, *vars7)
print('Prop 4.6 Case A: constant =', sp.factor(pF.coeff_monomial(1)))
neg = []
nq = 0
for mon, c in pF.terms():
    if sum(mon) == 0: continue
    cp = sp.Poly(c, m)
    if any(co < 0 for co in cp.all_coeffs()): neg.append((mon, c))
    if sum(mon) == 1:
        v = vars7[mon.index(1)]
        print('  linear', v, sp.factor(c))
    else:
        nq += 1
        if not (cp.degree() == 1 and cp.all_coeffs()[0] >= 1 and cp.all_coeffs()[1] >= 0):
            print('  quadratic coef not of form am+b:', mon, c)
print('  nonzero quadratic coefficients:', nq, '  coefficients with a negative m-coefficient:', neg)
pats = [('011','101','110'),('011','100','110'),('001','110'),('010','101'),('000','010'),('000','110'),('001','010'),('010','100')]
for pat in pats:
    val = sp.factor(F.subs({Dv[t]: (1 if t in pat else 0) for t in free}))
    print('  pattern', pat, '->', val)

# Case B: types 000,100,011,111 only; j colours of A1\V not in A3. Direct formula with true |I|.
print('Case B:')
n000, n100, n011, j = sp.symbols('n000 n100 n011 j')
def hB(n000_, n100_, n011_, j_, kk):
    # build explicit lists and brute-force the house count
    V = list(range(kk))
    cnt = {'000': n000_, '100': n100_, '011': n011_}
    cnt['111'] = kk - n000_ - n100_ - n011_
    typ = []
    for t, c in cnt.items(): typ += [t]*c
    Rset = {c for c, t in zip(V, typ) if t[0] == '1'}
    A = {c for c, t in zip(V, typ) if t[1] == '1'}
    extra = kk - 1 - len(A)  # colours of A1 outside V
    out = list(range(100, 100 + extra))
    A1s = A | set(out)
    A3s = A | set(out[j_:]) | set(range(200, 200 + j_))
    Rs = Rset | set(range(300, 300 + kk - 1 - len(Rset)))
    return brute_house(A1s, A3s, set(V), set(V), Rs)

def brute_house(A1s, A3s, L2, L4, Rs):
    tot = 0
    for c2 in L2:
        for c4 in L4:
            if c2 == c4: continue
            r = len([y for y in Rs if y != c2 and y != c4])
            bb = sum(1 for a in A1s if a != c2 for c in A3s if c != c4 and c != a)
            tot += r * bb
    return tot

claims = {(1,1,0): 2*k**3-10*k**2+15*k-5, (2,0,0): (k-1)*(4*k**2-16*k+19), (0,2,1): 2*k**3-12*k**2+25*k-19}
for vec, poly in claims.items():
    ok = all(hB(*vec, 1, kk) - (target + qk).subs(k, kk) == poly.subs(k, kk) for kk in range(4, 10))
    print('  ', vec, 'matches claimed value for k=4..9:', ok)

# Prop 4.6 equality example: A1, A3, R = V minus three distinct colours
for kk in range(4, 10):
    V = set(range(kk))
    val = brute_house(V - {0}, V - {1}, V, V, V - {2})
    assert val == (target + qk).subs(k, kk)
print('Prop 4.6 equality example attains target+q_k for k=4..9')

# Prop 4.5
r = sp.symbols('r')
fC = (k-1)**2*(k-2)**2 - 2*(r-1)*(k-2)**2 + (r-1)*(r-2)
fV = (k-1)**2*(k-2)**2 - 2*r*(k-2)**2 + r*(r-1)
fO = k*(k-1)**2*(k-2) - 2*r*(k-1)*(k-2) + r*(r-1)
Dr = sp.expand(target - ((k - r)*fV + (r - 1)*fC))
print('Prop 4.5: D(r) degree in r:', sp.Poly(Dr, r).degree(), ' leading coef:', sp.factor(sp.Poly(Dr, r).LC()))
print('  D\'(k-1) =', sp.factor(sp.diff(Dr, r).subs(r, k-1)), ' D(k-1)-sigma =', sp.expand(Dr.subs(r, k-1) - sig),
      ' D(k-2) =', sp.factor(Dr.subs(r, k-2)))
print('  r=0 value =', sp.factor(target - (k-1)*fV.subs(r, 0)))
print('  fC-fV =', sp.factor(fC - fV), ' fO-fC at r=k-1 =', sp.factor((fO - fC).subs(r, k-1)),
      ' fO-fC at r=0:', sp.factor((fO-fC).subs(r, 0)))
# brute check of f-values: the 4-cycle count with base lists A and shoulder lists V\{y}
def cyc(A, S):
    return sum(1 for a in A for a2 in A if a2 != a for s in S if s != a for s2 in S if s2 != s and s2 != a2)
for kk in range(4, 8):
    for rr in range(0, kk):
        # V = {0..k-1}; A = rr colours of V plus k-1-rr outside
        V = set(range(kk)); A = set(range(rr)) | set(range(50, 50 + kk - 1 - rr))
        for y, f in [(0, fC), (kk-1, fV), (99, fO)]:
            if (y == 0 and rr == 0) or (y == kk-1 and rr == kk): continue
            assert cyc(A, V - {y}) == f.subs({k: kk, r: rr}), (kk, rr, y)
print('  f_C, f_V, f_O match brute force for k=4..7')

# Lemma 5.2 via brute force F(x',y) in configuration Delta
def Fxy(L1, L2_, L3, L4_, x, y):
    tot = 0
    for c1 in L1 - {x}:
        for c3 in L3 - {x}:
            if c3 == c1: continue
            for c2 in L2_ - {y}:
                if c2 == c1: continue
                for c4 in L4_ - {y}:
                    if c4 == c3 or c4 == c2: continue
                    tot += 1
    return tot
dg = -2*(k**4-5*k**3+10*k**2-8*k+1); dc = -2*(2*k**3-13*k**2+31*k-27)
for kk in range(4, 8):
    C = set(range(1, kk)); x, gam, c0_ = 0, 100, 1
    P_ = C | {x}; Vv = C | {gam}; B = {x, gam} | (C - {c0_})
    tgt = (kk - 1) * o.subs(k, kk)
    delta = lambda xp: tgt - sum(Fxy(P_, Vv, P_, Vv, xp, yy) for yy in B - {xp})
    assert delta(x) == sig.subs(k, kk)
    assert delta(gam) == dg.subs(k, kk)
    assert all(delta(c) == dc.subs(k, kk) for c in C - {c0_})
print('Lemma 5.2: delta_x=sigma_k, delta_gamma, delta_c match brute force for k=4..7')
print('  delta_x+delta_gamma =', sp.factor(sig + dg), '; delta_x+delta_c =', sp.factor(sig + dc))
print('  positivity after k=4+m:', sp.Poly(sp.expand(-(sig+dg)/2).subs(k,4+m), m).all_coeffs(), sp.Poly(sp.expand(-(sig+dc)/2).subs(k,4+m), m).all_coeffs())
# Cor 3.3 and Sec 6
dk = (k-1)*(k-2)*(k**2-5*k+7)
print('d_k identities:', sp.expand(dk - ((k-2)**4 + (k-2))) == 0, sp.expand(o - dk - sig) == 0,
      sp.factor(k*dk - (k-1)*o))
print('q=1 case:', sp.factor((k-1)*(k-2)*(k**2-7*k+13) - sig), ' value at k=4:', ((k-1)*(k-2)*(k**2-7*k+13) - sig).subs(k, 4))
ck = k*(k-1)*(k-2)*(k**3-6*k**2+14*k-13)
print('Lemma 2.1 IE:', sp.expand(k*(k-1)*(k-2) - 3*(k-1)*(k-2) + 3*(k-2) - 1 - (k**3-6*k**2+14*k-13)) == 0)
print('coef of |I| bound: -(k^2-k)(k-3) check')
