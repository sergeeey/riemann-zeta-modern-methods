"""EXACT_COMPUTED checks of the elementary numerical claims in the proof of the interval lemma (zeta-paper.pdf, Part II sec. 1, pp. 26-27)
and of the error-budget exponents (sec. 3 and (II.15)-(II.16)).  Model: mpmath, 50 digits.  Scope: finite checks of stated constants;
NOT a proof of the lemma (the proof is read separately, see bridge_dependency_map.md edge E2).

Run: python -I check_interval_lemma_constants.py
"""

import sys

import mpmath as mp

mp.mp.dps = 50
sys.stdout.reconfigure(encoding="utf-8")
out = {}

# 1. eta, c: eta = max(0.8 e^0.2, 1.2 e^-0.2) = 0.9825..., c = 0.008 < log((1+eta)/(2 eta)) = 0.00887...
a = mp.mpf("0.8") * mp.e ** mp.mpf("0.2")
b = mp.mpf("1.2") * mp.e ** mp.mpf("-0.2")
eta = max(a, b)
bound = mp.log((1 + eta) / (2 * eta))
out["eta"] = (mp.nstr(a, 12), mp.nstr(b, 12), mp.nstr(eta, 12))
out["log((1+eta)/(2eta))"] = mp.nstr(bound, 12)
out["c=0.008 < bound"] = bool(mp.mpf("0.008") < bound)

# 2. sigma >= 252 gives (sigma - theta)/(sigma - 2) <= e^c for every theta in (0,1): the worst case is theta -> 0
c = mp.mpf("0.008")
sigma_min = 2 * mp.e**c / (mp.e**c - 1)
out["sigma_min for theta->0"] = mp.nstr(sigma_min, 12)
out["sigma=252 works for all theta in (0,1)"] = bool((252 - 0) / (252 - 2) <= mp.e**c)
out["sigma=251 works (should be False)"] = bool((251 - 0) / (251 - 2) <= mp.e**c)

# 3. the density u^j e^{-(sigma-2)u} concentrates at j/(sigma-2); with j ~ (5/4)(sigma-2)U the window [U, 3U/2] maps to v = (sigma-2)u/j in [4/5, 6/5]
out["window ends v"] = (mp.nstr(mp.mpf(4) / 5, 6), mp.nstr(mp.mpf(6) / 5, 6))
out["base v e^{1-v} at 4/5, 6/5, 1"] = tuple(
    mp.nstr(v * mp.e ** (1 - v), 12) for v in (mp.mpf(4) / 5, mp.mpf(6) / 5, mp.mpf(1))
)

# 4. outside fraction of  int_0^inf u^j e^{-(sigma-2)u} du  versus C0 e^{-c j}: the ratio must stay bounded as U grows (C0 independent of U)
sigma = mp.mpf(252)
lam = sigma - 2
rows = []
for U in (20, 40, 80, 160, 320, 640):
    j = int(mp.nint(mp.mpf(5) / 4 * lam * U))
    # regularised incomplete gamma: P(j+1, x) = int_0^x t^j e^{-t} dt / j!
    lo = mp.gammainc(j + 1, 0, lam * U, regularized=True)  # mass at u < U
    hi = mp.gammainc(j + 1, lam * mp.mpf(3) / 2 * U, mp.inf, regularized=True)  # mass at u > 3U/2
    frac = lo + hi
    rows.append((U, j, mp.nstr(frac, 6), mp.nstr(frac / mp.e ** (-c * j), 6)))
out["outside fraction (U, j, fraction, fraction / e^{-c j})"] = rows
ratios = [mp.mpf(r[3]) for r in rows]
out["ratio bounded (max)"] = mp.nstr(max(ratios), 6)
out["ratio non-increasing for large U"] = bool(
    all(ratios[i + 1] <= ratios[i] * (1 + 1e-9) for i in range(2, len(ratios) - 1))
)

# 5. error-budget exponents in sec. 3: m = x^{1/2+O(eps)}, k = x^{9/2+O(eps)}, n = x^{2+O(eps)} => x/m = x^{1/2-O(eps)}, xm/k = x^{-3+O(eps)}, m = x^{1/2+O(eps)}, k/n^2 = x^{1/2+O(eps)}
half, nine_half, two = mp.mpf(1) / 2, mp.mpf(9) / 2, mp.mpf(2)
out["exponents (x/m, xm/k, m, k/n^2) at eps->0"] = tuple(
    mp.nstr(v, 6) for v in (1 - half, 1 + half - nine_half, half, nine_half - 2 * two)
)
out[
    "x/m + m >= 2 sqrt(x) for every m>0 (so exponent 1/2 cannot be improved inside this bookkeeping)"
] = bool(
    all(
        mp.mpf(10) ** 6 / m + m >= 2 * mp.sqrt(mp.mpf(10) ** 6) - mp.mpf(10) ** -30
        for m in (10, 100, 1000, 10**4)
    )
)

for k, v in out.items():
    print(f"{k}: {v}")
