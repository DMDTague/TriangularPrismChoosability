"""Independent rebuild of the Prop 4.7 (unequal shoulders) certificate of the prism paper.
Builds F0 = h^sharp - target from formula (4) directly, then checks Table 3, Table 2 and the
quadratic sign split, the constant c0, and the dual residuals."""
import re, itertools
from pathlib import Path
import sympy as sp

k = sp.symbols('k')
types = [''.join(t) for t in itertools.product('01', repeat=3)]  # tau_R tau_A1 tau_A3
free = [t for t in types if t != '111']
Dv = {t: sp.Symbol(f'D_{t}') for t in free}
Zv = {(a, b): sp.Symbol(f'Z_{a}_{b}') for a in types for b in types}
b = sum(Zv.values())
D = dict(Dv); D['111'] = k - b - sum(Dv.values())
P = {t: sum(Zv[(t, u)] for u in types) for t in types}
Q = {t: sum(Zv[(u, t)] for u in types) for t in types}
n2 = {t: D[t] + P[t] for t in types}
n4 = {t: D[t] + Q[t] for t in types}
R = lambda t: int(t[0]); A1 = lambda t: int(t[1]); A3 = lambda t: int(t[2])
I = lambda t: A1(t) * A3(t)

def total(f):  # sum over colours of U of indicator f(type)
    return sum(f(t) * (D[t] + P[t] + Q[t]) for t in types)

Ival = total(I) + (k - 1 - total(A1))
Dsize = k - b
RL2 = sum(R(t) * n2[t] for t in types); RL4 = sum(R(t) * n4[t] for t in types)
RD = sum(R(t) * D[t] for t in types)
M1 = (k - 1) * (k**2 - Dsize) - k * RL2 - k * RL4 + 2 * RD  # sum over pairs c2!=c4 of (k-1-R-R')

def G0(s, t):
    return (k - 1 - R(s) - R(t)) * ((k - 1 - A1(s)) * (k - 1 - A3(t)) + I(s) + I(t))

h = sum(n2[s] * n4[t] * G0(s, t) for s in types for t in types) \
    - sum(D[t] * G0(t, t) for t in types) - Ival * M1
o = (k - 2) * (k**3 - 6*k**2 + 14*k - 13)
F0 = sp.expand(h - (k - 1) * o)
order = [Dv[t] for t in free] + [Zv[(a, c)] for a in types for c in types]
names = [str(v) for v in order]
poly = sp.Poly(F0, *order)
quad, lin, c0 = {}, {v: sp.Integer(0) for v in order}, sp.Integer(0)
for mon, coef in poly.terms():
    deg = sum(mon)
    idx = [i for i, e in enumerate(mon) for _ in range(e)]
    coef = sp.expand(coef)
    if deg == 0: c0 = coef
    elif deg == 1: lin[order[idx[0]]] = coef
    elif deg == 2: quad[tuple(idx)] = coef
    else: raise SystemExit('degree > 2 term!')
