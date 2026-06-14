# Result Summary — A-10 · Вычислительная база
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE (with reformulated claim)

## Original claim → Reformulated claim
**Original (overreached, per skeptic):**
> "Independent toolkit computes first 100 zeros; all lie on Re=½."

**Reformulated (defensible, tool-verified):**
> Using mpmath, we located the first 100 nontrivial zeros of ζ(s) on the
> critical line (sign changes of Hardy Z), matching Odlyzko (18 digits) and
> mp.zetazero (1e-30). Independently, an argument-principle contour over the
> FULL strip width (Re∈[-0.5,1.5]) confirms NO off-line zeros up to T≈66, and
> the (verified-independent) Turing count extends "all-on-line" to T≈237.
> This reproduces a well-known computational fact; it does NOT prove RH.

## Evidence ledger
| Finding | Marker | Detail |
|---------|--------|--------|
| 100 zeros located on line | [VERIFIED-REAL] | matches external Odlyzko |
| No off-line zeros up to T≈66 | [VERIFIED-tool] | contour ξ'/ξ = on-line count |
| All-on-line to T≈237 | [VERIFIED-tool] | Turing nzeros, independence proven (CHECK 1) |
| Precision genuine | [VERIFIED-tool] | CHECK 3 monotone convergence |
| Conditional on mpmath | [CAVEAT] | single library; Odlyzko sole external anchor |
| Does not prove RH | [BY-DESIGN] | finite N; RH is universal |

## Skeptic resolution scorecard
| Caveat | Verdict | How |
|--------|---------|-----|
| CAVEAT-1 Re assigned | RESOLVED | contour measures full strip |
| CAVEAT-2 all mpmath | ACCEPTED | honest limitation, Odlyzko anchor |
| CAVEAT-3 trivial neg ctrl | RESOLVED | contour = real off-line detector |
| CAVEAT-4 Turing circular | DISMISSED | CHECK 1 proves independence |
| CAVEAT-5 no scaling | ACCEPTED | documented; Turing would catch miss |
| CAVEAT-6 precision inflated | PARTIAL | genuine vs zetazero; floor vs Odlyzko |

## Reviewer (code review) scorecard
| Finding | Severity | Status |
|---------|----------|--------|
| findroot single-point can run off interval | P0 | FIXED → two-point form [t_prev,t] (Brent). Bug was LATENT (results identical before/after — zeros well-separated at T≤250), fix is preventive for close zeros / large T |
| z_prev==0 exact-grid zero skipped | P1 | FIXED → explicit case |
| no guard on empty found[] | P2 | FIXED → RuntimeError |
Post-fix: ruff clean, verification PASS identical, CHECK 1-3 pass.

## Deliverable
A reusable, skeptic-hardened zeta toolkit (`src/zeta/`) for all later atoms:
- zeta, hardy_Z, hardy_theta
- find_zeros_on_critical_line (independent sign-change finder)
- argument_principle_count (off-line detector, in adversarial_checks)
- verify_zero_on_critical_line
