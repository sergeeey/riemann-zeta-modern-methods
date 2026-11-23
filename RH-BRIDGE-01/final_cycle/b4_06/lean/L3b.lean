import Mathlib

open PowerSeries

namespace H12.B4

noncomputable section

instance charP_ps (p : ℕ) [Fact p.Prime] : CharP (ZMod p)⟦X⟧ p :=
  charP_of_injective_ringHom (f := (PowerSeries.C : ZMod p →+* (ZMod p)⟦X⟧)) (PowerSeries.C_injective) p

private lemma inv_unique_aux {R : Type*} [CommRing R] (P A B : R) (hA : P * A = 1) (hB : P * B = 1) :
    A = B := by
  calc A = A * (P * B) := by rw [hB, mul_one]
    _ = (P * A) * B := by ring
    _ = B := by rw [hA, one_mul]

private lemma inv_pow_sub_one_dvd (p : ℕ) [Fact p.Prime] (G : (ZMod p)⟦X⟧)
    (hG : constantCoeff G = 1) :
    (X : (ZMod p)⟦X⟧) ^ p ∣ (G⁻¹) ^ p - 1 := by
  have hne : constantCoeff G ≠ 0 := by rw [hG]; exact one_ne_zero
  have hGI : G * G⁻¹ = 1 := PowerSeries.mul_inv_cancel G hne
  have hX : (X : (ZMod p)⟦X⟧) ∣ G - 1 := by
    rw [PowerSeries.X_dvd_iff]; simp [hG]
  obtain ⟨H, hH⟩ := hX
  have hGe : G = 1 + X * H := by rw [← hH]; ring
  have hGp : G ^ p = 1 + (X * H) ^ p := by
    rw [hGe, add_pow_char]; simp
  have hprod : G ^ p * (G⁻¹) ^ p = 1 := by rw [← mul_pow, hGI, one_pow]
  refine ⟨-((G⁻¹) ^ p * H ^ p), ?_⟩
  have : (G⁻¹) ^ p - 1 = (G⁻¹) ^ p * (1 - G ^ p) := by
    have : (G⁻¹) ^ p * G ^ p = 1 := by rw [mul_comm]; exact hprod
    linear_combination this
  rw [this, hGp, mul_pow]
  ring

