"""B-06 — Speiser criterion extended to larger T (reuses A-07's stable contour method).

Speiser (1934): RH <=> zeta'(s) has NO zeros in the open strip 0 < Re(s) < 1/2.

A-07 (experiments/20260614-A07-levinson-density/run_speiser.py) verified this up
to Im=50 via the argument principle: (1/2pi i) * contour_integral(zeta''/zeta').
That contour method is STABLE on the LEFT side (no zeros expected there -> no
poles of zeta''/zeta' near the contour). The RIGHT-side grid findroot search was
explicitly noted there as fragile (poles sit on the zeros themselves) — we do
NOT extend that part; extending the right-side zero catalogue is a different,
harder task than testing the Speiser criterion itself.

This script ONLY extends the LEFT-side count (the actual Speiser/RH-relevant
test) to larger T, reusing the exact same stable method, not reimplementing it.
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


def zeta_prime(s):
    return mp.zeta(s, derivative=1)


def zeta_double_prime(s):
    return mp.zeta(s, derivative=2)


def count_zeros_in_rect(re_lo, re_hi, im_lo, im_hi):
    """Argument principle: (1/2pi i) * contour integral of zeta''/zeta'.

    Identical method to A-07's run_speiser.py:count_zeros_in_rect — reused
    verbatim (not reimplemented) since that version already passed skeptic +
    reviewer review for the LEFT-side (stable) case.
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


def main() -> None:
    set_precision(30)

    # A-07 already established T=25, T=50 give count=0. Extend the ladder.
    T_LADDER = [50.0, 100.0, 200.0, 400.0, 800.0]
    results = []
    for T in T_LADDER:
        count = count_zeros_in_rect(0.05, 0.5, 0.1, T)
        n = int(mp.nint(count.real))
        # WHY: a non-negligible imaginary part or a real part far from an
        # integer signals numerical instability (a zero near the contour),
        # not necessarily a genuine Speiser violation — flag it, don't hide it.
        residual = abs(count.real - n) + abs(count.imag)
        results.append(
            {
                "T": T,
                "raw_count": (round(float(count.real), 6), round(float(count.imag), 6)),
                "rounded": n,
                "residual_from_integer": round(float(residual), 6),
                "stable": residual < 0.01,
                "consistent_with_RH": n == 0,
            }
        )
        print(f"T={T:>6.1f}  count={complex(count):.6f}  rounded={n}  stable={residual < 0.01}")

    all_stable = all(r["stable"] for r in results)
    all_zero = all(r["consistent_with_RH"] for r in results)
    verdict = "PASS" if (all_stable and all_zero) else "FALSIFIED-or-unstable"

    output = {
        "experiment": "20260719-B06-speiser-extended-T",
        "method": "reused from experiments/20260614-A07-levinson-density/run_speiser.py "
        "(count_zeros_in_rect, argument principle, LEFT side only)",
        "ladder": results,
        "all_numerically_stable": all_stable,
        "all_consistent_with_RH": all_zero,
        "verdict": verdict,
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("=" * 64)
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
