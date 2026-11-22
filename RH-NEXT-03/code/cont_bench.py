"""RH-NEXT-03 experiments: does the finite-matrix path Q(c) admit cheap incremental certification?

A. threshold: continuity of Q(L) and the derivative jump across L = log q (claim of Groskin, matrix von Mangoldt measure paper).
B. numerical rank (singular value decay) of a finite difference Q(c2) - Q(c1) between two real cutoffs with the same weights.
C. eigenvalue sensitivity: lambda_min, d ln lambda_min / dL and the Weyl step lambda_min / ||dQ/dc||.
D. parameter-interval certificate: widest c-interval [c, c+w] whose inertia one interval LDL^T certifies (vs a point certificate).
E. benchmark on a real task: locate the first positivity failure c*(N) of the Davenport-Heilbronn matrix between c=30 and c=31 (N=60):
   baseline = certified bisection (a certificate at every step) vs hybrid = non-rigorous secant on the last LDL pivot + two certificates.
Usage: python cont_bench.py <A|B|C|D|E>
"""

import sys
import time

import cert_chi as cc
import mpmath as mp
from flint import arb, ctx


def point(name, cint, N, prec, cstr):
    A, DIM, _ = cc.build_arb(name, cint, N, prec, c_arb=cstr)
    return A, DIM


def mid_mp(A, dps=60):
    n = len(A)
    M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = mp.mpf(A[i][j].mid().str(dps + 10, radius=False))
    return M


def exp_A():
    prec = 300
    N = 4
    ctx.prec = prec
    h = arb("1e-6")
    c0 = arb(13)

    def Qm(cint, cval):
        A, _ = point("chi3", cint, N, prec, cval.str(60, radius=False))
        return A

    # continuity at c = 13: weights up to 12 versus weights up to 13 (the new weight has value 0 at L = log 13)
    A12 = point("chi3", 12, N, prec, "13")[0]
    A13 = point("chi3", 13, N, prec, "13")[0]
    d = max(
        float(abs(A12[i][j] - A13[i][j]).upper())
        for i in range(2 * N + 1)
        for j in range(2 * N + 1)
    )
    print(f"A. continuity at c=13: max |Q(c=13, weights<=12) - Q(c=13, weights<=13)| = {d:.3e}")

    # one-sided derivatives wrt L
    def dQ(cint, ca, cb):
        Aa = Qm(cint, ca)
        Ab = Qm(cint, cb)
        dL = (cb / ca).log()
        return [[(Ab[i][j] - Aa[i][j]) / dL for j in range(2 * N + 1)] for i in range(2 * N + 1)]

    left = dQ(12, c0 - 2 * h, c0 - h)
    right = dQ(13, c0 + h, c0 + 2 * h)
    jump = [
        [float((right[i][j] - left[i][j]).mid()) for j in range(2 * N + 1)]
        for i in range(2 * N + 1)
    ]
    exp_val = (
        -2 / 13**0.5
    )  # -2 chi(13) Lambda(13)/(sqrt(13) log 13), chi_3(13)=+1, Lambda(13)=log 13
    dev = max(abs(jump[i][j] - exp_val) for i in range(2 * N + 1) for j in range(2 * N + 1))
    print(
        f"A. derivative jump (right - left, wrt L=log c) in every entry: expected {exp_val:.8f}; max deviation over all {(2 * N + 1) ** 2} entries = {dev:.2e} (h=1e-6, O(h) accuracy)"
    )


