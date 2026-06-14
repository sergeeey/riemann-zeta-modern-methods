"""A-12 visualization — Berry-Keating: density matches, positions do not.

figures/weyl_error.png   Weyl error vs T (log): correct 2pi shrinks, wrong pi grows
figures/fluctuation_S.png  S(T)=N_exact-smooth oscillating about 0 (what xp misses)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = json.loads((HERE / "metrics" / "table.json").read_text())
    T = [r["T"] for r in rows]
    weyl = [r["weyl_err"] for r in rows]
    weyl_wrong = [r["weyl_err_wrong"] for r in rows]
    S = [r["S"] for r in rows]

    # Figure 1: Weyl error, correct vs wrong normalization (log y)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.semilogy(
        T, weyl, "o-", color="#16a34a", ms=4, label="correct norm ℓx·ℓp=2π  (∝ 1/T, shrinks)"
    )
    ax.semilogy(
        T, weyl_wrong, "s--", color="#dc2626", ms=4, label="wrong norm ℓx·ℓp=π  (∝ T, grows)"
    )
    ax.set_xlabel("T (height on critical line)")
    ax.set_ylabel("|Weyl count − exact smooth count|  (log)")
    ax.set_title("Berry-Keating density: right normalization shrinks, wrong one grows")
    ax.legend()
    ax.grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "weyl_error.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'weyl_error.png'}")

    # Figure 2: fluctuation S(T) — what xp does NOT capture
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0, color="#888", lw=0.8)
    ax.plot(T, S, "o-", color="#7c3aed", ms=4, lw=1)
    ax.fill_between(T, S, 0, alpha=0.15, color="#7c3aed")
    ax.set_xlabel("T (height on critical line)")
    ax.set_ylabel("S(T) = N_exact(T) − smooth(T)")
    ax.set_title("Fluctuation S(T) — where the zeros actually sit (xp does NOT reproduce this)")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(HERE / "figures" / "fluctuation_S.png", dpi=130)
    plt.close(fig)
    print(f"  wrote {HERE / 'figures' / 'fluctuation_S.png'}")


if __name__ == "__main__":
    print("Generating figures...")
    main()
    print("Done.")
