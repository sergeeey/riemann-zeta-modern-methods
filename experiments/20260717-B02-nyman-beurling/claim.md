# B-02 — claim.md

**Stakes:** internal-only (sandbox scouting, not external-facing yet)
**Question type:** descriptive (does a finite-N computation match a proven asymptotic formula?)

## Source [VERIFIED — read directly, pdftotext of actual arXiv PDFs]
- Formula for d_N²: Bettin–Conrey–Farmer, arXiv:1211.5191, eq. in §1 (citing [Bag] for account).
- Explicit test polynomial + Theorem 1: same paper, `bettin_conrey_farmer_1211.5191.txt` lines ~95-127.
- Unconditional lower bound (Báez-Duarte–Balazard–Landreau–Saias, improved by Burnol): same paper,
  lines ~60-90 — liminf d_N² log N ≥ Σ_{Re(ρ)=1/2} m(ρ)²/|ρ|².

## Claim (falsifiable)
Under RH (assumed, not tested — same posture as every other atom in this project) and assuming
all nontrivial zeros are simple (so eq. 1 applies): the specific Dirichlet polynomial
V_N(s) = Σ_{n=1}^N (1 − log n/log N)·μ(n)/n^s satisfies

  I_N := (1/2π) ∫_{-∞}^{∞} |1 − V_N(1/2+it)|² / (1/4+t²) dt  →  (2+γ−log 4π)/log N   as N→∞.

**Check (measurable outcome):** compute I_N numerically for a ladder of N (e.g. 10, 30, 100, 300,
1000, 3000) and compare I_N·log(N) to the constant C = 2+γ−log(4π) ≈ 0.0461914...
(γ=Euler-Mascheroni ≈0.5772157, log(4π)≈2.5310393).

**Falsifiable predicate:** I_N·log(N) converges toward C as N grows (within numerical integration
error) → CONFIRMED (theorem's finite-N behavior matches, illustrates convergence rate). If it does
NOT trend toward C, or trends toward something else → FALSIFIED (either our implementation is
wrong, or literature transcription is wrong — investigate before concluding anything about the
theorem itself, which is peer-reviewed and not what's actually under test).

## What this does NOT mean
1. Does NOT test or prove RH — RH is an assumption baked into the theorem being illustrated.
2. Does NOT compute the true optimal d_N² (the infimum over ALL Dirichlet polynomials) — V_N is
   one specific candidate proven asymptotically optimal, not the exact infimum for finite N.
3. Does NOT verify the "mild condition" eq.(2) of Bettin-Conrey-Farmer (Σ1/|ζ'(ρ)|² growth) —
   that is a separate, harder analytic-number-theory claim we are not attempting to check.
4. A numerical match for feasible N (up to ~thousands) is NOT proof the N→∞ limit holds — it is
   consistent-with, same epistemic status as every finite-N check in this project (A-04, A-05, A-08).

## Assumptions
| # | Assumption | Status |
|---|---|---|
| A1 | RH is true | Unverifiable by us; stated explicitly, same as all RH-conditional atoms |
| A2 | All nontrivial zeros simple | Standard conjecture, not independently checked |
| A3 | Bettin-Conrey-Farmer Theorem 1 correctly transcribed from PDF | [VERIFIED] via direct pdftotext read, not WebFetch paraphrase (which fabricated fake theorem numbers earlier this session — cross-checked) |
