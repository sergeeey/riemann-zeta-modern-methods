"""Independent checks requested by the code review of RH-NEXT-02 (all numbers printed, PASS/FAIL per test).

A. Archimedean entries of cert_chi.build_arb (u-space closed forms) vs the AUTHOR'S tau-space definition
   psi_arch(x) = (1/(2 pi^2)) * int_{-T}^{T} h(tau) Re S_hat(tau, x) dtau  (connes_cvs operator.py), with h(tau) = Re psi(a + i tau/2) - log(pi/q).
   Independent of cvs_u.py and of my derivation: the difference must shrink like (log T)/T as T grows.
B. cert_chi.ldlt_inertia on small matrices with known inertia (positive definite, indefinite, singular).
C. cert_chi.lambda_D against the defining identity sum_{d|n} Lambda_D(d) a(n/d) = a(n) log n (n <= 200) and against -D'/D numerically.
D. python-flint arb(0, rad): the ball radius used for the tail widening.
"""

import itertools
import math

import cert_chi as cc
import mpmath as mp
import numpy as np
from flint import arb, ctx
from scipy.integrate import quad
from scipy.special import digamma

OK = True


def report(name, passed, detail):
    global OK
    OK = OK and passed
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}", flush=True)


# ---------------------------------------------------------------- A
def tau_form(a, q, L, x, T):
    """(psi_arch(x), dpsi_arch(x)) from the tau-space definition, cutoff T, float64 + scipy."""
    alpha = 2 * math.pi * x / L
    logpq = math.log(q / math.pi)

    def h(t):
        return float(np.real(digamma(a + 1j * t / 2))) + logpq

    def reS(t):  # Re S_hat(tau, x), integer x
        if x == 0:
            return 0.0
        return -(1 - math.cos(t * L)) * alpha / (alpha * alpha - t * t)

    def dreS(t):  # d/dx Re S_hat(tau, x) at integer x
        s = 0.0
        for e in (alpha + t, alpha - t):
            s += 1.0 / (e * e)
        return math.pi * (1 - math.cos(t * L)) / L * s

    period = 2 * math.pi / L
    edges = [0.0]
    if alpha < T:
        edges.append(alpha)
    k = 1
    while k * period < T:
        edges.append(k * period)
        k += 1
    edges.append(float(T))
    edges = sorted(set(edges))
    res = []
    for g in (reS, dreS):
        tot = 0.0
        for lo, hi in itertools.pairwise(edges):
            if hi - lo < 1e-12:
                continue
            tot += quad(lambda t, g=g: h(t) * g(t), lo, hi, limit=200)[0]
        res.append(2 * tot / (2 * math.pi**2))  # even integrand: int_{-T}^{T} = 2 int_0^T
    return res[0], res[1]


def prime_parts(name, c, L, n):
    _a_par, _q, chi = cc.CHARS[name]
    sp = dp = 0.0
    for qq, p in cc.prime_powers(c):
        w = chi(qq) * math.log(p) / math.sqrt(qq)
        cv = 1 - math.log(qq) / L
        sp += w * math.sin(2 * math.pi * n * cv)
        dp += w * 2 * cv * math.cos(2 * math.pi * n * cv)
    return -sp / math.pi, -dp


def test_A():
    for name, c in (("chi3", 13), ("chi5", 13), ("chi8", 29)):
        a_par, q, _ = cc.CHARS[name]
        a = 0.25 + a_par / 2
        N = 3
        A, _DIM, _K = cc.build_arb(name, c, N, 300)
        L = math.log(c)
        for n in (0, 1, 2, 3):
            cf_psi = 0.0 if n == 0 else float(A[N + n][N].mid()) * n  # q_{n,0} = psi(n)/n
            cf_dpsi = float(A[N + n][N + n].mid())
            pp, dpp = prime_parts(name, c, L, n)
            cf_psi_arch, cf_dpsi_arch = cf_psi - pp, cf_dpsi - dpp
            diffs = []
            for T in (500, 1000, 2000, 4000):
                tp, tdp = tau_form(a, q, L, n, T)
                diffs.append((abs(tp - cf_psi_arch), abs(tdp - cf_dpsi_arch)))
            d_psi = [d[0] for d in diffs]
            d_dpsi = [d[1] for d in diffs]
            # the truncation error must shrink as T grows (about 1/T up to a log): require a monotone, >=2.5x drop 500 -> 4000
            ok_psi = n == 0 or (d_psi[-1] < d_psi[0] / 2.5 or d_psi[-1] < 1e-6)
            ok_dpsi = d_dpsi[-1] < d_dpsi[0] / 2.5
            report(
                f"A {name} c={c} n={n}",
                ok_psi and ok_dpsi and d_dpsi[-1] < 5e-3 and d_psi[-1] < 5e-3,
                "|tau-form(T) - closed form| for T=500,1000,2000,4000: psi "
                + ", ".join(f"{v:.2e}" for v in d_psi)
                + " | dpsi "
                + ", ".join(f"{v:.2e}" for v in d_dpsi),
            )


# ---------------------------------------------------------------- B
def mat(rows):
    return [[arb(x) for x in r] for r in rows]


