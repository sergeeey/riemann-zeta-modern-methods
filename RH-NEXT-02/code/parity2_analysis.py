"""Analysis of variant B2 exactly as pre-registered in claim_B2.md (reads ../results/parity_B2.jsonl).
Model per c:  y = log10(lambda_min) ~ 1 + log10(q) + gamma_1 + I(odd), OLS, n = 20 (and a restriction q <= c).
Decision rules (fixed before the data):
  parity effect: same sign at both c, |t| >= 3 at both c, |coef| >= 0.5 decades
  conductor effect: same, with the coefficient per DOUBLING of q (coef_log10q * log10 2) >= 0.5 decades
  zero-height effect: same, per unit of gamma_1 >= 0.5 decades
  if |corr(log q, gamma_1)| > 0.9 or the design condition number > 30: q and gamma_1 are declared NOT separable (their rules are not applied)
Design condition number = cond of [1, standardized(log10 q), standardized(gamma_1), standardized(odd)].
"""

import json
import math

import numpy as np

with open("../results/parity_B2.jsonl", encoding="utf-8") as fh:
    rows = [json.loads(line) for line in fh]
bad = [
    r for r in rows if r["n_neg"] != 0 or r["undetermined"] is not None or r["gamma1_ref"] is None
]
print(f"cells: {len(rows)}; cells with n_neg != 0 or undetermined inertia: {len(bad)}")
rows = [r for r in rows if r not in bad]
LOG2 = math.log10(2)


def ols(rs, label):
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
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(res @ res) / ss_tot
    Z = np.column_stack([np.ones(n)] + [(c - c.mean()) / c.std() for c in (lq, g, odd)])
    cond = float(np.linalg.cond(Z))
    corr_qg = float(np.corrcoef(lq, g)[0, 1])
    corr_qp = float(np.corrcoef(lq, odd)[0, 1])
    corr_gp = float(np.corrcoef(g, odd)[0, 1])
    print(f"\n{label}: n={n}  R^2={r2:.3f}  residual sd={math.sqrt(s2):.2f} decades")
    print(
        f"  corr(log q, gamma_1)={corr_qg:+.2f}  corr(log q, odd)={corr_qp:+.2f}  corr(gamma_1, odd)={corr_gp:+.2f}  design cond={cond:.1f}"
    )
    names = ["intercept", "log10 q", "gamma_1", "odd"]
    for nm, b, e in zip(names, beta, se):
        print(f"  {nm:10s} coef = {b:+8.3f}  se = {e:6.3f}  t = {b / e:+7.2f}")
    return {"beta": beta, "t": beta / se, "corr_qg": corr_qg, "cond": cond, "n": n}


out = {}
for c in (13, 37):
    rs = [r for r in rows if r["c"] == c]
    out[c] = ols(rs, f"c={c}, all characters")
    rs2 = [r for r in rs if r["q"] <= c]
    if len(rs2) >= 8:
        out[(c, "q<=c")] = ols(rs2, f"c={c}, only q <= c")

print("\nDECISION (pre-registered rules, all-characters fits):")
b13, b37 = out[13], out[37]
sep = all(abs(o["corr_qg"]) <= 0.9 and o["cond"] <= 30 for o in (b13, b37))
print(f"  q and gamma_1 separable (|corr| <= 0.9 and cond <= 30 at both c): {sep}")


def decide(idx, scale, label, applicable=True):
    if not applicable:
        print(f"  {label}: not assessed (q and gamma_1 not separable)")
        return
    cs = [b13["beta"][idx] * scale, b37["beta"][idx] * scale]
    ts = [b13["t"][idx], b37["t"][idx]]
    same = (cs[0] > 0) == (cs[1] > 0)
    big = all(abs(t) >= 3 for t in ts) and all(abs(v) >= 0.5 for v in cs)
    print(
        f"  {label}: effect = {cs[0]:+.2f} (c=13), {cs[1]:+.2f} (c=37) decades; t = {ts[0]:+.1f}, {ts[1]:+.1f}; same sign {same}; DETECTED = {same and big}"
    )


decide(3, 1.0, "parity (odd vs even), decades")
decide(1, LOG2, "conductor, decades per doubling of q", sep)
decide(2, 1.0, "first-zero height, decades per unit gamma_1", sep)


print("\nRESIDUAL CHECK (pre-registered: one check of the linear form), all-characters fits:")
for c in (13, 37):
    rs = [r for r in rows if r["c"] == c]
    y = np.array([math.log10(float(r["lambda_min"])) for r in rs])
    lq = np.array([math.log10(r["q"]) for r in rs])
    g = np.array([float(r["gamma1_ref"]) for r in rs])
    odd = np.array([1.0 if r["parity"] == "odd" else 0.0 for r in rs])
    X = np.column_stack([np.ones(len(rs)), lq, g, odd])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    # curvature in log q and in gamma_1: correlation of residuals with the squared centred predictors
    cq = float(np.corrcoef(res, (lq - lq.mean()) ** 2)[0, 1])
    cg = float(np.corrcoef(res, (g - g.mean()) ** 2)[0, 1])
    worst = sorted(zip(res, [r["D"] for r in rs]), key=lambda t: -abs(t[0]))[:3]
    print(
        f"  c={c}: corr(residual, (log q - mean)^2) = {cq:+.2f}; corr(residual, (gamma_1 - mean)^2) = {cg:+.2f}; "
        f"largest residuals (decades, D): {[(round(float(a), 2), d) for a, d in worst]}"
    )