def exp_B():
    prec, N = 400, 16
    A1, _DIM = point("chi3", 23, N, prec, "23")
    A2, _ = point("chi3", 23, N, prec, "23.5")
    mp.mp.dps = 60
    D = mid_mp(A2) - mid_mp(A1)
    sv = mp.svd_r(D, compute_uv=False)
    sv = sorted([float(x) for x in sv], reverse=True)
    import math

    print("B. chi3 N=16: singular values of Q(23.5) - Q(23.0) (same weights), log10(s_k / s_1):")
    print("   k:    " + " ".join(f"{k:6d}" for k in (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 33)))
    print(
        "   log10:"
        + " ".join(
            f"{math.log10(sv[k - 1] / sv[0]):6.1f}"
            for k in (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 33)
        )
    )
    ranks = {tol: sum(1 for s in sv if s / sv[0] > tol) for tol in (1e-3, 1e-6, 1e-10, 1e-14)}
    print(f"   numerical rank at relative tolerance {ranks}")
    q1 = mid_mp(A1)
    sq = sorted([float(x) for x in mp.svd_r(q1, compute_uv=False)], reverse=True)
    print(
        f"   for comparison singular values of Q(23) itself: log10(s_33/s_1) = {math.log10(sq[-1] / sq[0]):.1f}, rank@1e-10: {sum(1 for s in sq if s / sq[0] > 1e-10)}"
    )


def exp_C():
    prec, N = 600, 16
    mp.mp.dps = 90
    out = []
    for cs in ("23", "23.001"):
        A, _ = point("chi3", 23, N, prec, cs)
        E, _V = mp.eigsy(mid_mp(A, 90))
        out.append(min(E))
    lam0, lam1 = out
    dL = mp.log(mp.mpf("23.001") / 23)
    print(
        f"C. chi3 c=23 N=16: lambda_min = {mp.nstr(lam0, 8)}; at c=23.001: {mp.nstr(lam1, 8)}; d ln(lambda_min)/dL = {mp.nstr((mp.log(lam1) - mp.log(lam0)) / dL, 6)}"
    )
    A1, _ = point("chi3", 23, N, prec, "23")
    A2, _ = point("chi3", 23, N, prec, "23.001")
    mp.mp.dps = 60
    D = mid_mp(A2) - mid_mp(A1)
    s1 = float(mp.svd_r(D, compute_uv=False)[0]) / 0.001
    print(
        f"C. ||dQ/dc||_2 ~ {s1:.3e};  Weyl step lambda_min/||dQ/dc|| ~ {float(lam0) / s1:.2e} in c (absolute perturbation bound; useless when lambda_min is tiny)"
    )


def certify_interval(name, cint, N, prec, mid, rad):
    A, DIM, _ = cc.build_arb(name, cint, N, prec, c_arb=(mid, rad))
    npos, nneg, und, _ = cc.ldlt_inertia(A, DIM)
    return npos, nneg, und, DIM


def exp_D():
    N = 16
    for prec in (1500, 3000):
        t0 = time.time()
        A, DIM = point("chi3", 23, N, prec, "23")
        npos, nneg, und, _ = cc.ldlt_inertia(A, DIM)
        t_pt = time.time() - t0
        print(
            f"D. prec={prec}: point certificate at c=23: n_pos={npos} n_neg={nneg} und={und}  time={t_pt:.2f}s"
        )
        best = None
        # WHY the scan goes to 10^-300: the first version stopped at 10^-60 and wrongly suggested "no width certifies";
        # interval LDL^T amplifies the input radius by about cond(Q)^2 ~ 1e52 for this matrix, so the threshold is much smaller.
        for k in list(range(1, 60, 3)) + list(range(60, 301, 5)):
            w = arb(10) ** (-k)
            mid = (arb(23) + w / 2).str(40 + k, radius=False)
            rad = (w / 2).str(10, radius=False)
            t0 = time.time()
            npos, nneg, und, DIM = certify_interval("chi3", 23, N, prec, mid, rad)
            ok = und is None and nneg == 0
            if ok:
                best = (k, time.time() - t0)
                break
        if best:
            print(
                f"D. prec={prec}: widest certified c-interval [23, 23+10^-{best[0]}] (first width in the scan 1e-1,1e-2,.. that certifies), time={best[1]:.2f}s"
            )
        else:
            print(f"D. prec={prec}: no interval width down to 1e-60 certified")