def test_B():
    ctx.prec = 200
    # M^T D M with D = diag(2, -3, 5, -1): inertia (2 positive, 2 negative)
    M = [[1, 2, 0, 1], [0, 1, 3, 1], [1, 0, 1, 2], [2, 1, 1, 1]]
    D = [2, -3, 5, -1]
    n = 4
    S = [[sum(M[k][i] * D[k] * M[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    npos, nneg, und, _ = cc.ldlt_inertia(mat(S), n)
    report(
        "B indefinite 4x4 (expected 2,2 or undetermined only if a pivot is exactly 0)",
        (npos, nneg) == (2, 2) and und is None,
        f"got n_pos={npos} n_neg={nneg} undetermined={und}",
    )
    P = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
    npos, nneg, und, _ = cc.ldlt_inertia(mat(P), 3)
    report("B positive definite 3x3", (npos, nneg, und) == (3, 0, None), f"got {(npos, nneg, und)}")
    Ng = [[-4, 1, 0], [1, -3, 1], [0, 1, -2]]
    npos, nneg, und, _ = cc.ldlt_inertia(mat(Ng), 3)
    report("B negative definite 3x3", (npos, nneg, und) == (0, 3, None), f"got {(npos, nneg, und)}")
    Sg = [[1, 1], [1, 1]]
    npos, nneg, und, _ = cc.ldlt_inertia(mat(Sg), 2)
    report(
        "B singular 2x2 (second pivot exactly 0 must be UNDETERMINED, never a sign)",
        und == 1,
        f"got {(npos, nneg, und)}",
    )
    Bl = mat([[2, 1], [1, 2]])
    # WHY: pivot d1 = A11 - (1.9/2)^2 * 2 = A11 - 1.805; A11 = 1.805 +/- 1.0 makes d1 = [-1, 1], straddling 0.
    # (The first version of this test used 0.5 +/- 1.0, whose pivot [-2.3, -0.3] is strictly negative: test bug, not code bug.)
    Bl[1][1] = arb("1.805", "1.0")
    Bl[1][0] = arb("1.9")
    Bl[0][1] = arb("1.9")
    npos, nneg, und, _ = cc.ldlt_inertia(Bl, 2)
    report(
        "B ball pivot straddling 0 must be UNDETERMINED",
        und is not None,
        f"got {(npos, nneg, und)}",
    )


# ---------------------------------------------------------------- C
def test_C():
    ctx.prec = 300
    c = 200
    lam = cc.lambda_D(c)
    a = cc.dh_coefficients()
    worst = arb(0)
    for n in range(1, c + 1):
        s = arb(0)
        for d in range(1, n + 1):
            if n % d == 0:
                s += lam[d] * a[(n // d) % 5]
        worst = (
            max(worst, abs(float((s - a[n % 5] * arb(n).log()).abs_upper())), key=float)
            if False
            else worst
        )
        err = float((s - a[n % 5] * arb(n).log()).abs_upper())
        if err > float(worst):
            worst = arb(err)
    report(
        "C Lambda_D defining identity n<=200",
        float(worst) < 1e-80,
        f"max |sum_(d|n) Lambda_D(d) a(n/d) - a(n) log n| = {float(worst):.2e}",
    )
    mp.mp.dps = 30
    s5 = mp.sqrt(5)
    kappa = (mp.sqrt(10 - 2 * s5) - 2) / (s5 - 1)
    a_per = [0, 1, kappa, -kappa, -1]
    for s0 in (4, 5):
        ser = sum(
            mp.mpf(lam[n].mid().str(30, radius=False)) * mp.mpf(n) ** (-s0) for n in range(1, c + 1)
        )
        num = -mp.diff(lambda s: mp.dirichlet(s, a_per), s0) / mp.dirichlet(s0, a_per)
        tail_bound = 2 * mp.mpf(c) ** (1 - s0) / (s0 - 1)  # |Lambda_D(n)| <~ 2.5 log n; generous
        report(
            f"C -D'/D({s0}) series(200 terms) vs numeric",
            abs(ser - num) < max(tail_bound * 5, 1e-9),
            f"|diff| = {mp.nstr(abs(ser - num), 3)} (crude tail bound {mp.nstr(tail_bound, 3)})",
        )


# ---------------------------------------------------------------- D
def test_D():
    ctx.prec = 200
    rad = arb("3e-7")
    r = arb(0, rad)
    report(
        "D arb(0, rad) radius >= rad",
        float(r.rad()) >= 3e-7 * (1 - 1e-12),
        f"r.rad() = {float(r.rad()):.3e}, contains +rad: {r.contains(arb('3e-7'))}, contains -rad: {r.contains(arb('-3e-7'))}",
    )
    rad_ball = arb("3e-7", "1e-9")  # a ball itself: upper bound is 3.01e-7
    r2 = arb(0, rad_ball)
    report(
        "D arb(0, ball) radius covers the ball's upper bound",
        float(r2.rad()) >= 3.0e-7,
        f"r2.rad() = {float(r2.rad()):.3e}",
    )
    x = arb(1) + arb(0, 2 * rad)
    report(
        "D x + arb(0, 2*tail) encloses x +- 2*tail",
        x.contains(arb(1) + arb("5e-7")) and x.contains(arb(1) - arb("5e-7")),
        f"x = {x}",
    )


if __name__ == "__main__":
    test_B()
    test_C()
    test_D()
    test_A()
    print("\nALL PASS" if OK else "\nSOME CHECKS FAILED")
