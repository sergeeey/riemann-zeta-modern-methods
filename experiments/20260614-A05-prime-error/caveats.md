# Caveats — A-05
Date: 2026-06-14
Source: skeptic [WEAKENED] + reviewer LGTM(P2) + tool verification

Unlike A-12/A-07, the measurement here is genuine (real quality of π≈li), not a
tautology. But the result is classical, and the table invites one dangerous
misreading. Skeptic's main concern accepted and fixed.

## CAVEAT-1 — li>π bias is NOT universal  → RESOLVED (skeptic HIGH)
The table shows li(x)>π(x) on all of [10²,10⁷]. This is the textbook trap:
Littlewood (1914) proved the sign of li−π changes infinitely often; the first
crossover is bounded near ~1.4×10³¹⁶ (Bays–Hudson 2000) — ~309 orders of magnitude
beyond our table. Absence of a flip here proves NOTHING about large x. Now warned
explicitly in stdout AND on the figure.

## CAVEAT-2 — Schoenfeld bound only valid x≥2657  → RESOLVED
x=100 (ratio 2.80) and x=1000 (ratio 1.11) exceed the bound — expected, the formula
is proven only for x≥2657 (Schoenfeld 1976 Thm 10). Rows marked "(*bound n/a)".

## CAVEAT-3 — not new  → ACCEPTED
Reproduces classical computations (Riesel–Göhl 1970; extended to x=10²⁵ by Büthe
2014). Novelty: none. Value: illustrative — shows concretely WHAT RH buys.

## CAVEAT-4 — empirical to 10⁷  → ACCEPTED
Like all our numerical atoms. Does not prove RH or von Koch; confirms consistency
on this range.

## CAVEAT-5 — what RH buys, quantified  → ADDED (skeptic suggestion)
The point of "what RH buys" needs the contrast:
- WITHOUT RH (best unconditional, Vinogradov–Korobov): error ~ x·exp(−c(ln x)^{3/5}(ln ln x)^{-1/5})
- WITH RH (von Koch): error = O(√x·ln x)
RH replaces a barely-better-than-x/(ln x)^k bound with a √x bound — that is the
buy. (We did not compute the unconditional curve; stated from literature.)

## CAVEAT-6 — li vs Li(offset)  → RESOLVED (reviewer P2)
mp.li(x) is the Cauchy PV from 0 (Schoenfeld notation), not Li(x)=li(x)−li(2).
Difference ~1.045, negligible for the bound check. Documented in code # WHY.

## What this does NOT mean
1. Does NOT prove RH (empirical to 10⁷).
2. Does NOT imply li>π for all x (Littlewood — the opposite is true infinitely often).
3. Is NOT a new result (classical, computed to 10²⁵ elsewhere).
4. The bound formula does not apply below x=2657.
