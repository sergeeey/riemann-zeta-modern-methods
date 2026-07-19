# B-03 — claim.md

**Stakes:** internal-only (illustrative landscape-note material, not a claim about RH)
**Question type:** descriptive (does a known zero of H_t move smoothly and stay
real as t varies through a small range around 0?)

## Source [VERIFIED via WebSearch, cross-confirmed by MathWorld/Wikipedia/arXiv:1801.05914]
- H_t(x) := ∫₀^∞ e^{tu²}·Φ(u)·cos(xu) du, Φ(u) := Σₙ (2π²n⁴e^{9u} − 3πn²e^{5u})·exp(−πn²e^{4u})
- de Bruijn-Newman constant Λ: H_t has ONLY real zeros for t≥Λ. RH ⟺ Λ≤0.
  Rodgers-Tao (2018, arXiv:1801.05914) proved Λ≥0 via GUE-repulsion. Currently
  known: 0≤Λ<½ (upper bound 2009, lower bound 2018).
- H_0's real zeros correspond to ζ zeros via x=2γ (γ=Im ρ for ρ=½+iγ) —
  confirmed below, not assumed from memory.

## Claim (falsifiable)
1. H_0(x) ≈ 0 at x=2γ₁ and x=2γ₂ (γ₁=14.134725..., γ₂=21.022040..., published
   Odlyzko values, same source as `src/zeta/reference.py`) — confirms the
   x=2γ calibration and that our Φ/H_t implementation matches the published
   formula (a wrong formula would not zero out at these specific x by chance).
2. Following the zero seeded at x=2γ₁ across t∈{−0.05,−0.02,0,0.02,0.05}, the
   root stays REAL (imaginary part negligible) and moves MONOTONICALLY with t.

**Check (measurable outcome):** \|H_0(2γₙ)\|<10⁻⁸ for n=1,2 (calibration);
root sequence strictly monotone in x as t increases.

**Falsifiable predicate:** if calibration fails (H_0 doesn't vanish near 2γₙ),
the formula/implementation is wrong — stop, do not proceed to tracking. If the
tracked root becomes non-real or non-monotone within this small, safely-inside-
known-bounds t range, that would itself be a notable (and re-checked) finding,
not silently smoothed over.

## What this does NOT mean
1. Does NOT prove or test RH, Λ≥0, or Λ≤0 — those are settled (Rodgers-Tao) or
   open (RH itself) at a level far beyond one numerically-tracked zero.
2. Does NOT demonstrate the Rodgers-Tao GUE-repulsion mechanism itself — that
   argument concerns anomalously CLOSE zero pairs potentially merging/going
   complex as t decreases. This atom tracks one well-separated, "boring" zero
   precisely because it is NOT expected to do anything dramatic — it is a
   smooth-deformation sanity illustration, not a search for the interesting
   (close-pair) case. Finding and tracking a genuine close pair is a
   separate, harder task (see decision.md).
3. Does NOT establish anything about the finite-Φ-series truncation's fidelity
   to the true (infinite-sum) Φ(u) at extreme t — only checked near t=0 with
   n≤5 terms (already negligible beyond n=2 per Φ(0)/Φ(1) magnitudes checked
   during Step 1).
4. A monotone, real track for ONE zero over a SMALL t-range is not evidence
   about the GLOBAL behavior of all zeros or the true value of Λ.

## Assumptions
| # | Assumption | Status |
|---|---|---|
| A1 | Φ(u), H_t(x) formula correctly transcribed | [VERIFIED-tool] via calibration against 2 independent published ζ zeros |
| A2 | 5-term truncation of Φ's series sufficient near u∈[0,4] | [VERIFIED-tool]: Φ(1) already ~5×10⁻⁷⁰ relative to Φ(0), n>1 terms decay far faster |
| A3 | findroot continuity (seeding each t from the previous root) tracks the SAME zero, not a neighbor | [INFERRED] from small t-steps (0.02–0.03) and smooth, monotone observed shifts (~0.01–0.03 in x per step) — no jump discontinuity observed |
