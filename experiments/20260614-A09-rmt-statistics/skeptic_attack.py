"""Skeptic adversarial tests for A-09 GUE claim.

Independent re-implementation. Does NOT use run_rmt_analysis code.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
TWO_PI = 2 * math.pi


# Load real zeros
zeros_file = HERE / "metrics" / "zeros.txt"
gammas = np.array([float(x) for x in zeros_file.read_text().split()])
print(f"[load] n={len(gammas)}, range=[{gammas[0]:.3f}, {gammas[-1]:.3f}]")


# ---------------------------------------------------------------------------
# ATTACK 1: Independent unfolding using actual Riemann-von Mangoldt N(T)
# The original code uses local density rho(t) = ln(t/2pi)/(2pi). Riemann-von
# Mangoldt theorem: N(T) ~ (T/2pi) ln(T/2pi) - T/2pi + 7/8 + O(log T). Derivative
# dN/dT = ln(T/2pi)/(2pi). So local density IS correct.
#
# Stronger unfolding: smooth N_bar(t) = t/(2pi) * (ln(t/2pi) - 1) + 7/8.
# Compute delta_i = N_bar(gamma_{i+1}) - N_bar(gamma_i). This should give the
# same distribution but uses the integrated form, less subject to local errors.
# ---------------------------------------------------------------------------
def N_bar(t):
    """Smooth part of zero-counting function (Riemann-von Mangoldt)."""
    return (t / TWO_PI) * (np.log(t / TWO_PI) - 1) + 7.0 / 8.0


def unfold_integrated(g):
    """Unfolding via integrated counting function — exact, not local approx."""
    n = N_bar(g)
    return np.diff(n)


def unfold_local_density(g):
    """Original code's method: gap * local_density."""
    gaps = np.diff(g)
    rho = np.log(g[:-1] / TWO_PI) / TWO_PI
    return gaps * rho


delta_int = unfold_integrated(gammas)
delta_loc = unfold_local_density(gammas)

print(
    f"\n[A1] Integrated  unfold: mean={np.mean(delta_int):.4f}, "
    f"P(<0.3)={np.mean(delta_int < 0.3):.4f}"
)
print(
    f"[A1] Local-dens  unfold: mean={np.mean(delta_loc):.4f}, "
    f"P(<0.3)={np.mean(delta_loc < 0.3):.4f}"
)
print(f"[A1] Max diff between methods: {np.max(np.abs(delta_int - delta_loc)):.5f}")


# ---------------------------------------------------------------------------
# ATTACK 2: Use SciPy's official KS test against the integrated GUE CDF
# Wigner surmise (GUE 2x2):  p(s) = (32/pi^2) s^2 exp(-(4/pi) s^2)
# CDF:  F(s) = erf((2/sqrt(pi)) s) - (4 s / pi) exp(-(4/pi) s^2)
# ---------------------------------------------------------------------------
def gue_cdf_exact(s):
    """Closed-form GUE Wigner surmise CDF.

    Derivation: integrate p(s) = (32/pi^2) s^2 exp(-(4/pi) s^2) from 0 to s.
    Sub u = (2/sqrt(pi)) s  =>  integrand = (4/sqrt(pi)) u^2 exp(-u^2).
    int_0^U u^2 exp(-u^2) du = (sqrt(pi)/4) erf(U) - (U/2) exp(-U^2).
    =>  F(s) = erf(u) - (2/sqrt(pi)) u exp(-u^2),  u = (2/sqrt(pi)) s.
    """
    from scipy.special import erf

    s = np.asarray(s, dtype=float)
    u = (2.0 / math.sqrt(math.pi)) * s
    return erf(u) - (2.0 / math.sqrt(math.pi)) * u * np.exp(-u * u)


def poisson_cdf(s):
    return 1 - np.exp(-np.asarray(s, dtype=float))


