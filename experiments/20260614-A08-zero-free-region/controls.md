# Controls — A-08
Date: 2026-06-14

## Positive Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| σ_zf(10²) vs lit | 0.9609 | 0.96094 | ✓ |
| σ_zf(10⁸⁰) vs lit | 0.9990 | 0.99902 | ✓ |
| σ_zf monotone ↑ | toward 1 | True | ✓ |
| crossover L=k·lnL | L≈8928 | log₁₀t=3877.5 (both agents confirm) | ✓ |

## Negative Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| gap σ_zf−½ grows | NOT shrink | 0.461→0.4996 (grows) | ✓ refutes "ZFR→½" |
| VK wider for moderate t | NO (only t>10³⁸⁷⁷) | vk_wider=False on table | ✓ |
| σ_zf in (½,1) | yes (valid t≥2) | all in (0.74,1) | ✓ |

## Verification notes
- **crossover discrepancy resolved:** my findroot gives log₁₀t≈3877 (k=(C/R)³=981.4);
  lit-review agent's prior estimate 10⁴³⁴ was WRONG. Both skeptic and reviewer
  independently re-derived 10³⁸⁷⁷ (skeptic by hand iteration, reviewer by sign
  analysis). My value stands. [VERIFIED-tool ×2 agents]
- findroot now bracketed [1000,20000] bisect — isolates the real root from the
  trivial L≈1 root (reviewer P2).
- **WEAK control on R:** REF table is DERIVED from R=5.558691, so "ref_match" is
  self-consistency, NOT independent verification. R is taken from MTY 2022 on trust
  (not verified against the PDF in this session).
