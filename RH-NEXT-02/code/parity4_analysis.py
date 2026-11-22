"""Analysis of variant B4 exactly as pre-registered in claim_B4.md.
Reads parity_B2.jsonl (N=16, c=13,37), parity_B3.jsonl (N=32 and N=16 at c=23) and parity_B4.jsonl (N=48, 64).
"""

import json
import math

import numpy as np

LOG2 = math.log10(2)
NS = (16, 32, 48, 64)
CS = (13, 23, 37)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


rows = (
    load("../results/parity_B2.jsonl")
    + load("../results/parity_B3.jsonl")
    + load("../results/parity_B4.jsonl")
)
bad = [
    r for r in rows if r["n_neg"] != 0 or r["undetermined"] is not None or r["gamma1_ref"] is None
]
print(f"cells: {len(rows)}; excluded (n_neg != 0 or undetermined inertia): {len(bad)}")
rows = [r for r in rows if r not in bad]
lam = {(r["D"], r["c"], r["N"]): float(r["lambda_min"]) for r in rows}
meta = {r["D"]: r for r in rows}
Ds = sorted(meta)
n64 = sum(1 for r in rows if r["N"] == 64)
n48 = sum(1 for r in rows if r["N"] == 48)
print(f"cells at N=48: {n48}, at N=64: {n64} (expected 60 each)")

print(
    "\nCHECK 1: monotonicity lambda(16) >= lambda(32) >= lambda(48) >= lambda(64) (relative tolerance 1e-6):"
)
viol = []
for D in Ds:
    for c in CS:
        seq = [(N, lam.get((D, c, N))) for N in NS]
        seq = [(N, v) for N, v in seq if v is not None]
        for (n1, v1), (n2, v2) in zip(seq[:-1], seq[1:]):
            if v2 > v1 * (1 + 1e-6):
                viol.append((D, c, n1, n2, v1, v2))
print(f"  violations: {len(viol)}" + (f"  e.g. {viol[:4]}" if viol else "  (none)"))

print("\nCHECK 3: |log10(lambda(N2)/lambda(N1))| per transition and c: median / max (D at max):")
for c in CS:
    for n1, n2 in ((16, 32), (32, 48), (48, 64)):
        ds = [
            (abs(math.log10(lam[(D, c, n2)] / lam[(D, c, n1)])), D)
            for D in Ds
            if (D, c, n1) in lam and (D, c, n2) in lam
        ]
        if ds:
            ds.sort(reverse=True)
            print(
                f"  c={c:>2} {n1:>2}->{n2:>2}: median {np.median([d for d, _ in ds]):6.2f}  max {ds[0][0]:6.2f} (D={ds[0][1]})  n={len(ds)}"
            )

print("\nCHECK 2: converged to N=64 if |log10(lambda(64)/lambda(48))| < 1:")
conv = {}
for c in CS:
    ok = []
    for D in Ds:
        if (D, c, 48) in lam and (D, c, 64) in lam:
            ok.append((D, abs(math.log10(lam[(D, c, 64)] / lam[(D, c, 48)])) < 1))
    conv[c] = {D for D, g in ok if g}
    nconv = len(conv[c])
    notc = [D for D, g in ok if not g]
    print(
        f"  c={c:>2}: {nconv} of {len(ok)} converged -> {'N=64 sufficient' if nconv >= 18 else 'N=64 NOT sufficient'}; not converged: {notc}"
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
    return beta, beta / se, r2, math.sqrt(s2), n


def verdicts(sets, label):
    res = {}
    print(f"\n{label}")
    print(
        f"{'c':>3} {'N':>3} {'n':>3} {'R2':>6} {'sd':>5} | {'parity(odd)':>15} | {'q per doubling':>15} | {'gamma_1 per unit':>16}"
    )
    for (c, N), rs in sets.items():
        if len(rs) < 8:
            print(f"{c:>3} {N:>3} {len(rs):>3}  (fewer than 8 cells: not fitted)")
            continue
        beta, t, r2, sd, n = fit(rs)
        res[(c, N)] = (beta, t)
        print(
            f"{c:>3} {N:>3} {n:>3} {r2:6.3f} {sd:5.2f} | {beta[3]:+6.2f} [{t[3]:+5.1f}] | {beta[1] * LOG2:+6.2f} [{t[1]:+5.1f}] | {beta[2]:+6.2f} [{t[2]:+5.1f}]"
        )
    if len(res) < len(sets):
        print("  (verdicts below only if all sets could be fitted)")
        return
    for idx, scale, name in (
        (3, 1.0, "parity (odd)"),
        (1, LOG2, "conductor q"),
        (2, 1.0, "first-zero height gamma_1"),
    ):
        effs = {k: v[0][idx] * scale for k, v in res.items()}
        strong = {k: abs(v[1][idx]) >= 3 and abs(effs[k]) >= 0.5 for k, v in res.items()}
        same = all(e > 0 for e in effs.values()) or all(e < 0 for e in effs.values())
        if all(strong.values()) and same:
            vd = "ROBUSTLY DETECTED"
        elif not any(strong.values()):
            vd = "ROBUSTLY NOT DETECTED"
        else:
            vd = "UNSTABLE (present in: " + ", ".join(f"c={k[0]}" for k in res if strong[k]) + ")"
        print(f"  {name}: {vd}; same sign in all sets: {same}")


by_cN = {(c, N): [r for r in rows if r["c"] == c and r["N"] == N] for c in CS for N in (32, 64)}
verdicts(
    {k: v for k, v in by_cN.items() if k[1] == 32},
    "CHECK 4a: regression at N=32 (all 20 characters; for comparison with B3)",
)
verdicts(
    {k: v for k, v in by_cN.items() if k[1] == 64},
    "CHECK 4b: regression at N=64 (all 20 characters)",
)
conv_sets = {(c, 64): [r for r in by_cN[(c, 64)] if r["D"] in conv[c]] for c in CS}
verdicts(conv_sets, "CHECK 4c: regression at N=64 on CONVERGED characters only (need >= 8 per set)")
