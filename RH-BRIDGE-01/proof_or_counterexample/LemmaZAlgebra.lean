import Mathlib

/-!
# Algebraic closing step of Lemma Z+ (H12-UNIFIED-RESEARCH-01)

Lemma Z+ (candidate_lemma.md) ends with a real-number inequality.  From the two trace bounds
  upper : Tr(P_T Q) <= (1+kappa) * eps * R,      lower : Tr(P_T Q) >= t * (w/D - sqrt(eta*w/D)),   t >= (1-e') * R
one gets   w - sqrt(eta*D*w) <= a*D   with   a = (1+kappa) * eps / (1-e').   This file proves what follows from that inequality:
  * `zplus_alg_cor`  : w <= D (eta + 2a)
  * `zplus_alg_sharp`: w <= D (sqrt eta + sqrt(eta + 4a))^2 / 4   (exact solution of the quadratic inequality; equality at eta = 0, w = a D)
It does NOT formalize the trace/projection part of the lemma (NOT_RUN in Lean).
-/

open Real

theorem zplus_alg_cor (w D η a : ℝ) (hD : 0 < D) (hw : 0 ≤ w) (hη : 0 ≤ η) (_ha : 0 ≤ a)
    (h : w - Real.sqrt (η * D * w) ≤ a * D) : w ≤ D * (η + 2 * a) := by
  have h1 : Real.sqrt (η * D * w) ≤ (η * D + w) / 2 := by
    rw [Real.sqrt_le_iff]
    constructor
    · positivity
    · nlinarith [sq_nonneg (η * D - w)]
  nlinarith

theorem zplus_alg_sharp (w D η a : ℝ) (hD : 0 < D) (hw : 0 ≤ w) (hη : 0 ≤ η) (ha : 0 ≤ a)
    (h : w - Real.sqrt (η * D * w) ≤ a * D) :
    w ≤ D * (Real.sqrt η + Real.sqrt (η + 4 * a)) ^ 2 / 4 := by
  set s := Real.sqrt w with hs
  have hs2 : s ^ 2 = w := Real.sq_sqrt hw
  have hs0 : 0 ≤ s := Real.sqrt_nonneg w
  set c := Real.sqrt (η * D) with hc
  have hc2 : c ^ 2 = η * D := Real.sq_sqrt (by positivity)
  have hc0 : 0 ≤ c := Real.sqrt_nonneg _
  have hmul : Real.sqrt (η * D * w) = c * s := by
    rw [Real.sqrt_mul (by positivity)]
  rw [hmul, ← hs2] at h
  set q := Real.sqrt (c ^ 2 + 4 * (a * D)) with hq
  have hq2 : q ^ 2 = c ^ 2 + 4 * (a * D) := Real.sq_sqrt (by positivity)
  have hq0 : 0 ≤ q := Real.sqrt_nonneg _
  have hmain : 2 * s ≤ c + q := by
    by_contra hcon
    push_neg at hcon
    nlinarith [hq2, hq0, hc0, hs0]
  -- w = s^2 <= ((c + q)/2)^2
  have hw2 : w ≤ ((c + q) / 2) ^ 2 := by
    rw [← hs2]
    nlinarith [hmain, hs0, hc0, hq0]
  -- rewrite c, q in terms of sqrt eta, sqrt (eta + 4a), sqrt D
  have hcq : c = Real.sqrt η * Real.sqrt D := by
    rw [hc, Real.sqrt_mul hη]
  have hqq : q = Real.sqrt (η + 4 * a) * Real.sqrt D := by
    have : c ^ 2 + 4 * (a * D) = (η + 4 * a) * D := by rw [hc2]; ring
    rw [hq, this, Real.sqrt_mul (by positivity)]
  have hD2 : Real.sqrt D ^ 2 = D := Real.sq_sqrt hD.le
  calc w ≤ ((c + q) / 2) ^ 2 := hw2
    _ = D * (Real.sqrt η + Real.sqrt (η + 4 * a)) ^ 2 / 4 := by
      rw [hcq, hqq]
      nlinarith [hD2]

#print axioms zplus_alg_cor
#print axioms zplus_alg_sharp
