"""EXACT_COMPUTED reproduction of identity (II.8) and the numbers of (II.24) of zeta-paper.pdf (p. 29 and p. 35) for q = 3, d = 23.

R_{q,d}(y) = S_{q,d}(y) - y log y + (1 + gamma + c_{chi_q} - c_{chi_d} - c_eta) y  =  G(y) + G_{chi_q}(y) - G_{chi_d}(y) - G_eta(y)
with S_{q,d}(y) = sum_{r<=y} Lambda(r)(1+chi_q(r))(1-chi_d(r))(y/r - 1), G_chi(y) = sum_{r<=y} Lambda(r) chi(r) (y/r - 1) + c_chi y,
c_chi = L'/L(1, chi) (c for the trivial character is replaced by the pair (G: -y log y + (1+gamma) y)).

Independent implementation: own sieve, own Legendre/Kronecker via Euler's criterion, mpmath L-function values (Hurwitz zeta).
Model: all prime powers up to y; chi_3, chi_23 real primitive characters; eta = chi_3 chi_23 (real, conductor 69).
Scope: y = 1000 and y = 10^6 (the two rows of (II.24)).  Not a proof of the identity; the direct and the combined evaluations agree to about 1e-53 (60-digit arithmetic), which checks the algebra for these two values of y only.
Run: python -I check_II8_identity.py
"""

import sys

import mpmath as mp

mp.mp.dps = 60
sys.stdout.reconfigure(encoding="utf-8")


def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i, v in enumerate(sieve) if v]


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


chi3 = lambda n: 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1)  # noqa: E731
chi23 = lambda n: legendre(n, 23)  # noqa: E731
eta = lambda n: chi3(n) * chi23(n)  # noqa: E731


def c_chi(chi, q):
    """L'/L(1, chi) via Hurwitz zeta: L(s, chi) = q^-s sum chi(a) zeta(s, a/q)."""
    vals = [chi(a) for a in range(q)]

    def L(s):
        return sum(vals[a] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q) if vals[a]) * mp.mpf(
            q
        ) ** (-s)

    # WHY symmetric differences: each Hurwitz term has a pole at s = 1 that cancels only in the sum, so L(1) and L'(1) are limits;
    # central differences with h = 1e-12 at 60 digits give errors ~h^2 = 1e-24 (checked against the paper's 6-digit values).
    h = mp.mpf(10) ** -12
    return ((L(1 + h) - L(1 - h)) / (2 * h)) / ((L(1 + h) + L(1 - h)) / 2)


c3, c23, c69 = c_chi(chi3, 3), c_chi(chi23, 23), c_chi(eta, 69)
print(
    "c_chi3, c_chi23, c_eta =",
    mp.nstr(c3, 8),
    mp.nstr(c23, 8),
    mp.nstr(c69, 8),
    "(paper: 0.368282, -0.422121, 0.056523)",
)

for Y in (1000, 10**6):
    pw = []  # (r, Lambda(r))
    for p in primes_upto(Y):
        r = p
        lp = mp.log(p)
        while r <= Y:
            pw.append((r, lp))
            r *= p
    y = mp.mpf(Y)
    S1 = sum(l * (y / r - 1) for r, l in pw)
    G = S1 - y * mp.log(y) + (1 + mp.euler) * y

    def Gchi(chi, c):
        return sum(l * chi(r) * (y / r - 1) for r, l in pw) + c * y

    G3, G23, G69 = Gchi(chi3, c3), Gchi(chi23, c23), Gchi(eta, c69)
    Sqd = sum(l * (1 + chi3(r)) * (1 - chi23(r)) * (y / r - 1) for r, l in pw)
    R_direct = Sqd - y * mp.log(y) + (1 + mp.euler + c3 - c23 - c69) * y
    R_comb = G + G3 - G23 - G69
    print(
        f"y={Y}: G={mp.nstr(G, 7)} G_chi3={mp.nstr(G3, 7)} G_chi23={mp.nstr(G23, 7)} G_eta={mp.nstr(G69, 7)} | R direct={mp.nstr(R_direct, 9)} combination={mp.nstr(R_comb, 9)} | |diff|={mp.nstr(abs(R_direct - R_comb), 3)}"
    )
print(
    "paper (II.24): y=1000: 1.531 1.040 1.332 -5.704 -> 6.944;  y=1e6: 11.040 -16.153 -97.818 -657.145 -> 749.850"
)
