# A Computational Landscape of the Riemann Hypothesis: What Twelve Numerical Atoms Show and Do Not Show

Status: draft v1 · 2026-07-19 · Not a proof, not a claim of progress toward one

> **Framing, stated before any result below:** this note does not attempt to prove
> or disprove the Riemann Hypothesis, and the probability that a project at this
> scale would do so is treated as ≈0 throughout (see `PLAN-2026H2.md` §0). Its
> value is a honestly-labeled map: which classical approaches were re-derived and
> verified computationally, where each one structurally stops, and — new in this
> note — where a deliberately independent counterexample function confirms the
> verification methodology itself is not simply confirmation-biased.

---

## 1. Method: atomize, verify, label

Rather than attacking RH directly, the project decomposed it into independent
computational "atoms" — each a small, falsifiable numerical or analytical claim,
run through a fixed discipline: state the claim before computing, define a
kill criterion, run positive and negative controls, and pass every result
through an adversarial (context-blind) review before promotion. Every atom below
carries one of four honest labels:

| Label | Meaning |
|---|---|
| **PROMOTE** | survived adversarial review, stands as stated (with caveats) |
| **understanding / illustration** | correct, but re-derives or illustrates a known result — not new |
| **WEAKENED** | real finding, narrower claim than first proposed |
| **PARKED** | attempted honestly, real technical obstacle found, not resolved this round |

No atom here is claimed to move the needle on RH itself. Several are explicitly
"the same wall, seen from a different side" — that repetition is itself the
finding, not padding.

---

## 2. The core atoms (A-04 .. A-12)

| Atom | What it checked | Verdict | One-line result |
|---|---|---|---|
| A-04 | ζ zeros on Re=½ up to T=300, two independent algorithms (Hardy Z sign changes + Turing's method) | SOLID-in-window | 138 zeros found, all on the line, in this window |
| A-05 | Prime-counting error \|π(x)−li(x)\| vs the von Koch (1901) RH-conditional bound | PROMOTE | error stays inside the bound to x≤10⁷, ratio shrinking — but Littlewood's oscillation (Skewes' number) means "li>π always" is explicitly NOT claimed |
| A-06 | Robin's inequality (genuine, zero-free-based) and Li's criterion coefficients | PROMOTE (Robin) / corrected (Li) | Robin holds to 10⁴ (26 known exceptions ≤5040); first Li-coefficient attempt was **circular** (assumed Re=½) — caught by this project's own adversarial pass, fixed via the zero-free formula |
| A-07 | Proportion of zeros provably on the line (Levinson-type density methods) | understanding | **Updated 2026-10-17:** the record is now ≥0.6725 (Alpöge–Furman arXiv:2608.13637; Lamzouri arXiv:2609.02882), by a Weil-form / rank-inertia method. The 41.7% (PRZZ 2020) figure was the mollifier-line record and is historical. Class ceiling for bandwidth-one certificates ≈0.682 |
| A-08 | Zero-free region's distance from Re=½ | understanding, corrects a common misconception | the gap **grows**, not shrinks, as height increases — the classical zero-free region approaches Re=1, not Re=½ |
| A-09 | Statistics of zero spacings vs. Random Matrix Theory (GUE) | PROMOTE ★ (strongest evidence, not proof) | KS-statistic strongly favors GUE over Poisson (0.041 vs 0.317, p≈10⁻¹⁷⁸) — this is *evidence* consistent with a spectral (Hilbert–Pólya) origin, not a derivation of one |
| A-10 | Computational toolkit itself (`src/zeta`) | PROMOTE (infrastructure) | independently verified against 3 methods; basis for every later atom |
| A-12 | Hilbert–Pólya operator candidates | understanding, direction closed for proof | no candidate (Berry–Keating xp included) gives zero *positions*, only *density* — same conclusion as the field's last ~90 years |

**The honest convergence (corrected 2026-07-19):** three of these — A-07 (density),
A-09 (statistics), A-12 (operator theory) — use genuinely different mathematical
machinery and each independently stops at the same place: the fine structure of
zeros immediately next to the critical line. This is a *localization* of where a
new idea would be needed, not a step toward finding one. (An earlier, broader
version of this claim in this project's own working notes conflated A-06 — a
*derivative* of A-08's zero-free constant, not an independent line — with this
triad; that conflation was caught and corrected via this project's own
adversarial-testing discipline, not by an outside reviewer.)

---

## 3. New in this round (B-01 .. B-07): approaching the same wall from other directions

