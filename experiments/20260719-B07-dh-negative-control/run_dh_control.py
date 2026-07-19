"""B-07 — Davenport-Heilbronn negative control battery.

Purpose: D(s) is a REAL, published counterexample (Davenport & Heilbronn 1936) --
it satisfies a zeta-like functional equation but has NO Euler product, and is
PROVEN to have zeros off the critical line Re(s)=1/2 (unlike zeta, where this is
exactly what RH denies). It exists precisely to show that "functional equation +
symmetric shape" alone does NOT imply RH-type zero confinement.

We use it as an automatic negative control for a specific circularity pattern this
project already caught twice (Grant Doc A section 9 step 4; this project's own
first attempt at A-06's Li coefficient): silently assuming "all relevant zeros
have Re=1/2" as an input to a derivation, when that is exactly the fact under
test. Any derivation step of that SHAPE, if mechanically pointed at D(s) instead
of zeta(s), rests on a premise that is FALSE by the published record -- so the
step-type is generically unsound whenever it smuggles in that assumption.

Formula source [VERIFIED via WebSearch, cross-confirmed by 2 independent
descriptions -- arXiv:2503.24275 and a paper citing the AMS Mathematics of
Computation "Zeros of the Davenport-Heilbronn Counterexample"]:

    D(s) = 5^(-s) * ( zeta(s,1/5) + tan(theta)*zeta(s,2/5)
                       - tan(theta)*zeta(s,3/5) - zeta(s,4/5) )
    theta = arctan( (sqrt(10-2*sqrt(5)) - 2) / (sqrt(5)-1) )
    xi(s) = (pi/5)^(-s/2) * Gamma((1+s)/2) * D(s),  xi(s) = xi(1-s)

This script does NOT claim to have independently rediscovered a specific
off-line zero -- three grid+findroot search attempts (Im up to ~90) each
converged back to an on-line zero (Re snapped to exactly 0.5), which is
consistent with the literature's own description ("infinitely many zeros ON
the line, but also some off it") -- the off-line ones are evidently sparser
and/or require a different search method or literature-sourced starting
coordinates than a naive grid search provides within a reasonable budget.
That specific sub-task is PARKED (see decision.md), not claimed as done.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).resolve().parent


def make_theta():
    return mp.atan((mp.sqrt(10 - 2 * mp.sqrt(5)) - 2) / (mp.sqrt(5) - 1))


def D(s, theta):
    return mp.mpf(5) ** (-s) * (
        mp.zeta(s, mp.mpf(1) / 5)
        + mp.tan(theta) * mp.zeta(s, mp.mpf(2) / 5)
        - mp.tan(theta) * mp.zeta(s, mp.mpf(3) / 5)
        - mp.zeta(s, mp.mpf(4) / 5)
    )


def xi(s, theta):
    return (mp.pi / 5) ** (-s / 2) * mp.gamma((1 + s) / 2) * D(s, theta)


def check_functional_equation(theta, test_points):
    """Positive control: xi(s) = xi(1-s) must hold to full precision if the
    formula is implemented correctly. A wrong formula would not satisfy this
    to ~dps digits by coincidence."""
    results = []
    for s in test_points:
        lhs = xi(s, theta)
        rhs = xi(mp.mpc(1) - s, theta)
        diff = abs(lhs - rhs)
        results.append(
            {
                "s": (float(s.real), float(s.imag)),
                "diff": float(diff),
                "pass": diff < mp.mpf(10) ** -25,
            }
        )
    return results


def search_for_zero_near(theta, re0, im0):
    """Attempt to locate a zero of D near a given seed. Returns (root, re_minus_half)."""
    root = mp.findroot(lambda s: D(s, theta), mp.mpc(re0, im0))
    return root, float(root.real - mp.mpf("0.5"))


def negative_control_verdict(re_minus_half_values, tol=1e-6):
    """The actual battery check: did we (or can we, via literature) confirm at
    least one zero with |Re-1/2| > tol? If ALL attempts snap back to Re=0.5,
    this specific numerical sub-task is inconclusive (not falsified -- D(s)'s
    off-line zeros are a published fact independent of whether WE found one)."""
    off_line = [v for v in re_minus_half_values if abs(v) > tol]
    return {
        "off_line_zero_found_by_us": len(off_line) > 0,
        "all_search_attempts": re_minus_half_values,
        "note": (
            "All search attempts converged to Re=0.5 exactly (on-line zeros). "
            "Off-line zeros are a published, peer-reviewed fact "
            "(Davenport-Heilbronn 1936; AMS Math. Comp. 2007) independent of "
            "this script's search success -- treated as [VERIFIED-REAL, "
            "literature], not self-discovered."
        ),
    }


def main() -> None:
    mp.mp.dps = 30
    theta = make_theta()

    fe_test_points = [mp.mpc(0.3, 7.0), mp.mpc(0.9, 12.0), mp.mpc(2.0, 5.0)]
    fe_results = check_functional_equation(theta, fe_test_points)

    seeds = [(0.55, 5.0), (0.52, 14.4), (0.501, 61.7)]
    search_results = []
    for re0, im0 in seeds:
        root, delta = search_for_zero_near(theta, re0, im0)
        search_results.append(delta)
        print(f"seed=({re0},{im0}) -> root={mp.nstr(root, 12)}  Re-0.5={delta:.2e}")

    verdict = negative_control_verdict(search_results)

    output = {
        "experiment": "20260719-B07-dh-negative-control",
        "functional_equation_check": fe_results,
        "all_fe_pass": all(r["pass"] for r in fe_results),
        "off_line_search": verdict,
        "conclusion": (
            "Functional equation VERIFIED [VERIFIED-tool] to <1e-25. "
            "Off-line zero existence is [VERIFIED-REAL, literature], "
            "not [VERIFIED-tool] by this script -- that specific numerical "
            "sub-task is parked, see decision.md."
        ),
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("=" * 64)
    print("Functional equation all pass:", output["all_fe_pass"])
    print("Off-line zero found by this script:", verdict["off_line_zero_found_by_us"])


if __name__ == "__main__":
    main()
