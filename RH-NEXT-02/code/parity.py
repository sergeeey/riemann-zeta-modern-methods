"""Variant B: parity of the character.  One (character, c, N) cell per call; prints one JSON line.
Usage: python parity.py <chi3|chi4|chim8|chi5|chi8> <c> <N>
Quantities: certified inertia (interval LDL^T), lambda_min, lambda_2, cond = lambda_max/lambda_min (mpmath, mid matrix),
gamma_1 from the first zero of the Fourier transform of the ground state, error against an independent mpmath.dirichlet zero.
"""

import json
import sys

import cert_chi as cc
import mpmath as mp

PERIODS = {
    "chi3": [0, 1, -1],
    "chi4": [0, 1, 0, -1],
    "chi5": [0, 1, -1, -1, 1],
    "chi8": [0, 1, 0, -1, 0, -1, 0, 1],
    "chim8": [0, 1, 0, 1, 0, -1, 0, -1],
}


def ref_zero(name):
    """First zero on the critical line from mpmath.dirichlet (independent of the matrix code)."""
    mp.mp.dps = 30
    per = PERIODS[name]
    ts = [mp.mpf(i) / 50 for i in range(20, 600)]
    vals = [abs(mp.dirichlet(mp.mpc(0.5, t), per)) for t in ts]
    cand = [
        ts[i]
        for i in range(1, len(ts) - 1)
        if vals[i] < vals[i - 1] and vals[i] < vals[i + 1] and vals[i] < 0.3
    ]
    z = mp.findroot(lambda s: mp.dirichlet(s, per), mp.mpc(0.5, cand[0]))
    return mp.im(z)


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
    name, c, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    a_par, q, _ = cc.CHARS[name]
    A, DIM, _ = cc.build_arb(name, c, N, 2000)
    npos, nneg, und, _ = cc.ldlt_inertia(A, DIM)
    mp.mp.dps = 100
    E, V = mp.eigsy(mid_matrix(A, 100))
    order = sorted(range(DIM), key=lambda i: E[i])
    lam = [E[i] for i in order]
    ref = ref_zero(name)
    mp.mp.dps = 100
    k = order[0]
    v = [V[i, k] for i in range(DIM)]
    g1 = first_zero(v, mp.log(c), N, ref)
    err = abs(g1 - ref) if g1 is not None else None
    print(
        json.dumps(
            {
                "char": name,
                "parity": "odd" if a_par else "even",
                "q": q,
                "c": c,
                "N": N,
                "n_pos": npos,
                "n_neg": nneg,
                "undetermined": und,
                "lambda_min": mp.nstr(lam[0], 6),
                "lambda_2": mp.nstr(lam[1], 6),
                "cond": mp.nstr(lam[-1] / lam[0], 6),
                "gamma1_ref": mp.nstr(ref, 15),
                "gamma1": mp.nstr(g1, 15) if g1 is not None else None,
                "log10_err": mp.nstr(mp.log10(err), 5) if err is not None and err > 0 else None,
            }
        ),
        flush=True,
    )
