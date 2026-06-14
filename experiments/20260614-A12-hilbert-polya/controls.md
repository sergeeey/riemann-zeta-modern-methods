# Controls — A-12
Date: 2026-06-14

## Positive Controls (should match known results)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| n_BK vs smooth θ/π+1 | match, err→0 | err 1.3e-4 → 2.7e-6 | ✓ |
| weyl_err·T → 1/(48π) | =0.0066315 (Stirling 3rd term) | 0.00663146, rel 0.0000% to T=5e5 | ✓ but TAUTOLOGY |
| S vs independent arg ζ/π | identical | max disagreement 0.00000 | ✓ not circular |
| mean S(T) | ≈0 (Selberg) | 0.029 | ✓ |
| std S(T) | ~0.31 (Selberg √(lnlnT/2π²)) | 0.373 | ✓ within CI |

## Negative Controls (should fail / differ)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| wrong norm ℓxℓp=π | error grows linearly | 5.5 → 275.8 | ✓ (but: just units scaling) |
| S(T) ≡ 0? | NO — must have spread | std 0.37 > 0 | ✓ positions not captured |

## CRITICAL honesty note (skeptic)
- weyl_err·T=1/(48π) is NOT an emergent property of xp — it is the next term of
  the Stirling expansion of θ(T). n_BK takes the first 2 terms; the residual IS
  the 3rd term. [VERIFIED-tool to T=500000, rel 0.0000%]. This is a TAUTOLOGY,
  not a discovery.
- "std persists 0.40 vs 0.34" is NOT significant: F=(0.40/0.34)²=1.38 < F_crit
  1.98 (df 24,24). It is noise. Correct statement: consistent with Selberg, the
  T-range is too small to see √(lnlnT) growth.
- The positive results restate Berry-Keating (1999) and Selberg (1946).
