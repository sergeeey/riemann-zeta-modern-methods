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

## Revival condition (for the harder, more interesting follow-up)
Locate a genuine close (Lehmer-type) pair of ζ zeros (candidate search
already flagged in today's earlier goal-expansion-100 idea #2 and
combinatorial-creativity idea 2 — both parked as separate ideas, not done),
then track BOTH zeros of that pair under H_t as t decreases from 0, to see
whether they approach each other and go complex, or repel and stay real
(the actual empirical content behind Rodgers-Tao's proof). This is a
genuinely separate, harder task from what this atom did.

## What's next
Not a new atom by itself — a calibration + illustration piece, usable
directly in a G3 landscape note (SYNTHESIS.md / PLAN-2026H2.md G3 goal).
