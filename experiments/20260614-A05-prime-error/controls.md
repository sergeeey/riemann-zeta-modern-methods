# Controls — A-05
Date: 2026-06-14

## Positive Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| π(x) vs reference | exact match | all 6 (π(10⁷)=664579) | ✓ |
| mp.li(2) | ≈1.0452 | 1.04516 | ✓ |
| mp.log natural | log(e)=1 | 1.0 | ✓ |
| Schoenfeld const 1/8π | ratio<1 for x≥2657 | 0.47,0.26,0.24,0.17 | ✓ |

## Negative Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| bound for x<2657 | NOT guaranteed | x=100 ratio=2.80, x=1000 ratio=1.11 (correctly excluded) | ✓ |
| li>π NOT universal | bias not a theorem | flagged: Littlewood, first flip ~10³¹⁶ | ✓ documented |
| error/√x bounded | modest | max 0.513 | ✓ |

## Verification notes
- π(x) exact (sympy sieve), not approximation — cross-checked vs published table.
- li(x) is Cauchy PV ∫₀ˣ (Schoenfeld Thm 12 notation), documented in code # WHY.
- The x<2657 rows are shown for visualization only; the Schoenfeld bound formula is
  proven only for x≥2657, so their ratio>1 is expected, not a violation.
- Key honesty control (skeptic HIGH): the li>π bias is the CLASSIC false
  extrapolation (Littlewood 1914 disproved "li always >π"). Warned in output + figure.