# Sanity check the CDFs
print(f"\n[A2] gue_cdf(0)={gue_cdf_exact(0):.6f}, gue_cdf(10)={gue_cdf_exact(10):.6f}")
print(f"[A2] poi_cdf(0)={poisson_cdf(0):.6f}, poi_cdf(10)={poisson_cdf(10):.6f}")

# Official SciPy KS test
ks_gue = stats.kstest(delta_int, gue_cdf_exact)
ks_poi = stats.kstest(delta_int, poisson_cdf)
print(f"\n[A2] scipy KS vs GUE      : D={ks_gue.statistic:.4f}, p={ks_gue.pvalue:.4e}")
print(f"[A2] scipy KS vs Poisson  : D={ks_poi.statistic:.4f}, p={ks_poi.pvalue:.4e}")
# A high p-value means cannot reject the hypothesis the sample comes from that CDF.


# ---------------------------------------------------------------------------
# ATTACK 3: Compare original code's KS implementation against scipy
# ---------------------------------------------------------------------------
def gue_pdf(s):
    return (32 / math.pi**2) * s**2 * np.exp(-(4 / math.pi) * s**2)


def poisson_pdf(s):
    return np.exp(-s)


def _cdf_on_grid(pdf_func, s_max=8.0, n=20000):
    grid = np.linspace(0, s_max, n)
    pdf = pdf_func(grid)
    cdf = np.cumsum(pdf) * (grid[1] - grid[0])
    cdf /= cdf[-1]
    return grid, cdf


def cdf_at(pdf_func, x):
    grid, cdf = _cdf_on_grid(pdf_func)
    return np.interp(x, grid, cdf)


# Compare with closed-form
grid = np.linspace(0, 5, 1000)
cdf_num = cdf_at(gue_pdf, grid)
cdf_ana = gue_cdf_exact(grid)
diff = np.max(np.abs(cdf_num - cdf_ana))
print(f"\n[A3] Max diff (numerical_cdf - analytical_cdf): {diff:.6f}")


# ---------------------------------------------------------------------------
# ATTACK 4: Test the NEG control independently. Generate independent Poisson
# sample (NOT using run_rmt_analysis code) and check it gets KS_poisson near 0.
# ---------------------------------------------------------------------------
rng = np.random.default_rng(123)
# Make a homogeneous Poisson with the same total length and density
# delta in unfolded space should be ~ Exp(1).
synth_unfolded = rng.exponential(1.0, size=2000)
ks_pp = stats.kstest(synth_unfolded, poisson_cdf)
ks_pg = stats.kstest(synth_unfolded, gue_cdf_exact)
print(
    f"\n[A4] Independent Poisson: KS_poisson={ks_pp.statistic:.4f} (p={ks_pp.pvalue:.3f}), "
    f"KS_gue={ks_pg.statistic:.4f}"
)


# ---------------------------------------------------------------------------
# ATTACK 5: Build empirical CDF from inhomogeneous Poisson process EXACTLY
# as run_rmt_analysis does, then independently verify it's actually Poisson
# ---------------------------------------------------------------------------
rng2 = np.random.default_rng(42)
g = [14.0]
for _ in range(2000):
    dens = math.log(g[-1] / TWO_PI) / TWO_PI
    g.append(g[-1] + rng2.exponential(1.0 / dens))
g_synth = np.array(g)
delta_synth_int = unfold_integrated(g_synth)
ks_synth_poi = stats.kstest(delta_synth_int, poisson_cdf)
ks_synth_gue = stats.kstest(delta_synth_int, gue_cdf_exact)
print("\n[A5] In-process synthetic Poisson (integrated unfold):")
print(f"     KS_poisson={ks_synth_poi.statistic:.4f} (p={ks_synth_poi.pvalue:.3f})")
print(f"     KS_gue    ={ks_synth_gue.statistic:.4f}")
print(f"     P(<0.3) = {np.mean(delta_synth_int < 0.3):.4f}")


