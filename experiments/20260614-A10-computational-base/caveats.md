# Caveats — A-10
Date: 2026-06-14
Source: skeptic agent [WEAKENED] verdict + tool-verified resolution

Each caveat below is either ACCEPTED (a real limitation we keep) or
RESOLVED (skeptic was right initially, fixed by adding a test).

---

## CAVEAT-1 — "Re=½ is assigned, not measured"  → RESOLVED
Skeptic: code sets `re=half` constant; finds zeros of Z(t) which lives only on
the line. So it proves "100 zeros ON the line", a known result since Gram 1903 —
NOT that there are no zeros OFF the line.
**Resolution [VERIFIED-tool]:** added contour count of ξ'/ξ over rectangle
Re∈[-0.5,1.5] (CHECK 2). This spans the full strip width and would count any
off-line zero. It returns exactly the on-line count (5,10,15) up to T≈66.
→ Re=½ IS measured (no off-line zeros) at least up to T≈66.
**Residual limitation:** direct contour verified only to T≈66 (15 zeros).
For zeros 16–100 (up to T≈237) we rely on mp.nzeros (see CAVEAT-4).

## CAVEAT-2 — "No true independence; everything is mpmath"  → ACCEPTED
All of siegelz, zetazero, zeta, nzeros live in mpmath and share Euler–Maclaurin /
Riemann–Siegel infrastructure. A systematic mpmath bug would fool all of them.
**Only external anchor:** Odlyzko published values (10 zeros, 18 digits).
**Mitigation:** the contour method (CHECK 2) is a different ALGORITHM (argument
principle on ξ, not Riemann–Siegel) — algorithmically independent even if same lib.
**Honest status:** results are conditional on mpmath correctness. For higher
assurance, cross-check against an independent library (e.g. Arb/FLINT, SageMath)
or against Odlyzko's full high-precision tables. Not done in this experiment.

## CAVEAT-3 — "Negative controls are trivial sanity-tests"  → RESOLVED
Skeptic: ζ(2)=π²/6, Z(18)≠0, ζ(½+14i)≠0 test the math library, not the claim.
**Resolution:** the contour off-line detector (CHECK 2) is the real negative
control for "off-line zero exists". The trivial three are retained as library
sanity but are no longer the basis of the verdict.

## CAVEAT-4 — "Turing count (nzeros) is circular with siegelz"  → DISMISSED
Skeptic (self-rated MEDIUM confidence): nzeros uses Riemann–Siegel like siegelz,
so nzeros==found is one algorithm agreeing with itself.
**Disproof [VERIFIED-tool]:** CHECK 1 coarsened our scan so it missed zeros
(29→21→6) while mp.nzeros stayed fixed at 29. If nzeros read our sign changes it
would have dropped too. It did not → nzeros is independent of our scan.

## CAVEAT-5 — "Does not scale; scan_step=0.1 misses close zeros"  → ACCEPTED
Valid for T≤250 (min gap ≈1.1). NOT safe for known close pairs (e.g. Lehmer
pair near t≈7005) or large T where gaps shrink ~2π/ln(t). Naive scaling will
miss zeros. The Turing completeness check WOULD detect the miss (count mismatch),
but the toolkit would need adaptive step / Riemann–Siegel refinement to fix it.

## CAVEAT-6 — "1e-30 precision is inflated"  → PARTIALLY ACCEPTED
- vs mp.zetazero (2.8e-30): GENUINE — CHECK 3 shows monotone convergence
  (2.2e-22 at dps15 → 1.3e-37 at dps30), real, not cached.
- vs Odlyzko (9.4e-19): this is a FLOOR set by reference.py storing only 18
  digits, NOT the algorithm's true accuracy. To claim more, store more reference
  digits.

---

## What this experiment does NOT mean (reaffirmed)
1. Does NOT prove the Riemann Hypothesis (only first ~100 zeros; RH is ∀).
2. Does NOT explain WHY Re=½ (mechanism is atoms A-12, A-14).
3. Does NOT establish anything beyond T≈237; contour-direct only to T≈66.
4. Is CONDITIONAL on mpmath correctness (single library, one external anchor).
