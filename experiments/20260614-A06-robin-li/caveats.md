# Caveats — A-06
Date: 2026-06-14
Source: skeptic [WEAKENED] + tool verification

## CAVEAT-1 — Li from-zeros is CIRCULAR → RESOLVED (the important one)
The first version computed λ_n via ρ=½±iγ — assuming Re=½, the very thing RH asserts.
By Bombieri-Lagarias, zeros on the line ⟹ λ_n>0 automatically, so "λ_n>0" was a
TAUTOLOGY, not a test. This is the SAME error we rejected in Grant's Doc A (assuming
the conclusion). **Fixed:** added λ₁ via the zero-free closed form 1+γ/2−ln(4π)/2
(= 0.0231, uses only constants, no zeros, no Re assumption) — a GENUINE positive
datapoint. The from-zeros λ_n are kept but explicitly tagged ILLUSTRATIVE. Their
agreement with the independent λ₁ is a weak check that the zeros really are on Re=½.

## CAVEAT-2 — 26 vs 27 exceptions → RESOLVED ([VERIFIED-tool] > [MEMORY])
Tool: 26 exceptions in n∈[3,5040]. n=2 excluded (ln ln 2<0 makes the bound negative;
the ratio test gives <1). Literature's "27" counts n=1 (degenerate) or n=2 by
convention (OEIS A067698 lists 26 for n≥3). My initial claim said 27 from memory —
corrected to 26 with explanation.

## CAVEAT-3 — Robin to 10⁴ is shallow → ACCEPTED
Only reproduces OEIS A067698 (known exceptions ≤5040). Colossally abundant numbers
>10⁴ (10080, 15120, …) NOT checked; literature checked to ~10^500 (Akbary-Friggstad).
A finite scan cannot find an RH violation among colossally abundant numbers anyway
(their ratios approach 1 very slowly). Genuine but not a strong test.

## CAVEAT-4 — λ₁ from-zeros truncation → ACCEPTED
0.02265 (2000 zeros) vs 0.0231 (exact) — ~2% from finite-sum truncation, sign correct.
The independent closed form is the authoritative value.

## What this experiment does NOT mean
1. Does NOT prove RH (both criteria are RH-equivalent; finite checks are empirical).
2. The Li from-zeros part does NOT independently test RH (circular; only λ₁-independent does).
3. The 26 Robin exceptions (≤5040) are part of the theorem, not counterexamples.
4. Robin scan (≤10⁴) does not cover large colossally abundant numbers.

## Honest value
- Robin: genuine zero-independent confirmation that the inequality holds to 10⁴
  (reproduces OEIS) — RH in arithmetic language.
- λ₁ independent > 0: a real (n=1) positive Li datapoint, zero-free.
- The session's recurring lesson, now self-inflicted and caught: assuming Re=½ to
  "verify" RH is circular — exactly Grant's error.
