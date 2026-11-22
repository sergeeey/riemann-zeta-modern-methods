"""Analysis of variant B (reads ../results/parity_B.jsonl): table, the pre-registered chi8-vs-chim8 criterion, rank correlations.
Usage: python parity_analysis.py
"""

import json
import math

from scipy.stats import spearmanr

with open("../results/parity_B.jsonl", encoding="utf-8") as fh:
    rows = [json.loads(line) for line in fh]
rows.sort(key=lambda r: (r["c"], r["N"], r["parity"], r["char"]))
print(
    f"{'char':6} {'par':4} {'q':>2} {'c':>3} {'N':>3} {'inertia':>10} {'lambda_min':>12} {'cond':>11} {'gamma1_ref':>17} {'log10 err':>10}"
)
for r in rows:
    inertia = str((r["n_pos"], r["n_neg"]))
    print(
        f"{r['char']:6} {r['parity']:4} {r['q']:>2} {r['c']:>3} {r['N']:>3} {inertia:>10} "
        f"{r['lambda_min']:>12} {r['cond']:>11} {r['gamma1_ref']:>17} {r['log10_err']!s:>10}"
    )

print("\nPRE-REGISTERED PAIR chi8 (even) vs chim8 (odd), same conductor 8 (claim_B.md):")
by = {(r["char"], r["c"], r["N"]): r for r in rows}
verdicts = []
for c in (13, 37):
    for N in (16, 32):
        e, o = by[("chi8", c, N)], by[("chim8", c, N)]
        d_lam = math.log10(float(e["lambda_min"]) / float(o["lambda_min"]))
        d_err = float(e["log10_err"]) - float(o["log10_err"])
        verdicts.append((d_lam, d_err))
        print(
            f"  c={c:>2} N={N:>2}: log10(lam_min even/odd) = {d_lam:+.2f}   log10err(even) - log10err(odd) = {d_err:+.2f}"
        )
lam_ok = all(v[0] > 0 for v in verdicts) or all(v[0] < 0 for v in verdicts)
lam_ok = lam_ok and all(abs(v[0]) >= 1 for v in verdicts)
err_ok = all(v[1] > 0 for v in verdicts) or all(v[1] < 0 for v in verdicts)
err_ok = err_ok and all(abs(v[1]) >= 3 for v in verdicts)
print(f"  criterion lambda_min (same sign in all 4 cells and >= 1 decade): {lam_ok}")
print(f"  criterion gamma_1 error (same sign in all 4 cells and >= 3 digits): {err_ok}")

print(
    "\nEXPLORATORY: Spearman rank correlation of log10(lambda_min) with gamma_1, parity (odd=1), conductor q, over the 5 characters:"
)
for c, N in sorted({(r["c"], r["N"]) for r in rows}):
    rs = [r for r in rows if (r["c"], r["N"]) == (c, N)]
    lam = [math.log10(float(r["lambda_min"])) for r in rs]
    rho_g = spearmanr([float(r["gamma1_ref"]) for r in rs], lam).statistic
    rho_p = spearmanr([1 if r["parity"] == "odd" else 0 for r in rs], lam).statistic
    rho_q = spearmanr([r["q"] for r in rs], lam).statistic
    order = " < ".join(
        f"{r['char']}({float(r['gamma1_ref']):.2f})"
        for r in sorted(rs, key=lambda r: float(r["lambda_min"]))
    )
    print(
        f"  c={c:>2} N={N:>2}: rho(gamma1)={rho_g:+.2f} rho(parity)={rho_p:+.2f} rho(q)={rho_q:+.2f}; lambda_min ascending: {order}"
    )
