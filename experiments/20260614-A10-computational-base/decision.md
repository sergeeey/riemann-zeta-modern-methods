# Decision — A-10 · Вычислительная база
Date: 2026-06-14
FL Step 10: Go/No-Go

## Decision: PROMOTE ✅

The atom is complete and the toolkit is validated for use by downstream atoms.

## Rationale
- Falsifiable claim (reformulated) holds under tool verification.
- Skeptic [WEAKENED] verdict addressed: 3 caveats RESOLVED/DISMISSED with tools,
  3 ACCEPTED as honest documented limitations.
- Positive + negative + adversarial controls all pass.
- Deliverable (src/zeta toolkit) is reusable and skeptic-hardened.

## What we now have (for the project)
1. A trustworthy way to compute ζ(s), Hardy Z(t), and locate zeros.
2. An independent off-line detector (argument principle on ξ) — reusable as the
   real test of "is a zero on the line?" in future atoms.
3. A template for the skeptic→stress-test→resolve loop that worked well here.

## What this does NOT license
- Any "RH is true / verified" language. Scope is first ~100 zeros, conditional
  on mpmath. This is reproduction of known fact, not progress on the proof.

## Next atom (recommendation)
With the toolkit ready, the highest-value next step is one of:
- **A-09 (RMT statistics)** — use the toolkit to compute zero-spacing statistics
  and compare to GUE. Directly feeds the Hilbert–Pólya direction (A-12).
- **A-04 (Hardy's theorem)** — understand the MECHANISM of "infinitely many on
  the line" (we have Z(t); now study why it changes sign infinitely often).
- **A-05 (prime error term)** — compute π(x)−Li(x), compare to O(√x logx); ties
  zeros to primes, the heart of why RH matters.

## Artifacts
- claim.md, estimand.md, controls.md, caveats.md, result_summary.md (this folder)
- run_verification.py, adversarial_checks.py, visualize.py
- metrics/run.json
- figures/hardy_Z.png, figures/zeros_complex.png
- src/zeta/ (toolkit, reference)

## Verdict routing
PROMOTE → stays in experiments/. No null_results/ or parked/ entry needed.
