"""Variant B2: one (fundamental discriminant D, c, N) cell per call; prints one JSON line.
Character = Kronecker symbol (D/n), conductor q = |D|, odd iff D < 0.
Usage: python parity2.py <D> <c> <N>      Self-test of the characters: python parity2.py selftest
"""

import json
import sys

import cert_chi as cc
import mpmath as mp
from sympy.ntheory.residue_ntheory import jacobi_symbol

ALL_D = [-3, -4, -7, -8, -11, -15, -19, -20, -23, -24, 5, 8, 12, 13, 17, 21, 24, 28, 29, 33]


def kronecker_symbol(a, n):
    """Kronecker symbol (a/n) for n >= 1 (Jacobi symbol for odd n, plus the rule for factors of 2)."""
    if n == 0:
        # WHY: (a/0) = 1 only for a = +-1; without this the loop below never ends for n = 0 (bug found when period(D) hung)
        return 1 if abs(a) == 1 else 0
    result = 1
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            result = -result
    if n == 1:
        return result
    return result * jacobi_symbol(a % n, n)


def chi_of(D):
    return lambda n: int(kronecker_symbol(D, n))


def register(D):
    name = f"D{D}"
    cc.CHARS[name] = (1 if D < 0 else 0, abs(D), chi_of(D))
    return name


def period(D):
    return [int(kronecker_symbol(D, n)) for n in range(abs(D))]


def selftest():
    ok = True
    for D in ALL_D:
        q = abs(D)
        chi = chi_of(D)
        periodic = all(chi(n) == chi(n + q) for n in range(3 * q)) and chi(0) == 0 and len(period(D)) == q
        parity = chi(q - 1) == (-1 if D < 0 else 1) if q > 2 else True
        multiplicative = all(
            chi(m * n) == chi(m) * chi(n) for m in range(1, 12) for n in range(1, 12)
        )
        print(
            f"D={D:>3} q={q:>2} periodic={periodic} chi(-1)=sign(D): {parity} completely multiplicative={multiplicative}"
        )
        ok = ok and periodic and parity and multiplicative
    # match the character tables used in variant B
    table = {-3: "chi3", -4: "chi4", 5: "chi5", 8: "chi8", -8: "chim8"}
    for D, nm in table.items():
        same = all(chi_of(D)(n) == cc.CHARS[nm][2](n) for n in range(1, 100))
        print(f"D={D} equals the variant-B table {nm}: {same}")
        ok = ok and same
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


def ref_zero(D):
    """First zero of L(s, chi_D) on the critical line: first sign change of the Hardy-type function (mpmath.dirichlet, independent)."""
    mp.mp.dps = 30
    per = period(D)
    q = abs(D)
    a = 1 if D < 0 else 0

    def Z(t):
        s = mp.mpc(0.5, t)
        theta = mp.im(mp.loggamma((s + a) / 2)) - (t / 2) * mp.log(mp.pi / q)
        return mp.re(mp.exp(1j * theta) * mp.dirichlet(s, per))

    ts = [mp.mpf(i) / 50 for i in range(5, 1500)]
    prev_t, prev = ts[0], Z(ts[0])
    for t in ts[1:]:
        cur = Z(t)
        if prev * cur < 0:
            return mp.findroot(Z, (prev_t, t), solver="anderson")
        prev_t, prev = t, cur
    raise RuntimeError("no zero found below t = 30")


def mid_matrix(A, dps):
    n = len(A)
    M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = mp.mpf(A[i][j].mid().str(dps + 20, radius=False))
    return M


def first_zero(v, L, N, guess):
    def F(t):
        s = mp.mpf(0)
        for i, nn in enumerate(range(-N, N + 1)):
            b = t + 2 * mp.pi * nn / L
            s += (
                ((-1) ** nn)
                * v[i]
                * (L if abs(b) < mp.mpf(10) ** -60 else 2 * mp.sin(b * L / 2) / b)
            )
        return s

    lo, hi = guess - mp.mpf("1.5"), guess + mp.mpf("1.5")
    ts = [lo + (hi - lo) * i / 300 for i in range(301)]
    vals = [F(t) for t in ts]
    for i in range(300):
        if vals[i] * vals[i + 1] < 0:
            return mp.findroot(F, (ts[i], ts[i + 1]), solver="anderson")
    return None


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    D, c, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    # WHY optional dps/prec: for N >= 48 lambda_min can fall below 1e-100, so the eigen-solver needs more digits than 100
    DPS = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    PREC = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
    name = register(D)
    a_par, q, _ = cc.CHARS[name]
    while True:
        A, DIM, _ = cc.build_arb(name, c, N, PREC)
        npos, nneg, und, _ = cc.ldlt_inertia(A, DIM)
        if und is None or PREC >= 16000:
            break
        PREC *= 2  # undetermined pivot: certify again with twice the bits (the certificate itself is never relaxed)
    mp.mp.dps = DPS
    E, V = mp.eigsy(mid_matrix(A, DPS))
    order = sorted(range(DIM), key=lambda i: E[i])
    lam = [E[i] for i in order]
    ref = ref_zero(D)
    mp.mp.dps = DPS
    v = [V[i, order[0]] for i in range(DIM)]
    g1 = first_zero(v, mp.log(c), N, ref)
    err = abs(g1 - ref) if g1 is not None else None
    print(
        json.dumps(
            {
                "D": D,
                "parity": "odd" if a_par else "even",
                "q": q,
                "c": c,
                "N": N,
                "dps": DPS,
                "prec_bits": PREC,
                "n_pos": npos,
                "n_neg": nneg,
                "undetermined": und,
                "lambda_min": mp.nstr(lam[0], 8),
                "lambda_2": mp.nstr(lam[1], 8),
                "cond": mp.nstr(lam[-1] / lam[0], 6),
                "gamma1_ref": mp.nstr(ref, 15),
                "gamma1": mp.nstr(g1, 15) if g1 is not None else None,
                "log10_err": mp.nstr(mp.log10(err), 5) if err is not None and err > 0 else None,
            }
        ),
        flush=True,
    )
