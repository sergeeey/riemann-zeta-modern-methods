"""EXACT_COMPUTED (rational arithmetic) exponent slack of the 14 clauses of SizeKRel (src/Formalism/SharpRestriction/ElevenLe.lean:35-50) at the sizes allowed by
SizeN, SizeM, SizeK (same file).  Everything is a log_x exponent of the form a + b*eps with exact Fractions; theta = eps/100 (szTh).

Model (what is computed): m = x^mu, n = x^nu, k = x^kappa with
  mu    in 1/2 - eps/16 +- theta   (SizeM: x^{-theta} sqrt(x*delta1) <= m <= x^{theta} sqrt(x*delta1), delta1 = x^{-eps/8}),
  nu    in 2 + 8 eps +- theta      (SizeN),
  kappa in 9/2 + 10 eps +- theta   (SizeK);
f = 2n, r = k + m - 1 ~ k, rankBudget = n x^{-eps}, L = x^eps, sqrt(x) -> 1/2; constants, logs and C_Gam count as exponent 0 ("x^{o(1)}").
A clause is "binding" if its slack, minimised over all 8 corners of the windows, has leading term 0 + b*eps with small b (< 1 here), "automatic" if the
eps^0 part of the slack is positive.  Scope: ordering of exponents only; the unknown constants C_Gam and the size of log(rdE) are not modelled
(clause 8 is evaluated with log log rdE -> 0; the SizeQD clauses of the same bundle bound log q, log d by x^{eps/5+theta}).
Run: python -I sizekrel_exponents.py
"""

import itertools
import sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
TH = F(1, 100)  # theta / eps


def ex(a, b):
    return (F(a), F(b))


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def scale(c, x):
    return (F(c) * x[0], F(c) * x[1])


ZERO, EPS, THETA, HALF = ex(0, 0), ex(0, 1), ex(0, TH), ex(F(1, 2), 0)
cent = {"mu": ex(F(1, 2), F(-1, 16)), "nu": ex(2, 8), "kappa": ex(F(9, 2), 10)}
win = {"mu": THETA, "nu": THETA, "kappa": THETA}


def clauses(mu, nu, ka):
    L = EPS
    rb = sub(nu, EPS)  # rankBudget exponent
    return [
        (1, "x^th m^5 f L x^eps <= k", add(THETA, scale(5, mu), nu, L, EPS), ka),
        (2, "8 C_Gam m^5 f L <= k", add(scale(5, mu), nu, L), ka),
        (3, "k <= sqrt(x) n rankBudget", ka, add(HALF, nu, rb)),
        (4, "sqrt(k/m) <= rankBudget", scale(F(1, 2), sub(ka, mu)), rb),
        (5, "m^2 L <= k", add(scale(2, mu), L), ka),
        (6, "m sqrt(x) log x <= k", add(mu, HALF), ka),
        (7, "x^th m^6 L <= k log k", add(THETA, scale(6, mu), L), ka),
        (8, "x^th m^3 L log rdE <= k log^2 k", add(THETA, scale(3, mu), L), ka),
        (9, "log f <= sqrt(rS)", ZERO, scale(F(1, 2), mu)),
        (10, "log^2 f <= m^2 L", ZERO, add(scale(2, mu), L)),
        (11, "x^th loglog b <= r f log r", THETA, add(ka, nu)),
        (12, "x^th L <= f log k", add(THETA, L), nu),
        (13, "f <= m^2 n", nu, add(scale(2, mu), nu)),
        (14, "f <= r^2", nu, scale(2, ka)),
    ]


def worst(num):
    """minimum slack (rhs - lhs) over the 8 window corners; returns (a, b) lexicographically minimal (a first, then b)."""
    best = None
    for s_mu, s_nu, s_ka in itertools.product((-1, 1), repeat=3):
        mu = add(cent["mu"], scale(s_mu, win["mu"]))
        nu = add(cent["nu"], scale(s_nu, win["nu"]))
        ka = add(cent["kappa"], scale(s_ka, win["kappa"]))
        _, _, lhs, rhs = clauses(mu, nu, ka)[num - 1]
        sl = sub(rhs, lhs)
        if best is None or sl < best:
            best = sl
    return best


print(f"{'#':>2} {'clause':34} {'slack at centre':>18} {'worst corner':>16}  class")
for i, name, lhs, rhs in clauses(cent["mu"], cent["nu"], cent["kappa"]):
    c = sub(rhs, lhs)
    w = worst(i)
    if w[0] > 0:
        cls = "automatic (eps^0 slack %s)" % w[0]
    elif w[0] == 0 and w[1] > 0:
        cls = "BINDING (slack %s eps, > 0)" % w[1]
    else:
        cls = "VIOLATED"
    print(
        f"{i:>2} {name:34} {str(c[0]) + ' + ' + str(c[1]) + ' eps':>18} {str(w[0]) + ' + ' + str(w[1]) + ' eps':>16}  {cls}"
    )

# derived consequence of the two binding clauses: 1 and 4 force nu >= 4 mu + 4 eps + theta
mu0, nu0, ka0 = cent["mu"], cent["nu"], cent["kappa"]
need = add(scale(4, mu0), scale(4, EPS), THETA)
print(
    "\nclauses 1 and 4 together: k >= x^th m^5 f L x^eps and k <= m n^2 x^{-2eps}  =>  n >= x^{4 mu + 4 eps + th}"
)
print(
    "  required nu >= %s + %s eps; SizeN centre %s + %s eps; margin %s + %s eps"
    % (need[0], need[1], nu0[0], nu0[1], *sub(nu0, need))
)
# clause 3 follows from clause 4 and the upper window of SizeM
mu_hi = add(cent["mu"], THETA)
imp3 = sub(add(HALF, nu0, sub(nu0, EPS)), add(mu_hi, scale(2, nu0), scale(-2, EPS)))
print(
    "clause 3 from clause 4: k <= m n^2 x^{-2eps} <= x^{mu_hi + 2 nu - 2 eps}; needed bound 1/2 + 2 nu - eps; leftover %s + %s eps (>= 0 means implied)"
    % imp3
)
# epsilon -> 0 limit: only clauses with a == 0 can be binding
print(
    "\nAt eps -> 0 (mu, nu, kappa) = (1/2, 2, 9/2): clause 1 slack 0, clause 2 slack 0, clause 4 slack 0, clause 3 slack %s"
    % sub(add(HALF, scale(2, ex(2, 0))), ex(F(9, 2), 0))[0]
)
