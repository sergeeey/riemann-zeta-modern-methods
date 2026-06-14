# Result Summary — A-06 · Robin & Li criteria
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE (Robin genuine; Li corrected after circularity)

## Results
**Robin (genuine, zero-independent):**
- σ(n) < e^γ·n·ln(ln n) holds for all n≥5041 up to 10⁴.
- 26 exceptions, all in [3,5040]; extremal n=5040 (ratio 1.00556); max ratio for
  n≥5041 is 0.977<1. RH in arithmetic language.

**Li (corrected):**
- λ₁ = 0.023096 via zero-free closed form (1+γ/2−ln4π/2) — GENUINE positive datapoint.
- λ_n from zeros (n=2..20) ASSUME Re=½ → ILLUSTRATIVE only (skeptic: circular).
- from-zeros λ₁=0.02265 agrees with independent → weak check zeros are on Re=½.

## Evidence ledger
| Finding | Marker | Note |
|---------|--------|------|
| Robin holds to 10⁴, 26 exc ≤5040 | [VERIFIED-tool] | zero-independent, genuine |
| λ₁>0 independent | [VERIFIED-tool] | zero-free closed form |
| Li from-zeros λ_n>0 | [CIRCULAR] | assumes Re=½, illustrative only |
| 26 not 27 exceptions | [VERIFIED-tool] | corrected from [MEMORY] |
| not new | [ACKNOWLEDGED] | reproduces OEIS A067698 |

## Skeptic scorecard
| Caveat | Verdict |
|--------|---------|
| Li circular (assumes Re=½) | RESOLVED (added independent λ₁; tagged rest illustrative) |
| 26 vs 27 | RESOLVED (tool=26, corrected) |
| Robin shallow (≤10⁴) | ACCEPTED |
| λ₁ truncation 2% | ACCEPTED |

## The meta-lesson (most valuable part)
A-06 is where the session's recurring failure mode bit US: I "verified" Li's
criterion by assuming Re=½ — the same circular move (assume the conclusion) that we
REJECTED in Grant's Doc A. The skeptic caught it; the fix (zero-free λ₁) restores one
genuine datapoint. Net: Robin is a real arithmetic-language confirmation; Li-from-zeros
is a cautionary tale, now correctly labeled.
