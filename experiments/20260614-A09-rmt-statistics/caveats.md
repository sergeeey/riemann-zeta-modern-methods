# Caveats — A-09
Date: 2026-06-14
Source: skeptic [WEAKENED] + independent scipy audit (skeptic_attack.py, tool-run)

## CAVEAT-1 — Wigner surmise ≠ exact GUE  → ACCEPTED
Comparison is against the 2×2 Wigner surmise, not the exact N→∞ Gaudin/Mehta
distribution. They differ ~3–5% in the tails. Correct wording: "consistent with
the Wigner GUE surmise", not "follows exact GUE".

## CAVEAT-2 — Low height T∈[14, 2515]  → ACCEPTED
Odlyzko-grade tests use T~10²⁰. At T~2500 finite-size corrections ~1/ln(T)≈13%
are not negligible. Our P(δ<0.3)=0.014 vs surmise 0.027 (and <s²>=1.148 vs 1.178)
shows the zeros are slightly MORE rigid than the surmise — consistent with known
finite-T corrections, but cannot be cleanly separated from them at this height.

## CAVEAT-3 — KS formally rejects exact i.i.d. surmise  → ACCEPTED (expected)
scipy KS to GUE: D=0.041, p=0.0022. Formally this rejects "spacings are i.i.d.
draws from the Wigner surmise" at the 0.002 level. Two reasons, both benign:
(a) finite-T corrections (CAVEAT-2); (b) zeros are CORRELATED (spectral rigidity),
not i.i.d. — so the i.i.d. KS null is the wrong null for a strong claim.
The qualitative verdict (GUE-like, not Poisson) is unaffected: KS_Poisson p=10⁻¹⁷⁸.

## CAVEAT-4 — GUE/ζ link is a CONJECTURE  → ACCEPTED
Montgomery (1973) pair-correlation + Odlyzko (1987) numerics = strong evidence,
NOT a theorem. This experiment is more numerical evidence, not a proof.

## CAVEAT-5 — moments now added  → RESOLVED
Skeptic asked for an independent discriminator beyond KS. Added <s²>:
real 1.148, GUE 1.178, Poisson 2.0 → confirms GUE side, far from Poisson.

## CAVEAT-6 — pipeline-faking ruled out  → DISMISSED
Concern: does unfolding manufacture GUE? Disproved twice: (a) our synthetic
Poisson control → Poisson; (b) skeptic's independent Exp(1) sample → Poisson
(p=0.50). The code does not impose level repulsion.

---

## What this experiment does NOT mean
1. Does NOT prove the Riemann Hypothesis.
2. Does NOT prove the Montgomery–Odlyzko conjecture (adds evidence only).
3. Does NOT extrapolate beyond T≈2515 without more data.
4. Does NOT distinguish exact GUE from "GUE-like with finite-T corrections".
5. Tests Wigner surmise, not the exact Gaudin distribution.
