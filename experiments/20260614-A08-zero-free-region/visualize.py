"""A-08 visualization — the zero-free boundary moves AWAY from Re=1/2.

figures/zfr_gap.png  sigma_zf(t) (classical & VK) climbing toward Re=1, the
critical line Re=1/2 with real zeros, and the widening gap between them.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = json.loads((HERE / "metrics" / "run.json").read_text())["rows"]
    lt = [r["log10_t"] for r in rows]
    sc = [r["sigma_classical"] for r in rows]
    sv = [r["sigma_vk"] for r in rows]

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    # critical line + real zeros (illustrative dots along Re=1/2)
    ax.axhline(0.5, color="#16a34a", lw=1.8, label="Re=½ — where the zeros actually are")
    ax.plot(lt, [0.5] * len(lt), "o", color="#16a34a", ms=5)
    # zero-free boundaries
    ax.plot(
        lt, sc, "s-", color="#dc2626", ms=5, label="proven ZFR boundary σ_zf (classical, R=5.5587)"
    )
    ax.plot(lt, sv, "^--", color="#ea580c", ms=5, label="VK boundary (wider only at t>10³⁸⁷⁷)")
    # the gap
    ax.fill_between(lt, sc, 0.5, alpha=0.12, color="#dc2626")
    ax.annotate(
        "GAP grows →\n(boundary moves toward Re=1,\nnot toward ½)",
        xy=(130, 0.75),
        fontsize=9,
        color="#b91c1c",
        ha="center",
    )
    ax.set_xlabel("log₁₀(t)")
    ax.set_ylabel("Re(s) = σ")
    ax.set_ylim(0.45, 1.02)
    ax.set_title(
        "Zero-free region: the proven boundary climbs toward Re=1\n"
        "the gap to Re=½ GROWS with t — it never approaches the critical line"
    )
    ax.legend(loc="center right", fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "zfr_gap.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'zfr_gap.png'}")


if __name__ == "__main__":
    print("Generating figure...")
    main()
    print("Done.")
