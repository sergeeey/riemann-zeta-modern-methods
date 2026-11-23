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
