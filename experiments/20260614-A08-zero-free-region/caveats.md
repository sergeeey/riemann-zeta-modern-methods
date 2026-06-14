# Caveats — A-08
Date: 2026-06-14
Source: skeptic [WEAKENED] + reviewer LGTM(P2) + tool verification

## CAVEAT-1 — "ZFR does not approach ½" is about POINTWISE ZFR only → CRITICAL, RESOLVED
The claim that the zero-free boundary moves toward Re=1 (not ½) is true ONLY for
**pointwise** zero-free regions of the form σ>1−f(t) (de la Vallée-Poussin,
Vinogradov-Korobov, MTY). It does NOT mean classical methods are blind near ½:
- **Zero-density theorems** (Bourgain, Guth-Maynard 2024) bound the NUMBER of zeros
  off the line — they say off-line zeros are rare.
- **Proportion on the line** — our OWN A-07: Levinson 1/3, PRZZ 41.7% of zeros are
  EXACTLY on Re=½. That is direct information at ½, not "approaching".
- **Selberg CLT** describes ζ on the line itself.
Without this distinction, a reader wrongly concludes "classical theory is helpless
near ½". It is not. A-08 is the pointwise-ZFR face of the wall; A-07 is the
density/proportion face. Both stall at the a/lnT strip, by different mechanisms.

## CAVEAT-2 — "gap grows" is largely arithmetic → ACCEPTED
σ_zf−½ → ½ because 1/ln t → 0. The non-trivial content is (a) the explicit MTY
constant R=5.558691 (a real research result, not arithmetic) and (b) the crossover
solved numerically. The experiment ILLUSTRATES published bounds; it is not a new
math result.

## CAVEAT-3 — R taken on trust → ACCEPTED
R=5.558691 and C=55.241 are from Mossinghoff-Trudgian-Yang 2022, NOT verified
against the source PDF in this session. The REF table is derived from R, so its
agreement is self-consistency, not independent validation. To harden: cite the MTY
theorem number + value directly.

## CAVEAT-4 — crossover number corrected → RESOLVED
VK overtakes classical at t > 10^3877 (my findroot, k=(C/R)³=981.4). The lit-review
agent's earlier "10^434" was wrong; skeptic and reviewer both independently
re-derived 10^3877. Either way it is astronomical, but the correct figure is 10^3877.

## CAVEAT-5 — region of validity → ACCEPTED
MTY bound holds for |t|≥2. Within validity σ_zf∈(0.74,1)⊂(½,1). Below t≈1.2 the
formula would dip under ½, but that is outside the theorem — not a real feature.

## What this experiment does NOT mean
1. Does NOT prove RH (ZFR gives a sliver near Re=1).
2. Does NOT mean classical theory is silent near ½ (see CAVEAT-1: density + A-07).
3. Is NOT a new result (illustrates MTY 2022 + von Koch).
4. The gap is not closable by better constants — any σ>1−f(t), f→0, gives σ_zf→1.
