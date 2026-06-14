# Controls — A-07
Date: 2026-06-14

## Positive Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| First 5 zeros of ζ' (right) vs lit-review | match | err 2-6e-6, all 5 | ✓ |
| All right-side zeros Re>½ | yes | min Re=0.9647 | ✓ |
| mp.zeta(s,derivative=1) API | = numerical diff | agree to 1e-15 | ✓ [VERIFIED-tool] |
| zero of ζ' genuine | residual≈0 | confirmed via mp.diff independently | ✓ |

## Negative Controls
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| ζ' zeros LEFT of line (0<Re<½) | 0 (Speiser ⟺ RH) | 0 to Im≤25 AND ≤50 | ✓ |
| ζ' zeros RIGHT exist | >0 (else test vacuous) | 5 found to Im=50 | ✓ |
| contour ∮ right unstable | known artifact | (used findroot instead, per ICE) | ✓ documented |

## Verification notes
- API independence: zeta(s,derivative=1) cross-checked vs mp.diff(zeta) → 1e-15. Not a
  single-path artifact.
- "residual 1.29e-7" at the ROUNDED reference (2.46316,23.29832) is just the rounding
  to 5 digits; findroot's actual root has residual <1e-8 (the code's confirm threshold).
- Left-region count is exactly 0 (not asymptotic) — the contour there is stable
  because there are no zeros (hence no poles of ζ''/ζ') inside.