private lemma coeff_lt_of_dvd (p : ℕ) {A B : (ZMod p)⟦X⟧} (h : (X : (ZMod p)⟦X⟧) ^ p ∣ A - B)
    (n : ℕ) (hn : n < p) : coeff n A = coeff n B := by
  obtain ⟨C, hC⟩ := h
  have : A = B + X ^ p * C := by rw [← hC]; ring
  rw [this, map_add, PowerSeries.coeff_X_pow_mul']
  simp [Nat.not_le.mpr hn]

private lemma trunc_aux (p : ℕ) [Fact p.Prime] (G : (ZMod p)⟦X⟧) (hG : constantCoeff G = 1)
    (m : ℕ) (hm : 0 < m) (hd : (X : (ZMod p)⟦X⟧) ^ p ∣ (G⁻¹) ^ m - 1) (n : ℕ) (hn : n < p) :
    coeff n ((G⁻¹) ^ (m - 1)) = coeff n G := by
  have hne : constantCoeff G ≠ 0 := by rw [hG]; exact one_ne_zero
  have hGI : G * G⁻¹ = 1 := PowerSeries.mul_inv_cancel G hne
  have e : (G⁻¹) ^ (m - 1) = G * (G⁻¹) ^ m := by
    obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
    simp only [Nat.add_sub_cancel, pow_succ]
    calc (G⁻¹) ^ k = (G⁻¹) ^ k * (G * G⁻¹) := by rw [hGI, mul_one]
      _ = _ := by ring
  rw [e]
  apply coeff_lt_of_dvd p _ n hn
  have : G * (G⁻¹) ^ m - G = G * ((G⁻¹) ^ m - 1) := by ring
  rw [this]
  exact Dvd.dvd.mul_left hd G

theorem L3b_frobenius_trunc (p : ℕ) [Fact p.Prime] (G : (ZMod p)⟦X⟧) (hG : constantCoeff G = 1)
    (n : ℕ) (hn : n < p) :
    coeff n ((G⁻¹) ^ (p * (p + 1) - 1)) = coeff n G ∧ coeff n ((G⁻¹) ^ (p - 1)) = coeff n G := by
  have hp := (Fact.out : p.Prime).pos
  have h1 := inv_pow_sub_one_dvd p G hG
  constructor
  · apply trunc_aux p G hG _ (by positivity) _ n hn
    rw [pow_mul]
    exact h1.trans (by simpa using sub_dvd_pow_sub_pow ((G⁻¹) ^ p) 1 (p + 1))
  · exact trunc_aux p G hG p hp h1 n hn

theorem L3c_reduction (p : ℕ) [Fact p.Prime] (F : ℚ⟦X⟧) (h0 : constantCoeff F = 1)
    (hint : ∀ n, padicNorm p (coeff n F) ≤ 1) :
    ∃ G : (ZMod p)⟦X⟧, constantCoeff G = 1 ∧
      (∀ n, ∃ z : ℤ_[p], (z : ℚ_[p]) = ((coeff n F : ℚ) : ℚ_[p]) ∧ PadicInt.toZMod z = coeff n G) ∧
      ∀ M n, padicNorm p (coeff n ((F⁻¹) ^ M)) ≤ 1 ∧
        ∃ z : ℤ_[p], (z : ℚ_[p]) = ((coeff n ((F⁻¹) ^ M) : ℚ) : ℚ_[p]) ∧
          PadicInt.toZMod z = coeff n ((G⁻¹) ^ M) := by
  have hnorm : ∀ n, ‖((coeff n F : ℚ) : ℚ_[p])‖ ≤ 1 := by
    intro n; rw [Padic.eq_padicNorm]; exact_mod_cast hint n
  have hex : ∀ n, ∃ z : ℤ_[p], (z : ℚ_[p]) = ((coeff n F : ℚ) : ℚ_[p]) :=
    fun n => ⟨⟨_, hnorm n⟩, rfl⟩
  choose zf hzf using hex
  let Fz : ℤ_[p]⟦X⟧ := PowerSeries.mk zf
  let ι : ℚ →+* ℚ_[p] := Rat.castHom ℚ_[p]
  let ιz : ℤ_[p] →+* ℚ_[p] := PadicInt.Coe.ringHom
  have hinj : Function.Injective ιz := fun a b h => Subtype.ext h
  have hcoef : ∀ n, ((coeff n Fz : ℤ_[p]) : ℚ_[p]) = ((coeff n F : ℚ) : ℚ_[p]) := by
    intro n
    simp only [Fz, coeff_mk]
    exact hzf n
  have hmap : map ιz Fz = map ι F := by
    ext n
    simp only [coeff_map]
    exact hcoef n
  have hFz0 : constantCoeff Fz = 1 := by
    apply hinj
    have h := congrArg (coeff 0) hmap
    simp only [coeff_map, coeff_zero_eq_constantCoeff_apply] at h
    rw [h, h0]; simp
  let Hz : ℤ_[p]⟦X⟧ := PowerSeries.invOfUnit Fz 1
  have hFH : Fz * Hz = 1 := PowerSeries.mul_invOfUnit Fz 1 (by simpa using hFz0)
  have hB : map ιz Hz = map ι (F⁻¹) := by
    apply inv_unique_aux (map ι F)
    · rw [← hmap, ← map_mul, hFH]; simp
    · rw [← map_mul, PowerSeries.mul_inv_cancel F (by rw [h0]; exact one_ne_zero)]
      simp
  let G : (ZMod p)⟦X⟧ := map (PadicInt.toZMod : ℤ_[p] →+* ZMod p) Fz
  have hG0 : constantCoeff G = 1 := by
    have h : coeff 0 G = PadicInt.toZMod (coeff 0 Fz) := coeff_map _ _ _
    simp only [coeff_zero_eq_constantCoeff_apply] at h
    rw [h, hFz0]; simp
  have hGH : map (PadicInt.toZMod : ℤ_[p] →+* ZMod p) Hz = G⁻¹ := by
    apply inv_unique_aux G
    · rw [← map_mul, hFH]; simp
    · exact PowerSeries.mul_inv_cancel G (by rw [hG0]; exact one_ne_zero)
  refine ⟨G, hG0, fun n => ⟨coeff n Fz, ?_, ?_⟩, fun M n => ?_⟩
  · exact hcoef n
  · simp only [G, coeff_map]
  · have hc : (((coeff n ((F⁻¹) ^ M) : ℚ)) : ℚ_[p]) = ιz (coeff n (Hz ^ M)) := by
      have hh : map ιz (Hz ^ M) = map ι ((F⁻¹) ^ M) := by
        rw [map_pow (map ιz) Hz M, map_pow (map ι) (F⁻¹) M, hB]
      have : coeff n (map ιz (Hz ^ M)) = coeff n (map ι ((F⁻¹) ^ M)) := by rw [hh]
      rw [coeff_map, coeff_map] at this
      exact this.symm
    refine ⟨?_, coeff n (Hz ^ M), hc.symm, ?_⟩
    · have h1 : ((padicNorm p (coeff n ((F⁻¹) ^ M)) : ℚ) : ℝ) = ‖((coeff n (Hz ^ M) : ℤ_[p]) : ℚ_[p])‖ := by
        rw [← Padic.eq_padicNorm, hc]; rfl
      have h2 : ‖((coeff n (Hz ^ M) : ℤ_[p]) : ℚ_[p])‖ ≤ 1 := PadicInt.norm_le_one _
      exact_mod_cast (h1 ▸ h2)
    · rw [← hGH, ← map_pow, coeff_map]

end

end H12.B4

#print axioms H12.B4.L3b_frobenius_trunc
#print axioms H12.B4.L3c_reduction
