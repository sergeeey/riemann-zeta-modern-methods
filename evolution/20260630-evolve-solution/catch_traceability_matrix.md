# Catch Traceability Matrix

Date: 2026-06-30
Purpose: first evidence gate for turning H-12 into a Skeptic Engine case-study / golden-set seed.

Status labels:

- `TRACE-OK`: direct artifact path found in this repository.
- `TRACE-PARTIAL`: artifact exists, but reproduction still needs a focused rerun or source extraction.
- `NEEDS-REVIEW`: do not use externally before independent review.

## Matrix

| # | Catch | Type | Source artifact | Evidence label | Trace status | Reproduction / gate |
|---:|---|---|---|---|---|---|
| 1 | Grant Doc A inserts an RH-equivalent step. | Circularity | `null_results/20260614-grant-rh-audit.md`; `SKEPTIC-ENGINE-CASE.md` | `[CODE]` | TRACE-OK | Re-read Grant audit sections for Doc A; verify claim is framed as proof rejection, not formula critique. |
| 2 | Grant Doc B treats Spectral Isomorphism / bounded deviation as proven; Thm 5.3 numerically false. | Conditional-as-proven + numerical falsification | `null_results/20260614-grant-rh-audit.md`; `SKEPTIC-ENGINE-CASE.md` | `[CODE]` / `[VERIFIED-tool]` in source artifact | TRACE-OK | Re-run or preserve the Thm 5.3 calculation before using as benchmark ground truth. |
| 3 | A-06 Li from-zeros assumed `rho = 1/2 + i gamma`. | Self-inflicted circularity | `experiments/20260614-A06-robin-li/caveats.md`; `experiments/20260614-A06-robin-li/decision.md` | `[CODE]` | TRACE-OK | Verify fixed path uses zero-free lambda_1 and labels from-zeros illustrative. |
| 4 | A-12 `1/(48*pi)` was Stirling tautology, not emergence. | Tautology-as-discovery | `experiments/20260614-A12-hilbert-polya/caveats.md`; `experiments/20260614-A12-hilbert-polya/decision.md` | `[CODE]` | TRACE-OK | Re-run `run_berry_keating.py` only if external packet needs numeric reproduction. |
| 5 | A-09 “zeros follow GUE” needed weakening. | Overclaim | `experiments/20260614-A09-rmt-statistics/caveats.md`; `experiments/20260614-A09-rmt-statistics/skeptic_attack.py` | `[CODE]` | TRACE-OK | Keep wording as GUE-like evidence, not exact-GUE proof. |
| 6 | A-07 Speiser test does not illustrate Levinson's mollifier method directly. | Overclaim | `experiments/20260614-A07-levinson-density/caveats.md`; `experiments/20260614-A07-levinson-density/review_levinson_speiser.md` | `[CODE]` | TRACE-OK | Confirm final wording says connected to zeta-prime view, not reproducing Levinson. |
| 7 | A-08 “ZFR does not approach 1/2” only applies to pointwise ZFR. | Misleading scope | `experiments/20260614-A08-zero-free-region/caveats.md` | `[CODE]` | TRACE-OK | Ensure packet distinguishes pointwise ZFR from density methods. |
| 8 | A-08 crossover was `10^3877`, not `10^434`. | Numerical error | `experiments/20260614-A08-zero-free-region/caveats.md`; `experiments/20260614-A08-zero-free-region/run_zero_free.py` | `[VERIFIED-tool]` — rerun 2026-07-17, `run_zero_free.py` VERDICT: PASS, crossover confirmed `10^3877` | TRACE-OK | Re-run done 2026-07-17. No further action before external use. |
| 9 | A-05 table risked implying `li(x) > pi(x)` always. | Dangerous extrapolation | `experiments/20260614-A05-prime-error/caveats.md` | `[CODE]` | TRACE-OK | Keep Littlewood/Skewes caveat next to any figure/table. |
| 10 | A-10 single-point `findroot` could run off interval. | Latent bug | `experiments/20260614-A10-computational-base/result_summary.md`; `src/zeta/toolkit.py` | `[CODE]` | TRACE-OK | Verify implementation uses two-point bracket `[t_prev, t]`; smoke import passed on 2026-06-30. |
| 11 | A-06 Robin exceptions were 26, not memory-claimed 27. | Memory vs tool | `experiments/20260614-A06-robin-li/caveats.md`; `experiments/20260614-A06-robin-li/decision.md` | `[VERIFIED-tool]` — rerun 2026-07-17, `run_robin_li.py` VERDICT: PASS, 26 exceptions confirmed, max=5040 | TRACE-OK | Re-run done 2026-07-17. No further action before external use. |

## Gate Result

Current pass: 11 `TRACE-OK`, 0 `TRACE-PARTIAL`, 0 missing. (updated 2026-07-17)

Numeric ground-truth reruns — DONE 2026-07-17:
- #8 (A-08 crossover): `run_zero_free.py` VERDICT PASS, crossover confirmed `10^3877`.
- #11 (A-06 Robin exceptions): `run_robin_li.py` VERDICT PASS, 26 exceptions confirmed, max=5040.
- #2 (Thm 5.3 falsification): already carries concrete computed numbers in source
  (`null_results/20260614-grant-rh-audit.md:43`, m=5→90, m=50→78, m=1000→48, mean·24=87.08≠84) —
  no separate script existed; this is not a bare claim, no rerun action needed.

**V5 cross-model blind review — DONE 2026-07-17.**
Executed via `codex exec` (OpenAI gpt-5.5, reasoning=high — different model family from Claude,
satisfying Independent Verification Strength Ladder's "Medium" independence tier). Context
Asymmetry Rule followed: Codex was given ONLY the raw mathematical claim/data for each catch
(verbatim source text, computed numbers), with NO framing, NO prior verdict, NO session history,
and explicitly instructed to judge independently. Full transcript: `v5_codex_review_20260717.txt`.

| # | Catch | Independent verdict | Confidence | Agrees with original? |
|---:|---|---|---|---|
| 1 | Grant Doc A §9 circularity | CIRCULAR-CONFIRMED | 9/10 | Yes |
| 2 | Thm 5.3 numerical falsification | FALSE-CONFIRMED | 10/10 | Yes |
| 3 | A-06 Li from-zeros circularity | CIRCULAR-CONFIRMED | 9/10 | Yes |

All three catches independently reproduced by a different model with no shared reasoning
context. This closes the last open gate from `variant_tournament.md` line 61.

**External-use condition: SATISFIED.** All 11 catches TRACE-OK, both numeric ground-truth
reruns done, V5 cross-model review done with 3/3 agreement. Track C-1 (evidence gate) is
CLOSED — ready for Track C-2 (transfer to `E:\skeptic-engine-manuscript`).
