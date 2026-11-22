"""Diagnostics for the interval-in-c construction (experiment D) and tests of the c_arb guard in cert_chi.build_arb.

Run from RH-NEXT-03/code.  Reproduces: (1) the old string construction of the ball had its lower end
below c (review finding M3); (2) the arb-arithmetic construction keeps the ball strictly inside [c, c+1];
(3) the guard rejects balls that cross an integer; (4) the control: point string and ("23", "0") agree.
"""

import cert_chi as cc
from cont_bench import window_ball
from flint import arb, ctx

prec, N = 1500, 16
ctx.prec = prec

print("(1) old construction from decimal strings: lower end relative to c = 23")
for k in (60, 30, 10, 3):
    w = arb(10) ** (-k)
    mid = (arb(23) + w / 2).str(40 + k, radius=False)
    rad = (w / 2).str(10, radius=False)
    cb = arb(mid, rad)
    print(
        f"  k={k}: lower-23 = {float(cb.lower() - 23):+.2e}, upper-23 = {float(cb.upper() - 23):+.2e}, radius = {float(cb.rad()):.3e} (requested {float(w / 2):.3e})"
    )

print("(2) new construction window_ball(23, k): [23 + 0.1 w, 23 + 1.1 w]")
for k in (60, 30, 10, 3):
    cb = window_ball(23, k)
    w = float(arb(10) ** (-k))
    print(
        f"  k={k}: (lower-23)/w = {float((cb.lower() - 23) * arb(10) ** k):.4f} (expect 0.1), (upper-23)/w = {float((cb.upper() - 23) * arb(10) ** k):.4f} (expect 1.1), radius/w = {float(cb.rad()) / w:.4f}"
    )
    cc.build_arb("chi3", 23, N, prec, c_arb=cb)  # must not raise

print("(3) guard: balls that cross an integer or leave [c, c+1] must raise ValueError")
cases = {
    "crosses c from below  [22.999, 23.001]": arb(23, "0.001"),
    "contains c+1 side     [23.5, 24.5]": arb("24", "0.5"),
    "inside [23, 24]       [23.2, 23.4]": arb("23.3", "0.1"),
    "exact left end        23": arb(23),
    "exact right end       24": arb(24),
}
for label, ball in cases.items():
    try:
        cc.build_arb("chi3", 23, 4, 300, c_arb=ball)
        print(f"  {label}: accepted")
    except ValueError:
        print(f"  {label}: REJECTED")

print("(4) control: the same point as a string and as a degenerate tuple")
A, DIM, K = cc.build_arb("chi3", 23, N, prec, c_arb="23")
print("  point '23':", cc.ldlt_inertia(A, DIM)[:3])
A, DIM, K = cc.build_arb("chi3", 23, N, prec, c_arb=("23", "0"))
print("  tuple ('23','0'):", cc.ldlt_inertia(A, DIM)[:3])
