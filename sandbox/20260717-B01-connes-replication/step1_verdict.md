# B-01 Step 1 — CDT verdict (2026-07-17)

## Source trace [VERIFIED via WebFetch + pdftotext of the actual arXiv PDF]
- arXiv:2602.04022, Alain Connes, "The Riemann Hypothesis: Past, Present and a Letter Through Time" — real, exists, 42pp, submitted 2026-02-03.
- Full text extracted: `connes_2602.04022.txt` (pdftotext -layout, 2751 lines).
- "Letter to Riemann" section: lines ~1590-1690. Numerical table of differences: lines ~1660-1668 —
  matches the claimed 2.60179e-55 for the first zero, decreasing precision to ~1e-2 for the 50th. REAL, not fabricated.
- Underlying theory (§4.1 Weil positivity, §6.1-6.4): real, standard Riemann-Weil explicit formula
  (eq. 8-10), Theorem 6.1 (Connes-van Suijlekom, joint paper [32]), Hermite/prolate-spheroidal
  machinery (Slepian-Pollak-Landau). Not pseudo-math.

## What IS given (sufficient to understand, not yet to code)
- Weil's quadratic form Q_W via explicit formula (eq. 9-10): sum over local places W_p (primes) +
  archimedean W_R. Fully written out, standard.
- Fact 6.2/6.3: characterizes the theoretical minimizer via Hermite functions h0, h4 and prolate
  spheroidal wave functions h_{0,α}, h_{4,α} (Slepian-Pollak, standard signal-processing objects).
- Theorem 6.1: the actual RH-on-a-line-for-truncation result (real zeros of finite-truncation
  quadratic form's Fourier transform), sourced to Connes-van Suijlekom [32] (peer-reviewed).

## What is NOT given here (the actual numerical recipe)
- Footnote 14: "It is used for the trigonometric truncation at N=100 in the computation presented
  in the letter" — the exact discretization (which N=100 basis, how W_p/W_R become a finite matrix)
  is NOT spelled out in this paper. It points to **reference [25]: A. Connes and C. Consani,
  "Spectral triples and Γ-cycles", Enseign. Math. 69 (2023), no.1-2** — a real, separate,
  peer-reviewed 2023 paper.

## CDT verdict: PARTIALLY REPLICABLE-BY-TEXT — needs [25] before any code
- The theory is genuine and well-documented (no fabrication risk).
- A from-scratch numerical replication without [25] is possible in principle (build Q_W from
  eq. 9-10 in some finite trigonometric basis, diagonalize, extract Mellin zeros) but would be a
  DIFFERENT discretization than Connes', so a mismatch would prove nothing about replication —
  it would just be "our own construction," not a check of his claim.
- Getting [25]'s exact recipe is a second paper-read (12 pages est. in Enseign. Math., likely
  technical) before any code — pushes this past a single-session "read + code" budget.

## Update after reading [25]/arXiv:2106.01715 (Connes-Consani, "Spectral Triples and Zeta-Cycles")

The exact recipe is now known [VERIFIED — read directly from the paper, section 2 + 5.3-5.4]:
1. Trigonometric orthonormal basis φ_n on [-L/2, L/2] (eq. 2.21) — straightforward.
2. Matrix Δ(n,m) = Q_W(φ_n, φ_m) built from Weil's explicit formula (eq. 2.3-2.4/2.6,
   archimedean W_R + prime terms W_p) — implementable, real work but bounded.
3. A rank-k perturbed operator D(α,k) depending on support length α (defined in §4, NOT
   read in this pass) whose eigenvalues are tracked as α is SWEPT over a range.
4. An independent unperturbed operator D0(α) whose spectrum satisfies a known quantization
   condition α^(iy) = 1.
5. Zeros are NOT read directly off one diagonalization. They are selected by an EMPIRICAL
   MATCHING CRITERION: find α values where eigenvectors of D(α,k) coincide (in Hilbert-space
   distance) with eigenvectors of D0(α) — see Figures 44-54, a full multi-stage numerical
   scan+match pipeline, not a single computation.
6. Only the eigenvalues selected by that matching criterion are reported as zero approximations
   (Figure 53: "first 31 eigenvalues selected using the last criterion").

## Final decision: PARK

Tooling is not the blocker (mpmath/scipy suffice for every individual step). The blocker is
**genuine scope**: this is a multi-stage empirical pipeline (parameter sweep over α + eigenvalue
tracking + independent-operator construction + eigenvector-matching selection), which took the
original authors substantial dedicated work (7+ figures in the empirical section alone) to build
and tune. Realistic honest estimate: weeks of focused numerical work to faithfully reproduce
their exact method — not ">2 sessions," which was the plan's stated kill threshold. This clears
the kill criterion by a wide margin.

**Verdict: `[PARK]`** per `null_results/ vs parked/ Protocol` (falsification-ladder.md) — this is
valid, real, well-documented mathematics, not falsified; just deprioritized on cost grounds.

**Revival condition:** committing ≥2 weeks of dedicated numerical-research time specifically to
this replication, OR discovering that §4 (D(α,k) construction, not yet read) is materially
simpler than the empirical section suggests.

**What survives / Parked Pearl:**
- Original branch: B-01, independent replication of Connes 2026 "Letter to Riemann" zero
  approximation via Weil quadratic form extremization.
- What was killed: the *quick-replication* framing — this cannot be a 1-2 session atom.
- What survives: the underlying claim is real, sourced, non-fabricated math (both papers
  verified to exist and say what the letter claims); full formulas extracted and archived here
  (`connes_2602.04022.txt`, `connes_consani_2106.01715.txt`) for a future real attempt.
- Forbidden use: do not cite this parked entry as "replication attempted" — no code was written,
  only source verification. Do not claim partial replication.
