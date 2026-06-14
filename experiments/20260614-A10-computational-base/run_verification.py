"""A-10 verification run — Falsification Ladder Steps 3-8.

Triple-independent verification that the first 100 nontrivial zeros of zeta(s)
lie on Re(s)=1/2:

  Method A  sign-change scan of Hardy Z(t)        (our toolkit, primary)
  Method B  mpmath.zetazero(n)                     (different algorithm)
  Method C  Odlyzko published values              (external source)
  Turing    mp.nzeros(T) total count in strip     (argument principle)

The Turing check is the real RH verification: if #zeros-found-on-line equals
#total-zeros-in-strip, then ALL zeros up to T are on the critical line.

Outputs metrics/run.json. Prints a human-readable summary.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import mpmath as mp

# --- make src/ importable -------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from zeta.reference import ODLYZKO_FIRST_10  # noqa: E402
from zeta.toolkit import (  # noqa: E402
    find_zeros_on_critical_line,
    set_precision,
    zeta,
)

# --- config ---------------------------------------------------------------
DPS = 30
N_TARGET = 100
T_MAX = 250.0  # ~100th zero is near t≈236.5
SCAN_STEP = 0.1  # min zero gap near T_MAX is ~1.1, so 0.1 is safe


def main() -> None:
    set_precision(DPS)
    started = time.time()
    half = mp.mpf(1) / 2

    # --- Method A: independent sign-change scan --------------------------
    print(f"[A] Scanning Hardy Z(t) for sign changes up to t={T_MAX} ...")
    found = find_zeros_on_critical_line(T_MAX, scan_step=SCAN_STEP, max_zeros=N_TARGET)
    print(f"[A] Found {len(found)} zeros on the critical line.")
    if not found:
        raise RuntimeError(f"No zeros found in [0.5, {T_MAX}] with step {SCAN_STEP} — check config")

    # --- Turing completeness: total zeros in strip up to t of last found -
    # WHY: if count-on-line == total-in-strip, every zero up to T is on Re=1/2.
    t_check = float(found[-1].t) + 0.5
    total_in_strip = int(mp.nzeros(t_check))
    print(
        f"[Turing] mp.nzeros({t_check:.3f}) = {total_in_strip} "
        f"(total zeros in strip, argument principle)"
    )

    # --- Method C: external Odlyzko cross-check (first 10) ---------------
    odlyzko = [mp.mpf(v) for v in ODLYZKO_FIRST_10]
    err_vs_odlyzko = [abs(found[i].t - odlyzko[i]) for i in range(len(odlyzko))]
    max_err_odlyzko = max(err_vs_odlyzko)

    # --- Method B: mpmath.zetazero cross-check (first 10) ---------------
    zz = [mp.zetazero(i + 1).imag for i in range(10)]
    err_vs_zz = [abs(found[i].t - zz[i]) for i in range(10)]
    max_err_zz = max(err_vs_zz)

    # --- residuals: |zeta(1/2+it)| at every found zero ------------------
    max_residual = max(found_i.residual for found_i in found)

    # --- Re deviation: by construction we evaluate at Re=1/2 -------------
    # The substantive RH check is the Turing count, not Re (which we fix).
    re_dev = max(abs(z.re - half) for z in found)

    # --- NEGATIVE CONTROLS ----------------------------------------------
    neg = {}
    # (a) zeta(2) = pi^2/6 != 0
    z2 = zeta(mp.mpf(2))
    neg["zeta(2)_value"] = mp.nstr(z2, 15)
    neg["zeta(2)_equals_pi2_over_6"] = bool(abs(z2 - mp.pi**2 / 6) < mp.mpf(10) ** -20)
    # (b) Z(18) — between zeros #1(14.13) and #2(21.02): not a zero
    neg["Z(18)_nonzero"] = bool(abs(mp.siegelz(18)) > mp.mpf("0.1"))
    # (c) zeta(1/2 + 14.0 i) close to but != 0
    near = abs(zeta(half + 1j * mp.mpf("14.0")))
    neg["zeta(0.5+14i)_abs"] = mp.nstr(near, 8)
    neg["zeta(0.5+14i)_nonzero"] = bool(near > mp.mpf("0.001"))

    # --- VERDICT ---------------------------------------------------------
    turing_ok = len(found) == total_in_strip
    odlyzko_ok = max_err_odlyzko < mp.mpf(10) ** -10
    zz_ok = max_err_zz < mp.mpf(10) ** -10
    residual_ok = max_residual < mp.mpf(10) ** -8
    neg_ok = all(
        [
            neg["zeta(2)_equals_pi2_over_6"],
            neg["Z(18)_nonzero"],
            neg["zeta(0.5+14i)_nonzero"],
        ]
    )
    verdict = "PASS" if all([turing_ok, odlyzko_ok, zz_ok, residual_ok, neg_ok]) else "FAIL"

    elapsed = time.time() - started

    result = {
        "experiment": "20260614-A10-computational-base",
        "dps": DPS,
        "n_target": N_TARGET,
        "t_max": T_MAX,
        "scan_step": SCAN_STEP,
        "zeros_found_on_line": len(found),
        "total_zeros_in_strip_turing": total_in_strip,
        "turing_complete_all_on_line": turing_ok,
        "max_err_vs_odlyzko": mp.nstr(max_err_odlyzko, 5),
        "max_err_vs_zetazero": mp.nstr(max_err_zz, 5),
        "max_residual_abs_zeta": mp.nstr(max_residual, 5),
        "max_re_deviation_from_half": mp.nstr(re_dev, 5),
        "negative_controls": neg,
        "checks": {
            "turing_ok": turing_ok,
            "odlyzko_ok": odlyzko_ok,
            "zetazero_ok": zz_ok,
            "residual_ok": residual_ok,
            "negative_controls_ok": neg_ok,
        },
        "verdict": verdict,
        "elapsed_seconds": round(elapsed, 1),
        "first_5_zeros_t": [mp.nstr(found[i].t, 18) for i in range(5)],
    }

    out = Path(__file__).resolve().parent / "metrics" / "run.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- human summary --------------------------------------------------
    print("\n" + "=" * 60)
    print(f"VERDICT: {verdict}")
    print("=" * 60)
    print(f"Zeros found on line : {len(found)}")
    print(f"Total in strip (Turing): {total_in_strip}  -> all on line: {turing_ok}")
    print(f"Max err vs Odlyzko  : {mp.nstr(max_err_odlyzko, 5)}")
    print(f"Max err vs zetazero : {mp.nstr(max_err_zz, 5)}")
    print(f"Max |zeta(1/2+it)|  : {mp.nstr(max_residual, 5)}")
    print(f"Negative controls   : {neg_ok}")
    print(f"Elapsed             : {elapsed:.1f}s")
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
