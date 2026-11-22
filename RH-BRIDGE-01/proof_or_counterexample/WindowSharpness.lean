import Mathlib

/-!
# Window sharpness (counterexample sign part) and the exponent system of H4

H12-BRIDGE-DISCOVERY-01.  Two small statements, both elementary:

1. `window_sharpness_sign`: for `g u = exp (β u) * cos (γ u)` and every window length `L < π / γ`,
   there are arbitrarily large `U` with `g < 0` on all of `[U, U + L]`.  Together with
   `F s = (s - β) / ((s - β)^2 + γ^2)` (poles `β ± iγ`, closed form checked numerically, not formalized here)
   this shows that a one-sided bound on windows of bounded `log`-length does not exclude poles with real part `β > θ`.
   Only the sign part is formalized.

2. `exponent_system`: the linear system of H4 (`μ = 1/2`, `κ ≥ 5μ + ν`, `κ ≤ 2ν + 1/2`) forces `ν ≥ 2`, and `ν = 2` forces `κ = 9/2`.
-/

open Real

theorem window_sharpness_sign (β γ L U₀ : ℝ) (hγ : 0 < γ) (_hL : 0 < L) (hLπ : L < π / γ) :
    ∃ U : ℝ, U₀ ≤ U ∧ ∀ u ∈ Set.Icc U (U + L), Real.exp (β * u) * Real.cos (γ * u) < 0 := by
  have hγL : γ * L < π := by
    have := (lt_div_iff₀ hγ).1 hLπ
    linarith
  obtain ⟨k, hk⟩ := exists_nat_gt ((γ * U₀) / (2 * π))
  have hk' : γ * U₀ < 2 * π * k := by
    have h2 : 0 < 2 * π := by positivity
    have := (div_lt_iff₀ h2).1 hk
    linarith
  set X : ℝ := π / 2 + 2 * π * k + (π - γ * L) / 2 with hX
  have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
  have hXge : γ * U₀ < X := by
    have : 0 < π := Real.pi_pos
    have : 0 ≤ 2 * π * (k : ℝ) := by positivity
    rw [hX]
    nlinarith
  refine ⟨X / γ, ?_, ?_⟩
  · rw [le_div_iff₀ hγ]
    linarith
  · intro u hu
    obtain ⟨hu1, hu2⟩ := hu
    have hgu1 : X ≤ γ * u := by
      have := mul_le_mul_of_nonneg_left hu1 hγ.le
      rwa [mul_div_cancel₀ _ hγ.ne'] at this
    have hgu2 : γ * u ≤ X + γ * L := by
      have := mul_le_mul_of_nonneg_left hu2 hγ.le
      have e : γ * (X / γ + L) = X + γ * L := by
        field_simp
      linarith
    have hpi : 0 < π := Real.pi_pos
    have hlow : π / 2 < γ * u - k * (2 * π) := by
      rw [hX] at hgu1
      nlinarith
    have hup : γ * u - k * (2 * π) < π + π / 2 := by
      rw [hX] at hgu2
      nlinarith
    have hcos : Real.cos (γ * u) < 0 := by
      have e : Real.cos (γ * u - k * (2 * π)) = Real.cos (γ * u) := Real.cos_sub_nat_mul_two_pi (γ * u) k
      rw [← e]
      exact Real.cos_neg_of_pi_div_two_lt_of_lt hlow hup
    exact mul_neg_of_pos_of_neg (Real.exp_pos _) hcos

theorem exponent_system (μ ν κ : ℝ) (h1 : μ = 1 / 2) (h4 : 5 * μ + ν ≤ κ) (h3 : κ ≤ 2 * ν + 1 / 2) :
    2 ≤ ν ∧ (ν = 2 → κ = 9 / 2) := by
  subst h1
  constructor
  · linarith
  · intro hν
    subst hν
    linarith

#print axioms window_sharpness_sign
#print axioms exponent_system
