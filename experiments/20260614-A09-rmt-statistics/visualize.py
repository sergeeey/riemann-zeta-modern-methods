"""A-09 visualization — NNSD of zeta zeros vs GUE and Poisson.

figures/nnsd.png        histogram of unfolded spacings + GUE curve + Poisson curve
figures/nnsd_neg.png    same for the synthetic Poisson control (sanity)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from run_rmt_analysis import (  # noqa: E402
    gue_pdf,
    poisson_pdf,
    synthetic_poisson_like,
    unfold,
)


def _plot(delta: np.ndarray, title: str, fname: str, data_label: str) -> None:
    s = np.linspace(0, 4, 400)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(
        delta,
        bins=40,
        range=(0, 4),
        density=True,
        color="#cbd5e1",
        edgecolor="#94a3b8",
        label=f"{data_label} (n={len(delta)})",
    )
    ax.plot(s, gue_pdf(s), color="#dc2626", lw=2.2, label="GUE (Wigner surmise)")
    ax.plot(s, poisson_pdf(s), color="#2563eb", lw=2.2, ls="--", label="Poisson")
    ax.set_xlabel("normalized spacing  s")
    ax.set_ylabel("probability density")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(HERE / "figures" / fname, dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / fname}")


def main() -> None:
    gammas = np.array([float(x) for x in (HERE / "metrics" / "zeros.txt").read_text().split()])
    print("Generating figures...")
    _plot(
        unfold(gammas),
        "Zeta zero spacings: closer to GUE than Poisson",
        "nnsd.png",
        "zeta zeros",
    )

    synth = synthetic_poisson_like(len(gammas) - 1)
    _plot(
        unfold(synth),
        "Negative control: synthetic Poisson -> Poisson",
        "nnsd_neg.png",
        "synthetic Poisson",
    )
    print("Done.")


if __name__ == "__main__":
    main()
