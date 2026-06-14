"""A-06 visualization — Robin & Li criteria (RH from the arithmetic side).

figures/robin.png  Robin ratio sigma(n)/(e^gamma n lnln n) vs n; threshold 1;
                   exceptions (>=1) all at n<=5040, extremal at 5040.
figures/li.png     Li coefficients lambda_n > 0 for n=1..20.
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
    exceptions = set(data["robin"]["exceptions"])

    # Robin: recompute a sparse curve for the plot (exact values are in run.json logic;
    # here we just need shape) — read from a quick recompute via stored exceptions.
    import sympy
    import mpmath as mp

    mp.mp.dps = 20
    eg = float(mp.e**mp.euler)
    import math

    ns = list(range(3, 10001, 1))
    ratios = [float(sympy.divisor_sigma(n)) / (eg * n * math.log(math.log(n))) for n in ns]

    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.axhline(1.0, color="#dc2626", lw=1.5, ls="--", label="Robin threshold = 1 (RH boundary)")
    ax.plot(ns, ratios, color="#2563eb", lw=0.6, alpha=0.7)
    exc_n = [n for n in ns if n in exceptions]
    exc_r = [float(sympy.divisor_sigma(n)) / (eg * n * math.log(math.log(n))) for n in exc_n]
    ax.plot(
        exc_n,
        exc_r,
        "o",
        color="#dc2626",
        ms=5,
        label=f"exceptions ≥1 (all n≤5040, count={len(exceptions)})",
    )
    ax.axvline(5040, color="#16a34a", lw=1, ls=":", label="n=5040 (last & extremal)")
    ax.set_xscale("log")
    ax.set_xlabel("n (log)")
    ax.set_ylabel("σ(n) / (e^γ·n·ln ln n)")
    ax.set_title("Robin's criterion: σ(n) ratio dips below 1 for n>5040 (⟺ RH)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "robin.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'robin.png'}")

    # Li
    lambdas = data["li"]["lambdas"]
    n = [d["n"] for d in lambdas]
    lam = [d["lambda_n (2000 zeros, assumes Re=1/2)"] for d in lambdas]
    lam1_indep = data["li"]["lambda_1_independent"]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0, color="#888", lw=0.8)
    ax.bar(
        n,
        lam,
        color="#cbd5e1",
        edgecolor="#94a3b8",
        alpha=0.9,
        label="λ_n from zeros (ASSUMES Re=½ — illustrative, circular as RH test)",
    )
    ax.plot(
        [1],
        [lam1_indep],
        "o",
        color="#16a34a",
        ms=10,
        label=f"λ₁ INDEPENDENT = {lam1_indep:.4f} (zero-free, genuine >0)",
    )
    ax.set_xlabel("n")
    ax.set_ylabel("λ_n")
    ax.set_title(
        "Li's criterion: only λ₁ (zero-free closed form) is a genuine RH datapoint;\n"
        "λ_n from zeros assume Re=½ (skeptic: circular)"
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "li.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'li.png'}")


if __name__ == "__main__":
    print("Generating figures...")
    main()
    print("Done.")
