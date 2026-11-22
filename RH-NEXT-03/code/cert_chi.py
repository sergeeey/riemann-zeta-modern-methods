"""Cutoff-free interval certificate of the CvS Galerkin matrix for L(s, chi) (real characters).

Closed forms (derivation in RH-NEXT-02/gate0.md): with a = 1/4 + a_par/2, b = pi n / L, w = 2 b,
c_k = 2k + 2a, z = a + i b:
  psi_arch(n)  = Im psi(z)/(2 pi) - (w/pi) * sum_k exp(-c_k L)/(c_k^2 + w^2)
  dpsi_arch(n) = log(q/pi) + Re psi(z) + Re psi'(z)/(2L) - (2/L) * sum_k Re[exp(-c_k L)/(c_k - i w)^2]
prime part (exact): psi_p(n) = -(1/pi) sum w_q sin(2 pi n (1 - log q/L)),
                    dpsi_p(n) = -sum w_q 2 (1 - log q/L) cos(2 pi n (1 - log q/L)),  w_q = chi(q) log p / sqrt(q)
No pole term for a non-principal character.  q_{m,n} = (psi(m)-psi(n))/(m-n), q_nn = dpsi(n).
Geometric sums are truncated with a rigorous tail bound and the ball is widened by it.
Usage: python cert_chi.py <chi3|chi4|chi5|chi8> <c> <N> <prec_bits> [--compare]
"""

import sys
import time

from flint import acb, arb, ctx

CHARS = {
    "chi3": (1, 3, lambda n: 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1)),
    "chi4": (1, 4, lambda n: 0 if n % 2 == 0 else (1 if n % 4 == 1 else -1)),
    "chi5": (0, 5, lambda n: {0: 0, 1: 1, 2: -1, 3: -1, 4: 1}[n % 5]),
    "chi8": (0, 8, lambda n: {1: 1, 3: -1, 5: -1, 7: 1}.get(n % 8, 0)),
    "dh": (
        1,
        5,
        None,
    ),  # Davenport-Heilbronn: odd type (a=3/4), conductor 5, weights built in build_arb
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


def dh_coefficients():
    """Dirichlet coefficients a(n) mod 5 of the Davenport-Heilbronn function, as Arb balls."""
    s5 = arb(5).sqrt()
    kappa = ((10 - 2 * s5).sqrt() - 2) / (s5 - 1)
    return [arb(0), arb(1), kappa, -kappa, arb(-1)]