### B-02 — Nyman–Beurling criterion (Bettin–Conrey–Farmer's optimal polynomial)
**WEAKENED/illustration.** The theorem's asymptotic constant is not visibly
approached at computationally reachable N (10–3000) — I_N grows rather than
shrinks toward it. Two controls (an analytically-exact negative control, and a
quadrature-stability check across four breakpoint schemes) rule out an
implementation bug. The paper's own text explains this: it explicitly notes its
result contradicts what Landreau–Richards' numerical graphs would suggest at
moderate N — a documented pre-asymptotic effect, not a new finding, but an
independent confirmation of the same "slow approach" pattern seen elsewhere in
this landscape.

### B-03 — de Bruijn–Newman heat flow
**PROMOTE (illustration).** Implemented H_t(x) = ∫e^{tu²}Φ(u)cos(xu)du, calibrated
against two published ζ zeros (H₀(2γₙ)≈0 to 19–21 digits — strong confirmation
the formula is correctly transcribed). One well-separated zero, tracked across
t∈[−0.05, 0.05], moves smoothly and stays real — consistent with, but not a test
of, the proven bound 0≤Λ<½ (Rodgers–Tao 2018 proved Λ≥0 via GUE-repulsion; RH ⟺
Λ≤0). This atom deliberately did *not* search for a close (Lehmer-type) zero
pair — that is the scientifically sharper, harder test of the actual mechanism,
and is noted as follow-up, not claimed here.

### B-06 — Speiser's criterion at larger height
**PARKED, not falsified.** RH ⟺ ζ' has no zeros in 0<Re(s)<½ (Speiser 1934,
verified up to Im=50 in A-07). Extending this via the same contour-integration
method to T~100–800 hit growing *numerical* instability (not a genuine zero
count) — a Substrate Gate issue, explicitly not recorded as evidence for or
against Speiser's criterion. Revival requires either adaptive precision scaling
with T or a fundamentally different (non-contour) zero-counting method.

### B-07 — Davenport–Heilbronn negative control
**PROMOTE (scoped).** D(s), the classical 1936 counterexample — same
zeta-type functional equation, no Euler product, *proven* to have zeros off the
critical line — was implemented via its Hurwitz-zeta form and verified against
the functional equation ξ(s)=ξ(1−s) to <10⁻²⁵. This exists to check that this
project's own verification methodology can correctly say "no" when the answer
is no, not just "yes" on ζ. Three numerical search attempts for a specific
off-line zero all converged to on-line zeros instead (the abundant case) — the
off-line-zero *existence* is cited from the published record, not
self-rediscovered this round; a genuinely unbiased search (contour counting,
not grid+findroot) is the noted follow-up.

---

## 4. What this landscape does and does not establish

**Does establish:**
- A reusable, cross-checked computational toolkit (`src/zeta`) and a
  now-validated methodology for catching circular reasoning before it ships
  (caught in this project's own first draft, and in an external "proof" —
  see `null_results/20260614-grant-rh-audit.md`).
- A concrete localization of where classical methods stop: the strip
  ½≤σ<½+a/lnT immediately beside the critical line, approached independently
  from density theory (A-07), statistics (A-09), operator theory (A-12), and
  now approximation theory (B-02) and heat-flow dynamics (B-03).
- A working negative control (B-07): the verification methodology does not
  simply confirm whatever it is pointed at.

**Does not establish:**
- Any part of a proof of RH, or of Λ=0, or of an improved zero-free region,
  density record, or operator construction.
- That the "wall" pattern reflects one deep, unified cause rather than several
  independently-arrived-at technical limits that happen to share a similar
  quantitative shape (a distinct earlier question this project examined
  directly via cross-tool testing and left as `LOCAL-CAUSE`, not
  `PART-OF-MACROSYSTEM` — see session notes, not reproduced here as a formal
  atom).
- That any atom's numerical range (T≤50–800, N≤3000, or similar) generalizes
  beyond what was actually computed.

---

## 5. Rejected external claim (for the record)

Two PDFs by an independent author (R. E. Grant, 2026, not peer-reviewed) claiming
proofs of RH were audited and REJECTED: both rest on circular steps that assume
the conclusion under a different name (see `null_results/20260614-grant-rh-audit.md`
for the full trace, including one numerically **false** claimed theorem,
confirmed independently by two separate audit passes weeks apart).

---

## 6. Artifacts

`src/zeta/` (toolkit) · `experiments/20260614-A04..A12-*/` · `experiments/20260717-B02-*/`
`experiments/20260719-B03-*/`, `20260719-B06-*/` (parked, in `sandbox/`), `20260719-B07-*/`
`null_results/`, `parked/`, `sandbox/INDEX.md` (full registry with verdicts and dates)
`SYNTHESIS.md` (shorter internal synthesis, this note is the fuller external-facing version)

*Repository: github.com/sergeeey/riemann-zeta-modern-methods*
