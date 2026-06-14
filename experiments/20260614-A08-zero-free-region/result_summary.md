# Result Summary — A-08 · Zero-free region
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE as UNDERSTANDING

Illustrates published bounds (not new), but corrects a real misconception and
completes the "wall" picture from the Re=1 side.

## The result
| log₁₀ t | σ_zf (proven free) | gap to ½ |
|---------|-------------------|----------|
| 2 | 0.9609 | 0.461 |
| 6 | 0.9870 | 0.487 |
| 80 | 0.9990 | 0.499 |
| 200 | 0.9996 | 0.4996 |

- The proven zero-free boundary CLIMBS toward Re=1 as t grows; the gap to ½ GROWS,
  not shrinks. ZFR gives a sliver near Re=1, never near ½.
- VK overtakes classical only at t > 10³⁸⁷⁷ (computed; corrects lit-agent's 10⁴³⁴).
- The gap is QUALITATIVE: any σ>1−f(t) with f→0 yields σ_zf→1; no constant closes it.

## Key correction (value beyond arithmetic)
Refutes the common misconception "ZFR gradually approaches ½". It moves the OTHER
way. BUT (CAVEAT-1) this is about POINTWISE ZFR; density theorems and proportion
results (our A-07: 41.7% ON the line) DO give information at ½. A-08 and A-07 are
the two faces of the same wall.

## Evidence ledger
| Finding | Marker | Note |
|---------|--------|------|
| σ_zf climbs to 1, gap grows | [VERIFIED-tool] | monotone, gap 0.46→0.4996 |
| crossover t>10³⁸⁷⁷ | [VERIFIED-tool ×2] | skeptic+reviewer confirm; agent's 10⁴³⁴ wrong |
| matches MTY table | [VERIFIED-tool] | but self-consistent (R on trust) |
| pointwise≠density | [DOCS] | A-07 gives 41.7% AT ½ |
| not new | [ACKNOWLEDGED] | illustrates MTY 2022 |

## Skeptic scorecard
| Caveat | Verdict |
|--------|---------|
| pointwise vs density (CRITICAL) | RESOLVED (CAVEAT-1, links A-07) |
| "gap grows" arithmetic | ACCEPTED |
| R on trust / REF self-consistent | ACCEPTED |
| crossover number | RESOLVED (10³⁸⁷⁷ confirmed ×2) |
Reviewer: LGTM (P2 bracket + mkdir applied).

## Takeaway for the project
A-08 completes the convergence picture: from the Re=1 side, the proven boundary
moves AWAY from ½ and the gap is qualitative. Paired with A-07 (from ½, only 41.7%
proven on the line) the two classical fronts leave exactly the a/lnT strip next to
the line uncontrolled — the same wall every other atom hit.
