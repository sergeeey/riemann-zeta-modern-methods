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

/-- carry in base p forces p ∣ binom(2j,j) (Kummer). -/
theorem choose_dvd_of_carry (p : ℕ) [hp : Fact p.Prime] (j : ℕ) (h : p ≤ 2 * (j % p)) :
    p ∣ Nat.choose (2 * j) j := by
  have h2 : p ≤ j + j := by have := Nat.mod_le j p; omega
  have hlog : 0 < Nat.log p (j + j) := Nat.log_pos hp.out.one_lt h2
  have key := padicValNat_choose' (p := p) (n := j) (k := j) (b := Nat.log p (j + j) + 1)
    (Nat.lt_succ_self _)
  have hpos : 0 < padicValNat p (Nat.choose (j + j) j) := by
    rw [key]
    apply Finset.card_pos.mpr
    refine ⟨1, ?_⟩
    simp only [Finset.mem_filter, Finset.mem_Ico, pow_one]
    refine ⟨⟨le_refl _, by omega⟩, by omega⟩
  have : p ∣ Nat.choose (j + j) j := dvd_of_one_le_padicValNat hpos
  simpa [two_mul] using this

theorem divisor_mod_four (r j d : ℕ) (h : 4 * j + 1 = d * (4 * r + 3)) : d % 4 = 3 := by
  have : d * (4 * r + 3) = 4 * (d * r) + 3 * d := by ring
  omega

theorem quotient_upper_bound (r j d : ℕ) (hj : j ≤ (4 * r + 3) * (r + 1))
    (h : 4 * j + 1 = d * (4 * r + 3)) : d ≤ 4 * r + 3 + 1 := by
  by_contra hnot
  have hgt : (4 * r + 3) + 2 ≤ d := by omega
  have hmul_le : ((4 * r + 3) + 2) * (4 * r + 3) ≤ d * (4 * r + 3) := Nat.mul_le_mul_right _ hgt
  have hm : 4 * ((4 * r + 3) * (r + 1)) = (4 * r + 3) * ((4 * r + 3) + 1) := by ring
  have hleft : 4 * j + 1 ≤ 4 * ((4 * r + 3) * (r + 1)) + 1 := by omega
  nlinarith [hmul_le, hleft, hm]

theorem denominator_index_digit (r h j : ℕ) (hden : 4 * j + 1 = (4 * h + 3) * (4 * r + 3)) :
    j = h * (4 * r + 3) + (3 * r + 2) := by
  have hid : (4 * h + 3) * (4 * r + 3) = 4 * (h * (4 * r + 3) + (3 * r + 2)) + 1 := by ring
  omega

theorem padicNorm_nat_le_inv (p : ℕ) [hp : Fact p.Prime] (c : ℕ) (hc : p ∣ c) :
    padicNorm p (c : ℚ) ≤ (p : ℚ)⁻¹ := by
  have h := (padicNorm.dvd_iff_norm_le (p := p) (n := 1) (z := (c : ℤ))).mp (by rw [pow_one]; exact_mod_cast hc)
  simpa using h

/-- L1 (Step 2): every φ_j with j ≤ n₁, j ≠ q is p-integral. -/
theorem L1_phi_integral (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) (j : ℕ)
    (hj : j ≤ n1Idx p) (hjq : j ≠ qIdx p) : padicNorm p (phi j) ≤ 1 := by
  have hpp : p.Prime := Fact.out
  obtain ⟨r, hr⟩ : ∃ r, p = 4 * r + 3 := ⟨p / 4, by omega⟩
  have hq : qIdx p = 4 * r * r + 6 * r + 2 := by
    have h2 : p ^ 2 = 4 * (4 * r * r + 6 * r + 2) + 1 := by rw [hr]; ring
    unfold qIdx; omega
  have hn1 : n1Idx p = (4 * r + 3) * (r + 1) := by
    have h2 : p * (p + 1) = 4 * ((4 * r + 3) * (r + 1)) := by rw [hr]; ring
    unfold n1Idx; omega
  rw [hn1] at hj
  rw [hq] at hjq
  have hphi : phi j = ((Nat.choose (2 * j) j : ℕ) : ℚ) / (((4 ^ j * (4 * j + 1) : ℕ)) : ℚ) := by
    unfold phi; push_cast; rfl
  rw [hphi, padicNorm.div]
  have h4 : ¬ p ∣ 4 ^ j := by
    intro h
    have := hpp.dvd_of_dvd_pow h
    have h4' : p ∣ 2 ^ 2 := by norm_num; exact this
    have := hpp.dvd_of_dvd_pow h4'
    have := (Nat.prime_dvd_prime_iff_eq hpp Nat.prime_two).mp this
    omega
  have hn4 : padicNorm p ((4 ^ j : ℕ) : ℚ) = 1 := (padicNorm.nat_eq_one_iff _).mpr h4
  have hnc : padicNorm p ((Nat.choose (2 * j) j : ℕ) : ℚ) ≤ 1 := padicNorm.of_int _
  by_cases hd : p ∣ 4 * j + 1
  · obtain ⟨d, hd'⟩ := hd
    have hd2 : 4 * j + 1 = d * (4 * r + 3) := by rw [hd', hr]; ring
    have hm := divisor_mod_four r j d hd2
    have hb := quotient_upper_bound r j d hj hd2
    have hdlt : d < p := by
      rcases (by omega : d < 4 * r + 3 ∨ d = 4 * r + 3) with h | h
      · omega
      · exfalso
        apply hjq
        subst h
        nlinarith
    have hdpos : 0 < d := by
      rcases Nat.eq_zero_or_pos d with h | h
      · subst h; omega
      · exact h
    have hndvd : ¬ p ∣ d := Nat.not_dvd_of_pos_of_lt hdpos hdlt
    have hnd : padicNorm p ((4 * j + 1 : ℕ) : ℚ) = (p : ℚ)⁻¹ := by
      rw [hd', Nat.cast_mul, padicNorm.mul, (padicNorm.nat_eq_one_iff _).mpr hndvd,
        padicNorm.padicNorm_p_of_prime, mul_one]
    -- digit and carry
    have hmod : d % 4 = 3 := hm
    obtain ⟨h, hh⟩ : ∃ h, d = 4 * h + 3 := ⟨d / 4, by omega⟩
    have hjd := denominator_index_digit r h j (by rw [← hh]; exact hd2)
    have hjmod : j % p = 3 * r + 2 := by
      rw [hjd, hr, Nat.mul_comm h, Nat.mul_add_mod]
      exact Nat.mod_eq_of_lt (by omega)
    have hdiv : p ∣ Nat.choose (2 * j) j :=
      choose_dvd_of_carry p j (by rw [hjmod]; omega)
    have hc := padicNorm_nat_le_inv p _ hdiv
    rw [Nat.cast_mul, padicNorm.mul, hn4, one_mul, hnd]
    have hppos : (0 : ℚ) < (p : ℚ)⁻¹ := by
      have : (0 : ℚ) < p := by exact_mod_cast hpp.pos
      positivity
    rw [div_le_one hppos]
    exact hc
  · have hn : padicNorm p ((4 * j + 1 : ℕ) : ℚ) = 1 := (padicNorm.nat_eq_one_iff _).mpr hd
    rw [Nat.cast_mul, padicNorm.mul, hn4, hn]
    simpa using hnc

end

end H12.B4

#print axioms H12.B4.L1_phi_integral
