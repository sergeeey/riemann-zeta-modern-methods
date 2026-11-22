"""Analysis of variant B6 exactly as pre-registered in claim_B6.md.
Best estimate of lambda_min for (c, D):
  - the 14 small-conductor cells (c=37: D=-3,-4; c=53 and 79: D in -3,-4,5,-7,-8,8): the N=96 value if |log10(l96/l64)| < 1, otherwise excluded;
  - every other (c, D) with c in {37, 53, 79}: the N=64 value if |log10(l64/l48)| < 1 (otherwise excluded).
"""

import json
import math

import numpy as np

LOG2 = math.log10(2)
CS = (37, 53, 79)
SMALL = {37: (-3, -4), 53: (-3, -4, 5, -7, -8, 8), 79: (-3, -4, 5, -7, -8, 8)}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


rows = []
for f in ("B2", "B3", "B4", "B5", "B6"):
    rows += load(f"../results/parity_{f}.jsonl")
bad = [
    r for r in rows if r["n_neg"] != 0 or r["undetermined"] is not None or r["gamma1_ref"] is None
]
print(f"cells loaded: {len(rows)}; excluded (n_neg != 0 or undetermined): {len(bad)}")
rows = [r for r in rows if r not in bad]
lam = {(r["D"], r["c"], r["N"]): float(r["lambda_min"]) for r in rows}
meta = {(r["D"], r["c"], r["N"]): r for r in rows}
n96 = [k for k in lam if k[2] == 96]
print(f"N=96 cells present: {len(n96)} of 14 expected")

print("\nCHECK 1: interlacing lambda(96) <= lambda(64):")
v = [
    (D, c, lam[(D, c, 64)], lam[(D, c, 96)])
    for (D, c, N) in n96
    if lam[(D, c, 96)] > lam[(D, c, 64)] * (1 + 1e-6)
]
print(f"  violations: {len(v)} {v[:3] if v else ''}")

print("\nCHECK 2: N=96 vs N=64: |log10(l96/l64)| and convergence (< 1 decade):")
conv96 = {}
for c in CS:
    for D in SMALL[c]:
        if (D, c, 96) in lam:
            d = math.log10(lam[(D, c, 96)] / lam[(D, c, 64)])
            conv96[(D, c)] = abs(d) < 1
            print(
                f"  c={c} D={D:>3}: l64={lam[(D, c, 64)]:.3e}  l96={lam[(D, c, 96)]:.3e}  log10(l96/l64) = {d:+.2f}  {'converged' if abs(d) < 1 else 'NOT converged'}"
            )
        else:
            print(f"  c={c} D={D:>3}: N=96 cell missing (timeout or failure)")
missing = [(D, c) for c in CS for D in SMALL[c] if (D, c, 96) not in lam]
print(
    f"  converged: {sum(conv96.values())} of {len(conv96)}; missing: {missing if missing else 'none'}"
)


def best_rows(c):
    out, dropped = [], []
    for D in sorted({k[0] for k in lam if k[1] == c and k[2] == 64}):
        if D in SMALL[c]:
            if (D, c, 96) in lam and conv96.get((D, c)):
                r = dict(meta[(D, c, 96)])
                out.append(r)
            else:
                dropped.append(D)
        else:
            if (
                abs(math.log10(lam[(D, c, 64)] / lam[(D, c, 48)])) < 1
                if (D, c, 48) in lam
                else True
            ):
                out.append(meta[(D, c, 64)])
            else:
                dropped.append(D)
    return out, dropped


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
    return beta, beta / se, se, r2, math.sqrt(s2), n


def conv64_rows(c):
    return [
        meta[(D, c, 64)]
        for D in sorted({k[0] for k in lam if k[1] == c and k[2] == 64})
        if (D, c, 48) in lam and abs(math.log10(lam[(D, c, 64)] / lam[(D, c, 48)])) < 1
    ]


all64 = {
    c: [meta[(D, c, 64)] for D in sorted({k[0] for k in lam if k[1] == c and k[2] == 64})]
    for c in CS
}
best = {}
print(
    "\nCHECK 4: regression on BEST ESTIMATES (log10 lambda_min ~ 1 + log10 q + gamma_1 + I(odd)):"
)
print(
    f"{'c':>3} {'kept':>4} {'R2':>6} {'sd':>5} | {'parity(odd) [t]':>16} | {'q per doubling [t]':>19} | {'gamma_1 per unit [t] (se)':>27}  dropped"
)
res_best = {}
for c in CS:
    rs, dropped = best_rows(c)
    if len(rs) < 10:
        print(f"{c:>3} {len(rs):>4}  (fewer than 10 characters kept: no fit)  dropped {dropped}")
        continue
    beta, t, se, r2, sd, n = fit(rs)
    res_best[c] = (beta, t)
    print(
        f"{c:>3} {n:>4} {r2:6.3f} {sd:5.2f} | {beta[3]:+7.2f} [{t[3]:+5.1f}] | {beta[1] * LOG2:+8.2f} [{t[1]:+6.1f}] | {beta[2]:+8.2f} [{t[2]:+5.1f}] ({se[2]:.2f})  dropped {dropped}"
    )

print("\nVERDICTS on best estimates (pre-registered rule):")
if len(res_best) == len(CS):
    for idx, scale, name in (
        (3, 1.0, "parity (odd)"),
        (1, LOG2, "conductor q"),
        (2, 1.0, "first-zero height gamma_1"),
    ):
        effs = {c: res_best[c][0][idx] * scale for c in CS}
        strong = {c: abs(res_best[c][1][idx]) >= 3 and abs(effs[c]) >= 0.5 for c in CS}
        same = all(e > 0 for e in effs.values()) or all(e < 0 for e in effs.values())
        vd = (
            "ROBUSTLY DETECTED"
            if all(strong.values()) and same
            else (
                "ROBUSTLY NOT DETECTED"
                if not any(strong.values())
                else "UNSTABLE (present at c = " + ", ".join(str(c) for c in CS if strong[c]) + ")"
            )
        )
        print(f"  {name}: {vd}; same sign at all three c: {same}")
else:
    print("  no verdict: fewer than 10 characters kept at some c")

print("\nCHECK 5: gamma_1 coefficient (decades per unit) under three data choices:")
print(f"{'c':>3} | {'N=64 all 20':>16} | {'N=64 converged only':>20} | {'best estimates':>16}")
for c in CS:
    a = fit(all64[c])
    cv = conv64_rows(c)
    b = fit(cv) if len(cv) >= 8 else None
    bb = res_best.get(c)
    fmt = lambda beta, t: f"{beta[2]:+6.2f} [{t[2]:+5.1f}]"
    print(
        f"{c:>3} | {fmt(a[0], a[1]):>16} | {(fmt(b[0], b[1]) + f' n={b[5]}') if b else 'n/a':>20} | {fmt(*bb) if bb else 'n/a':>16}"
    )
