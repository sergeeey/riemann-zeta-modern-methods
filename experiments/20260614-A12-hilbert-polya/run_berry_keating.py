"""A-12 — Berry-Keating semiclassical check (FL Steps 3-8).

Tests ONE falsifiable consequence of the Hilbert-Polya / Berry-Keating idea:
does the H=xp semiclassical level count reproduce the zeta zero-counting function?

Three counting functions on the critical line:
  n_BK(T)   = (T/2pi)(ln(T/2pi) - 1) + 7/8      Berry-Keating Weyl count (l_x*l_p=2pi)
  smooth(T) = theta(T)/pi + 1                    exact smooth part (Riemann-Siegel theta)
  N_exact(T)= nzeros(T)                          exact count (argument principle)

Claim: n_BK == smooth up to O(1/T)  (BK reproduces the DENSITY — why xp is natural)
       S(T) = N_exact - smooth oscillates about 0, std>0  (positions NOT reproduced)

Negative control: wrong normalization l_x*l_p=pi -> Weyl error grows LINEARLY,
proving 2*pi is a necessity, not a fudge.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from zeta.toolkit import set_precision  # noqa: E402

HERE = Path(__file__).resolve().parent
TWO_PI = 2 * mp.pi


def n_berry_keating(T, lxlp=None):
    """Berry-Keating Weyl level count for H=xp with cell area l_x*l_p.

    Default l_x*l_p = 2*pi (one Planck cell) -> matches zeta smooth count.
    """
    if lxlp is None:
        lxlp = TWO_PI
    T = mp.mpf(T)
    return (T / TWO_PI) * (mp.log(T / lxlp) - 1) + mp.mpf(7) / 8


def smooth_count(T):
    """Exact smooth part of N(T): theta(T)/pi + 1 (Riemann-Siegel theta)."""
    return mp.siegeltheta(mp.mpf(T)) / mp.pi + 1


def main() -> None:
    set_precision(30)

    # T grid — avoid landing exactly on zeros by using .137 offset
    t_values = [mp.mpf(t) + mp.mpf("0.137") for t in range(50, 2501, 50)]

    rows = []
    for T in t_values:
        n_bk = n_berry_keating(T)
        n_bk_wrong = n_berry_keating(T, lxlp=mp.pi)  # wrong normalization
        smooth = smooth_count(T)
        n_exact = int(mp.nzeros(float(T)))
        S = n_exact - smooth
        # Independent S(T): (1/pi) arg zeta(1/2+iT), the principal branch.
        # WHY: rules out circularity (S above uses nzeros, which uses theta).
        # Valid because |S|<1 here, so principal arg == continuous S (no 2pi jump).
        S_direct = float(mp.arg(mp.zeta(mp.mpf(1) / 2 + 1j * T)) / mp.pi)
        rows.append(
            {
                "T": float(T),
                "n_bk": float(n_bk),
                "smooth": float(smooth),
                "n_exact": n_exact,
                "weyl_err": float(abs(n_bk - smooth)),
                "weyl_err_wrong": float(abs(n_bk_wrong - smooth)),
                "S": float(S),
                "S_direct": S_direct,
            }
        )

    weyl_err = [r["weyl_err"] for r in rows]
    weyl_err_wrong = [r["weyl_err_wrong"] for r in rows]
    S_vals = [r["S"] for r in rows]
    # circularity check: S (from nzeros) vs S_direct (from arg zeta) must agree
    max_S_disagreement = max(abs(r["S"] - r["S_direct"]) for r in rows)
    S_independent_ok = max_S_disagreement < 0.05

    n = len(S_vals)
    mean_S = sum(S_vals) / n
    std_S = (sum((s - mean_S) ** 2 for s in S_vals) / n) ** 0.5
    max_abs_S = max(abs(s) for s in S_vals)

    # --- checks ---
    # 1. Weyl error (correct norm) shrinks with T (O(1/T))
    weyl_shrinks = weyl_err[-1] < weyl_err[0]
    # quantitative: weyl_err * T ~ const (1/(48pi)); check it stays bounded small
    weyl_times_T = [r["weyl_err"] * r["T"] for r in rows]
    weyl_is_oneoverT = max(weyl_times_T) < 0.02  # 1/(48pi)~0.0066, allow margin

    # 2. Wrong normalization error GROWS (linear)
    wrong_grows = weyl_err_wrong[-1] > 10 * weyl_err_wrong[0]

    # 3. S(T) centered near 0 but with nonzero spread (positions NOT captured)
    S_centered = abs(mean_S) < 0.5
    S_has_spread = std_S > 0.1
    # 4. S spread does NOT shrink to 0 (BK does not converge to true positions)
    half = n // 2
    std_first = (sum((s - mean_S) ** 2 for s in S_vals[:half]) / half) ** 0.5
    std_second = (sum((s - mean_S) ** 2 for s in S_vals[half:]) / (n - half)) ** 0.5
    S_persists = std_second > 0.1

    verdict = (
        "PASS"
        if all(
            [
                weyl_shrinks,
                weyl_is_oneoverT,
                wrong_grows,
                S_centered,
                S_has_spread,
                S_persists,
                S_independent_ok,
            ]
        )
        else "FAIL"
    )

    result = {
        "experiment": "20260614-A12-hilbert-polya",
        "t_range": [50, 2500],
        "n_points": n,
        "weyl_error_correct_norm": {
            "at_T50": round(weyl_err[0], 8),
            "at_T2500": round(weyl_err[-1], 8),
            "max_weyl_err_times_T": round(max(weyl_times_T), 5),
            "shrinks_as_1_over_T": weyl_is_oneoverT,
        },
        "weyl_error_wrong_norm_pi": {
            "at_T50": round(weyl_err_wrong[0], 4),
            "at_T2500": round(weyl_err_wrong[-1], 4),
            "grows_linearly": wrong_grows,
        },
        "fluctuation_S": {
            "mean": round(mean_S, 4),
            "std": round(std_S, 4),
            "max_abs": round(max_abs_S, 4),
            "std_first_half": round(std_first, 4),
            "std_second_half": round(std_second, 4),
            "centered_near_0": S_centered,
            "has_nonzero_spread": S_has_spread,
            "persists_not_shrinking": S_persists,
            "max_disagreement_vs_arg_zeta": round(max_S_disagreement, 5),
            "S_independent_confirmed": S_independent_ok,
        },
        "checks": {
            "weyl_shrinks": weyl_shrinks,
            "weyl_is_O(1/T)": weyl_is_oneoverT,
            "wrong_norm_grows": wrong_grows,
            "S_centered": S_centered,
            "S_has_spread": S_has_spread,
            "S_persists": S_persists,
            "S_not_circular": S_independent_ok,
        },
        "verdict": verdict,
        "interpretation": (
            "Berry-Keating xp reproduces the DENSITY of zeros (smooth count) "
            "to O(1/T), but the fluctuation S(T) — where RH lives — is NOT "
            "reproduced. xp counts HOW MANY zeros, not WHERE. Density match is "
            "necessary, NOT sufficient: does NOT prove the operator exists."
        ),
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    # also dump the per-T table for the figure
    (HERE / "metrics" / "table.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # --- summary ---
    print("=" * 64)
    print(f"VERDICT: {verdict}")
    print("=" * 64)
    print("Berry-Keating Weyl count vs exact zeta smooth count:")
    print(f"  Weyl err (correct 2pi): T=50 -> {weyl_err[0]:.2e},  T=2500 -> {weyl_err[-1]:.2e}")
    print(
        f"  weyl_err * T (~1/48pi=0.0066): max={max(weyl_times_T):.5f}  [O(1/T): {weyl_is_oneoverT}]"
    )
    print(
        f"  Weyl err (WRONG pi)   : T=50 -> {weyl_err_wrong[0]:.2f},  T=2500 -> {weyl_err_wrong[-1]:.2f}  [grows: {wrong_grows}]"
    )
    print("Fluctuation S(T) = N_exact - smooth:")
    print(f"  mean={mean_S:.4f} (centered: {S_centered})  std={std_S:.4f} (spread: {S_has_spread})")
    print(
        f"  max|S|={max_abs_S:.4f}  std 1st/2nd half: {std_first:.3f}/{std_second:.3f} (persists: {S_persists})"
    )
    print(
        f"  S vs independent arg-zeta: max disagreement={max_S_disagreement:.5f} "
        f"(not circular: {S_independent_ok})"
    )
    print("\n-> xp gives the DENSITY (how many), NOT the positions (where). S(T)=RH not captured.")


if __name__ == "__main__":
    main()
