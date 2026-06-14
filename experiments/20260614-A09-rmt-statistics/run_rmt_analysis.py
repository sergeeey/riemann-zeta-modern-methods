"""A-09 step 2 — RMT statistics of zeta zeros (FL Steps 3-8).

Reads cached zeros, unfolds them to mean spacing 1, builds the nearest-neighbour
spacing distribution (NNSD), and compares to two references:

  GUE Wigner surmise   p(s) = (32/pi^2) s^2 exp(-(4/pi) s^2)   [level repulsion]
  Poisson              p(s) = exp(-s)                          [no repulsion]

Verdict PASS if zeros are significantly closer to GUE than to Poisson.

Negative control: a synthetic inhomogeneous Poisson process with the SAME mean
density is pushed through the SAME unfolding+histogram code. It must come out as
Poisson (not GUE) — proving the pipeline does not manufacture level repulsion.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TWO_PI = 2 * math.pi


# --- reference distributions ---------------------------------------------
def gue_pdf(s: np.ndarray) -> np.ndarray:
    return (32 / math.pi**2) * s**2 * np.exp(-(4 / math.pi) * s**2)


def poisson_pdf(s: np.ndarray) -> np.ndarray:
    return np.exp(-s)


def _cdf_on_grid(pdf_func, s_max: float = 8.0, n: int = 20000):
    grid = np.linspace(0, s_max, n)
    pdf = pdf_func(grid)
    cdf = np.cumsum(pdf) * (grid[1] - grid[0])
    cdf /= cdf[-1]  # normalize (GUE surmise integrates to 1 already; guard)
    return grid, cdf


def cdf_at(pdf_func, x: np.ndarray) -> np.ndarray:
    grid, cdf = _cdf_on_grid(pdf_func)
    return np.interp(x, grid, cdf)


def ks_distance(samples: np.ndarray, pdf_func) -> float:
    """Two-sided KS distance between empirical samples and a theoretical CDF."""
    xs = np.sort(samples)
    n = len(xs)
    cdf_vals = cdf_at(pdf_func, xs)
    emp_hi = np.arange(1, n + 1) / n
    emp_lo = np.arange(0, n) / n
    return float(max(np.max(emp_hi - cdf_vals), np.max(cdf_vals - emp_lo)))


# --- unfolding -----------------------------------------------------------
def unfold(gammas: np.ndarray) -> np.ndarray:
    """Normalize gaps to mean spacing 1 using local density ln(t/2pi)/2pi."""
    gaps = np.diff(gammas)
    local_density = np.log(gammas[:-1] / TWO_PI) / TWO_PI
    return gaps * local_density


# --- negative control ----------------------------------------------------
def synthetic_poisson_like(n: int, seed: int = 42) -> np.ndarray:
    """Inhomogeneous Poisson points with the SAME mean density as zeta zeros.

    gamma_{k+1} = gamma_k + Exp(mean = 1/density(gamma_k)). Unfolding this MUST
    give Poisson NNSD — if our pipeline instead returned GUE, it would be a bug.
    """
    rng = np.random.default_rng(seed)
    g = [14.0]
    for _ in range(n):
        dens = math.log(g[-1] / TWO_PI) / TWO_PI
        g.append(g[-1] + rng.exponential(1.0 / dens))
    return np.array(g)


def summarize(delta: np.ndarray, label: str) -> dict:
    ks_gue = ks_distance(delta, gue_pdf)
    ks_poi = ks_distance(delta, poisson_pdf)
    return {
        "label": label,
        "n_spacings": int(len(delta)),
        "mean_spacing": round(float(np.mean(delta)), 4),
        # second moment: independent discriminator (skeptic CAVEAT-5).
        # GUE Wigner surmise <s^2> = 3*pi/8 ~ 1.178; Poisson <s^2> = 2.0
        "second_moment": round(float(np.mean(delta**2)), 4),
        "frac_below_0.3": round(float(np.mean(delta < 0.3)), 4),
        "ks_to_gue": round(ks_gue, 4),
        "ks_to_poisson": round(ks_poi, 4),
        "closer_to": "GUE" if ks_gue < ks_poi else "Poisson",
    }


def main() -> None:
    zeros_file = HERE / "metrics" / "zeros.txt"
    gammas = np.array([float(x) for x in zeros_file.read_text().split()])
    print(f"Loaded {len(gammas)} zeros (first={gammas[0]:.3f}, last={gammas[-1]:.3f})")

    delta = unfold(gammas)
    real = summarize(delta, "zeta zeros (real)")

    # reference fractions below 0.3 for context
    grid = np.linspace(0, 0.3, 2000)
    gue_frac = float(np.trapezoid(gue_pdf(grid), grid))
    poi_frac = float(np.trapezoid(poisson_pdf(grid), grid))

    # negative control — match the real spacing count (len(delta)) exactly
    synth = synthetic_poisson_like(len(delta))
    synth_delta = unfold(synth)
    neg = summarize(synth_delta, "synthetic Poisson (neg control)")

    # sensitivity: two halves
    half = len(delta) // 2
    lo = summarize(delta[:half], "first half")
    hi = summarize(delta[half:], "second half")

    # --- verdict ---
    real_ok = real["closer_to"] == "GUE" and real["ks_to_gue"] < real["ks_to_poisson"]
    neg_ok = neg["closer_to"] == "Poisson"  # pipeline does not fake GUE
    unfold_ok = abs(real["mean_spacing"] - 1.0) < 0.1
    verdict = "PASS" if (real_ok and neg_ok and unfold_ok) else "FAIL"

    result = {
        "experiment": "20260614-A09-rmt-statistics",
        "n_zeros": int(len(gammas)),
        "height_range": [round(float(gammas[0]), 2), round(float(gammas[-1]), 2)],
        "real_zeros": real,
        "reference_frac_below_0.3": {
            "gue": round(gue_frac, 4),
            "poisson": round(poi_frac, 4),
        },
        "reference_second_moment": {"gue_wigner": 1.1781, "poisson": 2.0},
        "negative_control_synthetic_poisson": neg,
        "sensitivity_halves": {"first": lo, "second": hi},
        "checks": {
            "real_closer_to_gue": real_ok,
            "neg_control_is_poisson": neg_ok,
            "unfolding_mean_is_1": unfold_ok,
        },
        "verdict": verdict,
    }
    out = HERE / "metrics" / "run.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- summary ---
    print("\n" + "=" * 62)
    print(f"VERDICT: {verdict}")
    print("=" * 62)
    print(
        f"REAL zeros : closer_to={real['closer_to']}  "
        f"KS_gue={real['ks_to_gue']}  KS_poisson={real['ks_to_poisson']}"
    )
    print(
        f"             mean_spacing={real['mean_spacing']}  "
        f"P(d<0.3)={real['frac_below_0.3']} "
        f"(GUE~{gue_frac:.3f}, Poisson~{poi_frac:.3f})"
    )
    print(f"             <s^2>={real['second_moment']} (GUE~1.178, Poisson~2.0)")
    print(
        f"NEG control: closer_to={neg['closer_to']}  "
        f"KS_gue={neg['ks_to_gue']}  KS_poisson={neg['ks_to_poisson']}"
    )
    print(f"Sensitivity: 1st half -> {lo['closer_to']}, 2nd half -> {hi['closer_to']}")
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
