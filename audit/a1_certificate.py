"""Independent audit of Proposition 4.7 (unequal shoulders) of
'The triangular prism is enumeratively chromatic-choosable'.

Written from the manuscript, not from checks/certificate_rebuild.py.
1. Build F0 = h_sharp - target symbolically, by an independent derivation of formula (4).
2. Classify the 2,556 quadratic coefficients by sign for every integer k >= 6.
3. Charge nonpositive quadratic terms to the later variable (c*v_i*v_j >= c*k*v_j).
4. Compare l'_v and the residuals with the appendix table parsed from paper/main.tex.
5. Verify the polynomial multipliers (k >= 9) and the fixed-k multipliers (k = 6,7,8) exactly.
All arithmetic is exact (sympy rationals / integer polynomials).
"""
import itertools, re, sys
from fractions import Fraction
import sympy as sp

k = sp.Symbol('k')
ROUTE2 = []  # polynomials that needed real-root isolation
TYPES = [''.join(t) for t in itertools.product('01', repeat=3)]   # (R, A1, A3)
FREE = [t for t in TYPES if t != '111']
inR  = lambda t: int(t[0]); inA1 = lambda t: int(t[1]); inA3 = lambda t: int(t[2])

Dsym = {t: sp.Symbol(f'D_{t}') for t in FREE}
Zsym = {(s, t): sp.Symbol(f'Z_{s}_{t}') for s in TYPES for t in TYPES}
ORDER = [Dsym[t] for t in FREE] + [Zsym[(s, t)] for s in TYPES for t in TYPES]
NAMES = [str(v) for v in ORDER]
b = sp.Add(*Zsym.values())
Dcnt = dict(Dsym); Dcnt['111'] = k - b - sp.Add(*Dsym.values())

# Colour classes of U = L2 u L4. Each class: (count, type, in L2, in L4).
classes = [(Dcnt[t], t, 1, 1) for t in TYPES]
classes += [(Zsym[(s, t)], s, 1, 0) for s in TYPES for t in TYPES]   # P-member (L2 only)
classes += [(Zsym[(s, t)], t, 0, 1) for s in TYPES for t in TYPES]   # Q-member (L4 only)

def w(c2, c4, Ival):
    """Summand of formula (4) for shoulder colours of types c2, c4 (c2 != c4)."""
    roof = k - 1 - inR(c2) - inR(c4)
    bases = (k - 1 - inA1(c2)) * (k - 1 - inA3(c4)) - Ival \
            + inA1(c2) * inA3(c2) + inA1(c4) * inA3(c4)
    return roof * bases

# |I| replaced by |I n U| + (k-1-|A1 n U|)  (Lemma 4.4 with A1)
IU  = sp.Add(*[n * inA1(t) * inA3(t) for n, t, _, _ in classes])
A1U = sp.Add(*[n * inA1(t) for n, t, _, _ in classes])
Ival = IU + (k - 1 - A1U)

# Sum over ordered pairs (c2 in L2, c4 in L4, c2 != c4), done class by class:
# pairs of colours from classes i (as c2) and j (as c4); subtract c2 == c4 within a class.
h = 0
L2cl = [(n, t) for n, t, a, _ in classes if a]
L4cl = [(n, t) for n, t, _, c in classes if c]
h += sp.Add(*[n2 * n4 * w(t2, t4, Ival) for n2, t2 in L2cl for n4, t4 in L4cl])
h -= sp.Add(*[Dcnt[t] * w(t, t, Ival) for t in TYPES])     # same colour on both shoulders
o_k = (k - 2) * (k**3 - 6*k**2 + 14*k - 13)
F0 = sp.expand(h - (k - 1) * o_k)

poly = sp.Poly(F0, *ORDER)
c0 = 0; lin = {i: sp.Integer(0) for i in range(71)}; quad = {}
for mon, coef in poly.terms():
    idx = [i for i, e in enumerate(mon) for _ in range(e)]
    if len(idx) == 0: c0 = sp.expand(coef)
    elif len(idx) == 1: lin[idx[0]] = sp.expand(coef)
    elif len(idx) == 2: quad[tuple(sorted(idx))] = sp.expand(coef)
    else: sys.exit('FAIL: degree > 2')
out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

say('c0 =', sp.factor(c0), '| matches paper -2(k-1)(2k^2-10k+13):',
    sp.expand(c0 + 2*(k-1)*(2*k**2-10*k+13)) == 0)
