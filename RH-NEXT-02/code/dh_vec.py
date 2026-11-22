"""Most negative eigenvector of the DH matrix (mid values of the Arb matrix) and where its Fourier transform lives.
Usage: python dh_vec.py <c> <N>
"""

import sys

import cert_chi as cc
import mpmath as mp

c, N = int(sys.argv[1]), int(sys.argv[2])
mp.mp.dps = 120
A, DIM, K = cc.build_arb("dh", c, N, 2400)
Q = mp.matrix(DIM, DIM)
for i in range(DIM):
    for j in range(DIM):
        Q[i, j] = mp.mpf(A[i][j].mid().str(130, radius=False))
E, V = mp.eigsy(Q)
order = sorted(range(DIM), key=lambda i: E[i])
neg = [(i, E[i]) for i in order if E[i] < 0]
print(
    f"dh c={c} N={N}: negative eigenvalues (mid matrix, 120 digits): {[mp.nstr(e, 6) for _, e in neg]}"
)
L = mp.log(c)
k = order[0]
v = [V[i, k] for i in range(DIM)]


def F(t):
    s = mp.mpf(0)
    for i, nn in enumerate(range(-N, N + 1)):
        b = t + 2 * mp.pi * nn / L
        s += ((-1) ** nn) * v[i] * (L if abs(b) < mp.mpf(10) ** -60 else 2 * mp.sin(b * L / 2) / b)
    return s


ts = [mp.mpf(i) / 4 for i in range(4 * 150 + 1)]
pw = [abs(F(t)) ** 2 for t in ts]
tot = sum(pw)
# spectral weight of the most negative direction by height

bins = [(0, 40), (40, 80), (80, 92), (92, 130), (130, 150)]
for lo, hi in bins:
    w = sum(p for t, p in zip(ts, pw) if lo <= t < hi) / tot
    print(f"  weight of |xi_hat(t)|^2 for t in [{lo},{hi}): {mp.nstr(w, 6)}")
imax = max(range(len(ts)), key=lambda i: pw[i])
print("  peak of |xi_hat|^2 at t =", mp.nstr(ts[imax], 6))
