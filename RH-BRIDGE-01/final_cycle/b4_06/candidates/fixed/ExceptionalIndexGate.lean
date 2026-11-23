import Mathlib
/-!
H12 B4-06: arithmetic skeleton for unique exceptional Phi coefficient.
NOT KERNEL CHECKED: this container has no Lean or Lake.
No `sorry`, no custom axioms.
These lemmas treat index arithmetic, not p-adic valuations.
-/

namespace H12.B4

private def p (r : ℕ) : ℕ := 4*r + 3
private def n0 (r : ℕ) : ℕ := r + 1
private def q (r : ℕ) : ℕ := 4*r*r + 6*r + 2
private def n1 (r : ℕ) : ℕ := p r * n0 r

/-- First index is below p, and the first resonance is below two exceptional indices. -/
theorem resonance_region (r : ℕ) :
    n0 r < p r ∧ n1 r = q r + n0 r ∧ n1 r < 2 * q r := by
  dsimp [n0, n1, p, q]
  constructor
  · omega
  constructor
  · ring
  · nlinarith [Nat.zero_le (r*r)]

/-- The denominator 4j+1 being a multiple of p forces its quotient d to be 3 mod 4. -/
theorem divisor_mod_four (r j d : ℕ)
    (h : 4*j+1 = d * p r) : d % 4 = 3 := by
  have hlin : 4*j+1 = 4*(d*r)+3*d := by
    calc
      4*j+1 = d * p r := h
      _ = 4*(d*r)+3*d := by simp [p]; ring
  omega

/-- All possible small quotients are strictly below p except the one equal to p. -/
theorem quotient_below_or_exceptional (r d : ℕ)
    (hd : d % 4 = 3) (hbound : d ≤ p r + 1) :
    d < p r ∨ d = p r := by
  dsimp [p] at *
  omega

/-- In the exceptional divisor case, j is exactly q. -/
theorem divisor_equals_p_implies_exceptional (r j : ℕ)
    (h : 4*j+1 = p r * p r) : j = q r := by
  have hquad : p r * p r = 4 * q r + 1 := by
    simp [p, q]
    ring
  omega

/-- The resonance endpoint implies the quotient bound d ≤ p+1. -/
theorem quotient_upper_bound (r j d : ℕ)
    (hj : j ≤ n1 r)
    (h : 4*j+1 = d * p r) : d ≤ p r + 1 := by
  have hmul : 4 * n1 r = p r * (p r + 1) := by
    simp [n1, n0, p]
    ring
  by_contra hnot
  have hgt : p r + 2 ≤ d := by omega
  have hp : 0 < p r := by simp [p]
  have hmul_le : (p r + 2) * p r ≤ d * p r := Nat.mul_le_mul_right (p r) hgt
  have hleft : 4*j+1 ≤ 4*n1 r+1 := by omega
  nlinarith [hmul_le, hleft, hmul]

/-- Purely arithmetic classification of all denominators divisible by p up to n1. -/
theorem only_exceptional_divisor_or_small (r j d : ℕ)
    (hj : j ≤ n1 r)
    (h : 4*j+1 = d * p r) :
    d < p r ∨ j = q r := by
  have hm := divisor_mod_four r j d h
  have hb := quotient_upper_bound r j d hj h
  rcases quotient_below_or_exceptional r d hm hb with hlo | heq
  · exact Or.inl hlo
  · right
    apply divisor_equals_p_implies_exceptional r j
    simpa [heq] using h

/-- The remainder s=(3p-1)/4 has a base-p carry when doubled. -/
theorem carry_remainder (r : ℕ) :
    3*r+2 < p r ∧ p r ≤ 2*(3*r+2) := by
  dsimp [p]
  omega

/-- Each small divisor d=4h+3 gives a base-p digit s independent of h. -/
theorem denominator_index_digit (r h j : ℕ)
    (hden : 4*j+1 = (4*h+3)*p r) :
    j = h*(p r)+(3*r+2) := by
  have hid : 4*(h*(p r)+(3*r+2))+1 = (4*h+3)*p r := by
    simp [p]
    ring
  omega

end H12.B4
