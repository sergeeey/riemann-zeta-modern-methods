# Decision — A-08 · Zero-free region
Date: 2026-06-14
FL Step 10: Go/No-Go

## Decision: PROMOTE (as understanding) ✅

## Rationale
- Illustrates published ZFR bounds (MTY 2022) and corrects a real misconception:
  the proven boundary moves toward Re=1, the gap to ½ GROWS (not shrinks).
- Tool-verified: σ_zf table matches lit; crossover 10³⁸⁷⁷ confirmed by BOTH agents
  (and corrects the lit-agent's erroneous 10⁴³⁴).
- Skeptic [WEAKENED] addressed: the critical pointwise-vs-density distinction is now
  explicit (CAVEAT-1), linking to our own A-07 (41.7% ON the line). R-on-trust noted.
- Reviewer LGTM; findroot bracketed, metrics mkdir added.
- Integrity: did NOT let "ZFR doesn't reach ½" imply "classical theory is helpless
  near ½" — that would be false and A-07 disproves it.

## What this atom adds to the project
The Re=1 face of the wall. Combined with A-07 (the ½ face), the two classical
fronts (zero-free from above, proportion/density from below) leave exactly the
a/lnT strip next to the line uncontrolled — confirming the session's convergence
finding from a new angle.

## What this does NOT license
- No "RH supported/closer". No "classical theory silent near ½" (false — see A-07).
- No claim that better constants help (qualitative barrier).

## Project status
7 atoms now: A-04/A-05/A-07/A-08/A-09/A-10/A-12 + Grant REJECT + SYNTHESIS.
A-08 strengthens the convergence conclusion. Synthesis should be updated to fold in
the A-08 (Re=1 side) + A-07 (½ side) duality as the sharpest statement of the wall.

## Next step
- Update SYNTHESIS.md with the A-07/A-08 duality (two faces of the wall).
- Then: remaining atoms are low-value (A-01/02/03/06 proven base; A-11 meta; A-13/14)
  → natural stopping point, or pivot to a publishable "computational landscape" note.

## Artifacts
- estimand.md, claim.md, controls.md, caveats.md, result_summary.md
- review_zfr (lit map in agent output), run_zero_free.py, visualize.py
- metrics/run.json, figures/zfr_gap.png

## Verdict routing
PROMOTE (understanding) → stays in experiments/. Triggers SYNTHESIS.md update.
