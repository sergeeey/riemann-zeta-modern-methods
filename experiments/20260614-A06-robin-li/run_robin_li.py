"""A-06 — Robin & Li criteria: RH in arithmetic language (FL Steps 3-8).

Robin (1984): RH  <=>  sigma(n) < e^gamma * n * ln(ln n)  for all n >= 5041.
  (sigma = sum of divisors; exactly 27 exceptions at n<=5040, extremal n=5040.)
Li (1997):    RH  <=>  lambda_n > 0  for all n>=1,
  lambda_n = sum_rho [1 - (1 - 1/rho)^n]  over nontrivial zeros rho.

Robin: exact sigma via sympy, dense n up to N_MAX.
Li: lambda_n from the 2000 zeros computed in A-09 (reused), n=1..20.
Both are RH-equivalent — a NEW angle (divisors / lambda_n) vs counting zeros.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp
import sympy

HERE = Path(__file__).resolve().parent
ZEROS_FILE = HERE.parent / "20260614-A09-rmt-statistics" / "metrics" / "zeros.txt"

N_MAX_ROBIN = 10000
N_LI = 20


def robin_ratio(n, e_gamma):
    """sigma(n) / (e^gamma * n * ln(ln n))."""
    sig = mp.mpf(int(sympy.divisor_sigma(n)))
    return sig / (e_gamma * n * mp.log(mp.log(n)))


def li_lambda_from_zeros(zeros_imag, n):
    """lambda_n via sum over rho = 1/2 +/- i*gamma.

    WARNING (skeptic): this ASSUMES Re(rho)=1/2 by construction, so lambda_n>0 is
    a CONSEQUENCE of putting the zeros on the line, NOT an independent test of RH
    (Bombieri-Lagarias: zeros on the line => lambda_n>0 automatically). Kept as an
    ILLUSTRATION of the formula, not as RH evidence. The independent test is
    li_lambda_1_independent below (zero-free, uses only constants).
    """
    half = mp.mpf(1) / 2
    total = mp.mpf(0)
    for g in zeros_imag:
        for rho in (mp.mpc(half, g), mp.mpc(half, -g)):
            total += 1 - (1 - 1 / rho) ** n
    return total.real  # imaginary parts cancel over conjugate pairs


def li_lambda_1_independent():
    """lambda_1 = 1 + gamma/2 - ln(4*pi)/2  (Bombieri-Lagarias / Coffey).

    Closed form in terms of constants only — does NOT use the zeros and does NOT
    assume Re=1/2. This IS a genuine (n=1) datapoint: lambda_1>0 is real evidence.
    If it matches the from-zeros value, that agreement is a weak check that the
    zeros really sit on Re=1/2 (rather than us having assumed it).
    """
    return 1 + mp.euler / 2 - mp.log(4 * mp.pi) / 2


def main() -> None:
    mp.mp.dps = 30
    e_gamma = mp.e**mp.euler

    # --- ROBIN ---
    exceptions = []
    max_ratio_above = mp.mpf(0)  # max ratio for n>=5041 (should be <1)
    for n in range(2, N_MAX_ROBIN + 1):
        r = robin_ratio(n, e_gamma)
        if r >= 1:
            exceptions.append(n)
        elif n >= 5041:
            max_ratio_above = max(max_ratio_above, r)
    ratio_5040 = float(robin_ratio(5040, e_gamma))

    robin_ok = (
        len(exceptions) > 0 and max(exceptions) == 5040 and all(n <= 5040 for n in exceptions)
    )
    no_exc_above_5040 = all(n <= 5040 for n in exceptions)

    # --- LI ---
    # INDEPENDENT lambda_1 (zero-free, no Re=1/2 assumption) — the genuine test.
    lam1_indep = float(li_lambda_1_independent())
    # FROM-ZEROS lambda_n (assumes Re=1/2; illustrative, NOT an independent RH test).
    zeros = [mp.mpf(x) for x in ZEROS_FILE.read_text().split()]
    z2000 = zeros[:2000]
    z500 = zeros[:500]
    lambdas = []
    for n in range(1, N_LI + 1):
        ln_full = float(li_lambda_from_zeros(z2000, n))
        ln_500 = float(li_lambda_from_zeros(z500, n))
        lambdas.append(
            {
                "n": n,
                "lambda_n (2000 zeros, assumes Re=1/2)": round(ln_full, 6),
                "lambda_n (500 zeros)": round(ln_500, 6),
                "positive": ln_full > 0,
                "sign_stable": (ln_full > 0) == (ln_500 > 0),
            }
        )
    all_li_positive = all(d["positive"] for d in lambdas)
    li_sign_stable = all(d["sign_stable"] for d in lambdas)
    lam1_from_zeros = lambdas[0]["lambda_n (2000 zeros, assumes Re=1/2)"]
    # genuine check: independent lambda_1 > 0, AND from-zeros converges to it
    lam1_indep_positive = lam1_indep > 0
    lam1_agree = abs(lam1_indep - lam1_from_zeros) < 0.01  # ~truncation tolerance

    verdict = (
        "PASS"
        if all([robin_ok, no_exc_above_5040, lam1_indep_positive, lam1_agree, li_sign_stable])
        else "FAIL"
    )

    result = {
        "experiment": "20260614-A06-robin-li",
        "robin": {
            "n_max_checked": N_MAX_ROBIN,
            "n_exceptions": len(exceptions),
            "max_exception": max(exceptions) if exceptions else None,
            "ratio_at_5040": round(ratio_5040, 5),
            "max_ratio_for_n_ge_5041": round(float(max_ratio_above), 5),
            "exceptions_all_le_5040": no_exc_above_5040,
            "exceptions": exceptions,
        },
        "li": {
            "n_checked": N_LI,
            "lambda_1_independent": round(lam1_indep, 6),
            "lambda_1_from_zeros": lam1_from_zeros,
            "lambda_1_independent_positive": lam1_indep_positive,
            "lambda_1_agreement": lam1_agree,
            "all_from_zeros_positive_ILLUSTRATIVE": all_li_positive,
            "sign_stable_500_vs_2000": li_sign_stable,
            "circularity_note": (
                "from-zeros lambda_n ASSUMES Re=1/2 -> positivity is automatic, NOT an "
                "independent RH test. Only lambda_1_independent (constants, zero-free) is genuine."
            ),
            "lambdas": lambdas,
        },
        "checks": {
            "robin_exceptions_bounded_5040": robin_ok,
            "robin_no_exception_above_5040": no_exc_above_5040,
            "li_lambda1_independent_positive": lam1_indep_positive,
            "li_lambda1_agree_indep_vs_zeros": lam1_agree,
            "li_from_zeros_sign_stable": li_sign_stable,
        },
        "verdict": verdict,
        "interpretation": (
            "Robin: inequality holds for all n>=5041 up to N_MAX; exceptions are the 26 "
            "known n in [3,5040] (n=2 excluded since ln ln 2<0; literature's '27' counts "
            "n=1 or n=2 by convention). GENUINE result, sigma(n) independent of zeros. "
            "Li: lambda_1=0.0231 from the zero-free closed form (1+gamma/2-ln(4pi)/2) is a "
            "real positive datapoint; the from-zeros lambda_n ASSUME Re=1/2 and are only "
            "ILLUSTRATIVE (skeptic: circular as an RH test). Empirical to a finite bound."
        ),
    }
    (HERE / "metrics").mkdir(exist_ok=True)
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # --- summary ---
    print("=" * 64)
    print(f"VERDICT: {verdict}")
    print("=" * 64)
    print("ROBIN (sigma(n) < e^gamma n ln ln n  <=>  RH for n>=5041):")
    print(f"  checked n=2..{N_MAX_ROBIN}: {len(exceptions)} exceptions, max={max(exceptions)}")
    print(f"  ratio at n=5040 (extremal): {ratio_5040:.5f}  (>1, known last exception)")
    print(f"  max ratio for n>=5041: {float(max_ratio_above):.5f}  (<1 => RH-consistent)")
    print(f"  all exceptions <= 5040: {no_exc_above_5040}")
    print("\nLI (lambda_n > 0  <=>  RH):")
    print(
        f"  lambda_1 INDEPENDENT (zero-free closed form) = {lam1_indep:.6f}  (>0: {lam1_indep_positive}) [GENUINE]"
    )
    print(f"  lambda_1 from 2000 zeros = {lam1_from_zeros:.6f}  (agrees: {lam1_agree})")
    print("  from-zeros lambda_n (ASSUME Re=1/2 -> ILLUSTRATIVE, not an RH test):")
    for d in lambdas[:5]:
        print(f"    lambda_{d['n']} = {d['lambda_n (2000 zeros, assumes Re=1/2)']:>12}")
    print("\n-> Robin is genuine (zeros-independent). Li-from-zeros is circular (skeptic);")
    print("   only the zero-free lambda_1 is an independent positive datapoint.")


if __name__ == "__main__":
    main()
