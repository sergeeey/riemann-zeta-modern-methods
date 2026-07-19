# B-07 — claim.md

**Stakes:** internal-only (methodology tool, not a claim about RH itself)
**Question type:** descriptive (does our implementation of a known counterexample
function behave as the literature says, and can we use it as an automatic
negative control?)

## Source [VERIFIED via WebSearch, cross-confirmed by 2 independent descriptions]
- Davenport & Heilbronn (1936): a Dirichlet-series-like function D(s) satisfying
  a zeta-type functional equation but with NO Euler product, PROVEN to have
  zeros off the critical line Re(s)=1/2 (and even with Re(s)>1) — the classical
  textbook demonstration that "functional equation + symmetric shape" alone
  does not imply RH.
- Formula: D(s) = 5^(-s)·(ζ(s,1/5) + tanθ·ζ(s,2/5) − tanθ·ζ(s,3/5) − ζ(s,4/5)),
  θ = arctan((√(10−2√5)−2)/(√5−1)); ξ(s) = (π/5)^(-s/2)·Γ((1+s)/2)·D(s),
  ξ(s)=ξ(1−s). Consistent across two independently found descriptions
  (character table {χ(1),χ(2),χ(3),χ(4)}={1,i,−i,−1} matches both).

## Claim (falsifiable)
1. Our implementation of D(s) via Hurwitz zeta satisfies ξ(s)=ξ(1−s) to
   numerical precision (dps=30) at arbitrary test points — if the formula
   transcription is wrong, this would NOT hold by coincidence.
2. D(s) is established in the literature (not by us) to have zeros with
   Re(s)≠1/2 — this makes it a ready-made falsifier for any reasoning pattern
   that "proves" a zeta-type function's zeros are confined to the line by a
   step that secretly ASSUMES that confinement (the exact circularity this
   project caught in Grant Doc A §9 Step 4 and its own first draft of A-06's
   Li coefficient — both assumed ρ=½+iγ as an input).

**Check (measurable outcome):** (a) ξ(s)=ξ(1−s) numerically to <1e-25 at ≥3
arbitrary points → formula correctly implemented. (b) At least one zero found
by us OR cited from literature with |Re(s)−1/2|>1e-6 → the negative-control
premise (D violates RH-type confinement) is substantiated.

**Falsifiable predicate:** if (a) fails, the implementation is wrong — do not
use it. If (b) cannot be substantiated even via literature citation, the
negative-control claim about D(s) has no basis here — drop it.

## What this does NOT mean
1. Does NOT test or prove/disprove RH — D(s) is not ζ(s), it's a deliberately
   different counterexample construction.
2. Does NOT mean we personally rediscovered a specific off-line zero of D(s) —
   three grid+findroot search attempts (Im up to ~90) each converged back to
   an on-line zero. The off-line-zero *existence* claim rests on the published
   record (AMS Math. Comp. 2007 paper title is literally "Zeros of the
   Davenport-Heilbronn Counterexample"), marked [VERIFIED-REAL, literature],
   not [VERIFIED-tool] by us.
3. Does NOT constitute an automated text/NLP circularity detector — the
   "negative control" here is a worked demonstration (this experiment) that a
   specific assumption-smuggling step-shape is unsound, not a general-purpose
   scanner that could be pointed at an arbitrary new PDF.
4. A single worked example does NOT generalize to "any future proof attempt
   will be caught automatically" — this is one concrete, reusable illustration,
   not a universal filter.

## Assumptions
| # | Assumption | Status |
|---|---|---|
| A1 | D(s) formula (Hurwitz-zeta form) correctly transcribed | [VERIFIED-tool] via functional-equation self-consistency check, not just source-copying |
| A2 | Character values {1,i,−i,−1} for n=1..4 mod 5 correctly attributed | [VERIFIED], cross-confirmed by 2 independent WebSearch results |
| A3 | D(s) has zeros off Re=1/2 | [VERIFIED-REAL, literature] — Davenport & Heilbronn 1936; AMS Math. Comp. 2007 — NOT independently re-derived by us today |
