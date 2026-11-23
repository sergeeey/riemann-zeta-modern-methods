import Mathlib

/-!
# H12-B4-06: universal first-resonance congruence for `lagA`: p * lagA n1 = -(lagA n0) (mod p), p = 3 (mod 4)
SCOPE (read together): here `a_n` means exactly `lagA n`, the Lagrange-inversion formula (1) of
H12-PADIC-B4-06-PROOF.md. NOT formalized in this file: (i) the identification of `lagA n` with the
Laurent coefficients of the Weierstrass wp function (checked numerically only, n <= 60), (ii) Step 5
(the transfer wp -> h_n -> beta), (iii) the B4-05 two-source identity and the criterion c^((p^2-1)/4) = -1,
(iv) the identification with the author's beta. The theorem name refers to the first Dwork resonance index
n1 = p(p+1)/4 only; it is NOT the headline theorem of PROOF.md.
Build: concatenation of separately compiled modules (L1, L2/L5, L3a/L3d, L3b/L3c) + Final.lean;
the file as a whole is compiled and checked by itself (provenance of the modules is not needed for the check).
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

/-! ===== L3a / L3d (power series perturbation, truncation invariance) ===== -/

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
/-! ===== L3b / L3c (nilpotent Frobenius mod p, reduction via Z_p) ===== -/

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
/-! ===== L1 (p-integrality of phi_j, j <= n1, j /= q) ===== -/
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
/-! ===== L2 / L5 (p*phi_q = -1 mod p, phi_{n0} unit) ===== -/

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
/-! ### Assembly helpers (p-adic bookkeeping) -/

/-- norm of a rational equals the norm of any `ℤ_[p]` lift. -/
theorem norm_of_lift (p : ℕ) [Fact p.Prime] (x : ℚ) (z : ℤ_[p])
    (h : (z : ℚ_[p]) = ((x : ℚ) : ℚ_[p])) : padicNorm p x = ‖z‖ := by
  have h1 : ‖((x : ℚ) : ℚ_[p])‖ = padicNorm p x := Padic.eq_padicNorm x
  rw [← h1, ← h]
  exact PadicInt.norm_def.symm

/-- `toZMod z = 0` iff `‖z‖ < 1`. -/
theorem toZMod_eq_zero_iff_norm_lt (p : ℕ) [Fact p.Prime] (z : ℤ_[p]) :
    PadicInt.toZMod z = 0 ↔ ‖z‖ < 1 := by
  rw [← RingHom.mem_ker, PadicInt.ker_toZMod, IsLocalRing.mem_maximalIdeal, mem_nonunits_iff,
    PadicInt.isUnit_iff]
  exact ⟨fun h => lt_of_le_of_ne (PadicInt.norm_le_one z) h, fun h => h.ne⟩

/-- norm of a nonzero-mod-p lift is 1. -/
theorem norm_eq_one_of_toZMod_ne (p : ℕ) [Fact p.Prime] (z : ℤ_[p]) (h : PadicInt.toZMod z ≠ 0) :
    ‖z‖ = 1 := by
  by_contra hne
  exact h ((toZMod_eq_zero_iff_norm_lt p z).mpr (lt_of_le_of_ne (PadicInt.norm_le_one z) hne))

