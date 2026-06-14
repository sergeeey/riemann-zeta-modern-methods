"""A-07 visualization — Speiser: zeros of zeta' all lie RIGHT of the line.

figures/zeta_prime_zeros.png  zeros of zeta' in the complex plane; the region
left of Re=1/2 is empty (Speiser <=> RH), all found zeros have Re>1/2.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    data = json.loads((HERE / "metrics" / "run.json").read_text())
    coords = data["right_of_line"]["coords"]
    re = [c[0] for c in coords]
    im = [c[1] for c in coords]

    fig, ax = plt.subplots(figsize=(7, 7))
    # shade the forbidden (Speiser) region left of the line
    ax.axvspan(0, 0.5, color="#fee2e2", alpha=0.5, label="0<Re<½: NO zeros of ζ′ (Speiser ⟺ RH)")
    ax.axvline(0.5, color="#16a34a", lw=1.6, ls="--", label="critical line Re=½")
    ax.plot(re, im, "o", color="#7c3aed", ms=8, label=f"zeros of ζ′ (n={len(re)})")
    for r, i in zip(re, im):
        ax.annotate(f"  ({r:.2f}, {i:.1f})", (r, i), fontsize=8, va="center")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 52)
    ax.set_xlabel("Re(s)")
    ax.set_ylabel("Im(s)")
    ax.set_title("Speiser test: zeros of ζ′(s) all lie right of Re=½\n(left region empty ⟺ RH)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "zeta_prime_zeros.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'zeta_prime_zeros.png'}")


if __name__ == "__main__":
    print("Generating figure...")
    main()
    print("Done.")
