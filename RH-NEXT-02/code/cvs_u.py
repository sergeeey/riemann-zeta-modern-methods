"""u-space (cutoff-free) CvS Galerkin matrix, mpmath, NOT interval-certified.
Conventions: CvS arXiv:2511.23257 Prop 4.1; pieces as in connes_cvs operator.py.
psi(x) = prime + pole + arch;  q_{m,n} = (psi(m)-psi(n))/(m-n), q_nn = psi'(n).
Usage: python cvs_u.py <char: zeta|chi3|chi4|chi5|chi8> <c> <N> <dps>
"""

import sys

import mpmath as mp

CHARS = {
    # name: (a, q, chi(n) function, has_pole)  a=0 even char, a=1 odd char
    "zeta": (0, 1, lambda n: 1, True),
    "chi3": (1, 3, lambda n: 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1), False),
    "chi4": (1, 4, lambda n: 0 if n % 2 == 0 else (1 if n % 4 == 1 else -1), False),
    "chi5": (0, 5, lambda n: {0: 0, 1: 1, 2: -1, 3: -1, 4: 1}[n % 5], False),
    "chi8": (0, 8, lambda n: {1: 1, 3: -1, 5: -1, 7: 1}.get(n % 8, 0), False),
}


def prime_powers(c):
    out = []
    for p in range(2, c + 1):
        if all(p % d for d in range(2, int(p**0.5) + 1)):
            pk = p
            while pk <= c:
                out.append((pk, p))
                pk *= p
    return sorted(out)


def build(name, c, N):
    a_par, q, chi, has_pole = CHARS[name]
    c_mp = mp.mpf(c)
    L = mp.log(c_mp)
    pi = mp.pi
    a = mp.mpf(1) / 4 + mp.mpf(a_par) / 2  # 1/4 or 3/4
    kappa = -mp.euler - mp.log(pi) + mp.log(q)
    pp = [(n, mp.log(n), chi(n) * mp.log(p) / mp.sqrt(n)) for n, p in prime_powers(int(c))]
    lnL = mp.log(1 - mp.exp(-2 * L))

    def psi_all(n):
        x = mp.mpf(n)
        # prime piece
        ps = -sum(w * mp.sin(2 * pi * x * (1 - lg / L)) for _, lg, w in pp) / pi
        dps_ = -sum(w * 2 * (1 - lg / L) * mp.cos(2 * pi * x * (1 - lg / L)) for _, lg, w in pp)
        # pole piece (zeta only)
        if has_pole:
            ps += (
                mp.quad(lambda y: mp.sin(2 * pi * x * (1 - y / L)) * 2 * mp.cosh(y / 2), [0, L])
                / pi
            )
            dps_ += 2 * mp.quad(
                lambda y: (1 - y / L) * mp.cos(2 * pi * x * (1 - y / L)) * 2 * mp.cosh(y / 2),
                [0, L],
            )
        # archimedean piece, cutoff-free u-space formula
        with mp.workdps(mp.mp.dps + 30):
            I1 = mp.quad(
                lambda y: (
                    -mp.exp(-2 * a * y) * mp.sin(2 * pi * x * (1 - y / L)) / (1 - mp.exp(-2 * y))
                ),
                [0, L],
            )
            ps += (1 / pi) * I1  # (1/2pi)*2*I1 ; phi(0)=sin(2 pi x)=0 for integer x
            I2 = mp.quad(
                lambda y: (
                    (
                        mp.exp(-2 * y)
                        - (1 - y / L) * mp.cos(2 * pi * x * (1 - y / L)) * mp.exp(-2 * a * y)
                    )
                    / (1 - mp.exp(-2 * y))
                ),
                [0, L],
            )
            dps_ += kappa - lnL + 2 * I2
        return ps, dps_

    psi, dpsi = {}, {}
    for n in range(N + 1):
        psi[n], dpsi[n] = psi_all(n)
    for n in range(1, N + 1):
        psi[-n], dpsi[-n] = -psi[n], dpsi[n]
    size = 2 * N + 1
    Q = mp.matrix(size, size)
    for i, m in enumerate(range(-N, N + 1)):
        for j, n in enumerate(range(-N, N + 1)):
            Q[i, j] = dpsi[n] if m == n else (psi[m] - psi[n]) / (m - n)
    return Q, L


def ground_state_zero(Q, L, N, guess):
    E, V = mp.eigsy(Q)
    k = min(range(len(E)), key=lambda i: E[i])
    lam = E[k]
    v = [V[i, k] for i in range(2 * N + 1)]

    def F(t):
        s = mp.mpf(0)
        for i, nn in enumerate(range(-N, N + 1)):
            b = t + 2 * mp.pi * nn / L
            # basis U_n = exp(2 pi i n x / L) lives on [0, L] (CvS Prop 4.1); centring on [-L/2, L/2] gives (-1)^n
            s += (
                ((-1) ** nn)
                * v[i]
                * (L if abs(b) < mp.mpf(10) ** (-mp.mp.dps + 5) else 2 * mp.sin(b * L / 2) / b)
            )
        return s

    # bracket the first sign change of F in [guess-1.5, guess+1.5]
    lo, hi = guess - mp.mpf("1.5"), guess + mp.mpf("1.5")
    ts = [lo + (hi - lo) * i / 300 for i in range(301)]
    vals = [F(t) for t in ts]
    for i in range(300):
        if vals[i] * vals[i + 1] < 0:
            return lam, mp.findroot(F, (ts[i], ts[i + 1]), solver="anderson"), E
    return lam, None, E


if __name__ == "__main__":
    name, c, N, dps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    mp.mp.dps = dps
    known = {"zeta": mp.mpf("14.134725141734693790457251983562"), "chi3": mp.mpf("8.0397371650546")}
    Q, L = build(name, c, N)
    asym = max(abs(Q[i, j] - Q[j, i]) for i in range(Q.rows) for j in range(i))
    guess = known.get(name, mp.mpf(10))
    lam, g1, E = ground_state_zero(Q, L, N, guess)
    print(f"{name} c={c} N={N} dps={dps}  symmetry_err={mp.nstr(asym, 3)}")
    print("  lambda_min =", mp.nstr(lam, 8), " second =", mp.nstr(sorted(E)[1], 8))
    if g1 is not None:
        print("  gamma_1 =", mp.nstr(g1, 20))
        if name in known:
            print("  |err| vs known =", mp.nstr(abs(g1 - known[name]), 5))
    else:
        print("  no sign change found near guess")
