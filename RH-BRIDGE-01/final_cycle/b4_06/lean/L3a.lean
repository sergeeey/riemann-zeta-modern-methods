import Mathlib

open PowerSeries

namespace H12.B4

noncomputable section

lemma coeff_eq_of_dvd {K : Type*} [Field K] {A B : K⟦X⟧} {k n : ℕ}
    (h : (X : K⟦X⟧) ^ k ∣ A - B) (hn : n < k) : coeff n A = coeff n B := by
  have := (PowerSeries.X_pow_dvd_iff.mp h) n hn
  rw [map_sub] at this
  exact sub_eq_zero.mp this

lemma dvd_of_coeff_eq {K : Type*} [Field K] {A B : K⟦X⟧} {k : ℕ}
    (h : ∀ j, j < k → coeff j A = coeff j B) : (X : K⟦X⟧) ^ k ∣ A - B := by
  refine PowerSeries.X_pow_dvd_iff.mpr (fun m hm => ?_)
  rw [map_sub]
  exact sub_eq_zero.mpr (h m hm)

lemma pow_dvd_sub {K : Type*} [Field K] {A B : K⟦X⟧} {k : ℕ}
    (h : (X : K⟦X⟧) ^ k ∣ A - B) (M : ℕ) : (X : K⟦X⟧) ^ k ∣ A ^ M - B ^ M :=
  dvd_trans h (sub_dvd_pow_sub_pow A B M)

lemma inv_ne {K : Type*} [Field K] (F : K⟦X⟧) (hF : constantCoeff F = 1) :
    F * F⁻¹ = 1 :=
  PowerSeries.mul_inv_cancel F (by rw [hF]; exact one_ne_zero)

/-- L3a (first-order perturbation of an inverse power, truncated below X^(2q)). -/
theorem L3a_inv_pow_perturb {K : Type*} [Field K] (F : K⟦X⟧) (hF : constantCoeff F = 1)
    (e : K) (q N M : ℕ) (hqN : q ≤ N) (hN : N < 2 * q) :
    coeff N (((F + PowerSeries.C e * X ^ q)⁻¹) ^ M)
      = coeff N ((F⁻¹) ^ M) - (M : K) * e * coeff (N - q) ((F⁻¹) ^ (M + 1)) := by
  set G : K⟦X⟧ := F⁻¹ with hGdef
  set E : K⟦X⟧ := PowerSeries.C e * X ^ q with hE
  have hFG : F * G = 1 := inv_ne F hF
  have hF' : constantCoeff (F + E) = 1 := by
    rcases Nat.eq_zero_or_pos q with hq | hq
    · omega
    · simp [hE, hF, map_pow, zero_pow hq.ne']
  have hFG' : (F + E) * (F + E)⁻¹ = 1 := inv_ne (F + E) hF'
  have hE2 : (X : K⟦X⟧) ^ (2 * q) ∣ E ^ 2 := by
    refine ⟨PowerSeries.C (e ^ 2), ?_⟩
    rw [hE]
    have : (X : K⟦X⟧) ^ (2 * q) = (X ^ q) ^ 2 := by rw [← pow_mul, mul_comm]
    rw [this, mul_pow, map_pow]; ring
  -- Q = G - E G^2
  set Q : K⟦X⟧ := G - E * G ^ 2 with hQ
  have hQF : Q * (F + E) = 1 - E ^ 2 * G ^ 2 := by
    rw [hQ]; linear_combination (1 - E * G) * hFG
  have h1 : (X : K⟦X⟧) ^ (2 * q) ∣ (F + E)⁻¹ - Q := by
    have : (F + E)⁻¹ - Q = (F + E)⁻¹ * (E ^ 2 * G ^ 2) := by
      linear_combination Q * hFG' - (F + E)⁻¹ * hQF
    rw [this]
    exact dvd_mul_of_dvd_right (dvd_mul_of_dvd_left hE2 _) _
  have h2 : ∀ M : ℕ, (X : K⟦X⟧) ^ (2 * q) ∣
      Q ^ M - (G ^ M - (M : K⟦X⟧) * E * G ^ (M + 1)) := by
    intro M
    induction M with
    | zero => simp
    | succ M ih =>
      have eq : Q ^ (M + 1) - (G ^ (M + 1) - ((M + 1 : ℕ) : K⟦X⟧) * E * G ^ (M + 1 + 1))
          = (Q ^ M - (G ^ M - (M : K⟦X⟧) * E * G ^ (M + 1))) * Q
            + (M : K⟦X⟧) * G ^ (M + 3) * E ^ 2 := by
        rw [hQ]; push_cast; ring
      rw [eq]
      exact dvd_add (dvd_mul_of_dvd_left ih _) (dvd_mul_of_dvd_right hE2 _)
  have h3 : (X : K⟦X⟧) ^ (2 * q) ∣
      (F + E)⁻¹ ^ M - (G ^ M - (M : K⟦X⟧) * E * G ^ (M + 1)) := by
    have e3 : (F + E)⁻¹ ^ M - (G ^ M - (M : K⟦X⟧) * E * G ^ (M + 1))
        = ((F + E)⁻¹ ^ M - Q ^ M) + (Q ^ M - (G ^ M - (M : K⟦X⟧) * E * G ^ (M + 1))) := by ring
    rw [e3]
    exact dvd_add (pow_dvd_sub h1 M) (h2 M)
  rw [coeff_eq_of_dvd h3 hN]
  have e4 : (M : K⟦X⟧) * E * G ^ (M + 1) = PowerSeries.C ((M : K) * e) * (X ^ q * G ^ (M + 1)) := by
    rw [hE, map_mul, map_natCast]; ring
  rw [e4, map_sub, coeff_C_mul, coeff_X_pow_mul', if_pos hqN]

/-- L3d (coefficients of inverse powers up to degree N only depend on coefficients up to N). -/
theorem L3d_trunc_invariance {K : Type*} [Field K] (F G : K⟦X⟧) (hF : constantCoeff F = 1)
    (N M n : ℕ) (hn : n ≤ N) (h : ∀ j, j ≤ N → coeff j F = coeff j G) :
    coeff n ((F⁻¹) ^ M) = coeff n ((G⁻¹) ^ M) := by
  have hG : constantCoeff G = 1 := by
    have h0 := h 0 (Nat.zero_le _)
    rw [coeff_zero_eq_constantCoeff_apply, coeff_zero_eq_constantCoeff_apply, hF] at h0
    exact h0.symm
  have hFi : F * F⁻¹ = 1 := inv_ne F hF
  have hGi : G * G⁻¹ = 1 := inv_ne G hG
  have hd : (X : K⟦X⟧) ^ (N + 1) ∣ G - F :=
    dvd_of_coeff_eq (fun j hj => (h j (by omega)).symm)
  have key : F⁻¹ - G⁻¹ = F⁻¹ * G⁻¹ * (G - F) := by
    linear_combination G⁻¹ * hFi - F⁻¹ * hGi
  have h1 : (X : K⟦X⟧) ^ (N + 1) ∣ F⁻¹ - G⁻¹ := by
    rw [key]; exact dvd_mul_of_dvd_right hd _
  exact coeff_eq_of_dvd (pow_dvd_sub h1 M) (by omega)

end

end H12.B4

#print axioms H12.B4.L3a_inv_pow_perturb
#print axioms H12.B4.L3d_trunc_invariance
