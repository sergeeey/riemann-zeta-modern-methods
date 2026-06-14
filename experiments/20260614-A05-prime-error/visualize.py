"""A-05 visualization — what RH buys: the prime-counting error term.

figures/error_vs_bound.png  |li(x)-pi(x)| vs the von Koch/Schoenfeld bound (log-log)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = json.loads((HERE / "metrics" / "run.json").read_text())["rows"]
    x = [r["x"] for r in rows]
    abs_err = [r["abs_error"] for r in rows]
    bound = [r["schoenfeld_bound"] for r in rows]
    sqrtx = [math.sqrt(r["x"]) for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.loglog(
        x, bound, "s--", color="#dc2626", ms=5, label="von Koch / Schoenfeld bound  (1/8π)·√x·ln x"
    )
    ax.loglog(x, abs_err, "o-", color="#16a34a", ms=6, label="actual |li(x) − π(x)|")
    ax.loglog(x, sqrtx, ":", color="#888", lw=1, label="√x (reference scale)")
    ax.fill_between(x, abs_err, bound, alpha=0.12, color="#16a34a")
    ax.set_xlabel("x")
    ax.set_ylabel("error (log)")
    ax.set_title(
        "What RH buys: the prime error stays far below the von Koch bound\n"
        "(error ∝ √x·log x — the smallest possible in the PNT)"
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.2, which="both")
    ax.text(
        0.5,
        0.02,
        "Plot shows |error| vs bound, not the sign. li(x)>π(x) here is NOT "
        "universal —\nLittlewood (1914): sign flips ∞ often; first ~10³¹⁶ (Bays–Hudson).",
        transform=ax.transAxes,
        fontsize=7.5,
        color="#666",
        ha="center",
        va="bottom",
        style="italic",
    )
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "error_vs_bound.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'error_vs_bound.png'}")


if __name__ == "__main__":
    print("Generating figure...")
    main()
    print("Done.")
