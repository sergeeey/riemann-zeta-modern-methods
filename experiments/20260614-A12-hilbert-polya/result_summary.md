# Result Summary — A-12 · Hilbert–Pólya
Date: 2026-06-14
FL Step 8: Classification

## Classification: PROMOTE as CALIBRATION / UNDERSTANDING (not as contribution)

The skeptic was right: the numerical result re-derives known facts. We keep it
for its internal value (boundary understanding + toolkit calibration), and we are
explicit that it is NOT a research contribution.

## Two deliverables, clearly separated

### 1. Literature map (the real value of A-12) [DOCS]
All 5 Hilbert–Pólya operator candidates assessed:
| Candidate | Status | Root obstruction |
|-----------|--------|------------------|
| Berry–Keating xp | [HYPOTHESIS] | continuous spectrum; only mean density |
| Connes (adelic) | [HYPOTHESIS] | global trace formula conditional on RH (circular) |
| de Branges | [REFUTED for ζ] | Conrey–Li: positivity fails for ζ |
| Bender–Brody–Müller | [REFUTED as strategy] | Bellissard PRL: self-adjointness not established |
| Sierra (Rindler) | [HYPOTHESIS] | "proof in the limit"; regularization-dependent |
**Bottom line: no candidate provides a path to a proof. Operator unbuilt in 110+ years.**

### 2. Berry–Keating numerical check (honest scope)
- n_BK reproduces the smooth count to O(1/T) — but this is the Stirling expansion
  of θ (TAUTOLOGY, verified to T=5e5), NOT a property of xp.
- S(T) = N_exact − smooth oscillates (mean 0.03, std 0.37), confirmed independent
  of nzeros via arg ζ (agreement 0.00000). This is Selberg 1946.
- Conclusion: xp captures HOW MANY zeros, not WHERE. Known since Berry–Keating 1999.

## Evidence ledger
| Finding | Marker | Note |
|---------|--------|------|
| Density match = Stirling tautology | [VERIFIED-tool] | to T=500000, rel 0.0000% |
| S(T) real, not circular | [VERIFIED-tool] | vs arg ζ, 0.00000 |
| S consistent with Selberg | [VERIFIED-tool] | std 0.37 ~ 0.31 predicted |
| Results are not new | [ACKNOWLEDGED] | Berry-Keating 1999 + Selberg 1946 |
| No HP operator exists/proven | [DOCS] | all 5 candidates HYPOTHESIS/REFUTED |

## Skeptic scorecard
| Caveat | Verdict |
|--------|---------|
| 1/(48π) tautology | ACCEPTED (tool-confirmed) |
| "natural candidate" overclaim | ACCEPTED (downgraded) |
| std-persists not significant | ACCEPTED (F-test) |
| results not new | ACCEPTED |
| wrong-norm weak control | ACCEPTED |

## Honest takeaway for the project
A-12 closes the "spectral operator" direction as a SOURCE OF PROOF: the literature
has no working operator, and our own check confirms the most-cited candidate (xp)
only matches density (a necessary, weak condition). The A-09 GUE statistics remain
the strongest *evidence* for the HP picture — but evidence, not proof. Net: do not
invest further in building an operator; the leverage is elsewhere (A-05, A-07).
