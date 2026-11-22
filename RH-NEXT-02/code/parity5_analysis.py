"""Analysis of variant B5 exactly as pre-registered in claim_B5.md.
Models A (beta = -0.1418 c), B (beta = -1.1643 log c), C (beta = -0.427 - 0.1267 c) were fitted on c = 13, 23, 37 BEFORE the new data.
"""

import json
import math

import numpy as np

PRED = {
    53: {"A": -0.1418 * 53, "B": -1.1643 * math.log(53), "C": -0.427 - 0.1267 * 53},
    79: {"A": -0.1418 * 79, "B": -1.1643 * math.log(79), "C": -0.427 - 0.1267 * 79},
}
DPS = {(79, 64): 300, (53, 64): 250, (79, 48): 200, (53, 48): 200}
LOG2 = math.log10(2)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


rows = load("../results/parity_B5.jsonl")
bad = [
    r for r in rows if r["n_neg"] != 0 or r["undetermined"] is not None or r["gamma1_ref"] is None
]
print(f"cells: {len(rows)} (expected 80); excluded (n_neg != 0 or undetermined): {len(bad)}")
rows = [r for r in rows if r not in bad]
lam = {(r["D"], r["c"], r["N"]): float(r["lambda_min"]) for r in rows}

print("\nCHECK 5: interlacing lambda(64) <= lambda(48) (tolerance 1e-6):")
viol = [
    (D, c, lam[(D, c, 48)], lam[(D, c, 64)])
    for c in (53, 79)
    for D in sorted({r["D"] for r in rows})
    if (D, c, 48) in lam and (D, c, 64) in lam and lam[(D, c, 64)] > lam[(D, c, 48)] * (1 + 1e-6)
]
print(f"  violations: {len(viol)} {viol[:3] if viol else ''}")

print("\nCHECK 3: reliability (lambda_min < 10^-(dps-60) is flagged and excluded):")
unreliable = {}
for r in rows:
    if r["N"] == 64 and float(r["lambda_min"]) < 10 ** (-(DPS[(r["c"], 64)] - 60)):
        unreliable.setdefault(r["c"], []).append(r["D"])
print(f"  flagged: {unreliable if unreliable else 'none'}")

print("\nCHECK 4: convergence |log10(lambda(64)/lambda(48))| < 1:")
conv = {}
for c in (53, 79):
    Ds = sorted({r["D"] for r in rows if r["c"] == c})
    diffs = {
        D: abs(math.log10(lam[(D, c, 64)] / lam[(D, c, 48)]))
        for D in Ds
        if (D, c, 48) in lam and (D, c, 64) in lam
    }
    conv[c] = {D for D, d in diffs.items() if d < 1}
    worst = sorted(diffs.items(), key=lambda t: -t[1])[:3]
    print(
        f"  c={c}: {len(conv[c])} of {len(diffs)} converged; median |diff| = {np.median(list(diffs.values())):.2f}; largest: {[(D, round(d, 2)) for D, d in worst]}"
    )
    print(
        f"     not converged (D, decades): {sorted((D, round(d, 2)) for D, d in diffs.items() if d >= 1)}"
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
    return beta, se, r2, math.sqrt(s2), n


def fits(label, keep):
    out = {}
    print(f"\n{label}")
    print(
        f"{'c':>3} {'n':>3} {'R2':>6} {'sd':>5} | {'parity(odd)':>15} | {'q per doubling':>15} | {'gamma_1 per unit [t]  (se)':>26}"
    )
    for c in (53, 79):
        rs = [r for r in rows if r["c"] == c and r["N"] == 64 and keep(r)]
        if len(rs) < 8:
            print(f"{c:>3} {len(rs):>3}  (fewer than 8 cells, not fitted)")
            continue
        beta, se, r2, sd, n = fit(rs)
        out[c] = (float(beta[2]), float(se[2]))
        print(
            f"{c:>3} {n:>3} {r2:6.3f} {sd:5.2f} | {beta[3]:+6.2f} [{beta[3] / se[3]:+5.1f}] | {beta[1] * LOG2:+6.2f} [{beta[1] / se[1]:+5.1f}] | {beta[2]:+8.2f} [{beta[2] / se[2]:+5.1f}]  ({se[2]:.2f})"
        )
    return out


main = fits(
    "MAIN FIT (all reliable characters, N=64)", lambda r: r["D"] not in unreliable.get(r["c"], [])
)
conv_fit = fits(
    "SUPPLEMENTARY FIT (converged characters only)",
    lambda r: r["D"] in conv[r["c"]] and r["D"] not in unreliable.get(r["c"], []),
)

print("\nPRE-REGISTERED VERDICT (criterion 1: consistent if |obs - pred| <= 0.25 |pred|):")
if len(main) == 2:
    summary = {}
    for m in "ABC":
        rels = [abs(main[c][0] - PRED[c][m]) / abs(PRED[c][m]) for c in (53, 79)]
        summary[m] = rels
        print(
            f"  model {m}: predictions c=53 {PRED[53][m]:+.2f}, c=79 {PRED[79][m]:+.2f}; observed {main[53][0]:+.2f}, {main[79][0]:+.2f}; relative errors {rels[0]:.2f}, {rels[1]:.2f}; consistent at both: {max(rels) <= 0.25}"
        )
    ok = [m for m in "ABC" if max(summary[m]) <= 0.25]
    if "A" in ok and "C" in ok:
        print(
            "  => A and C are both consistent and indistinguishable at this precision: 'approximately linear in c'"
        )
    elif ok:
        print(f"  => consistent model(s): {ok}")
    else:
        print("  => NO model consistent at both c: none of the three forms is confirmed")
