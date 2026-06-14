# Decision — A-09 · RMT-статистика
Date: 2026-06-14
FL Step 10: Go/No-Go

## Decision: PROMOTE ✅

## Rationale
- Reformulated claim holds under tool + independent scipy verification.
- Level repulsion is unambiguous; Poisson rejected at p=10⁻¹⁷⁸.
- skeptic [WEAKENED] fully addressed: 2 DISMISSED/RESOLVED, 4 ACCEPTED as honest
  caveats (all about claim STRENGTH, none falsifying the qualitative result).
- reviewer LGTM; all numerics independently reproduced by scipy.
- Two independent negative controls prove the pipeline does not manufacture GUE.

## Key scientific takeaway
The zeros of ζ behave like eigenvalues of random Hermitian matrices (GUE), not
like independent random points. This is the empirical backbone of the
Hilbert–Pólya idea (A-12): if zeros are eigenvalues of a self-adjoint operator,
GUE statistics are exactly what we'd expect. A-09 confirms the data is consistent
with that picture (within finite-T limits).

## What this does NOT license
- No "RH true/verified" language. No "GUE proven". This is evidence for a
  conjecture, on a low height range.

## Next atom (recommendation)
- **A-12 (Hilbert–Pólya)** — now motivated by A-09 evidence. Study existing
  operator candidates (Berry–Keating xp, Connes), assess what's proven vs hoped.
  This is the deepest direction; A-09+A-10 toolkit supports it.
- Alternatively **A-05 (prime error term)** for a concrete, self-contained result
  tying zeros to π(x).

## Artifacts
- estimand.md, claim.md, controls.md, caveats.md, result_summary.md
- compute_zeros.py, run_rmt_analysis.py, visualize.py, skeptic_attack.py
- metrics/zeros.txt (2000 zeros), metrics/run.json
- figures/nnsd.png, figures/nnsd_neg.png

## Verdict routing
PROMOTE → stays in experiments/. No null_results/ entry.
