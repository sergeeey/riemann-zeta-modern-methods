# Decision — B-07 · Davenport-Heilbronn negative control

## Verdict: **PROMOTE (scoped down from the original sandbox idea)**

## What survived
- D(s) implemented via Hurwitz zeta, functional equation ξ(s)=ξ(1−s) verified
  to <10⁻²⁵ at 3 arbitrary points — [VERIFIED-tool], not just source-copied.
- The negative-control LOGIC itself: D(s) is a real, published, peer-reviewed
  case where "functional equation + symmetric shape" does NOT imply RH-type
  zero confinement — usable as a concrete, worked counterexample when
  auditing future reasoning steps in this project (or Grant-style external
  claims) for the specific circularity already caught twice (Grant Doc A,
  A-06 v1): silently assuming Re(ρ)=½ as an input to a derivation.

## Kill Analysis
**What was killed:** the original sandbox idea's implicit assumption that
finding a specific off-line zero of D(s) ourselves would be a same-session,
low-cost task ("outcome: прогон на Grant Doc A ✓" implied a quick check).
Three grid+findroot search attempts (seeds spanning Im≈5 to Im≈62, Re from
0.501 to 0.55) ALL converged to Re=0.5 exactly — the naive search method's
basin of attraction favors the literature-confirmed abundant on-line zeros
over the (also literature-confirmed, but evidently sparser or higher-Im)
off-line ones.

**What was NOT killed:** the existence of off-line zeros of D(s) itself —
that is settled, peer-reviewed mathematics (Davenport & Heilbronn 1936; AMS
Mathematics of Computation 2007, "Zeros of the Davenport-Heilbronn
Counterexample"), independent of whether our search found one today. Nor was
the core negative-control USE CASE killed — it does not require us to have
personally located a specific off-line zero, only that off-line zeros are
established to exist, which they are.

**Pattern note (3rd occurrence this session):** B-01 (Connes replication),
F1/B-06 (Speiser extended-T), and this off-line-zero search all shared the
same shape of surprise — an idea-generation step ("dешево", "one session")
underestimated the actual numerical/search cost once attempted. Worth folding
into how future idea-generation cost estimates are calibrated (see pearl
candidate below).

## Skeptic Step 8a
`[SKEPTIC-PRE-ANSWERED]`: predictable objection — "you didn't actually find
an off-line zero, so this doesn't prove anything" — addressed explicitly in
claim.md's "What this does NOT mean" #2 and controls.md, marked
[VERIFIED-REAL, literature] vs [VERIFIED-tool] throughout, not blurred.

## Revival condition (for the parked search sub-task)
One of: (a) obtain the AMS 2007 paper's own tabulated off-line zero
coordinates as a search seed (WebFetch on that PDF failed with HTTP 403 this
session — try a mirror, e.g. a university library proxy or a citing paper
that quotes the coordinates); (b) implement contour-integral zero-counting
per region (reusing A-07's `count_zeros_in_rect`-style method) instead of
grid+findroot, to get an unbiased count rather than a nearest-attractor
search.

## What's next
Not a new atom — this is a completed (scoped) methodology tool. No further
Track R session required unless the parked search sub-task is picked up.
