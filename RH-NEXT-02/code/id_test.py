"""Identity test: v^T Q v  vs  sum over zeros of L (on the critical line) of |xi_hat(gamma)|^2 * 2,
for the smooth test function xi(x) = sin^2(pi x / L) on [0, L]  (Fourier coefficients v_0 = 1/2, v_{+-1} = -1/4).
Calibrates the overall constant on chi3 (zeros from mpmath), then applies it to D (Davenport-Heilbronn).
Off-line zeros of D (0.8085+85.7i, ...) contribute ~ (85)^-6 here: negligible, so this tests the matrix, not the off-line effect.
Usage: python id_test.py <chi3|dh> <c> <T_zero_max>
"""

import sys

import cert_chi as cc
import mpmath as mp

mp.mp.dps = 30
name, c, TMAX = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])

A, DIM, K = cc.build_arb(name, c, 1, 400)
Q = [[mp.mpf(A[i][j].mid().str(40, radius=False)) for j in range(3)] for i in range(3)]
v = [mp.mpf(-1) / 4, mp.mpf(1) / 2, mp.mpf(-1) / 4]  # n = -1, 0, 1
Qv = sum(v[i] * v[j] * Q[i][j] for i in range(3) for j in range(3))
L = mp.log(c)
om = 2 * mp.pi / L


def Ahat(beta):
    if abs(beta) < mp.mpf(10) ** -20:
        return L
    return (mp.e ** (1j * beta * L) - 1) / (1j * beta)


def xihat(g):
    return Ahat(g) / 2 - (Ahat(g + om) + Ahat(g - om)) / 4


# zeros on the critical line
if name == "chi3":
    chi = [0, 1, -1]
    Zf = lambda t: mp.dirichlet(mp.mpc(0.5, t), chi)

    # Hardy-type real function: rotate phase using Gamma factor: theta ~ arg of Gamma((s+1)/2) (odd char) - t/2 log(pi/3)
    def Zreal(t):
        s = mp.mpc(0.5, t)
        return mp.re(
            mp.exp(1j * (mp.im(mp.loggamma((s + 1) / 2)) - t / 2 * mp.log(mp.pi / 3))) * Zf(t)
        )
else:
    s5 = mp.sqrt(5)
    kappa = (mp.sqrt(10 - 2 * s5) - 2) / (s5 - 1)
    a_per = [0, 1, kappa, -kappa, -1]

    def Zreal(t):
        s = mp.mpc(0.5, t)
        return mp.re((mp.pi / 5) ** (-s / 2) * mp.gamma((s + 1) / 2) * mp.dirichlet(s, a_per))


step = mp.mpf("0.1")
ts = [step * i for i in range(1, int(TMAX / 0.1) + 1)]
vals = [Zreal(t) for t in ts]
zeros = []
for i in range(len(ts) - 1):
    if vals[i] * vals[i + 1] < 0:
        zeros.append(mp.findroot(Zreal, (ts[i], ts[i + 1]), solver="anderson"))
S = 2 * sum(abs(xihat(g)) ** 2 for g in zeros)
print(
    f"{name} c={c}: zeros found up to {TMAX}: {len(zeros)}  first: {[mp.nstr(z, 8) for z in zeros[:3]]}"
)
print(
    f"  v^T Q v = {mp.nstr(Qv, 12)}   2*sum|xi_hat|^2 = {mp.nstr(S, 12)}   ratio = {mp.nstr(Qv / S, 12)}   L={mp.nstr(L, 8)}  1/L={mp.nstr(1 / L, 8)}"
)
