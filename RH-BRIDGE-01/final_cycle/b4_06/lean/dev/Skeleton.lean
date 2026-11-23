import Mathlib

/-!
# H12-B4-06 universal congruence: SKELETON (statements only; `sorry` marks work in progress)

NOT a result. This file fixes the exact statements of the lemmas that, assembled, give
  p * a_{n1} ≡ -a_{n0}   (mod p)   for every prime p ≡ 3 (mod 4),
where a_n is the Lagrange-inversion coefficient formula (1) of H12-PADIC-B4-06-PROOF.md.
Connection of `lagA` to the Weierstrass ℘ coefficients (ODE recurrence) is NOT formalized here.
-/

open PowerSeries

namespace H12.B4

noncomputable section

/-- φ_j = binom(2j, j) / (4^j (4j+1)). -/
def phi (j : ℕ) : ℚ := (Nat.choose (2 * j) j : ℚ) / ((4 : ℚ) ^ j * (4 * (j : ℚ) + 1))

/-- p-adic integrality and congruence mod p in ℚ (all quantities p-integral, difference of norm < 1). -/
def PCong (p : ℕ) (x y : ℚ) : Prop :=
  padicNorm p x ≤ 1 ∧ padicNorm p y ≤ 1 ∧ padicNorm p (x - y) < 1

/-- q = (p²-1)/4, n₀ = (p+1)/4, n₁ = p(p+1)/4. -/
def qIdx (p : ℕ) : ℕ := (p ^ 2 - 1) / 4
def n0Idx (p : ℕ) : ℕ := (p + 1) / 4
def n1Idx (p : ℕ) : ℕ := p * (p + 1) / 4

/-- The power series Φ(u) = Σ φ_j u^j over ℚ. -/
def PhiSeries : ℚ⟦X⟧ := PowerSeries.mk phi

/-- Lagrange coefficient formula (1): a_n = -(1/(2n-1)) [u^n] Φ^{-(4n-2)}. -/
def lagA (n : ℕ) : ℚ :=
  -(1 / (2 * (n : ℚ) - 1)) * PowerSeries.coeff n ((PhiSeries⁻¹) ^ (4 * n - 2))

/-- L1 (Step 2): every φ_j with j ≤ n₁, j ≠ q is p-integral. -/
theorem L1_phi_integral (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) (j : ℕ)
    (hj : j ≤ n1Idx p) (hjq : j ≠ qIdx p) : padicNorm p (phi j) ≤ 1 := by
  sorry

/-- L2 (Step 3): p·φ_q is a p-adic unit congruent to -1 mod p. -/
theorem L2_pphi_q (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    padicNorm p ((p : ℚ) * phi (qIdx p)) = 1 ∧ PCong p ((p : ℚ) * phi (qIdx p)) (-1) := by
  sorry

/-- L3a (first-order perturbation of an inverse power, truncated below X^(2q)). -/
theorem L3a_inv_pow_perturb {K : Type*} [Field K] (F : K⟦X⟧) (hF : constantCoeff F = 1)
    (e : K) (q N M : ℕ) (hqN : q ≤ N) (hN : N < 2 * q) :
    coeff N (((F + PowerSeries.C e * X ^ q)⁻¹) ^ M)
      = coeff N ((F⁻¹) ^ M) - (M : K) * e * coeff (N - q) ((F⁻¹) ^ (M + 1)) := by
  sorry

/-- L3b (nilpotent Frobenius in characteristic p, below X^p). -/
theorem L3b_frobenius_trunc (p : ℕ) [Fact p.Prime] (G : (ZMod p)⟦X⟧) (hG : constantCoeff G = 1)
    (n : ℕ) (hn : n < p) :
    coeff n ((G⁻¹) ^ (p * (p + 1) - 1)) = coeff n G ∧ coeff n ((G⁻¹) ^ (p - 1)) = coeff n G := by
  sorry

/-- L3d (coefficients of inverse powers up to degree N only depend on coefficients up to N). -/
theorem L3d_trunc_invariance {K : Type*} [Field K] (F G : K⟦X⟧) (hF : constantCoeff F = 1)
    (N M n : ℕ) (hn : n ≤ N) (h : ∀ j, j ≤ N → coeff j F = coeff j G) :
    coeff n ((F⁻¹) ^ M) = coeff n ((G⁻¹) ^ M) := by
  sorry

/-- L3c (reduction mod p of inverse powers of a p-integral series with constant term 1):
all coefficients stay p-integral and reduce to the corresponding coefficients over `ZMod p`. -/
theorem L3c_reduction (p : ℕ) [Fact p.Prime] (F : ℚ⟦X⟧) (h0 : constantCoeff F = 1)
    (hint : ∀ n, padicNorm p (coeff n F) ≤ 1) :
    ∃ G : (ZMod p)⟦X⟧, constantCoeff G = 1 ∧
      (∀ n, ∃ z : ℤ_[p], (z : ℚ_[p]) = ((coeff n F : ℚ) : ℚ_[p]) ∧ PadicInt.toZMod z = coeff n G) ∧
      ∀ M n, padicNorm p (coeff n ((F⁻¹) ^ M)) ≤ 1 ∧
        ∃ z : ℤ_[p], (z : ℚ_[p]) = ((coeff n ((F⁻¹) ^ M) : ℚ) : ℚ_[p]) ∧
          PadicInt.toZMod z = coeff n ((G⁻¹) ^ M) := by
  sorry

/-- L5: φ_{n₀} is a p-adic unit. -/
theorem L5_phi_n0_unit (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    padicNorm p (phi (n0Idx p)) = 1 := by
  sorry

/-- FINAL: first-resonance congruence for the Lagrange coefficients, every prime p ≡ 3 mod 4. -/
theorem B4_06_first_resonance (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    PCong p ((p : ℚ) * lagA (n1Idx p)) (-(lagA (n0Idx p))) ∧ padicNorm p (lagA (n0Idx p)) = 1 := by
  sorry

end

end H12.B4
