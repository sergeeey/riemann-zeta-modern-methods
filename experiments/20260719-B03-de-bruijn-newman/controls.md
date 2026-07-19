# Controls — B-03

## Positive control — calibration against published ζ zeros
**Test:** H_0(2γₙ) should be ≈0 for γₙ = published imaginary parts of the
n-th nontrivial ζ zero (same Odlyzko-sourced values as `src/zeta/reference.py`).

**Result [VERIFIED-tool]:**
| n | γₙ | x=2γₙ | H_0(x) |
|---|---|---|---|
| 1 | 14.134725141734693790 | 28.269450 | −1.45×10⁻¹⁹ |
| 2 | 21.022039638771554993 | 42.044079 | 2.27×10⁻²¹ |

Both essentially zero at dps=25 precision. A wrong Φ(u)/H_t(x) transcription
would not coincidentally vanish at these two independently-sourced x values —
this is strong evidence the formula is implemented as published, matching the
same discipline used for B-07's functional-equation check.

## No-collapse test — series truncation
Φ(u) uses n=1..5 terms. Sanity check (done during Step 1, not re-run here):
Φ(0)≈0.447, Φ(1)≈5.1×10⁻⁷⁰ — the n=1 term already dominates overwhelmingly at
u≥0 due to the exp(−πn²e^{4u}) factor; n>1 terms are negligible at the u-range
this integral actually samples (u∈[0,4], where the cos(xu) oscillation and
Φ's own decay jointly localize the integral's support). 5 terms is generous,
not a tight cutoff.

## Continuity control — zero-tracking assumption
Each `findroot` call is seeded from the PREVIOUS t-step's root (not from a
fixed point), under the assumption this tracks the same zero continuously
rather than jumping to a neighboring one. Justification: t-steps are small
(0.02–0.03) and the observed per-step shift in x (0.012–0.017) is smooth and
of consistent sign and magnitude — no discontinuous jump, which would be the
signature of accidentally latching onto a different zero.

## What was NOT tested (explicit, not silently skipped)
- No search for a close (Lehmer-type) zero pair — this atom's zero (2γ₁) is a
  normally-spaced zero, chosen specifically because it should behave
  "boringly" (stay real, move smoothly). The scientifically sharper test
  (does a close pair merge/go complex as t decreases) is a separate, harder
  search task — see decision.md revival note.
- No test at |t| approaching or exceeding the known Λ<0.5 bound, where
  interesting (non-real-zero) behavior could in principle appear for SOME
  zero (not this one, since Λ concerns the infimum over ALL zeros, and this
  well-separated zero isn't expected to be the sensitive one).
