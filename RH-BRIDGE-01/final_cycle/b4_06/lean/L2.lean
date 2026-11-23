import Mathlib

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

section Aux

variable (p : ℕ) [hp : Fact p.Prime]

/-- (A p + B)! = (A p)! * w with w ≡ B! (mod p). -/
lemma blk1 (A B : ℕ) : ∃ w : ℤ, ((A * p + B).factorial : ℤ) = ((A * p).factorial : ℤ) * w ∧
    (w : ZMod p) = (B.factorial : ZMod p) := by
  induction B with
  | zero => exact ⟨1, by simp, by simp⟩
  | succ B ih =>
    obtain ⟨w, h1, h2⟩ := ih
    refine ⟨((A * p + B + 1 : ℕ) : ℤ) * w, ?_, ?_⟩
    · rw [show A * p + (B + 1) = (A * p + B) + 1 by ring, Nat.factorial_succ, Nat.cast_mul, h1]
      ring
    · rw [Int.cast_mul, Int.cast_natCast, h2, Nat.factorial_succ B]
      push_cast
      simp [ZMod.natCast_self]

/-- ((A p)! = p^A * A! * u, u ≡ (-1)^A (mod p). -/
lemma blk2 (A : ℕ) : ∃ u : ℤ, ((A * p).factorial : ℤ) = (p : ℤ) ^ A * (A.factorial : ℤ) * u ∧
    (u : ZMod p) = (-1) ^ A := by
  induction A with
  | zero => exact ⟨1, by simp, by simp⟩
  | succ A ih =>
    obtain ⟨u, h1, h2⟩ := ih
    obtain ⟨w, h3, h4⟩ := blk1 p A (p - 1)
    have hp1 : 1 ≤ p := hp.out.one_lt.le
    have e : (A + 1) * p = (A * p + (p - 1)) + 1 := by
      zify [hp1]; ring
    have e' : ((A * p + (p - 1) + 1 : ℕ) : ℤ) = ((A : ℤ) + 1) * p := by
      rw [← e]; push_cast; ring
    refine ⟨u * w, ?_, ?_⟩
    · rw [e, Nat.factorial_succ, Nat.cast_mul, h3, h1, Nat.factorial_succ A, e']
      push_cast
      ring
    · rw [Int.cast_mul, h2, h4, ZMod.wilsons_lemma]
      ring

lemma blk3 (A B : ℕ) : ∃ u : ℤ, ((A * p + B).factorial : ℤ) = (p : ℤ) ^ A * (A.factorial : ℤ) * u ∧
    (u : ZMod p) = (-1) ^ A * (B.factorial : ZMod p) := by
  obtain ⟨u, h1, h2⟩ := blk2 p A
  obtain ⟨w, h3, h4⟩ := blk1 p A B
  refine ⟨u * w, ?_, ?_⟩
  · rw [h3, h1]; ring
  · rw [Int.cast_mul, h2, h4]

/-- Wilson reflection: k! (p-1-k)! = (-1)^(k+1) in ZMod p. -/
lemma refl_fact (k : ℕ) (hk : k ≤ p - 1) :
    (k.factorial : ZMod p) * ((p - 1 - k).factorial : ZMod p) = (-1) ^ (k + 1) := by
  induction k with
  | zero => simp [ZMod.wilsons_lemma]
  | succ k ih =>
    have ih' := ih (by omega)
    have hp2 : p - 1 - k = (p - 1 - (k + 1)) + 1 := by omega
    rw [hp2, Nat.factorial_succ] at ih'
    push_cast at ih'
    have hc0 : (((p - 1 - (k + 1) + 1) + (k + 1) : ℕ) : ZMod p) = 0 := by
      rw [show (p - 1 - (k + 1) + 1) + (k + 1) = p by omega]
      exact ZMod.natCast_self p
    push_cast at hc0
    have hc : ((p - 1 - (k + 1) : ℕ) : ZMod p) + 1 = -((k : ZMod p) + 1) := by
      linear_combination hc0
    rw [hc] at ih'
    rw [Nat.factorial_succ k]
    push_cast
    linear_combination (-1 : ZMod p) * ih'

lemma not_dvd_four (hp3 : p % 4 = 3) : ¬ p ∣ 4 := by
  intro h
  have h1 := Nat.le_of_dvd (by norm_num) h
  have h2 : p = 3 := by omega
  rw [h2] at h
  exact absurd h (by decide)

lemma qIdx_facts (hp3 : p % 4 = 3) :
    ∃ r : ℕ, p = 4 * r + 3 ∧ qIdx p = r * p + (3 * r + 2) ∧ p ^ 2 = 4 * qIdx p + 1 ∧
      qIdx p = (p - 1) * (r + 1) := by
  obtain ⟨r, hr⟩ : ∃ r, p = 4 * r + 3 := ⟨p / 4, by omega⟩
  have h : p ^ 2 = 4 * (r * p + (3 * r + 2)) + 1 := by rw [hr]; ring
  have hq : qIdx p = r * p + (3 * r + 2) := by
    unfold qIdx; rw [h]; omega
  have hp1 : p - 1 = 4 * r + 2 := by omega
  refine ⟨r, hr, hq, by rw [hq]; exact h, ?_⟩
  rw [hq, hp1]
  have : r * p = r * (4 * r + 3) := by rw [← hr]
  rw [this]; ring

lemma key_choose (hp3 : p % 4 = 3) :
    ∃ c : ℕ, Nat.choose (2 * qIdx p) (qIdx p) = p * c ∧ (c : ZMod p) = -1 := by
  obtain ⟨r, hr, hq, -, -⟩ := qIdx_facts p hp3
  have hlt1 : r < p := by omega
  have hlt2 : 3 * r + 2 < p := by omega
  have hlt3 : 2 * r + 1 < p := by omega
  rw [hq]
  have e2 : 2 * (r * p + (3 * r + 2)) = (2 * r + 1) * p + (2 * r + 1) := by rw [hr]; ring
  obtain ⟨u1, h1, h1'⟩ := blk3 p (2 * r + 1) (2 * r + 1)
  obtain ⟨u2, h2, h2'⟩ := blk3 p r (3 * r + 2)
  have hC := Nat.choose_mul_factorial_mul_factorial
    (show r * p + (3 * r + 2) ≤ 2 * (r * p + (3 * r + 2)) by omega)
  rw [show 2 * (r * p + (3 * r + 2)) - (r * p + (3 * r + 2)) = r * p + (3 * r + 2) by omega] at hC
  have hZ : ((Nat.choose (2 * (r * p + (3 * r + 2))) (r * p + (3 * r + 2)) : ℕ) : ℤ) *
      ((r * p + (3 * r + 2)).factorial : ℤ) * ((r * p + (3 * r + 2)).factorial : ℤ)
      = ((2 * (r * p + (3 * r + 2))).factorial : ℤ) := by exact_mod_cast hC
  have hfac : ((2 * (r * p + (3 * r + 2))).factorial : ℤ)
      = (p : ℤ) ^ (2 * r + 1) * ((2 * r + 1).factorial : ℤ) * u1 := by rw [e2]; exact h1
  rw [hfac, h2] at hZ
  set C := Nat.choose (2 * (r * p + (3 * r + 2))) (r * p + (3 * r + 2)) with hCdef
  have hpz : (p : ℤ) ≠ 0 := by exact_mod_cast hp.out.ne_zero
  have hmain : (C : ℤ) * (((r.factorial : ℤ)) * u2) ^ 2 = p * (((2 * r + 1).factorial : ℤ) * u1) := by
    have hp2r : (p : ℤ) ^ (2 * r) ≠ 0 := pow_ne_zero _ hpz
    apply mul_left_cancel₀ hp2r
    linear_combination hZ
  -- nonvanishing in ZMod p
  have hr0 : (r.factorial : ZMod p) ≠ 0 := by
    rw [Ne, ZMod.natCast_eq_zero_iff, Nat.Prime.dvd_factorial hp.out]; omega
  have hs0 : ((3 * r + 2).factorial : ZMod p) ≠ 0 := by
    rw [Ne, ZMod.natCast_eq_zero_iff, Nat.Prime.dvd_factorial hp.out]; omega
  have hu2 : (u2 : ZMod p) ≠ 0 := by
    rw [h2']
    exact mul_ne_zero (pow_ne_zero _ (neg_ne_zero.mpr one_ne_zero)) hs0
  have hmainZ := congrArg (Int.cast : ℤ → ZMod p) hmain
  push_cast at hmainZ
  rw [ZMod.natCast_self, zero_mul] at hmainZ
  have hCz : (C : ZMod p) = 0 := by
    have := (mul_eq_zero.mp hmainZ)
    rcases this with h | h
    · exact h
    · exact absurd (pow_eq_zero_iff (two_ne_zero)|>.mp h) (mul_ne_zero hr0 hu2)
  obtain ⟨c, hc⟩ := (ZMod.natCast_eq_zero_iff _ _).mp hCz
  have hmain2 : (c : ℤ) * (((r.factorial : ℤ)) * u2) ^ 2 = ((2 * r + 1).factorial : ℤ) * u1 := by
    apply mul_left_cancel₀ hpz
    rw [hc] at hmain
    push_cast at hmain
    linear_combination hmain
  have hmain2Z := congrArg (Int.cast : ℤ → ZMod p) hmain2
  push_cast at hmain2Z
  rw [h1', h2'] at hmain2Z
  refine ⟨c, hc, ?_⟩
  -- Wilson facts
  have hrs := refl_fact p r (by omega)
  rw [show p - 1 - r = 3 * r + 2 by omega] at hrs
  have htt := refl_fact p (2 * r + 1) (by omega)
  rw [show p - 1 - (2 * r + 1) = 2 * r + 1 by omega] at htt
  have hneg : ((-1 : ZMod p)) ^ (2 * r + 1) = -1 := by
    rw [pow_succ, pow_mul]; simp
  have hneg2 : ((-1 : ZMod p)) ^ (2 * r + 1 + 1) = 1 := by
    rw [pow_succ, hneg]; simp
  have hm : (((-1 : ZMod p)) ^ r) ^ 2 = 1 := by
    rw [← pow_mul, mul_comm, pow_mul]; simp
  have hrs2 : ((r.factorial : ZMod p) * ((3 * r + 2).factorial : ZMod p)) ^ 2 = 1 := by
    rw [hrs, ← pow_mul, mul_comm, pow_mul]; simp
  have E1 : (c : ZMod p) * (((r.factorial : ZMod p) * ((3 * r + 2).factorial : ZMod p)) ^ 2
      * (((-1 : ZMod p)) ^ r) ^ 2) = -(((2 * r + 1).factorial : ZMod p) * ((2 * r + 1).factorial : ZMod p)) := by
    rw [hneg] at hmain2Z
    linear_combination hmain2Z
  rw [hrs2, hm, htt, hneg2] at E1
  linear_combination E1

end Aux

/-- L2 (Step 3): p·φ_q is a p-adic unit congruent to -1 mod p. -/
theorem L2_pphi_q (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    padicNorm p ((p : ℚ) * phi (qIdx p)) = 1 ∧ PCong p ((p : ℚ) * phi (qIdx p)) (-1) := by
  obtain ⟨r, hr, hq, h4, hq2⟩ := qIdx_facts p hp
  obtain ⟨c, hc, hcz⟩ := key_choose p hp
  have hpq : (p : ℚ) ≠ 0 := by exact_mod_cast (Fact.out : p.Prime).ne_zero
  have h4q : (4 * (qIdx p : ℚ) + 1) = (p : ℚ) ^ 2 := by exact_mod_cast h4.symm
  have hx : (p : ℚ) * phi (qIdx p) = (c : ℚ) / (4 : ℚ) ^ (qIdx p) := by
    unfold phi
    rw [h4q, hc]
    push_cast
    field_simp
  have hne4 : (4 : ZMod p) ≠ 0 := by
    intro h
    have h' : ((4 : ℕ) : ZMod p) = 0 := by exact_mod_cast h
    rw [ZMod.natCast_eq_zero_iff] at h'
    exact not_dvd_four p hp h'
  have hpow : (4 : ZMod p) ^ (qIdx p) = 1 := by
    rw [hq2, pow_mul, ZMod.pow_card_sub_one_eq_one hne4, one_pow]
  have h4nat : ((4 ^ qIdx p : ℕ) : ZMod p) = 1 := by push_cast; exact hpow
  have hcnd : ¬ p ∣ c := by
    intro h
    have h' := (ZMod.natCast_eq_zero_iff c p).mpr h
    rw [hcz] at h'
    exact one_ne_zero (neg_eq_zero.mp h')
  have h4nd : ¬ p ∣ 4 ^ qIdx p := by
    intro h
    have h' := (ZMod.natCast_eq_zero_iff _ p).mpr h
    rw [h4nat] at h'
    exact one_ne_zero h'
  have hn4 : padicNorm p ((4 : ℚ) ^ qIdx p) = 1 := by
    have := (padicNorm.nat_eq_one_iff (p := p) (4 ^ qIdx p)).mpr h4nd
    exact_mod_cast this
  have hnc : padicNorm p (c : ℚ) = 1 := (padicNorm.nat_eq_one_iff c).mpr hcnd
  have hn : padicNorm p ((c : ℚ) / (4 : ℚ) ^ qIdx p) = 1 := by
    rw [padicNorm.div, hnc, hn4]; simp
  rw [hx]
  refine ⟨hn, hn.le, by simp, ?_⟩
  have e : (c : ℚ) / (4 : ℚ) ^ qIdx p - (-1) = ((c + 4 ^ qIdx p : ℕ) : ℚ) / (4 : ℚ) ^ qIdx p := by
    push_cast; field_simp; ring
  rw [e, padicNorm.div, hn4, div_one]
  have hdvd : p ∣ c + 4 ^ qIdx p := by
    rw [← ZMod.natCast_eq_zero_iff]
    push_cast
    rw [hcz, hpow]; ring
  exact (padicNorm.nat_lt_one_iff _).mpr hdvd

/-- L5: φ_{n₀} is a p-adic unit. -/
theorem L5_phi_n0_unit (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    padicNorm p (phi (n0Idx p)) = 1 := by
  obtain ⟨r, hr⟩ : ∃ r, p = 4 * r + 3 := ⟨p / 4, by omega⟩
  have hn0 : n0Idx p = r + 1 := by unfold n0Idx; omega
  have hC : ¬ p ∣ Nat.choose (2 * (r + 1)) (r + 1) := by
    intro h
    have h2 := Nat.choose_mul_factorial_mul_factorial (show r + 1 ≤ 2 * (r + 1) by omega)
    have h3 : p ∣ (2 * (r + 1)).factorial := by
      rw [← h2]; exact (h.mul_right _).mul_right _
    rw [Nat.Prime.dvd_factorial (Fact.out)] at h3
    omega
  have h4 : ¬ p ∣ 4 ^ (r + 1) := fun h => not_dvd_four p hp (Nat.Prime.dvd_of_dvd_pow Fact.out h)
  have h5 : ¬ p ∣ 4 * (r + 1) + 1 := by
    intro h
    have e : 4 * (r + 1) + 1 = p + 2 := by omega
    rw [e] at h
    have h2 := (Nat.dvd_add_right (dvd_refl p)).mp h
    have := Nat.le_of_dvd (by norm_num) h2
    omega
  have hden : ¬ p ∣ 4 ^ (r + 1) * (4 * (r + 1) + 1) := fun h =>
    ((Nat.Prime.dvd_mul Fact.out).mp h).elim h4 h5
  unfold phi
  rw [hn0]
  have e : ((4 : ℚ) ^ (r + 1) * (4 * ((r + 1 : ℕ) : ℚ) + 1))
      = ((4 ^ (r + 1) * (4 * (r + 1) + 1) : ℕ) : ℚ) := by push_cast; ring
  rw [e, padicNorm.div, (padicNorm.nat_eq_one_iff _).mpr hC,
    (padicNorm.nat_eq_one_iff _).mpr hden]
  simp

end

end H12.B4

#print axioms H12.B4.L2_pphi_q
#print axioms H12.B4.L5_phi_n0_unit