# ---------------------------------------------------------------------------
# ATTACK 6: Sub-bands sensitivity at MUCH finer granularity
# Split first 2000 zeros into 5 bands. Is GUE-shape stable?
# ---------------------------------------------------------------------------
print("\n[A6] Sub-band sensitivity (5 bands, 400 zeros each):")
for i in range(5):
    a, b = i * 400, (i + 1) * 400
    sub = gammas[a : b + 1]
    d = unfold_integrated(sub)
    ks_g = stats.kstest(d, gue_cdf_exact)
    ks_p = stats.kstest(d, poisson_cdf)
    print(
        f"  band {i + 1}: t=[{sub[0]:.1f},{sub[-1]:.1f}], "
        f"KS_gue={ks_g.statistic:.4f}, KS_poi={ks_p.statistic:.4f}, "
        f"closer={'GUE' if ks_g.statistic < ks_p.statistic else 'Poisson'}"
    )


# ---------------------------------------------------------------------------
# ATTACK 7: Stronger discriminator — moments of the spacing distribution
# GUE Wigner surmise:
#   <s>   = 1      (by construction of unfolding)
#   <s^2> = 3 pi / 8 ~ 1.1781
#   sigma = sqrt(<s^2> - 1) ~ 0.4220
# Poisson:
#   <s>   = 1
#   <s^2> = 2
#   sigma = 1
# These are predictions; should match.
# ---------------------------------------------------------------------------
m2_real = np.mean(delta_int**2)
sig_real = math.sqrt(m2_real - np.mean(delta_int) ** 2)
m2_synth = np.mean(delta_synth_int**2)
sig_synth = math.sqrt(m2_synth - np.mean(delta_synth_int) ** 2)
print("\n[A7] Moments of spacing distribution:")
print(f"  real zeros : <s>={np.mean(delta_int):.4f}, <s^2>={m2_real:.4f}, sigma={sig_real:.4f}")
print(
    f"  synth Poiss: <s>={np.mean(delta_synth_int):.4f}, <s^2>={m2_synth:.4f}, "
    f"sigma={sig_synth:.4f}"
)
print("  GUE pred   : <s^2>=1.1781, sigma=0.4220")
print("  Poiss pred : <s^2>=2.0000, sigma=1.0000")


# ---------------------------------------------------------------------------
# ATTACK 8: Bootstrap KS - is KS_gue=0.04 significantly small?
# Generate many GUE samples of size 1999, compute KS to GUE CDF.
# If real-zeros KS sits inside the bootstrap distribution -> consistent with GUE.
# ---------------------------------------------------------------------------
# Sample from GUE: use rejection sampling on the surmise PDF.
def sample_gue(n, rng):
    """Rejection sample from GUE Wigner surmise."""
    out = []
    M = gue_pdf(np.array([0.78]))[0]  # mode ~ pi/4? approximate peak height
    while len(out) < n:
        s = rng.exponential(1.0, size=n * 2)
        u = rng.uniform(0, M, size=n * 2)
        accept = u < gue_pdf(s)
        out.extend(s[accept].tolist())
    return np.array(out[:n])


rng3 = np.random.default_rng(7)
ks_bootstrap = []
for _ in range(200):
    sample = sample_gue(1999, rng3)
    ks = stats.kstest(sample, gue_cdf_exact).statistic
    ks_bootstrap.append(ks)
ks_bootstrap = np.array(ks_bootstrap)
real_ks = stats.kstest(delta_int, gue_cdf_exact).statistic
pct = np.mean(ks_bootstrap >= real_ks) * 100
print(
    f"\n[A8] Bootstrap GUE KS: median={np.median(ks_bootstrap):.4f}, "
    f"95th={np.percentile(ks_bootstrap, 95):.4f}"
)
print(f"     Real zeros KS = {real_ks:.4f}")
print(
    f"     {pct:.1f}% of GUE samples have KS >= real_ks (high = real is more GUE-like than typical GUE)"
)


print("\n=== END SKEPTIC TESTS ===")
