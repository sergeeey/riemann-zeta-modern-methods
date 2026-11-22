"""EXACT_COMPUTED check of the closed form used in proof_or_counterexample/window_sharpness.md:
F(s) = int_0^inf e^{beta u} cos(gamma u) e^{-s u} du = (s - beta) / ((s - beta)^2 + gamma^2)  for Re s > beta,
and of the sign pattern: cos(gamma u) < 0 on windows of length < pi/gamma, so g < 0 <= e^{theta u} there.
Model: mpmath quadrature at 30 digits, beta = 0.8, gamma = 14.134725 (first zero height of zeta, only as a scale), theta = 0.6.
Run: python -I check_window_counterexample.py
"""

import sys

import mpmath as mp

mp.mp.dps = 30
sys.stdout.reconfigure(encoding="utf-8")
beta, gamma, theta = mp.mpf("0.8"), mp.mpf("14.134725"), mp.mpf("0.6")


def F_closed(s):
    return (s - beta) / ((s - beta) ** 2 + gamma**2)


for s in (mp.mpc(2.5, 0.0), mp.mpc(3.0, 7.0), mp.mpc(1.5, -14.0)):
    num = mp.quad(lambda u: mp.e ** ((beta - s) * u) * mp.cos(gamma * u), mp.linspace(0, 60, 400))
    print(
        f"s={s}: quadrature={mp.nstr(num, 15)} closed form={mp.nstr(F_closed(s), 15)} |diff|={mp.nstr(abs(num - F_closed(s)), 3)}"
    )

print(
    "poles of the closed form:",
    [mp.nstr(beta + 1j * gamma, 8), mp.nstr(beta - 1j * gamma, 8)],
    "real part",
    beta,
    "> theta",
    theta,
)
print(
    "denominator on the real axis, minimum over s in [0, 50]:",
    mp.nstr(min((s - beta) ** 2 + gamma**2 for s in [mp.mpf(x) / 10 for x in range(0, 500)]), 8),
    "(> 0, so no real pole)",
)

# a window of length L < pi/gamma inside the negative phase of cos at arbitrarily large U
L = mp.pi / gamma * mp.mpf("0.9")
ok = True
rows = []
for k in (10, 100, 1000, 10**5):
    U = (
        mp.pi / (2 * gamma) + 2 * mp.pi * k / gamma + (mp.pi / gamma - L) / 2
    )  # centred in the negative interval
    pts = [U + L * mp.mpf(i) / 200 for i in range(201)]
    worst = max(
        mp.e ** (beta * u) * mp.cos(gamma * u) for u in pts
    )  # largest value of g on the window
    ok = ok and worst < 0
    rows.append((int(k), mp.nstr(U, 8), mp.nstr(worst, 6)))
print(
    f"window length L={mp.nstr(L, 6)} < pi/gamma={mp.nstr(mp.pi / gamma, 6)}; (k, U, max of g on [U, U+L]) :",
    rows,
)
print("g < 0 <= e^{theta u} on all sampled windows:", ok)
