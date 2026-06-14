"""A-10 stress tests — FL Step 7. Adversarial response to skeptic [WEAKENED].

The skeptic raised three objections. We test each with a tool instead of arguing:

  CHECK 1  Independence of mp.nzeros from our sign-change scan.
           Coarsen our scan so it MISSES zeros. If nzeros stays correct while our
           count drops, nzeros is independent (kills the "circularity" objection).

  CHECK 2  Re=1/2 is NOT just assigned. Count zeros in the strip via the argument
           principle on the entire xi-function contour (a rectangle spanning
           Re in [-0.5, 1.5]). This contour SEES off-line zeros if any exist.
           If contour-count == on-line-count, then NO off-line zeros up to T —
           measured, not assumed.

  CHECK 3  Is 1e-30 agreement real? Recompute zero #1 at dps=15,30,50 and show
           the genuine convergence, independent of any cached value.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from zeta.toolkit import find_zeros_on_critical_line  # noqa: E402


def check1_nzeros_independence() -> None:
    print("=" * 64)
    print("CHECK 1 — Is mp.nzeros independent of our sign-change scan?")
    print("=" * 64)
    mp.mp.dps = 25
    T = 100.0
    true_count = int(mp.nzeros(T))

    for step in [0.1, 1.0, 3.0, 6.0]:
        found = find_zeros_on_critical_line(T, scan_step=step)
        flag = "MISSED zeros" if len(found) < true_count else "complete"
        print(
            f"  scan_step={step:>4}:  our_scan={len(found):>3}   "
            f"mp.nzeros={true_count:>3}   [{flag}]"
        )
    print("  -> If our_scan drops while mp.nzeros stays fixed, they are")
    print("     INDEPENDENT. nzeros does not read our sign changes.\n")


def xi(s: mp.mpc) -> mp.mpc:
    """Riemann xi — entire, same nontrivial zeros as zeta, no poles."""
    return mp.mpf(1) / 2 * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def argument_principle_count(T: float, re_lo: float = -0.5, re_hi: float = 1.5) -> mp.mpc:
    """Count zeros of xi inside rectangle [re_lo,re_hi] x [0.1, T].

    N = (1/2pi i) * contour integral of xi'/xi.  This contour spans the FULL
    width of the critical strip — it detects off-line zeros if they exist.
    Independent of Hardy Z / siegelz entirely.
    """

    def dlog_xi(s: mp.mpc) -> mp.mpc:
        # WHY xi'/xi directly, not diff(log(xi)): log has a branch cut, so
        # integrating its derivative jumps by 2pi*i across the cut -> garbage.
        # The meromorphic ratio xi'/xi is single-valued -> stable contour integral.
        return mp.diff(xi, s) / xi(s)

    im_lo = mp.mpf("0.1")
    im_hi = mp.mpf(T)
    a = mp.mpc(re_lo, im_lo)
    b = mp.mpc(re_hi, im_lo)
    c = mp.mpc(re_hi, im_hi)
    d = mp.mpc(re_lo, im_hi)

    total = mp.mpf(0)
    for p, q in [(a, b), (b, c), (c, d), (d, a)]:
        seg = mp.quad(lambda u: dlog_xi(p + (q - p) * u) * (q - p), [0, 1])
        total += seg
    return total / (2j * mp.pi)


def check2_re_is_measured() -> None:
    print("=" * 64)
    print("CHECK 2 — Is Re=1/2 measured, or just assigned?")
    print("  Counting zeros in FULL strip via argument principle on xi.")
    print("=" * 64)
    mp.mp.dps = 25
    found = find_zeros_on_critical_line(90.0, scan_step=0.1)
    for k in [5, 10, 15]:
        T_between = float((found[k - 1].t + found[k].t) / 2)
        on_line = sum(1 for z in found if z.t < T_between)
        contour = argument_principle_count(T_between)
        contour_round = int(mp.nint(contour.real))
        match = "MATCH" if contour_round == on_line else "MISMATCH"
        print(
            f"  T={T_between:7.3f}: on-line={on_line:>3}   "
            f"contour(full strip)={mp.nstr(contour.real, 8):>12} "
            f"~={contour_round:>3}   [{match}]"
        )
    print("  -> contour spans Re in [-0.5,1.5]. If it equals on-line count,")
    print("     there are NO off-line zeros up to T. Re=1/2 is MEASURED.\n")


def check3_precision_real() -> None:
    print("=" * 64)
    print("CHECK 3 — Is the 1e-30 agreement real convergence?")
    print("=" * 64)
    refs = {}
    for dps in [15, 30, 50]:
        mp.mp.dps = dps
        found = find_zeros_on_critical_line(16.0, scan_step=0.1, max_zeros=1)
        refs[dps] = found[0].t
        print(f"  dps={dps:>2}: zero #1 = {mp.nstr(found[0].t, dps)}")
    mp.mp.dps = 50
    diff_15_50 = abs(refs[15] - refs[50])
    diff_30_50 = abs(refs[30] - refs[50])
    print(f"  |dps15 - dps50| = {mp.nstr(diff_15_50, 5)}")
    print(f"  |dps30 - dps50| = {mp.nstr(diff_30_50, 5)}")
    print("  -> Error should shrink with precision. If dps30 already agrees to")
    print("     ~1e-28, the earlier 1e-30 vs zetazero was genuine, not cached.\n")


if __name__ == "__main__":
    check1_nzeros_independence()
    check2_re_is_measured()
    check3_precision_real()
