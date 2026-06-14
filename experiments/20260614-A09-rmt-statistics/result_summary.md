# Result Summary — A-09 · RMT-статистика
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE (with reformulated claim)

## Original claim → Reformulated claim
**Original (overreached):**
> "Spacings follow GUE, showing level repulsion, not Poisson."

**Reformulated (defensible, tool + scipy verified):**
> The normalized spacings of the first 2000 zeros of ζ(s) (heights 14–2515) are
> dramatically closer to the Wigner GUE surmise (KS=0.041) than to Poisson
> (KS=0.317, p=10⁻¹⁷⁸): level repulsion is unambiguous (P(δ<0.3)=0.014 vs 0.26
> for Poisson; <s²>=1.15 vs 2.0). This is strong numerical EVIDENCE consistent
> with the Montgomery–Odlyzko conjecture. A small, statistically-significant
> over-repulsion vs the 2×2 surmise (p=0.002) is expected from finite-T
> corrections (~1/ln T) and from the zeros being a correlated (not i.i.d.) process.
> It is NOT a proof of RH or of the GUE link.

## Evidence ledger
| Finding | Marker | Detail |
|---------|--------|--------|
| Level repulsion present | [VERIFIED-REAL] | P(δ<0.3)=0.014, <s²>=1.15 |
| Far from Poisson | [VERIFIED-REAL] | KS=0.317, p=10⁻¹⁷⁸ |
| Close to GUE surmise | [VERIFIED-REAL] | KS=0.041, scipy-confirmed |
| Stable across height | [VERIFIED-tool] | 5 sub-bands all → GUE |
| Pipeline not faking GUE | [VERIFIED-tool] | 2 independent Poisson controls → Poisson |
| Slight over-repulsion | [CAVEAT] | finite-T + correlations, expected |
| GUE link is conjecture | [BY-DESIGN] | evidence, not proof |

## Skeptic resolution scorecard
| Caveat | Verdict |
|--------|---------|
| C1 surmise≠exact GUE | ACCEPTED (wording) |
| C2 low height | ACCEPTED |
| C3 KS rejects iid | ACCEPTED (expected, wrong null) |
| C4 conjecture | ACCEPTED |
| C5 moments missing | RESOLVED (added <s²>) |
| C6 pipeline fakes GUE | DISMISSED (2 controls) |

## Reviewer scorecard
LGTM (P2 only). All numerics scipy-verified. Fixed: figure label, off-by-one in
synthetic count, added moments. ruff clean.

## Deliverable
- RMT analysis pipeline (reusable for higher-T runs)
- Independent scipy audit harness (skeptic_attack.py)
- Strong evidence feeding the Hilbert–Pólya direction (A-12)
