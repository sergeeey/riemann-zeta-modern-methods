"""A-07 — Speiser test + Levinson illustration (FL Steps 3-8).

Speiser (1934): RH  <=>  zeta'(s) has NO zeros in 0 < Re(s) < 1/2.

We test this numerically up to Im=50:
  LEFT  of the line (0<Re<1/2): count zeros of zeta' via argument principle.
        Expected 0 (Speiser <=> RH). Contour is STABLE here (no zeros -> no poles).
  RIGHT of the line: locate zeros of zeta' by findroot on a grid (NOT contour:
        the contour integral of zeta''/zeta' is unstable at the poles sitting on
        the zeros themselves — lit-review got 4.06 instead of 5).

Then: first 5 right-side zeros vs literature reference (all Re>1/2).

Levinson context: his method counts zeros of zeta ON the line via zeros of zeta'.
Record is ~41.7% (PRZZ 2020), NOT 100%, due to zeros of zeta' in the strip
1/2 <= sigma < 1/2 + a/log T (structural loss). Empirical fraction is 100%;
proven is 41.7% — the gap is the limit of the PROVABLE, not the observable.
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

# Literature reference: first 5 zeros of zeta'(s) (lit-review, mpmath dps=30)
REF_ZEROS_PRIME = [
    (2.46316, 23.29832),
    (1.28650, 31.70825),
    (2.30757, 38.48998),
    (1.38276, 42.29096),
    (0.96469, 48.84716),
]


def zeta_prime(s):
    return mp.zeta(s, derivative=1)


def zeta_double_prime(s):
    return mp.zeta(s, derivative=2)


def count_zeros_in_rect(re_lo, re_hi, im_lo, im_hi):
    """Argument principle: (1/2pi i) * contour integral of zeta''/zeta'.

    Counts zeros of zeta' inside the rectangle. Stable when no zeros lie ON the
    contour or inside near it (use for the LEFT region where we expect 0).
    """

    def dlog(s):
        return zeta_double_prime(s) / zeta_prime(s)

    a = mp.mpc(re_lo, im_lo)
    b = mp.mpc(re_hi, im_lo)
    c = mp.mpc(re_hi, im_hi)
    d = mp.mpc(re_lo, im_hi)
    total = mp.mpf(0)
    for p, q in [(a, b), (b, c), (c, d), (d, a)]:
        total += mp.quad(lambda u: dlog(p + (q - p) * u) * (q - p), [0, 1])
    return total / (2j * mp.pi)


def find_zeros_right(im_max=50.0, im_search=55.0):
    """Locate zeros of zeta' with Re>1/2, 0<Im<im_max via findroot on a grid.

    WHY im_search > im_max: a zero near the top edge (e.g. Im~48.8) is missed if
    the grid stops right at it; search higher, then keep only Im<im_max. WHY a
    fine Re grid: Muller's method from a far start can skip a root (the 5th zero
    at Re~0.96 was missed by a coarse Re grid).
    """
    found = []
    re_starts = [0.65, 0.8, 0.95, 1.1, 1.3, 1.5, 1.8, 2.1, 2.4, 2.7]
    im = 2.0
    while im < im_search:
        for re in re_starts:
            try:
                root = mp.findroot(zeta_prime, mp.mpc(re, im))
            except Exception:
                continue
            r_re, r_im = float(root.real), float(root.imag)
            if not (0.5 < r_re < 3.5 and 0.5 < r_im < im_search):
                continue
            if any(abs(root - z) < mp.mpf("0.01") for z in found):
                continue
            if abs(zeta_prime(root)) < mp.mpf(10) ** -8:
                found.append(root)
        im += 1.5
    found = [z for z in found if float(z.imag) < im_max]
    found.sort(key=lambda z: z.imag)
    return found


def main() -> None:
    set_precision(30)

    # --- LEFT of line: Speiser test (expect 0) ---
    count_left_25 = count_zeros_in_rect(0.05, 0.5, 0.1, 25.0)
    count_left_50 = count_zeros_in_rect(0.05, 0.5, 0.1, 50.0)
    n_left_25 = int(mp.nint(count_left_25.real))
    n_left_50 = int(mp.nint(count_left_50.real))

    # --- RIGHT of line: locate zeros (findroot grid) ---
    right = find_zeros_right(50.0)
    right_coords = [(round(float(z.real), 5), round(float(z.imag), 5)) for z in right]
    min_re_right = min(float(z.real) for z in right) if right else None

    # --- compare first 5 to reference ---
    matches = []
    for i, ref in enumerate(REF_ZEROS_PRIME):
        if i < len(right):
            got = right[i]
            err = abs(mp.mpc(*ref) - got)
            matches.append(
                {
                    "ref": ref,
                    "got": (round(float(got.real), 5), round(float(got.imag), 5)),
                    "err": float(err),
                    "match": float(err) < 0.01,
                }
            )

    # --- checks ---
    speiser_left_zero = (n_left_25 == 0) and (n_left_50 == 0)
    right_nonempty = len(right) >= 5
    all_right_match = len(matches) == 5 and all(m["match"] for m in matches)
    all_re_above_half = (min_re_right is not None) and (min_re_right > 0.5)

    verdict = (
        "PASS"
        if all([speiser_left_zero, right_nonempty, all_right_match, all_re_above_half])
        else "FAIL"
    )

    result = {
        "experiment": "20260614-A07-levinson-density",
        "speiser_left_of_line": {
            "count_re_below_half_im_to_25": round(float(count_left_25.real), 4),
            "count_re_below_half_im_to_50": round(float(count_left_50.real), 4),
            "rounded_25": n_left_25,
            "rounded_50": n_left_50,
            "is_zero_consistent_with_RH": speiser_left_zero,
        },
        "right_of_line": {
            "n_found_to_im50": len(right),
            "coords": right_coords,
            "min_Re": round(min_re_right, 5) if min_re_right else None,
            "all_Re_above_half": all_re_above_half,
        },
        "first5_vs_reference": matches,
        "levinson_context": {
            "record_fraction_on_line": "41.7% (PRZZ 2020, >5/12)",
            "chain": "Levinson 1/3 (1974) -> Conrey 2/5 (1989) -> BCY 41.05% (2011) -> PRZZ 41.7% (2020)",
            "ceiling_reason": "structural loss: zeros of zeta' in strip 1/2<=sigma<1/2+a/lnT",
            "empirical_fraction": "100% (all known zeros on line)",
            "gap_meaning": "41.7% is the limit of the PROVABLE, 100% is observed",
        },
        "checks": {
            "speiser_left_is_zero": speiser_left_zero,
            "right_has_zeros": right_nonempty,
            "first5_match_reference": all_right_match,
            "all_right_Re_above_half": all_re_above_half,
        },
        "verdict": verdict,
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # --- summary ---
    print("=" * 64)
    print(f"VERDICT: {verdict}")
    print("=" * 64)
    print("SPEISER TEST (RH <=> no zeros of zeta' left of critical line):")
    print(f"  zeros of zeta' in 0<Re<1/2, Im<=25: {float(count_left_25.real):.4f} -> {n_left_25}")
    print(f"  zeros of zeta' in 0<Re<1/2, Im<=50: {float(count_left_50.real):.4f} -> {n_left_50}")
    print(f"  Speiser holds (=0, consistent with RH): {speiser_left_zero}")
    print(f"\nZeros of zeta' RIGHT of line (Im<=50): found {len(right)}, min Re={min_re_right:.4f}")
    for m in matches:
        print(f"  ref={m['ref']}  got={m['got']}  err={m['err']:.2e}  match={m['match']}")
    print(
        f"\nLevinson: proven {result['levinson_context']['record_fraction_on_line']}, "
        f"empirical 100%. Gap = limit of the provable."
    )


if __name__ == "__main__":
    main()
