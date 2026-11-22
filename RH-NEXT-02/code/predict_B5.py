"""Pre-registration helper for variant B5: fit competing scaling laws for the gamma_1 coefficient on the EXISTING data
(c = 13, 23, 37 at N = 64) and print their predictions for c = 53 and 79.  Run BEFORE the new cells are computed.
Models for beta(c) = coefficient of gamma_1 (decades per unit) in  log10 lambda_min ~ 1 + log10 q + gamma_1 + I(odd):
  A: beta = k * c            (through the origin)
  B: beta = k * log c        (through the origin)
  C: beta = a + b * c        (affine in c)
"""

import json
import math

import numpy as np


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


rows = (
    load("../results/parity_B2.jsonl")
    + load("../results/parity_B3.jsonl")
    + load("../results/parity_B4.jsonl")
)
CS = (13, 23, 37)
beta = {}
for c in CS:
    rs = [r for r in rows if r["c"] == c and r["N"] == 64]
    y = np.array([math.log10(float(r["lambda_min"])) for r in rs])
    X = np.column_stack(
        [
            np.ones(len(rs)),
            [math.log10(r["q"]) for r in rs],
            [float(r["gamma1_ref"]) for r in rs],
            [1.0 if r["parity"] == "odd" else 0.0 for r in rs],
        ]
    )
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    beta[c] = float(b[2])
print("observed gamma_1 coefficients at N=64:", {c: round(v, 3) for c, v in beta.items()})
c_arr = np.array(CS, dtype=float)
b_arr = np.array([beta[c] for c in CS])
kA = float((b_arr * c_arr).sum() / (c_arr**2).sum())
L_arr = np.log(c_arr)
kB = float((b_arr * L_arr).sum() / (L_arr**2).sum())
bC, aC = np.polyfit(c_arr, b_arr, 1)
print(
    f"A: beta = {kA:.4f} * c        residuals on the 3 points: {[round(float(x), 2) for x in b_arr - kA * c_arr]}"
)
print(
    f"B: beta = {kB:.4f} * log c    residuals on the 3 points: {[round(float(x), 2) for x in b_arr - kB * L_arr]}"
)
print(
    f"C: beta = {aC:.3f} + {bC:.4f} * c  residuals on the 3 points: {[round(float(x), 2) for x in b_arr - (aC + bC * c_arr)]}"
)
print("\nPREDICTIONS (decades per unit gamma_1):")
for c in (53, 79):
    print(f"  c={c}:  A {kA * c:+.2f}   B {kB * math.log(c):+.2f}   C {aC + bC * c:+.2f}")