def lambda_D(c):
    """Lambda_D(n), n = 1..c, defined by sum_{d|n} Lambda_D(d) a(n/d) = a(n) log n  (a(1) = 1)."""
    a_per = dh_coefficients()
    lam = {}
    # WHY push-style: acc[n] = sum_{d|n, d<n} lam[d] a(n/d) is filled from each d, O(c log c) instead of O(c^2)
    acc = [arb(0)] * (c + 1)
    for n in range(1, c + 1):
        lam[n] = a_per[n % 5] * arb(n).log() - acc[n]
        for m in range(2 * n, c + 1, n):
            acc[m] = acc[m] + lam[n] * a_per[(m // n) % 5]
    return lam


def build_arb(name, c, N, prec, c_arb=None):
    a_par, q, chi = CHARS[name]
    ctx.prec = prec
    # WHY c_arb: RH-NEXT-03 needs REAL c (decimal string) or a parameter INTERVAL (mid_str, rad_str);
    # `c` stays the integer that fixes which prime-power / n weights are present (weights change only at integers).
    if c_arb is None:
        c_ball = arb(c)
    elif isinstance(c_arb, tuple):
        c_ball = arb(c_arb[0], c_arb[1])
    elif isinstance(c_arb, arb):
        c_ball = c_arb
    else:
        c_ball = arb(c_arb)
    if c_arb is not None and not (c_ball.lower() >= c and c_ball.upper() <= c + 1):
        # WHY this guard (review of RH-NEXT-03, finding M3): the weight set is fixed by the integer `c`, and the
        # formulas are valid only while the real parameter lies in [c, c+1]: below c the weight of n = c would have
        # to be 0, not the continued formula; above c+1 the weight of n = c+1 (a prime power or an n for D) may be
        # missing. Both ends are continuous (a new weight starts at 0), so the closed interval is allowed.
        # Without the check a ball that crosses an integer silently certifies the wrong matrix family.
        raise ValueError(
            f"c_arb ball {c_ball.str(20)} is not inside [{c}, {c + 1}]: weight set for c={c} would be wrong"
        )
    L = c_ball.log()
    PI = arb.pi()
    a = arb("0.25") + arb(a_par) / 2
    # number of geometric terms so that exp(-c_K L) < 2^-(prec+30)
    K = int(((prec + 30) * 0.6931472 / float(L) - float(2 * a)) / 2) + 3
    cK = 2 * K + 2 * a
    one_m = 1 - (-2 * L).exp()
    tail = (-cK * L).exp() / (
        cK * cK * one_m
    )  # bounds both sums' tails (|1/z^2|, 1/(c^2+w^2) <= 1/c_K^2)
    widen = lambda x: x + arb(0, 2 * tail)

    if name == "dh":
        # Davenport-Heilbronn: weights Lambda_D(n)/sqrt(n) over ALL n <= c, from -D'/D = sum Lambda_D(n) n^-s
        lam = lambda_D(c)
        pos = [arb(n).log() for n in range(2, c + 1)]
        wts = [lam[n] / arb(n).sqrt() for n in range(2, c + 1)]
    else:
        pdata = prime_powers(c)
        pos = [arb(qq).log() for qq, _ in pdata]
        wts = [arb(chi(qq)) * arb(p).log() / arb(qq).sqrt() for qq, p in pdata]

    psi = {0: arb(0)}
    dpsi = {}
    for n in range(N + 1):
        b = PI * n / L
        w = 2 * b
        z = acb(a, b)
        dig = z.digamma()
        tri = z.polygamma(acb(1))
        S = arb(0)
        R = arb(0)
        for k in range(K):
            ck = 2 * k + 2 * a
            e = (-ck * L).exp()
            S += e / (ck * ck + w * w)
            R += (acb(e) / acb(ck, -w) ** 2).real
        S = widen(S)
        R = widen(R)
        arch = dig.imag / (2 * PI) - (w / PI) * S if n > 0 else arb(0)
        d_arch = (arb(q) / PI).log() + dig.real + tri.real / (2 * L) - (2 / L) * R
        # prime part
        sp = arb(0)
        dp = arb(0)
        for y, wq in zip(pos, wts):
            cc = 1 - y / L
            ang = 2 * PI * n * cc
            sp += wq * ang.sin()
            dp += wq * 2 * cc * ang.cos()
        if n > 0:
            psi[n] = -sp / PI + arch
        dpsi[n] = -dp + d_arch
    for n in range(1, N + 1):
        psi[-n] = -psi[n]
        dpsi[-n] = dpsi[n]
    DIM = 2 * N + 1
    A = [[None] * DIM for _ in range(DIM)]
    for i in range(DIM):
        m = i - N
        for j in range(DIM):
            n = j - N
            A[i][j] = dpsi[n] if m == n else (psi[m] - psi[n]) / (m - n)
    return A, DIM, K


def ldlt_inertia(A, DIM):
    d = [None] * DIM
    Lf = [[arb(0)] * DIM for _ in range(DIM)]
    npos = nneg = 0
    pivots = []
    for i in range(DIM):
        s = A[i][i]
        for k in range(i):
            s = s - Lf[i][k] * Lf[i][k] * d[k]
        d[i] = s
        if s > 0:
            npos += 1
        elif s < 0:
            nneg += 1
        else:
            return npos, nneg, i, pivots
        pivots.append(s)
        for j in range(i + 1, DIM):
            t = A[j][i]
            for k in range(i):
                t = t - Lf[j][k] * Lf[i][k] * d[k]
            Lf[j][i] = t / d[i]
    return npos, nneg, None, pivots


if __name__ == "__main__":
    name, c, N, prec = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    t0 = time.time()
    A, DIM, K = build_arb(name, c, N, prec)
    maxrad = max(float(A[i][j].rad()) for i in range(DIM) for j in range(DIM))
    print(
        f"{name} c={c} N={N} prec={prec} bits  dim={DIM}  K_terms={K}  build={time.time() - t0:.1f}s  max entry radius={maxrad:.3e}"
    )
    if "--compare" in sys.argv:
        import cvs_u as cu
        import mpmath as mp

        mp.mp.dps = 50
        Q, _ = cu.build(name, c, N)
        worst = 0
        for i in range(DIM):
            for j in range(DIM):
                diff = abs(mp.mpf(A[i][j].mid().str(55, radius=False)) - Q[i, j])
                worst = max(worst, float(diff))
        print(
            f"  compare vs independent mpmath quadrature builder: max |entry diff| = {worst:.3e}"
        )
    t1 = time.time()
    npos, nneg, und, piv = ldlt_inertia(A, DIM)
    if und is None:
        print(
            f"  CERTIFIED inertia: n_pos={npos} n_neg={nneg}  (ldlt {time.time() - t1:.1f}s)"
        )
        print(
            "  smallest pivot (ball):", min(piv, key=lambda s: float(s.mid())).str(12)
        )
    else:
        print(f"  UNDETERMINED at pivot {und} (ball contains 0): raise prec")
