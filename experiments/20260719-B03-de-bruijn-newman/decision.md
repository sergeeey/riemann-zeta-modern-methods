# Decision — B-03 · de Bruijn-Newman heat flow

## Verdict: **PROMOTE (illustration)**

## What survived
- Φ(u)/H_t(x) formula [VERIFIED via WebSearch, cross-confirmed MathWorld/
  Wikipedia/arXiv:1801.05914], implementation calibrated against 2
  independent published ζ zeros (H_0(2γ₁), H_0(2γ₂) both ~0 to 19-21 digits).
- One well-separated zero tracked smoothly and monotonically across
  t∈[−0.05,0.05], stays real throughout — consistent with (not a test of)
  the known 0≤Λ<½ bounds.
- Unlike B-06 (Speiser) and parts of B-07, this atom's numerics were
  well-behaved on the FIRST attempt — no Substrate Gate issue, no
  instability. Worth noting as a genuine counter-example to today's "ideas
  are always more expensive than estimated" pattern — not every atom is.

## Kill Analysis
**What was killed:** nothing — the claim (calibration + smooth monotone
track for this specific zero) held exactly as stated, first attempt.

**What this does NOT establish (by design, not by failure):** the
Rodgers-Tao GUE-repulsion mechanism itself, which concerns close pairs, not
this well-separated zero. This atom is a calibration/illustration piece for
G3 (landscape note), not a probe of the interesting dynamical case.

## Skeptic Step 8a
`[SKEPTIC-PRE-ANSWERED]`: predictable objection — "this doesn't show anything
about WHY Λ≥0, since you picked a boring zero" — addressed explicitly in
claim.md/controls.md ("What this does NOT mean" #2, "What was NOT tested").
The atom's scope was deliberately the calibration/smooth-motion illustration,
not the close-pair mechanism, decided BEFORE running (see claim.md), not
narrowed after seeing a clean result.

## Revival condition (for the harder, more interesting follow-up) — ATTEMPTED, PARKED
Located the real, documented Lehmer pair (γ≈7005.06286617, γ≈7005.10056467,
gap≈0.0377 vs typical spacing ~1 at this height — [VERIFIED via WebSearch,
Wikipedia "Lehmer pair" + MathWorld; both refined and confirmed genuine ζ
zeros via direct evaluation, |ζ|~1e-9..1e-8 at the cited values before
refinement, exact after `findroot`).

**Attempt 1 — direct findroot on H_t at x≈2γ:** at this height (x≈14010),
naive `mp.quad([0,u_max])` gives H_0≈0.0064 (NOT near zero) — the fixed
breakpoint scheme fails to resolve the much-faster cos(xu) oscillation at
this x (same failure mode as B-06's contour instability). Fixed by
segmenting the integration into 80 sub-intervals (dps=20): H_0(2γ)≈-4×10⁻²²,
calibration restored. But `findroot` (Newton) from this corrected H_t then
converged to x≈12704 — an unrelated, distant root — in 232s, evidently
thrown off by evaluation cost/noise or the nearby second zero confusing the
local derivative estimate.

**Attempt 2 — bracketing scan instead of Newton:** scanned x0±0.15 around
2γ₁ in steps of 0.05. Result: H_0 stays at the SAME tiny magnitude
(~-4×10⁻²²) across nearly the entire window, jumping by 4 orders of
magnitude only at the window's edge. This means the separation between the
two zeros in x (≈0.075, twice the 0.038 gap in γ) is smaller than or
comparable to this integration scheme's own approximation-error floor —
the method cannot currently distinguish "near zero 1" from "near zero 2" at
this resolution; a sign-change bracket for each zero separately isn't
resolvable without a finer/adaptive scheme.

**Verdict: PARKED** (2 honest attempts, not a 3rd, per this project's own
discipline). Substrate Gate: BLOCKED-INFRASTRUCTURE for this specific
close-pair case, not evidence about the pair's actual behavior under H_t.

**Revival condition:** adaptive precision/segmentation that scales with how
close the target zeros are (not just with x), OR reformulate using a method
less sensitive to this than direct H_t evaluation + root-finding (e.g., an
argument-principle contour count in a tiny box around the pair, analogous to
A-07's stable left-side Speiser count) — a genuinely separate numerical
engineering task, not a quick fix.

## What's next
Not a new atom by itself — a calibration + illustration piece, usable
directly in a G3 landscape note (SYNTHESIS.md / PLAN-2026H2.md G3 goal).
