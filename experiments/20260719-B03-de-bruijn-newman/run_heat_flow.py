"""B-03 -- de Bruijn-Newman heat flow: track a zero of H_t(x) across t.

H_t(x) := integral_0^inf e^{t*u^2} * Phi(u) * cos(x*u) du
Phi(u) := sum_{n=1}^inf (2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}) * exp(-pi*n^2*e^{4u})

[VERIFIED via WebSearch, consistent across MathWorld/Wikipedia/arXiv:1801.05914]
H_0's real zeros correspond to zeta zeros on the critical line via x = 2*gamma
(gamma = Im(rho) for a zeta zero rho = 1/2+i*gamma) -- confirmed numerically
below against the first two published zeta zeros (14.134725..., 21.022040...).

The de Bruijn-Newman constant Lambda is defined so H_t has ONLY real zeros for
t >= Lambda. RH <=> Lambda <= 0. Rodgers-Tao (2018) proved Lambda >= 0 using a
GUE-repulsion argument. Currently known: 0 <= Lambda < 1/2.

Scope of this atom (illustrative, not a new mathematical result): track how a
SINGLE, well-separated zero (2*gamma_1, from the first zeta zero) moves as t
varies through a small range around 0. This demonstrates the heat-flow
deformation exists and is smooth for this zero -- it does NOT attempt to find
a close (Lehmer-type) pair or demonstrate the actual real-to-complex
transition mechanism Rodgers-Tao's proof concerns (that would need locating an
anomalously close pair first, a separate, harder search -- see decision.md).
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).resolve().parent

# Published zeta zero imaginary parts (Odlyzko tables, same source already used
# in src/zeta/reference.py) -- used only for scale calibration (x = 2*gamma).
GAMMA_1 = mp.mpf("14.134725141734693790")
GAMMA_2 = mp.mpf("21.022039638771554993")


def Phi(u, n_terms=5):
    total = mp.mpf(0)
    for n in range(1, n_terms + 1):
        term = (
            2 * mp.pi**2 * n**4 * mp.e ** (9 * u) - 3 * mp.pi * n**2 * mp.e ** (5 * u)
        ) * mp.e ** (-mp.pi * n**2 * mp.e ** (4 * u))
        total += term
    return total


def H(t, x, u_max=4.0):
    def integrand(u):
        return mp.e ** (t * u**2) * Phi(u) * mp.cos(x * u)

    return mp.quad(integrand, [0, u_max])


def calibration_check():
    """Positive control: H_0 must vanish at x=2*gamma_1 and x=2*gamma_2."""
    results = []
    for gamma, label in [(GAMMA_1, "gamma_1"), (GAMMA_2, "gamma_2")]:
        x = 2 * gamma
        val = H(0, x)
        results.append({"label": label, "x": float(x), "H_0(x)": float(val)})
    return results


def track_zero(seed_x, t_values):
    """Follow one zero of H_t across a ladder of t values, seeding each
    findroot from the previous result (continuity assumption -- valid for a
    smoothly-varying, well-separated zero)."""
    seed = seed_x
    track = []
    for t in t_values:
        root = mp.findroot(lambda x: H(t, x), seed)
        track.append({"t": t, "x": float(root.real if hasattr(root, "real") else root)})
        seed = root
    return track


def main() -> None:
    mp.mp.dps = 25

    calib = calibration_check()
    print("Calibration (H_0 at x=2*gamma_n, expect ~0):")
    for c in calib:
        print(f"  {c['label']}: x={c['x']:.6f}  H_0(x)={c['H_0(x)']:.3e}")

    t_values = [-0.05, -0.02, 0.0, 0.02, 0.05]
    seed = float(2 * GAMMA_1)
    track = track_zero(mp.mpf(seed), t_values)
    print("\nZero track (seed = 2*gamma_1):")
    for row in track:
        print(f"  t={row['t']:+.3f}  x={row['x']:.10f}")

    xs = [row["x"] for row in track]
    monotone = all(xs[i] > xs[i + 1] for i in range(len(xs) - 1))

    output = {
        "experiment": "20260719-B03-de-bruijn-newman",
        "calibration": calib,
        "calibration_pass": all(abs(c["H_0(x)"]) < 1e-8 for c in calib),
        "zero_track": track,
        "monotone_decrease_with_t": monotone,
        "scope_note": (
            "Illustrates smooth real-axis motion of ONE well-separated zero. "
            "Does NOT search for or track a close (Lehmer-type) pair, and does "
            "NOT itself demonstrate the Rodgers-Tao real-to-complex mechanism "
            "-- see decision.md."
        ),
    }
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\nCalibration pass:", output["calibration_pass"])
    print("Monotone decrease with t:", monotone)


if __name__ == "__main__":
    main()
