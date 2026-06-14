# Skeptic Engine vs the Riemann Hypothesis — a one-day live case study

**What this is.** A demo asset for the Skeptic Engine (scientific-verification
project). Over a single day, an AI research loop attacked the Riemann Hypothesis by
atomization (8 sub-problems) and audited two outside "proof" papers. At every step a
context-blind skeptic agent + a code reviewer ran against each claim. This document
collects **every circularity, tautology, overclaim, and numerical error they caught**
— including ones the author (the AI itself) committed.

**Why it matters for the Engine.** The single most valuable thing a verification
engine can do is catch *assume-the-conclusion* — the error that makes plausible-looking
"proofs" wrong. Here the Engine caught it **three times**: twice in an outside author's
papers, and once in the project's *own* code. That last one is the strongest possible
proof the loop is not theater: it flagged an error its own author didn't see.

---

## The catches (chronological, all tool-verified)

| # | Where | Claim as written | What the skeptic caught | Type | Resolution |
|---|-------|------------------|-------------------------|------|------------|
| 1 | Grant Doc A (outside paper) | "Geometric proof of RH" | §9 Step 4 inserts \|Σ xᵖ/ρ\|=O(√x) — which IS RH (von Koch). Assumes the conclusion. | **Circularity** | REJECT |
| 2 | Grant Doc B (outside paper) | "iHarmonic proof of RH" | Author's own text (p.87) marks the Spectral Isomorphism a *conjecture*; Thm 5.3 numerically false | **Conditional-as-proven** | REJECT |
| 3 | **A-06 Li (our own code)** | "λ_n>0 ⟺ RH, verified" | Code set ρ=½+iγ — *assumed* Re=½, the very thing RH asserts ⟹ λ_n>0 automatic (Bombieri-Lagarias). **Same error as Grant Doc A.** | **Circularity (self-inflicted)** | Fixed: zero-free λ₁=0.0231 |
| 4 | A-12 Hilbert-Pólya | "1/(48π) emerges from xp geometry" | It's just the 3rd Stirling term of θ — a tautology, verified identical to T=5·10⁵ | **Tautology-as-discovery** | Reframed, not a result |
| 5 | A-09 RMT | "zeros follow GUE" | True only as *evidence* for a conjecture; Wigner surmise ≠ exact GUE; finite-T | **Overclaim** | Softened to "evidence" |
| 6 | A-07 Levinson | "illustrates Levinson's method" | Speiser test ≠ the mollifier method; doesn't reproduce it | **Overclaim** | Reworded |
| 7 | A-08 zero-free region | "ZFR does not approach ½" | True only for *pointwise* ZFR; density methods + A-07 (41.7% on ½) do reach ½ | **Misleading scope** | Disclaimer added |
| 8 | A-08 crossover | "VK overtakes at 10⁴³⁴" (lit-agent) | Wrong; bracketed solve gives 10³⁸⁷⁷ — confirmed independently by skeptic AND reviewer | **Numerical error** | Corrected |
| 9 | A-05 prime error | table shows li(x)>π(x) everywhere | Invites "li>π always" — false; Littlewood: ∞ sign flips, first ~10³¹⁶ (Skewes) | **Dangerous extrapolation** | Warning added (stdout+figure) |
| 10 | A-10 toolkit | "zeros found correctly" | reviewer: findroot single-point can run off-interval (latent P0) | **Latent bug** | Two-point Brent |
| 11 | A-06 Robin | "27 exceptions" (from memory) | Tool: 26 exceptions in [3,5040]; memory was wrong | **Memory vs tool** | Corrected to 26 |

---

## The error taxonomy the Engine detects

1. **Assume-the-conclusion (circularity)** — #1, #2, #3. The deadliest class: the
   "proof" silently inserts RH (or an RH-equivalent) as a step. Caught in two outside
   papers *and* in the project's own Li implementation.
2. **Tautology-as-discovery** — #4. A known identity dressed up as an emergent finding.
3. **Overclaim** — #5, #6. Evidence presented as proof; an analogy presented as a method.
4. **Misleading scope / extrapolation** — #7, #9. A locally-true statement that misleads
   when read globally.
5. **Numerical / memory error** — #8, #10, #11. Wrong constant, latent bug, stale recall.

---

## The headline result

**The Engine caught the project committing the exact error it had just rejected in an
outside paper.** Grant's Doc A was rejected for inserting RH as a step (circularity).
Three atoms later, the project's own Li-criterion code did the same thing — assumed
Re=½ to "verify" RH. A context-blind skeptic, given only the claim and the code (no
author intent, no reasoning chain), flagged it. The author had not noticed.

This is the core value proposition of a verification engine: **self-deception is nearly
invisible from the inside.** A reviewer who shares your goal shares your blind spot. A
context-blind adversary, scoring only "does the claim hold?", does not.

---

## Honest boundaries (the Engine applies to itself)
- This is a methodology demo, not a benchmark. N=11 catches on one project, one day.
- The skeptic ran on Claude (same model family as the author) — cross-model would be
  stronger; here context-asymmetry (no shared reasoning chain) provided the independence.
- "Caught" means flagged + tool-confirmed; severity varied (circularity = critical,
  memory slip = minor).

---

## For the Skeptic Engine roadmap
- This is a ready golden-set entry: **RH proof-paper audit + self-audit**, with
  ground-truth (von Koch circularity is unambiguous).
- The assume-the-conclusion detector is the highest-value feature — it generalizes
  beyond math to any "we proved X" claim that secretly uses X.
- Next: run the same loop on 3–5 more arXiv/Zenodo RH "proofs" to build a labeled set.

*Source material: `experiments/` (8 atoms), `null_results/20260614-grant-rh-audit.md`,
`SYNTHESIS.md`. Repo: github.com/sergeeey/riemann-zeta-modern-methods.*
