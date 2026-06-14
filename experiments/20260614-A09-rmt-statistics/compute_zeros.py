"""A-09 step 1 — compute and cache the first N nontrivial zeros.

Saved to metrics/zeros.txt (one imaginary part per line, high precision) so the
analysis and sensitivity runs reuse them without recomputing.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from zeta.toolkit import find_zeros_on_critical_line, set_precision  # noqa: E402

N = 2000
DPS = 20
# N(T)~2000 near T~2520; give headroom.
T_MAX = 2600.0
SCAN_STEP = 0.1  # mean gap near T_MAX ~ 0.8, so 0.1 is safe


def main() -> None:
    set_precision(DPS)
    t0 = time.time()
    print(f"Computing first {N} zeros up to T={T_MAX} (dps={DPS})...")
    zeros = find_zeros_on_critical_line(T_MAX, scan_step=SCAN_STEP, max_zeros=N)
    dt = time.time() - t0
    print(f"Found {len(zeros)} zeros in {dt:.1f}s")

    out = Path(__file__).resolve().parent / "metrics" / "zeros.txt"
    lines = [mp.nstr(z.t, 18) for z in zeros]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} zeros to {out}")
    print(f"First: {lines[0]}")
    print(f"Last:  {lines[-1]}")


if __name__ == "__main__":
    main()