/-- FINAL: first-resonance congruence for the Lagrange coefficients, every prime p ≡ 3 mod 4. -/
theorem B4_06_first_resonance (p : ℕ) [hpf : Fact p.Prime] (hp : p % 4 = 3) :
    PCong p ((p : ℚ) * lagA (n1Idx p)) (-(lagA (n0Idx p))) ∧ padicNorm p (lagA (n0Idx p)) = 1 := by
  have hp3 : 3 ≤ p := by have := hpf.out.two_le; omega
  obtain ⟨r, hr⟩ : ∃ r, p = 4 * r + 3 := ⟨p / 4, by omega⟩
  have hq : qIdx p = 4 * r * r + 6 * r + 2 := by
    have h1 : p ^ 2 = 4 * (4 * r * r + 6 * r + 2) + 1 := by rw [hr]; ring
    unfold qIdx
    rw [Nat.sub_eq_of_eq_add h1]
    exact Nat.mul_div_cancel_left _ (by norm_num)
  have hn0 : n0Idx p = r + 1 := by unfold n0Idx; omega
  have hn1 : n1Idx p = (4 * r + 3) * (r + 1) := by
    have h1 : p * (p + 1) = 4 * ((4 * r + 3) * (r + 1)) := by rw [hr]; ring
    unfold n1Idx
    rw [h1]
    exact Nat.mul_div_cancel_left _ (by norm_num)
  have h4 : 4 * n1Idx p = p * (p + 1) := by rw [hn1, hr]; ring
  have hqn : n0Idx p < qIdx p := by rw [hn0, hq]; nlinarith [Nat.zero_le (r * r)]
  have hqn1 : qIdx p ≤ n1Idx p := by rw [hq, hn1]; nlinarith [Nat.zero_le (r * r)]
  have hn1q : n1Idx p < 2 * qIdx p := by rw [hq, hn1]; nlinarith [Nat.zero_le (r * r)]
  have hn1n0 : n1Idx p = qIdx p + n0Idx p := by rw [hq, hn1, hn0]; ring
  have hn0p : n0Idx p < p := by rw [hn0]; omega
  have hn0n1 : n0Idx p ≤ n1Idx p := by omega
  have hP2 : 2 ≤ p * (p + 1) := by nlinarith
  have h4n0 : 4 * n0Idx p = p + 1 := by omega
  have hD : padicNorm p ((2 * (n1Idx p : ℚ) - 1)) = 1 := by
    have : (2 * (n1Idx p : ℚ) - 1) = ((2 * (n1Idx p : ℤ) - 1 : ℤ) : ℚ) := by push_cast; ring
    rw [this, padicNorm.int_eq_one_iff]
    intro h
    have h1 : (p : ℤ) ∣ 1 := by
      have h2 : (p : ℤ) ∣ (p : ℤ) * (2 * (r + 1)) := dvd_mul_right _ _
      have h3 : (1 : ℤ) = (p : ℤ) * (2 * (r + 1)) - (2 * (n1Idx p : ℤ) - 1) := by
        rw [hn1, hr]; push_cast; ring
      rw [h3]; exact dvd_sub h2 h
    have := Int.eq_one_of_dvd_one (by positivity) h1
    have := hpf.out.one_lt
    omega
  have hD0 : padicNorm p ((2 * (n0Idx p : ℚ) - 1)) = 1 := by
    have : (2 * (n0Idx p : ℚ) - 1) = ((2 * (n0Idx p : ℤ) - 1 : ℤ) : ℚ) := by push_cast; ring
    rw [this, padicNorm.int_eq_one_iff]
    intro h
    have h1 := Int.le_of_dvd (by omega) h
    omega
  have hDne : (2 * (n1Idx p : ℚ) - 1) ≠ 0 := by
    intro h; rw [h] at hD; simp at hD
  have hD0ne : (2 * (n0Idx p : ℚ) - 1) ≠ 0 := by
    intro h; rw [h] at hD0; simp at hD0
  -- integer identities used in ZMod p
  have hDint : (2 * (n1Idx p : ℤ) - 1) = (p : ℤ) * (2 * (r + 1)) - 1 := by
    rw [hn1, hr]; push_cast; ring
  have hD0int : 2 * (2 * (n0Idx p : ℤ) - 1) = (p : ℤ) - 1 := by omega
  have hM0nat : 4 * n1Idx p - 2 + 2 = p * (p + 1) := by omega
  set q := qIdx p with hqdef
  set n0 := n0Idx p with hn0def
  set n1 := n1Idx p with hn1def
  -- the series
  have hΦ : ∀ j, coeff j PhiSeries = phi j := fun j => by simp [PhiSeries]
  have hΦ0 : constantCoeff PhiSeries = 1 := by
    rw [← PowerSeries.coeff_zero_eq_constantCoeff_apply, hΦ]; simp [phi]
  have hq0 : q ≠ 0 := by omega
  let F : ℚ⟦X⟧ := PowerSeries.mk fun j => if j ≤ n1 ∧ j ≠ q then phi j else 0
  have hFc : ∀ j, coeff j F = if j ≤ n1 ∧ j ≠ q then phi j else 0 := fun j => by simp [F]
  have hF0 : constantCoeff F = 1 := by
    rw [← PowerSeries.coeff_zero_eq_constantCoeff_apply, hFc,
      if_pos ⟨Nat.zero_le _, fun h => hq0 h.symm⟩]
    simp [phi]
  have hFint : ∀ n, padicNorm p (coeff n F) ≤ 1 := by
    intro n; rw [hFc]; split_ifs with h
    · exact L1_phi_integral p hp n h.1 h.2
    · simp
  have hΨ : ∀ j, j ≤ n1 → coeff j (F + PowerSeries.C (phi q) * X ^ q) = phi j := by
    intro j hj
    rw [map_add, hFc, PowerSeries.coeff_C_mul_X_pow]
    by_cases hjq : j = q
    · simp [hjq]
    · simp [hj, hjq]
  obtain ⟨M0, hM0⟩ : ∃ M0, M0 = 4 * n1 - 2 := ⟨_, rfl⟩
  have hM1 : M0 + 1 = p * (p + 1) - 1 := by omega
  have hP4 : 4 * n0 - 2 = p - 1 := by omega
  have key1 : coeff n1 ((PhiSeries⁻¹) ^ M0) = coeff n1 ((F⁻¹) ^ M0)
      - (M0 : ℚ) * phi q * coeff n0 ((F⁻¹) ^ (M0 + 1)) := by
    have e1 : coeff n1 ((PhiSeries⁻¹) ^ M0)
        = coeff n1 (((F + PowerSeries.C (phi q) * X ^ q)⁻¹) ^ M0) :=
      L3d_trunc_invariance PhiSeries (F + PowerSeries.C (phi q) * X ^ q) hΦ0 n1 M0 n1 le_rfl
        (fun j hj => by rw [hΦ, hΨ j hj])
    have e2 := L3a_inv_pow_perturb F hF0 (phi q) q n1 M0 hqn1 hn1q
    have hsub : n1 - q = n0 := by omega
    rw [hsub] at e2
    rw [e1]; exact e2
  have key0 : coeff n0 ((PhiSeries⁻¹) ^ (p - 1)) = coeff n0 ((F⁻¹) ^ (p - 1)) :=
    L3d_trunc_invariance PhiSeries F hΦ0 n0 (p - 1) n0 le_rfl (fun j hj => by
      rw [hΦ, hFc, if_pos ⟨by omega, by omega⟩])
  have hlag1 : lagA n1 = -(1 / (2 * (n1 : ℚ) - 1)) *
      (coeff n1 ((F⁻¹) ^ M0) - (M0 : ℚ) * phi q * coeff n0 ((F⁻¹) ^ (M0 + 1))) := by
    unfold lagA; rw [← hM0, key1]
  have hlag0 : lagA n0 = -(1 / (2 * (n0 : ℚ) - 1)) * coeff n0 ((F⁻¹) ^ (p - 1)) := by
    unfold lagA; rw [hP4, key0]
  -- reduction mod p of the inverse powers
  obtain ⟨G, hG0, hGz, hGM⟩ := L3c_reduction p F hF0 hFint
  obtain ⟨hc1, z1, hz1c, hz1r⟩ := hGM M0 n1
  obtain ⟨hc2, z2, hz2c, hz2r⟩ := hGM (M0 + 1) n0
  obtain ⟨hc0, z0, hz0c, hz0r⟩ := hGM (p - 1) n0
  obtain ⟨zF, hzFc, hzFr⟩ := hGz n0
  have hfrob := L3b_frobenius_trunc p G hG0 n0 hn0p
  have hz2' : PadicInt.toZMod z2 = coeff n0 G := by rw [hz2r, hM1]; exact hfrob.1
  have hz0' : PadicInt.toZMod z0 = coeff n0 G := by rw [hz0r]; exact hfrob.2
  have hphi_n0 : coeff n0 F = phi n0 := by rw [hFc, if_pos ⟨hn0n1, by omega⟩]
  have hgne : coeff n0 G ≠ 0 := by
    intro h0
    have h1 : PadicInt.toZMod zF = 0 := by rw [hzFr]; exact h0
    have h2 := (toZMod_eq_zero_iff_norm_lt p zF).mp h1
    have h3 : padicNorm p (phi n0) = ‖zF‖ := by
      rw [← hphi_n0]; exact norm_of_lift p _ zF hzFc
    have h5 : ((padicNorm p (phi n0) : ℚ) : ℝ) = 1 := by exact_mod_cast L5_phi_n0_unit p hp
    rw [h3] at h5
    exact absurd h5 (ne_of_lt h2)
  -- the lift of p * phi_q and its residue -1
  obtain ⟨_, hwa, _, hwc⟩ := L2_pphi_q p hp
  have hwn : ‖(((p : ℚ) * phi q : ℚ) : ℚ_[p])‖ ≤ 1 := by rw [Padic.eq_padicNorm]; exact_mod_cast hwa
  let w : ℤ_[p] := ⟨(((p : ℚ) * phi q : ℚ) : ℚ_[p]), hwn⟩
  have hwcoe : (w : ℚ_[p]) = (((p : ℚ) * phi q : ℚ) : ℚ_[p]) := rfl
  have hwZ : PadicInt.toZMod w = -1 := by
    have hn : ‖w + 1‖ < 1 := by
      have h1 : padicNorm p ((p : ℚ) * phi q + 1) = ‖w + 1‖ := by
        apply norm_of_lift
        push_cast
        rw [hwcoe]; push_cast; ring
      have hwc' : padicNorm p ((p : ℚ) * phi q + 1) < 1 := by
        simpa [sub_neg_eq_add] using hwc
      have hwc'' : ((padicNorm p ((p : ℚ) * phi q + 1) : ℚ) : ℝ) < 1 := by exact_mod_cast hwc'
      rw [h1] at hwc''
      exact hwc''
    have h2 := (toZMod_eq_zero_iff_norm_lt p (w + 1)).mpr hn
    rw [map_add, map_one] at h2
    exact eq_neg_of_add_eq_zero_left h2
  -- rational quantities
  set c1 := coeff n1 ((F⁻¹) ^ M0) with hc1def
  set c2 := coeff n0 ((F⁻¹) ^ (M0 + 1)) with hc2def
  set c0 := coeff n0 ((F⁻¹) ^ (p - 1)) with hc0def
  set N1 : ℚ := (p : ℚ) * c1 - (M0 : ℚ) * ((p : ℚ) * phi q) * c2 with hN1def
  have hpa1 : (p : ℚ) * lagA n1 = -N1 / (2 * (n1 : ℚ) - 1) := by
    rw [hlag1, hN1def]; field_simp
  have ha0 : lagA n0 = -c0 / (2 * (n0 : ℚ) - 1) := by
    rw [hlag0]; field_simp
  -- integral lift of N1
  set S1 : ℤ_[p] := (p : ℤ_[p]) * z1 - (M0 : ℤ_[p]) * w * z2 with hS1def
  have hS1 : (S1 : ℚ_[p]) = ((N1 : ℚ) : ℚ_[p]) := by
    rw [hS1def, hN1def]
    push_cast
    rw [hz1c, hz2c, hwcoe]; push_cast; ring
  have hN1norm : padicNorm p N1 ≤ 1 := by
    have h := norm_of_lift p N1 S1 hS1
    have h2 : ((padicNorm p N1 : ℚ) : ℝ) ≤ 1 := by rw [h]; exact PadicInt.norm_le_one S1
    exact_mod_cast h2
  have hz0norm : ‖z0‖ = 1 := norm_eq_one_of_toZMod_ne p z0 (by rw [hz0']; exact hgne)
  have hc0norm : padicNorm p c0 = 1 := by
    have h := norm_of_lift p c0 z0 hz0c
    have h2 : ((padicNorm p c0 : ℚ) : ℝ) = 1 := by rw [h, hz0norm]
    exact_mod_cast h2
  have hA : padicNorm p ((p : ℚ) * lagA n1) ≤ 1 := by
    rw [hpa1, padicNorm.div, padicNorm.neg, hD, div_one]; exact hN1norm
  have hnormA0 : padicNorm p (lagA n0) = 1 := by
    rw [ha0, padicNorm.div, padicNorm.neg, hc0norm, hD0, div_one]
  have hB : padicNorm p (-(lagA n0)) ≤ 1 := by rw [padicNorm.neg, hnormA0]
  -- the congruence
  set Nn : ℚ := N1 * (2 * (n0 : ℚ) - 1) + c0 * (2 * (n1 : ℚ) - 1) with hNndef
  have hV : ((p : ℚ) * lagA n1 - (-(lagA n0))) * ((2 * (n1 : ℚ) - 1) * (2 * (n0 : ℚ) - 1)) = -Nn := by
    rw [hpa1, ha0, hNndef]; field_simp; ring
  set D0z : ℤ_[p] := ((2 * (n0 : ℤ) - 1 : ℤ) : ℤ_[p]) with hD0zdef
  set Dz : ℤ_[p] := ((2 * (n1 : ℤ) - 1 : ℤ) : ℤ_[p]) with hDzdef
  set Sn : ℤ_[p] := S1 * D0z + z0 * Dz with hSndef
  have hSn : (Sn : ℚ_[p]) = ((Nn : ℚ) : ℚ_[p]) := by
    rw [hSndef, hNndef]
    push_cast
    rw [hS1, hz0c, hD0zdef, hDzdef, PadicInt.coe_intCast, PadicInt.coe_intCast]; push_cast; ring
  have hpz : ((p : ℕ) : ZMod p) = 0 := ZMod.natCast_self p
  have hM0z : ((M0 : ℕ) : ZMod p) = -2 := by
    have hM0p : M0 + 2 = p * (p + 1) := by omega
    have h := congrArg (Nat.cast : ℕ → ZMod p) hM0p
    push_cast at h
    rw [hpz] at h
    linear_combination h
  have he0 : 2 * (2 * (n0 : ZMod p) - 1) = -1 := by
    have h := congrArg (Int.cast : ℤ → ZMod p) hD0int
    push_cast at h
    rw [h, hpz]; ring
  have he1 : 2 * (n1 : ZMod p) - 1 = -1 := by
    have h := congrArg (Int.cast : ℤ → ZMod p) hDint
    push_cast at h
    rw [h, hpz]; ring
  have hSnz : PadicInt.toZMod Sn = 0 := by
    rw [hSndef, hS1def, hD0zdef, hDzdef]
    simp only [map_add, map_mul, map_sub, map_natCast, map_intCast]
    push_cast
    rw [hz2', hz0', hwZ, hpz, hM0z, he1]
    linear_combination (-(coeff n0 G)) * he0
  have hSnlt : ‖Sn‖ < 1 := (toZMod_eq_zero_iff_norm_lt p Sn).mp hSnz
  have hNnnorm : padicNorm p Nn < 1 := by
    have h := norm_of_lift p Nn Sn hSn
    have h2 : ((padicNorm p Nn : ℚ) : ℝ) < 1 := by rw [h]; exact hSnlt
    exact_mod_cast h2
  have hC : padicNorm p ((p : ℚ) * lagA n1 - (-(lagA n0))) < 1 := by
    have h := congrArg (padicNorm p) hV
    rw [padicNorm.mul, padicNorm.mul, hD, hD0, padicNorm.neg] at h
    rw [mul_one, mul_one] at h
    rw [h]; exact hNnnorm
  exact ⟨⟨hA, hB, hC⟩, hnormA0⟩

end

end H12.B4

#print axioms H12.B4.B4_06_first_resonance