print('c0 =', sp.factor(c0), '  paper: -2(k-1)(2k^2-10k+13) ->', sp.expand(c0 + 2*(k-1)*(2*k**2-10*k+13)) == 0)
print('number of quadratic monomials with nonzero coef:', len(quad), ' of possible', 71*72//2)

def sign_on(p, lo):
    # sign of polynomial p on integers >= lo (check 6..9 exactly, then real roots on [10,inf))
    vals = [p.subs(k, v) for v in range(lo, 10)]
    pp = sp.Poly(p, k)
    if pp.is_zero: return 0
    roots = [r for r in sp.real_roots(pp) if r >= 10]
    lc = pp.LC()
    s_inf = 1 if lc > 0 else -1
    return vals, roots, s_inf

nonneg, nonpos, mixed = [], [], []
for key, c in quad.items():
    vals, roots, s_inf = sign_on(c, 6)
    if all(v >= 0 for v in vals) and s_inf > 0 and not roots: nonneg.append(key)
    elif all(v <= 0 for v in vals) and s_inf < 0 and not roots: nonpos.append(key)
    else: mixed.append((key, c))
print('nonneg:', len(nonneg), ' nonpos:', len(nonpos), ' mixed:', len(mixed))
for key, c in mixed[:10]: print('  mixed', [names[i] for i in key], c)

# charging: c*v_i*v_j (i<=j), c<=0, charged c*k to v_j
lp = dict(lin)
for key in nonpos:
    i, j = key
    lp[order[max(i, j)]] += quad[key] * k
lp = {v: sp.expand(e) for v, e in lp.items()}

# parse paper table 3
tex = (Path(__file__).resolve().parents[1] / 'paper' / 'main.tex').read_text()
rows = re.findall(r'^\$([DZ])_\{([01]{3})(?:,([01]{3}))?\}\$ & \$(.*?)\$ & \$(.*?)\$ & \$(.*?)\$\\\\', tex, re.M)
assert len(rows) == 71, len(rows)
tab = {}
for kind, t1, t2, l, r10, v10 in rows:
    name = f'D_{t1}' if kind == 'D' else f'Z_{t1}_{t2}'
    conv = lambda s: sp.sympify(s.replace(' ', '').replace('k^{', 'k**(').replace('}', ')').replace('^', '**').replace('k', '*k').replace('+*k', '+k').replace('-*k', '-k').lstrip('*') if False else s)
    def parse(s):
        s = s.replace(' ', '')
        s = re.sub(r'k\^\{(\d+)\}', r'k**\1', s)
        s = re.sub(r'(\d)k', r'\1*k', s)
        return sp.sympify(s, locals={'k': k})
    tab[name] = (parse(l), parse(r10), sp.Rational(v10.replace(' ', '')))

bad = [n for n in names if sp.expand(lp[sp.Symbol(n)] - tab[n][0]) != 0]
print('ell_prime mismatches vs Table 3:', bad)

# M columns and y
def col(name):
    if name.startswith('D_'):
        t = name[2:]
        return [0, 1 - A1(t), 1 - A3(t), 1 - R(t)]
    _, t, u = name.split('_')
    return [1, (1-A1(t)) + (1-A1(u)) - 1, (1-A3(t)) + (1-A3(u)) - 1, (1-R(t)) + (1-R(u)) - 1]
ypoly = [sp.Rational(1, 10)*(9*k**3+9*k**2+1867*k-17997), 0,
         sp.Rational(1, 10)*(17*k**3-133*k**2-869*k+10788), sp.Rational(1, 10)*(17*k**3-116*k**2-537*k+6949)]
print('c0+sum y =', sp.factor(c0 + sum(ypoly)))
badr, minroot, minr10 = [], 0, None
for n in names:
    r = sp.expand(lp[sp.Symbol(n)] - sum(a*y for a, y in zip(col(n), ypoly)))
    if sp.expand(10*r - tab[n][1]) != 0 or r.subs(k, 10) != tab[n][2]: badr.append(n)
    rr = [x for x in sp.real_roots(sp.Poly(r, k))]
    if rr: minroot = max(minroot, max(float(x) for x in rr))
    v = r.subs(k, 10); minr10 = v if minr10 is None else min(minr10, v)
    assert sp.Poly(r, k).LC() > 0
print('residual mismatches:', badr, ' largest real root of any residual:', round(minroot, 3), ' min r(10):', minr10)
for yy in ypoly[:1] + ypoly[2:]:
    rr = [float(x) for x in sp.real_roots(sp.Poly(yy, k))]
    print('  y roots', [round(x, 3) for x in rr])

# fixed-k certificates (Table 2)
fixed = {6: ([66, 0, 87, 130], 33), 7: ([218, 13, 175, 252], 166), 8: ([519, 8, 316, 288], 277),
         9: ([sp.Rational(3048, 5), 0, sp.Rational(4587, 10), sp.Rational(5113, 10)], sp.Rational(1098, 5))}
for kk, (y, s) in fixed.items():
    res = {n: lp[sp.Symbol(n)].subs(k, kk) - sum(a*yy for a, yy in zip(col(n), y)) for n in names}
    zeros = [n for n, v in res.items() if v == 0]
    print(f'k={kk}: c0={c0.subs(k,kk)}, c0+sum y={c0.subs(k,kk)+sum(y)} (paper {s}), min residual={min(res.values())}, zeros={zeros}')
