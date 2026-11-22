"""Counterexample to the 'good set has density close to 1' variant of the window criterion (candidate H2/B3 in RH-BRIDGE-01).

g_N(u) = exp(beta u) * (F_N(gamma u) - 1),  F_N = Fejer kernel  F_N(t) = sum_{|j|<=N} (1 - |j|/(N+1)) e^{i j t}
       = sin^2((N+1) t/2) / ((N+1) sin^2(t/2)).
F_N - 1 has no zero frequency, so the Mellin-Laplace transform
       Phi(s) = int_0^inf g_N(u) e^{-s u} du = sum_{0<|j|<=N} c_j / (s - beta - i j gamma),  c_j = 1 - |j|/(N+1),
is meromorphic on C with only the non-real simple poles beta + i j gamma (j != 0).  Hence there is no real pole, and g_N satisfies the
analytic hypotheses (a), (b) of window_sharpness.md for 0 < theta < beta <= 2, while
       g_N(u) <= 0 <= e^{theta u}   whenever  sin^2(gamma u / 2) >= 1/(N+1)                       (*)
because F_N(t) <= 1/((N+1) sin^2(t/2)).  The exceptional set has density (2/pi) arcsin(1/sqrt(N+1)) -> 0 (per period).
What this script does: (1) checks the closed-form transform against numerical integration; (2) checks (*) on a grid; (3) prints the exact bad fraction.
Run: python -I check_density_counterexample.py
"""

import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")


def fejer_minus_one(t, n):
    s = np.sin(t / 2)
    num = np.sin((n + 1) * t / 2) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        val = np.where(np.abs(s) < 1e-12, n + 1.0, num / ((n + 1) * s**2))
    return val - 1.0


def series_fejer_minus_one(t, n):
    return sum(2 * (1 - j / (n + 1)) * np.cos(j * t) for j in range(1, n + 1))


beta, gamma, theta = 1.5, 0.7, 0.6
for n in (3, 10, 40):
    # (0) kernel identity
    t = np.linspace(0.01, 6.27, 2001)
    err0 = np.max(np.abs(fejer_minus_one(t, n) - series_fejer_minus_one(t, n)))
    # (1) transform at s = beta + 1.3 + 0.4i: compare closed form with numerical integral (decay e^{-1.3 u})
    s = beta + 1.3 + 0.4j
    u = np.linspace(0, 60, 2_400_001)
    g = np.exp(beta * u) * series_fejer_minus_one(gamma * u, n)
    num = np.trapezoid(g * np.exp(-s * u), u)
    closed = sum(
        (1 - abs(j) / (n + 1)) / (s - beta - 1j * j * gamma) for j in range(-n, n + 1) if j != 0
    )
    err1 = abs(num - closed)
    # (2) inequality (*) on a grid
    uu = np.linspace(0, 400, 800_001)
    good = np.sin(gamma * uu / 2) ** 2 >= 1 / (n + 1)
    gv = series_fejer_minus_one(gamma * uu, n)
    viol = int(np.sum(good & (gv > 1e-12)))
    frac_bad = 1 - good.mean()
    exact_bad = (2 / np.pi) * np.arcsin(1 / np.sqrt(n + 1))
    # fraction of u with g_N(u) > 0 (actual bad set, subset of the guaranteed one)
    actual_bad = (gv > 0).mean()
    print(
        f"N={n:3d}: kernel identity err {err0:.1e}; transform err {err1:.1e}; violations of (*) {viol}; "
        f"guaranteed bad fraction (2/pi) asin(1/sqrt(N+1)) = {exact_bad:.4f} (grid {frac_bad:.4f}); actual fraction with g>0: {actual_bad:.4f}"
    )
