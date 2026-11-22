"""Analysis of variant B3 exactly as pre-registered in claim_B3.md.
Reads ../results/parity_B2.jsonl (c = 13, 37 at N = 16) and ../results/parity_B3.jsonl (the 80 new cells).
For each of the six (c, N) sets: OLS  log10(lambda_min) ~ 1 + log10 q + gamma_1 + I(odd), n = 20.
Stability criteria (fixed before the data):
  'robustly detected' : same sign in all six fits, |t| >= 3 in all six, |effect| >= 0.5 decades
                        (effect per doubling of q for the conductor, per unit gamma_1, coefficient of I(odd) for parity)
  'robustly NOT detected' : no fit with |t| >= 3 and |effect| >= 0.5
  otherwise 'unstable' and the sets where it is present are listed.
"""

import json
import math

import numpy as np

LOG2 = math.log10(2)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


rows = load("../results/parity_B2.jsonl") + load("../results/parity_B3.jsonl")
bad = [
    r for r in rows if r["n_neg"] != 0 or r["undetermined"] is not None or r["gamma1_ref"] is None
]
print(f"cells: {len(rows)}; cells with n_neg != 0 or undetermined inertia (excluded): {len(bad)}")
rows = [r for r in rows if r not in bad]
keys = sorted({(r["c"], r["N"]) for r in rows})
print(
    f"(c, N) sets: {keys}; cells per set: {[sum(1 for r in rows if (r['c'], r['N']) == k) for k in keys]}"
)


def fit(rs):
    y = np.array([math.log10(float(r["lambda_min"])) for r in rs])
    lq = np.array([math.log10(r["q"]) for r in rs])
    g = np.array([float(r["gamma1_ref"]) for r in rs])
    odd = np.array([1.0 if r["parity"] == "odd" else 0.0 for r in rs])
    X = np.column_stack([np.ones(len(rs)), lq, g, odd])
    n, k = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = float(res @ res) / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - float(res @ res) / float(((y - y.mean()) ** 2).sum())
    cq = float(np.corrcoef(res, (lq - lq.mean()) ** 2)[0, 1])
    cg = float(np.corrcoef(res, (g - g.mean()) ** 2)[0, 1])
    worst = sorted(zip(res, [r["D"] for r in rs]), key=lambda t: -abs(t[0]))[:2]
    return beta, beta / se, r2, math.sqrt(s2), cq, cg, [(round(float(a), 2), d) for a, d in worst]


results = {}
print("\nPER-SET FITS (coef [t]); conductor shown per doubling of q:")
print(
    f"{'c':>3} {'N':>3} {'R2':>6} {'sd':>5} | {'parity(odd)':>16} | {'q per doubling':>16} | {'gamma_1 per unit':>16} | resid-curvature(q,g) | worst residuals"
)
for k in keys:
    rs = [r for r in rows if (r["c"], r["N"]) == k]
    beta, t, r2, sd, cq, cg, worst = fit(rs)
    results[k] = (beta, t)
    print(
        f"{k[0]:>3} {k[1]:>3} {r2:6.3f} {sd:5.2f} | {beta[3]:+7.2f} [{t[3]:+5.1f}] | {beta[1] * LOG2:+7.2f} [{t[1]:+5.1f}] | {beta[2]:+7.2f} [{t[2]:+5.1f}] | {cq:+.2f} {cg:+.2f} | {worst}"
    )


def stability(idx, scale, label):
    effs = {k: results[k][0][idx] * scale for k in keys}
    ts = {k: results[k][1][idx] for k in keys}
    strong = {k: abs(ts[k]) >= 3 and abs(effs[k]) >= 0.5 for k in keys}
    same = all(e > 0 for e in effs.values()) or all(e < 0 for e in effs.values())
    if all(strong.values()) and same:
        verdict = "ROBUSTLY DETECTED"
    elif not any(strong.values()):
        verdict = "ROBUSTLY NOT DETECTED"
    else:
        verdict = (
            "UNSTABLE (present in: "
            + ", ".join(f"c={k[0]},N={k[1]}" for k in keys if strong[k])
            + ")"
        )
    print(
        f"  {label}: {verdict}; same sign in all six: {same}; strong in {sum(strong.values())} of 6"
    )


print("\nSTABILITY VERDICTS (pre-registered):")
stability(3, 1.0, "parity (odd)")
stability(1, LOG2, "conductor q")
stability(2, 1.0, "first-zero height gamma_1")

print("\nCHECK 1: |log10(lambda_min(N=32) / lambda_min(N=16))| per character, per c (flag > 1):")
by = {(r["D"], r["c"], r["N"]): float(r["lambda_min"]) for r in rows}
flags = []
for c in (13, 23, 37):
    diffs = []
    for D in sorted({r["D"] for r in rows}):
        a, b = by.get((D, c, 16)), by.get((D, c, 32))
        if a and b:
            d = abs(math.log10(b / a))
            diffs.append((d, D))
            if d > 1:
                flags.append((c, D, round(d, 2)))
    diffs.sort(reverse=True)
    print(
        f"  c={c}: median = {np.median([d for d, _ in diffs]):.2f}, max = {diffs[0][0]:.2f} (D={diffs[0][1]})"
    )
print(f"  flagged (N=16 not sufficient, |diff| > 1 decade): {flags if flags else 'none'}")

print(
    "\nCHECK 2: independent agreement, D = -3, c = 23, N = 16: lambda_min =",
    by.get((-3, 23, 16)),
    "(reference from the mpmath-quadrature builder cvs_u.py: 2.2008303e-26)",
)
ref = 2.2008303e-26
v = by.get((-3, 23, 16))
print(
    f"  relative difference = {abs(v - ref) / ref:.2e}  -> {'PASS' if abs(v - ref) / ref <= 1e-3 else 'FAIL'}"
)
