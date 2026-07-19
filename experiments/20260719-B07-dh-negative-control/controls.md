# Controls — B-07

## Positive control — functional equation self-consistency
**Test:** ξ(s) = ξ(1−s) at 3 arbitrary points (s=0.3+7i, 0.9+12i, 2.0+5i),
none of which are anywhere near a zero or special point.

**Result [VERIFIED-tool]:**
| s | \|ξ(s)−ξ(1−s)\| |
|---|---|
| 0.3+7i | 4.2×10⁻³² |
| 0.9+12i | 6.0×10⁻³⁴ |
| 2.0+5i | 1.2×10⁻³¹ |

All at the floor of dps=30 precision. A transcription error in the character
values, θ, or the Gamma/π prefactor would almost certainly NOT produce this
level of agreement by coincidence — this is strong evidence the formula is
implemented as published, not just superficially similar.

## Negative control — the actual point of this atom
D(s) itself IS the negative control (for the circularity pattern described in
claim.md), not something we run a separate check against. The "control" being
validated is: does an object satisfying a zeta-like functional equation
NECESSARILY have all its zeros on the symmetry line? Literature answer: NO —
proven, by construction. Our contribution here is a working, self-verified
implementation usable to demonstrate this to anyone auditing this project's
methodology, not a fresh mathematical discovery.

## No-collapse test — search robustness (partial, honest)
3 independent seed points ((0.55,5.0), (0.52,14.4), (0.501,61.7)), spanning
Im≈5 to Im≈62 and Re from 0.501 to 0.55 (i.e., varying both how close to the
line and how high) — ALL converged to Re=0.5 exactly. This is consistent
across seeds (not seed-dependent noise), which increases confidence that the
searched region (Im≲90) is genuinely dominated by on-line zeros, rather than
that any single search attempt was simply unlucky.

**What this test does NOT establish:** that D(s) has no off-line zeros in
this range — only that our grid+findroot method's basin of attraction favors
the (evidently more numerous) on-line zeros nearby. A method less biased
toward the nearest zero (e.g., contour-integral counting per region, as used
in A-07's Speiser check) would be needed to search this range more
conclusively — parked, see decision.md.
