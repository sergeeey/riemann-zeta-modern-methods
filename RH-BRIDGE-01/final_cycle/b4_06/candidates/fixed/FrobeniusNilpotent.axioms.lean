/-
H12-B4-06-FROBENIUS-04
Target: generic nilpotent Frobenius bridge in characteristic p.
NOT KERNEL-CHECKED: Lean/Lake unavailable in this environment.
No `sorry`, no custom axioms. `add_pow_char` is a Mathlib theorem.
-/
import Mathlib

namespace H12.B4

/--
An element of the form 1+x has pth power 1 in a commutative
ring of characteristic p whenever x^p=0.
This models 1+u A(u) in F_p[u]/(u^p).
-/
theorem frobenius_one_add_of_nilpotent
    (p : ℕ) [Fact (Nat.Prime p)]
    (R : Type*) [CommRing R] [CharP R p]
    (x : R) (hx : x ^ p = 0) :
    ((1 : R) + x) ^ p = 1 := by
  calc
    ((1 : R) + x) ^ p = (1 : R) ^ p + x ^ p :=
      add_pow_char (1 : R) x p
    _ = 1 := by simp [hx]

/-- The entire p(p+1)-power disappears in the truncated ring. -/
theorem frobenius_large_power_of_nilpotent
    (p : ℕ) [Fact (Nat.Prime p)]
    (R : Type*) [CommRing R] [CharP R p]
    (x : R) (hx : x ^ p = 0) :
    ((1 : R) + x) ^ (p * (p + 1)) = 1 := by
  rw [pow_mul, frobenius_one_add_of_nilpotent p R x hx, one_pow]

/--
Algebraic negative-exponent interface, avoiding any unjustified
inversion in a non-domain. Once F*G=1 and F^p=1, we have
F*G^(p(p+1))=F. In the truncated power-series ring,
F is the series with constant coefficient 1, G its inverse.
-/
theorem frobenius_inverse_truncation
    (p : ℕ) (R : Type*) [CommRing R]
    (F G : R) (hFG : F * G = 1)
    (hFp : F ^ p = 1) :
    F * G ^ (p * (p + 1)) = F := by
  have hGp : G ^ p = 1 := by
    have hprod : F ^ p * G ^ p = 1 := by
      calc
        F ^ p * G ^ p = (F * G) ^ p := (mul_pow F G p).symm
        _ = 1 := by rw [hFG, one_pow]
    simpa [hFp] using hprod
  rw [pow_mul, hGp, one_pow, mul_one]

/--
The exact variant used in Step 4 is the same theorem:
if F = 1+x with x^p = 0 and F*G = 1,
then F * G^(p(p+1)) = F.
`G^(p(p+1))` is the meaning of F^(-p(p+1)).
-/
theorem frobenius_step4_interface
    (p : ℕ) [Fact (Nat.Prime p)]
    (R : Type*) [CommRing R] [CharP R p]
    (x G : R) (hx : x ^ p = 0)
    (hInv : ((1 : R) + x) * G = 1) :
    ((1 : R) + x) * G ^ (p * (p + 1)) = (1 : R) + x := by
  exact frobenius_inverse_truncation p R ((1 : R) + x) G hInv
    (frobenius_one_add_of_nilpotent p R x hx)

end H12.B4
#print axioms H12.B4.frobenius_one_add_of_nilpotent
#print axioms H12.B4.frobenius_large_power_of_nilpotent
#print axioms H12.B4.frobenius_inverse_truncation
#print axioms H12.B4.frobenius_step4_interface
