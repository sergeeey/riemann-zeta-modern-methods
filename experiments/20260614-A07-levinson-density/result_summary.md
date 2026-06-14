# Result Summary — A-07 · Levinson density + Speiser
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE as UNDERSTANDING (not as contribution)

Same shape as A-12: numerical part re-derives known facts; value is the literature
map. Honest about it.

## Two deliverables

### 1. Literature map — why ~41% is a ceiling (the real value) [DOCS]
- Record chain: Levinson 1/3 (1974) → Conrey 2/5 (1989) → BCY 41.05% (2011) →
  **PRZZ 41.7% (>5/12, 2020)** = current record (NOT Pratt 41.28%; that was Feng
  2012, disputed).
- Ceiling cause: structural loss in the strip ½≤σ<½+a/lnT — a positive proportion
  of zeros of ζ' sit just right of the line and the method cannot separate them
  (Goldston–Suriajaya 2025 "inherent loss").
- θ=4/7 (mollifier length) is a Kloosterman-sum bound (Deshouillers–Iwaniec), not a
  fundamental constant. Lengthening the mollifier does NOT scale to 100% — a new
  idea is required.

### 2. Speiser numerical check (honest scope)
- RH ⟺ ζ' has no zeros in 0<Re<½. Confirmed to Im=50: left region empty (count=0).
- First 5 zeros of ζ' (right side) reproduced, all Re>½, match lit to ~1e-6.
- API mp.zeta(s,derivative=1) cross-checked vs mp.diff → agree to 1e-15 (not circular).

## Evidence ledger
| Finding | Marker | Note |
|---------|--------|------|
| Speiser holds to Im=50 (left empty) | [VERIFIED-tool] | argument principle = 0 |
| 5 zeros of ζ' right, Re>½ | [VERIFIED-tool] | match lit 1e-6 |
| ζ' API correct | [VERIFIED-tool] | vs mp.diff 1e-15 |
| 41.7% record + cause | [DOCS] | PRZZ 2020; literature, not computed here |
| not new, not Levinson's method | [ACKNOWLEDGED] | Speiser 1934; no mollifier |

## Skeptic scorecard
| Caveat | Verdict |
|--------|---------|
| "illustrates Levinson" overstated | ACCEPTED (reworded) |
| results not new | ACCEPTED |
| Im≤50 tiny | ACCEPTED |
| left-count doesn't probe a/lnT strip | ACCEPTED (key limitation) |
| 41% is literature, not ours | ACCEPTED |

## Honest takeaway for the project
The density frontier (A-07) is the real analytic battleground, and the ceiling is
NOT a tuning issue — it is structural (zeros of ζ' hugging the line). Combined with
A-12 (no operator) and A-09 (GUE is evidence not proof), the picture is consistent:
all classical routes stall at the same wall — the fine-scale behavior of zeros
right next to the line. That wall is where any real progress must happen.
