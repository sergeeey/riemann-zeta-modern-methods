# Caveats — A-07
Date: 2026-06-14
Source: skeptic [WEAKENED] + tool verification

Central finding (skeptic): the numerical part re-derives Speiser (1934) and known
zeros of ζ'. Like A-12, the real value is the literature map (why ~41%), not the
computation. Accepted.

## CAVEAT-1 — "illustrates Levinson's method" is overstated  → ACCEPTED
The Speiser test (locating zeros of ζ') is NOT Levinson's density method. Levinson
uses a MOLLIFIER and a mean-value integral; we did not reproduce that machinery.
The link is real but indirect: Levinson counts zeros of ζ on the line via zeros of
ζ' (Levinson–Montgomery). Correct wording: "Speiser test, connected to the ζ'-based
view that underlies Levinson", not "illustrates Levinson's method".

## CAVEAT-2 — results are not new  → ACCEPTED
Speiser equivalence (1934), zeros of ζ' all right of the line (known), the 41.7%
record (PRZZ 2020) — all from the literature. Our contribution is internal:
confirmed Speiser to Im=50 with our toolkit, and mapped WHY 41% is a ceiling.

## CAVEAT-3 — Im≤50 is tiny  → ACCEPTED
Like all our numerical checks (A-10/A-12), this is empirical to a small height. It
does not prove Speiser/RH; it is consistent with them in this range.

## CAVEAT-4 — left-count=0 does not probe the a/lnT strip  → ACCEPTED (important)
The 41% ceiling comes from zeros of ζ' just to the RIGHT of the line, in
½≤σ<½+a/lnT. Our left-region test (0<Re<½) correctly finds 0, but that is the
EASY side. We did NOT measure the near-line right-side density that actually causes
the ceiling. So this experiment confirms Speiser, but does not itself demonstrate
the 41% mechanism — that remains a literature result.

## CAVEAT-5 — 41% is a literature fact, not our result  → ACCEPTED
The record fraction and its cause are reported from review, not computed here.

## What this experiment does NOT mean
1. Does NOT prove RH (empirical Speiser check to Im=50).
2. Does NOT reproduce Levinson's density method (no mollifier).
3. Does NOT improve or even numerically demonstrate the 41% ceiling.
4. Is NOT a new result (Speiser 1934 + known ζ' zeros).

## What was genuinely useful
- Toolkit extended to ζ' and validated (API cross-checked, zeros match lit to 1e-6).
- First-hand confirmation of Speiser's equivalence direction (left = empty).
- Clear understanding: 41% ≠ a bug in the method; it is a structural loss near the
  line that needs a fundamentally new idea, not a longer mollifier.
