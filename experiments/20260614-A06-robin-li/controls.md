# Controls — A-06
Date: 2026-06-14

## Positive Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| σ(12) | 28 | 28 | ✓ |
| Robin ratio(5040) | ~1.0056 (extremal) | 1.00556 | ✓ |
| Robin exceptions | bounded, max=5040 | 26 exc, max=5040 | ✓ |
| λ₁ independent (1+γ/2−ln4π/2) | 0.023096 (known) | 0.023096 | ✓ GENUINE |
| λ₁ from-zeros → independent | converge | 0.02265 (agrees <0.01) | ✓ |

## Negative Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| Robin n≥5041 | no exception (ratio<1) | max ratio 0.977<1 | ✓ |
| λ₁ independent sign | >0 | 0.0231>0 | ✓ |
| from-zeros assumes Re=½ | circular (NOT a test) | flagged ILLUSTRATIVE | ✓ honest |

## Verification notes
- **Li circularity (skeptic, ACCEPTED):** the from-zeros λ_n use ρ=½±iγ, i.e. assume
  Re=½ → positivity is automatic (Bombieri-Lagarias), NOT an independent RH test.
  Only λ₁ via the zero-free closed form is genuine. Same error class as Grant Doc A
  (assuming the conclusion) — caught and corrected here.
- **26 vs 27 (skeptic, ACCEPTED):** tool gives 26 exceptions (n∈[3,5040]); n=2 excluded
  because ln ln 2<0. Literature's "27" counts n=1 or n=2 by convention. My [MEMORY]
  said 27; [VERIFIED-tool]=26 (OEIS A067698). interpretation corrected.
- Robin σ(n) is genuinely zero-independent (sympy sieve) — not circular.
