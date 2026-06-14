"""A-10 visualization — Hardy Z(t) and the zeros on the critical line.

Generates two figures:
  figures/hardy_Z.png        Z(t) on [0,50] with located zeros marked
  figures/zeros_complex.png  the first 100 zeros in the complex plane (all Re=1/2)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from zeta.toolkit import find_zeros_on_critical_line, hardy_Z, set_precision  # noqa: E402

FIG_DIR = Path(__file__).resolve().parent / "figures"


def plot_hardy_z() -> None:
    set_precision(25)
    ts = [i * 0.05 for i in range(int(50 / 0.05) + 1)]
    zs = [float(hardy_Z(t)) for t in ts]
    zeros = find_zeros_on_critical_line(50.0, scan_step=0.1)

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.axhline(0, color="#888", lw=0.8)
    ax.plot(ts, zs, color="#1d4ed8", lw=1.3, label="Hardy Z(t)")
    ax.plot(
        [float(z.t) for z in zeros],
        [0] * len(zeros),
        "o",
        color="#dc2626",
        ms=6,
        label=f"zeros (n={len(zeros)})",
    )
    ax.set_xlabel("t  (imaginary part of s = 1/2 + it)")
    ax.set_ylabel("Z(t)")
    ax.set_title("Hardy Z-function: real zeros = zeros of zeta on Re(s)=1/2")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "hardy_Z.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {FIG_DIR / 'hardy_Z.png'}")


def plot_zeros_complex() -> None:
    set_precision(25)
    zeros = find_zeros_on_critical_line(250.0, scan_step=0.1, max_zeros=100)

    fig, ax = plt.subplots(figsize=(4.8, 9))
    ax.axvline(0.5, color="#16a34a", lw=1.5, ls="--", label="critical line Re=1/2")
    ax.plot(
        [0.5] * len(zeros),
        [float(z.t) for z in zeros],
        "o",
        color="#dc2626",
        ms=4,
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("Re(s)")
    ax.set_ylabel("Im(s)")
    ax.set_title(f"First {len(zeros)} nontrivial zeros\nall on Re(s)=1/2")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "zeros_complex.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {FIG_DIR / 'zeros_complex.png'}")


if __name__ == "__main__":
    print("Generating figures...")
    plot_hardy_z()
    plot_zeros_complex()
    print("Done.")
