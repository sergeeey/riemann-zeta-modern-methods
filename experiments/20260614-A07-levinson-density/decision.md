# Decision — A-07 · Levinson density + Speiser
Date: 2026-06-14
FL Step 10: Go/No-Go

## Decision: PROMOTE (as understanding) ✅

## Rationale
- Literature map is the deliverable: the ~41% ceiling is structural (zeros of ζ'
  in the ½≤σ<½+a/lnT strip), not a tuning limit. Current record PRZZ 41.7% (2020).
- Speiser numerical check is technically correct (API verified, zeros match lit,
  left region empty to Im=50) but NOT new — skeptic [WEAKENED] accepted in full.
- Anti-trivialization integrity held (lesson from A-12): we did NOT dress up a
  re-derivation of Speiser 1934 as a contribution; framing is honest.

## Convergent finding across atoms (the real payoff of this session)
A-09 (GUE = evidence, not proof), A-12 (no operator exists/buildable), A-07 (density
method stalls at a structural wall) all point to the SAME obstruction: the
fine-scale behaviour of zeros immediately next to the critical line. Every classical
route — analytic (Levinson), spectral (Hilbert–Pólya), statistical (RMT) — hits this
wall. That convergence is itself the most useful project-level conclusion.

## What this does NOT license
- No "Speiser illustrates Levinson" / "we showed the 41% mechanism" claims.
- No "RH supported" — Speiser to Im=50 is empirical.

## Next steps (recommendation)
The project has now mapped the major classical directions. Options:
- **A-05 (prime error term)** — the one major atom left untouched; concrete payoff
  side (what RH BUYS), self-contained, uses the toolkit. Natural closer.
- **Synthesis** — write a project-level summary tying A-09/A-10/A-12/A-07 together
  around the "fine-scale wall" finding.
- **Stop** — 4 atoms + audit is a substantial, honest body of work.

## Artifacts
- estimand.md, claim.md, controls.md, caveats.md, result_summary.md
- review_levinson_speiser.md (literature map), run_speiser.py, visualize.py
- metrics/run.json, figures/zeta_prime_zeros.png

## Verdict routing
PROMOTE (understanding) → stays in experiments/. Convergence note → activeContext.
