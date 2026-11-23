import Mathlib
/-!
H12 B4-06: small algebraic interface after the formal power-series calculation.
UNCOMPILED candidate: `lean` and `lake` are unavailable in this runtime.
No `sorry`, no additional axioms.  This does *not* prove the
universal Lagrange/Frobenius or valuation lemmas: those are separately listed
in PROOF_OBLIGATIONS.md.
-/

namespace H12.B4

/-- The last algebraic step of B4-06, independent of the elliptic curve. -/
theorem normalized_residue_bridge (R : Type*) [CommRing R]
    (phi low high : R)
    (hLow : low = 2 * phi)
    (hHigh : high = -2 * phi) : high = -low := by
  rw [hLow, hHigh]
  ring

/-- Exact first example at p=3; this is rational arithmetic only. -/
theorem p3_normalized_coefficients :
    ((3 : ℚ) * (4 * (-(5 : ℚ)/12)) = -5) ∧
    ((3 : ℚ) * (3 * 220 * (-(13 : ℚ)/990)) = -26) := by
  constructor <;> norm_num

end H12.B4
#print axioms H12.B4.normalized_residue_bridge
#print axioms H12.B4.p3_normalized_coefficients