say('nonzero quadratic coefficients:', len(quad), 'of', 71*72//2)

def nonneg_from(p, lo):
    """Exact proof that integer-coefficient polynomial p(k) >= 0 for all real k >= lo.
    Route 1: shift k = lo + t; all coefficients >= 0 suffices.
    Route 2: p(lo) >= 0, positive leading coefficient, and no real root strictly above lo."""
    p = sp.Poly(sp.expand(p), k)
    if p.is_zero: return True
    t = sp.Symbol('t')
    q = sp.Poly(sp.expand(p.as_expr().subs(k, lo + t)), t)
    if all(c >= 0 for c in q.all_coeffs()):
        return True
    ROUTE2.append(str(p.as_expr()))
    return p.LC() > 0 and p.eval(lo) >= 0 and not any(r > lo for r in sp.real_roots(p))

def sign_class(c):
    """'+' if c(k) >= 0 for every integer k >= 6, '-' if <= 0, else 'mixed'."""
    pos = all(c.subs(k, v) >= 0 for v in range(6, 10)) and nonneg_from(c, 10)
    neg = all(c.subs(k, v) <= 0 for v in range(6, 10)) and nonneg_from(-c, 10)
    return '+' if pos else '-' if neg else 'mixed'

cls = {key: sign_class(c) for key, c in quad.items()}
npos = sum(v == '+' for v in cls.values()); nneg = sum(v == '-' for v in cls.values())
nmix = sum(v == 'mixed' for v in cls.values())
say('sign split for every integer k>=6: nonnegative', npos, '| nonpositive', nneg, '| mixed', nmix)
# A coefficient identically zero would count as both; there are none among the nonzero ones.

# Charging: c*v_i*v_j (i <= j, c <= 0) >= c*k*v_j, valid since 0 <= v_i <= k.
lp = dict(lin)
for (i, j), c in quad.items():
    if cls[(i, j)] == '-':
        lp[j] = sp.expand(lp[j] + c * k)

# Constraint matrix M (rows: b, A1-miss, A3-miss, R-miss), from the definitions in Section 4.
def col(i):
    if i < 7:
        t = FREE[i]; return (0, 1 - inA1(t), 1 - inA3(t), 1 - inR(t))
    s, t = list(Zsym)[i - 7]
    return (1, (1-inA1(s)) + (1-inA1(t)) - 1, (1-inA3(s)) + (1-inA3(t)) - 1, (1-inR(s)) + (1-inR(t)) - 1)
# Independent check of the constraint rows from |U| = k + b and |X| = k-1:
#   #(U \ X) - b = sum over classes of (1 - x) * count - b
for X, pos in (('A1', 1), ('A3', 2), ('R', 0)):
    lhs = sp.expand(sp.Add(*[n * (1 - int(t[pos])) for n, t, _, _ in classes]) - b)
    rhs = sp.expand(sp.Add(*[col(i)[{'A1': 1, 'A3': 2, 'R': 3}[X]] * ORDER[i] for i in range(71)]))
    say(f'constraint row {X}-miss matches appendix column formula:', sp.expand(lhs - rhs) == 0)

# Parse the appendix table from the manuscript.
tex = open(sys.argv[1]).read()
rows = re.findall(r'^\$([DZ])_\{([01,]+)\}\$ & \$(.+?)\$ & \$(.+?)\$ & \$(.+?)\$\\\\', tex, re.M)
paper = {}
for kind, idx, lpe, r10, rv10 in rows:
    name = f'{kind}_' + idx.replace(',', '_')
    P = lambda s: sp.sympify(s.replace('k^{3}', 'k**3').replace('k^{2}', 'k**2').replace(' k', '*k').replace('- *k','-k').replace('+ *k','+k'), locals={'k': k})
    paper[name] = (sp.expand(P(lpe)), sp.expand(P(r10)), sp.Rational(rv10.replace(' ', '')))
say('appendix rows parsed:', len(paper))

y = {'b': (9*k**3 + 9*k**2 + 1867*k - 17997) / sp.Integer(10), 'A1': sp.Integer(0),
     'A3': (17*k**3 - 133*k**2 - 869*k + 10788) / sp.Integer(10),
     'R': (17*k**3 - 116*k**2 - 537*k + 6949) / sp.Integer(10)}
yv = (y['b'], y['A1'], y['A3'], y['R'])
res = {i: sp.expand(lp[i] - sum(col(i)[r] * yv[r] for r in range(4))) for i in range(71)}

mism_l = [NAMES[i] for i in range(71) if sp.expand(lp[i] - paper[NAMES[i]][0]) != 0]
mism_r = [NAMES[i] for i in range(71) if sp.expand(10 * res[i] - paper[NAMES[i]][1]) != 0]
mism_v = [NAMES[i] for i in range(71) if res[i].subs(k, 10) != paper[NAMES[i]][2]]
say("l'_v mismatches vs appendix:", mism_l)
say('10*r_v mismatches vs appendix:', mism_r)
say('r_v(10) mismatches vs appendix:', mism_v)

# Polynomial certificate for k >= 9 (the paper uses it at k = 9 and for k >= 10).
ok_y = all(nonneg_from(10 * yi, 9) for yi in yv)
ok_r = all(nonneg_from(10 * res[i], 9) for i in range(71))
say('multipliers y >= 0 for all real k >= 9:', ok_y)
say('all 71 residuals >= 0 for all real k >= 9:', ok_r)
say('min residual at k=9:', min(res[i].subs(k, 9) for i in range(71)),
    '| at k=10:', min(res[i].subs(k, 10) for i in range(71)))
tot = sp.factor(c0 + sum(yv))
say('c0 + sum y =', tot, '| positive for k >= 1:', nonneg_from(sp.expand(10 * tot) - 1, 1))
roots = [float(r) for i in range(71) for r in sp.real_roots(sp.Poly(10 * res[i], k))]
say('largest real root of any residual: %.4f' % max(roots))

say('polynomials decided by real-root isolation (route 2):', len(ROUTE2))
# Fixed-k certificates of the appendix table.
fixed = {6: (66, 0, 87, 130, 33), 7: (218, 13, 175, 252, 166), 8: (519, 8, 316, 288, 277)}
for kv, (yb, ya1, ya3, yr, tot_paper) in fixed.items():
    r = {i: lp[i].subs(k, kv) - (col(i)[0]*yb + col(i)[1]*ya1 + col(i)[2]*ya3 + col(i)[3]*yr) for i in range(71)}
    zeros = [NAMES[i] for i in range(71) if r[i] == 0]
    say(f'k={kv}: c0={c0.subs(k, kv)}, c0+sum y={c0.subs(k, kv) + yb + ya1 + ya3 + yr} (paper {tot_paper}),',
        f'min residual={min(r.values())}, zero residuals={zeros}')

# Sanity: certificate chain F0 >= c0 + l'.v >= c0 + y.Mv >= c0 + sum y needs v >= 0, Mv >= 1, y >= 0.
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
import pickle; pickle.dump({'F0': F0, 'order': NAMES}, open(sys.argv[3], 'wb'))