def cert_pt(name, cint, N, prec, cs):
    A, DIM = point(name, cint, N, prec, cs)
    npos, nneg, und, piv = cc.ldlt_inertia(A, DIM)
    return npos, nneg, und, piv


def exp_E():
    N = 60
    name = "dh"
    time.time()
    n_cert = 0

    def dec(x):
        return mp.nstr(x, 25)

    # baseline: certified bisection on c in (30, 31); weights fixed to n <= 30 (cint=30); sign of the inertia certified at every step
    lo, hi = mp.mpf(30), mp.mpf(31)
    mp.mp.dps = 40
    t0 = time.time()
    steps = 0
    while hi - lo > mp.mpf("1e-9"):
        m = (lo + hi) / 2
        for prec in (700, 1500, 3000, 6000):
            npos, nneg, und, _ = cert_pt(name, 30, N, prec, dec(m))
            n_cert += 1
            if und is None:
                break
        steps += 1
        if und is not None:
            print(
                f"E. baseline: UNDETERMINED at c={dec(m)} even with {prec} bits; stopping, bracket [{dec(lo)}, {dec(hi)}]"
            )
            break
        if nneg == 0:
            lo = m
        else:
            hi = m
    t_base = time.time() - t0
    print(
        f"E. baseline certified bisection: bracket [{dec(lo)}, {dec(hi)}] width {mp.nstr(hi - lo, 3)}, {steps} steps, {n_cert} certificates, {t_base:.1f}s"
    )
    # hybrid: bracketed false position (Illinois) on the LAST LDL^T pivot (mid value; a non-rigorous tracker), then 2 certificates
    # WHY bracketed: the first version used a plain secant without a bracket and diverged to NaN (implementation bug, not a
    # property of the method); the bracket [30, 31] is the same initial information the baseline bisection receives.
    t0 = time.time()
    n_eval = 0

    def f(c):
        nonlocal n_eval
        n_eval += 1
        _, _, _und, piv = cert_pt(name, 30, N, 700, dec(c))
        return mp.mpf(piv[-1].mid().str(40, radius=False))

    lo, hi = mp.mpf(30), mp.mpf(31)
    flo, fhi = f(lo), f(hi)
    assert flo > 0 > fhi, (flo, fhi)
    side = 0
    it = 0
    for it in range(1, 80):
        c = (lo * fhi - hi * flo) / (fhi - flo)
        fc = f(c)
        if fc < 0:
            hi, fhi = c, fc
            if side == -1:
                flo /= 2
            side = -1
        else:
            lo, flo = c, fc
            if side == 1:
                fhi /= 2
            side = 1
        if hi - lo < mp.mpf("1e-11"):
            break
    cstar = (lo + hi) / 2
    d = mp.mpf("5e-10")
    ok = []
    for cs in (cstar - d, cstar + d):
        for prec in (1500, 3000, 6000):
            npos, nneg, und, _ = cert_pt(name, 30, N, prec, dec(cs))
            if und is None:
                break
        ok.append((dec(cs), npos, nneg, und))
    t_hyb = time.time() - t0
    print(f"E. hybrid: {it} Illinois iterations ({n_eval} pivot evaluations), c* = {dec(cstar)}; certificates at c*-5e-10 and c*+5e-10: {ok}; total {t_hyb:.1f}s")
    print(f"E. cost ratio baseline/hybrid = {t_base / t_hyb:.2f}; certificates: baseline {n_cert}, hybrid 2 (+ {n_eval} non-certified factorizations)")
    print(f"E. consistency: hybrid c* inside the baseline bracket: {lo <= (lo + hi) / 2 and mp.mpf('30.98938083928078413') <= cstar + d and cstar - d <= mp.mpf('30.98938084021210670')}")


if __name__ == "__main__":
    {"A": exp_A, "B": exp_B, "C": exp_C, "D": exp_D, "E": exp_E}[sys.argv[1]]()
