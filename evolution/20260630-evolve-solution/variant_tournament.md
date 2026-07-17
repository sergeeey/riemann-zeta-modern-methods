# H-12 Evolutionary Variant Tournament

Date: 2026-06-30
Method: `/evolve-solution` via `$evolutionary-search`
Decision: choose the smallest next mutation that returns value after H-12 stopped being a credible direct RH proof project.

## Context Loaded

[CODE] `.claude/memory/activeContext.md` says H-12 as research is closed; value is a live proof-of-concept / demo asset for Skeptic Engine.

[CODE] `SYNTHESIS.md` says the project did not prove RH, produced no new mathematical result, but produced a reusable toolkit, a landscape map, rejected bad proofs, and a methodology demonstration.

[CODE] `SKEPTIC-ENGINE-CASE.md` lists 11 caught circularities, overclaims, tautologies, numerical/memory errors, including one self-inflicted circularity in A-06 Li.

[CODE] Existing `null_results/` already contains the Grant RH audit reject entry.

## Fitness Function

Mode: `learning_value` with implementation tie-breaker.

| Dimension | Weight | Why |
|---|---:|---|
| evidence_gain | 0.25 | Should reduce uncertainty about project value. |
| baseline_delta | 0.20 | Must beat doing nothing. |
| falsifiability | 0.15 | Must be killable by traceability/review. |
| feasibility | 0.15 | Should be executable from current artifacts. |
| novelty | 0.10 | Should add a new value path, not repeat RH work. |
| reversibility | 0.10 | Should not contaminate math claims. |
| reuse_value | 0.05 | Should compound into methodology assets. |

Risk penalty is subtracted after weighted score on a 0-5 scale.

## Variants

| Variant | Mechanism | Smallest Test | Kill Condition | Fitness | Verdict |
|---|---|---|---|---:|---|
| V0 Pause/archive | Keep repo as-is; no new work. | Do nothing; preserve current state. | If downstream Skeptic Engine value exists, this leaves value unused. | 2.45 | Baseline |
| V1 Case-study packet | Turn 11 catches into a traceable Skeptic Engine golden-set seed. | Build catch-to-artifact matrix and evidence packet. | Fewer than 8/11 catches trace cleanly to source artifacts. | 4.15 | Winner |
| V2 Computational landscape note | Convert SYNTHESIS into an honest RH landscape article. | Draft outline with citations and caveats. | Requires literature claims beyond current evidence or implies novelty. | 3.05 | Park |
| V3 Extend proof-paper audit set | Audit 3-5 more RH proof papers to generalize taxonomy. | Select papers and run same FL/skeptic protocol. | Selection bias or no reproducible labeling protocol. | 3.70 | Next mutation after V1 |
| V4 Continue math attack on a/lnT strip | Search for new numerical or analytic insight near critical line. | Define one falsifiable experiment on strip behavior. | No path beyond re-demonstrating known barriers. | 2.35 | Kill for now |
| V5 Cross-model adversarial rerun | Re-run top catches with a different model/toolchain to test independence. | Blind-review 3 critical catches. | Same context leakage or no artifact trace. | 3.55 | Mutate into V1 review gate |

## Winner

V1 wins because it is the smallest reversible mutation that beats the baseline and aligns with the project’s verified conclusion: H-12 is valuable as a methodology/golden-set asset, not as a proof attempt.

## Red-Team Findings

| Finding | Severity | Response |
|---|---|---|
| The case can be accused of validation theater because the same broad AI ecosystem produced and judged artifacts. | HIGH | Require catch-to-artifact traceability and add V5 cross-model adversarial review before external claims. |
| The phrase “proof-of-concept” may overclaim generality from one project. | MEDIUM | Label as one-case demo; generalization remains `[NEEDS-REAL-DATA]` until 3-5 more audits exist. |
| Mathematical readers may misread the packet as RH progress. | HIGH | Lead with “no proof, no novelty claim”; separate math landscape from verification-engine evidence. |
| Continuing A-07/A-08 could feel intellectually attractive but has low VOI now. | MEDIUM | Park math continuation unless a new mechanism or external collaborator changes the fitness function. |

## Null Results / Parked Variants

- V2 parked: useful later, but lower direct value than Skeptic Engine packet.
- V4 killed for now: repeats known barrier work without a new mechanism.
- V5 merged as a review gate for V1 rather than standalone next step.

## Evolution Lineage

Current project state -> proof attempt closed -> methodology/case-study value identified -> variants compared -> V1 selected -> V3 reserved as next generalization step.

## Next Action

Create `catch_traceability_matrix.md` for the 11 catches. Minimum pass: 8/11 catches have direct file paths, evidence labels, baseline/negative-control note, and reproduction path. Do not transfer to the Skeptic Engine manuscript until the matrix passes this gate.
