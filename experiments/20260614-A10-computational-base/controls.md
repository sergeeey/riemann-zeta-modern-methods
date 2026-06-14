# Controls — A-10
Date: 2026-06-14

## Positive Controls (known-good → must reproduce)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| First 10 zeros vs Odlyzko [external] | match ≥10 digits | max err 9.4e-19 (floor = 18-digit reference) | ✓ PASS |
| First 10 zeros vs mp.zetazero [diff algo] | match | max err 2.8e-30 | ✓ PASS |
| Residual \|ζ(½+it)\| at each found zero | ≈ 0 | max 6.1e-29 | ✓ PASS |
| Zero #1 convergence dps 15→30→50 | error shrinks | 2.2e-22 → 1.3e-37 | ✓ PASS |

## Negative Controls (known-bad / non-zeros → must NOT be flagged)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| ζ(2) = π²/6 | ≠ 0, = 1.6449… | matches π²/6 to 1e-20 | ✓ PASS |
| Z(18) between zeros #1,#2 | ≠ 0 | \|Z(18)\| > 0.1 | ✓ PASS |
| ζ(½+14.0i) near but not a zero | ≠ 0 | 0.1056 | ✓ PASS |

## Adversarial / Off-line Detector (added after skeptic review)
| Control | Purpose | Result | Status |
|---------|---------|--------|--------|
| Contour count ξ'/ξ, Re∈[-0.5,1.5], T=35/51/66 | detect off-line zeros across FULL strip | 5=5, 10=10, 15=15 | ✓ PASS — no off-line zeros |
| nzeros independence (coarsen scan) | refute circularity | scan 29→6 while nzeros fixed 29 | ✓ PASS — independent |

Note: the contour control is the TRUE negative control for "off-line zero exists".
The three trivial sanity-checks above are necessary but not sufficient; the contour
integral is what actually measures Re (skeptic CAVEAT-1/CAVEAT-3 addressed).
