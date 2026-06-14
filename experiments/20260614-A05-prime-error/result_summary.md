# Result Summary — A-05 · Prime error term
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE (genuine illustrative result)

Unlike A-12/A-07 (re-derived tautologies), A-05 is a real measurement of the
π(x)≈li(x) approximation quality. Result is classical (not novel) but content-rich:
it shows concretely WHAT RH buys.

## The result
| x | π(x) | li(x) | li−π | von Koch bound | ratio |
|---|------|-------|------|----------------|-------|
| 10⁴ | 1229 | 1246.1 | 17.1 | 36.6 | 0.468 |
| 10⁵ | 9592 | 9629.8 | 37.8 | 144.9 | 0.261 |
| 10⁶ | 78498 | 78627.5 | 129.5 | 549.7 | 0.236 |
| 10⁷ | 664579 | 664918.4 | 339.4 | 2028.0 | 0.167 |

- Error stays FAR below the von Koch/Schoenfeld bound, and the ratio DECREASES —
  the actual error grows slower than √x·ln x on this range.
- This is the payoff side of RH: RH ⟺ the prime error is O(√x·ln x), the smallest
  possible. Without RH the best unconditional bound is barely sub-x.

## Evidence ledger
| Finding | Marker | Note |
|---------|--------|------|
| π(x) exact, matches refs | [VERIFIED-tool] | sympy sieve |
| error within von Koch bound (x≥2657) | [VERIFIED-tool] | ratio 0.17–0.47 |
| li(x) Cauchy PV correct | [VERIFIED-tool] | Schoenfeld notation |
| li>π bias NOT universal | [DOCS] | Littlewood 1914; flip ~10³¹⁶ |
| not new | [ACKNOWLEDGED] | classical, computed to 10²⁵ (Büthe) |

## Skeptic scorecard
| Caveat | Verdict |
|--------|---------|
| li>π extrapolation danger (HIGH) | RESOLVED (warned stdout+figure) |
| x<2657 bound n/a | RESOLVED (marked) |
| not new | ACCEPTED |
| empirical to 10⁷ | ACCEPTED |
| quantify "what RH buys" | ADDED (unconditional contrast in caveats) |
Reviewer: LGTM (P2 li-comment added).

## Takeaway for the project
A-05 is the "payoff" atom: it makes concrete why RH matters — it pins the prime
error to √x·ln x. Combined with the rest of the session, the project now covers
both sides: what RH WOULD GIVE (A-05) and why it's HARD to prove (A-07/A-09/A-12
all stall at the fine-scale wall near the line).
