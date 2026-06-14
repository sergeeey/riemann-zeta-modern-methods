# Decision — A-05 · Prime error term
Date: 2026-06-14
FL Step 10: Go/No-Go

## Decision: PROMOTE ✅

## Rationale
- Genuine measurement (not a tautology): π(x)≈li(x) quality, error vs von Koch bound.
- π(x) exact and reference-matched; error well inside Schoenfeld bound (ratio↓ to 0.17).
- Skeptic [WEAKENED] (framing) fully addressed: the li>π extrapolation trap is now
  loudly warned in stdout AND on the figure; x<2657 marked; novelty=none stated.
- Reviewer LGTM; li-notation documented.
- Anti-misleading integrity held: caught the classic "li always > π" trap before it
  could mislead (Littlewood/Skewes).

## What this atom contributes to the project
The PAYOFF side: it makes "why RH matters" concrete and measurable — RH pins the
prime-counting error to O(√x·ln x), the best possible. This complements the
"why it's hard" atoms.

## Project status after A-05
Major classical atoms now covered:
- A-10 base, A-04 verify, A-09 RMT, A-12 operator, A-07 density, A-05 payoff.
- Plus Grant-audit REJECT.
The session's convergent finding (all proof-routes stall at the fine-scale wall near
Re=½) plus the payoff (A-05) form a coherent picture. → Synthesis is the natural close.

## What this does NOT license
- No "li>π always", no "RH supported/proved". Empirical to 10⁷.

## Next step
**Synthesis** — one project-level document tying A-04/A-05/A-07/A-09/A-10/A-12 +
Grant-audit together around: (1) what RH buys, (2) where every classical route stalls.

## Artifacts
- estimand.md, claim.md, controls.md, caveats.md, result_summary.md
- run_prime_error.py, visualize.py
- metrics/run.json, figures/error_vs_bound.png

## Verdict routing
PROMOTE → stays in experiments/. Triggers synthesis phase.
