"""A-05 — Prime counting error term (FL Steps 3-8). What RH buys.

von Koch (1901): RH  <=>  pi(x) = li(x) + O(sqrt(x) log x).
Schoenfeld (1976): under RH, |pi(x) - li(x)| < (1/8pi) sqrt(x) ln(x) for x >= 2657.

We compute, for x = 10^2 .. 10^7:
  pi(x)  exact (sympy.primepi)
  li(x)  logarithmic integral (mpmath)
  error  = li(x) - pi(x)   (signed: positive means li overestimates)
and check the error stays within the Schoenfeld bound (consistent with RH) and
that li(x) > pi(x) holds on this range — WHILE noting Littlewood (1914): this bias
is NOT universal; the first crossover is near Skewes' number ~10^316.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp
import sympy

HERE = Path(__file__).resolve().parent

# Verified reference values of pi(x)
PI_REF = {
    100: 25,
    1000: 168,
    10000: 1229,
    100000: 9592,
    1000000: 78498,
    10000000: 664579,
}


def schoenfeld_bound(x):
    """(1/8pi) sqrt(x) ln(x) — valid for x >= 2657 under RH."""
    x = mp.mpf(x)
    return mp.sqrt(x) * mp.log(x) / (8 * mp.pi)


def main() -> None:
    mp.mp.dps = 30
    exps = [2, 3, 4, 5, 6, 7]
    rows = []
    for e in exps:
        x = 10**e
        pi_x = int(sympy.primepi(x))
        # WHY mp.li(x): Cauchy PV integral_0^x dt/ln t — matches Schoenfeld 1976
        # Thm 12 notation. NOT Li(x)=li(x)-li(2) (offset); use mp.li(x, offset=True)
        # for that. Difference ~li(2)=1.045, negligible for the bound check.
        li_x = mp.li(x)
        error = li_x - pi_x  # signed
        bound = schoenfeld_bound(x)
        rows.append(
            {
                "x": x,
                "pi_x": pi_x,
                "li_x": float(li_x),
                "error_li_minus_pi": float(error),
                "abs_error": float(abs(error)),
                "schoenfeld_bound": float(bound),
                "ratio_err_over_bound": float(abs(error) / bound),
                "err_over_sqrtx": float(abs(error) / mp.sqrt(x)),
                "li_greater_pi": bool(error > 0),
                "ref_pi": PI_REF.get(x),
                "pi_matches_ref": (PI_REF.get(x) is None) or (pi_x == PI_REF[x]),
            }
        )

    # --- checks ---
    pi_all_match = all(r["pi_matches_ref"] for r in rows)
    li_gt_pi_all = all(r["li_greater_pi"] for r in rows)
    # Schoenfeld bound only valid x>=2657
    bound_holds = all(r["ratio_err_over_bound"] < 1.0 for r in rows if r["x"] >= 2657)
    # error/sqrt(x) should stay modest (not blow up) — RH scale
    err_sqrt_bounded = max(r["err_over_sqrtx"] for r in rows) < 5.0

    verdict = "PASS" if all([pi_all_match, li_gt_pi_all, bound_holds, err_sqrt_bounded]) else "FAIL"

    result = {
        "experiment": "20260614-A05-prime-error",
        "rows": rows,
        "checks": {
            "pi_matches_reference": pi_all_match,
            "li_greater_pi_on_range": li_gt_pi_all,
            "schoenfeld_bound_holds_x_ge_2657": bound_holds,
            "err_over_sqrtx_bounded": err_sqrt_bounded,
        },
        "verdict": verdict,
        "interpretation": (
            "li(x) approximates pi(x) with error well inside the Schoenfeld/von "
            "Koch bound — this is WHAT RH buys: the smallest possible error in the "
            "prime number theorem, O(sqrt(x) log x). The li>pi bias holds to 10^7 "
            "but is NOT universal (Littlewood 1914: infinitely many crossovers, "
            "first near Skewes ~10^316). Empirical to 10^7; not a proof of RH."
        ),
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # --- summary ---
    print("=" * 70)
    print(f"VERDICT: {verdict}")
    print("=" * 70)
    print(f"{'x':>10} {'pi(x)':>10} {'li(x)':>12} {'li-pi':>10} {'bound':>10} {'ratio':>7}")
    for r in rows:
        mark = "" if r["x"] >= 2657 else "  (*bound n/a, x<2657)"
        print(
            f"{r['x']:>10} {r['pi_x']:>10} {r['li_x']:>12.1f} "
            f"{r['error_li_minus_pi']:>10.1f} {r['schoenfeld_bound']:>10.1f} "
            f"{r['ratio_err_over_bound']:>7.3f}{mark}"
        )
    print(f"\npi(x) matches reference : {pi_all_match}")
    print(f"Schoenfeld bound holds   : {bound_holds} (x>=2657, RH-consistent)")
    print(f"max |error|/sqrt(x)      : {max(r['err_over_sqrtx'] for r in rows):.3f}")
    print("\n*** WARNING — DO NOT EXTRAPOLATE THE li>pi BIAS ***")
    print("li(x)>pi(x) holds on [10^2,10^7], but this is NOT universal.")
    print("Littlewood (1914): the sign of li-pi changes infinitely often.")
    print("First crossover bounded near ~1.4e316 (Bays-Hudson 2000) — ~309 orders")
    print("of magnitude beyond this table. The bias here proves NOTHING about large x.")
    print("\n-> RH buys the smallest error in the PNT: O(sqrt(x) log x). Novelty: none")
    print("   (reproduces classical computations; value is illustrative).")


if __name__ == "__main__":
    main()
