/-!
# H12-B4-06: exact integer geometry of the first resonance

Source: H12-PADIC-B4-06-PROOF.md, Steps 2–4.
NOT KERNEL CHECKED in this environment (Lean/lake unavailable).
No sorry, axioms, placeholders or admitted theorems.

This file deliberately formalizes only the parameter geometry; the p-adic
unit/congruence lemmas remain obligations described in PROOF_OBLIGATIONS.md.
-/
import Mathlib

namespace H12.B4

/-- For primes p ≡ 3 mod 4, write p = 4r+3. -/
def primeParameter (r : ℕ) : ℕ := 4*r+3
/-- n₀ = (p+1)/4 = r+1. -/
def firstIndex (r : ℕ) : ℕ := r+1
/-- q = (p²-1)/4. -/
def exceptionalIndex (r : ℕ) : ℕ := 4*r*r+6*r+2
/-- n₁ = p n₀. -/
def resonanceIndex (r : ℕ) : ℕ := primeParameter r * firstIndex r

theorem exceptional_quadratic (r : ℕ) :
    (primeParameter r)^2 = 4*(exceptionalIndex r)+1 := by
  dsimp [primeParameter, exceptionalIndex]
  ring

theorem resonance_decomposition (r : ℕ) :
    resonanceIndex r = exceptionalIndex r + firstIndex r := by
  dsimp [resonanceIndex, primeParameter, exceptionalIndex, firstIndex]
  ring

theorem isolated_exceptional_support (r : ℕ) :
    resonanceIndex r < 2*(exceptionalIndex r) := by
  dsimp [resonanceIndex, primeParameter, exceptionalIndex, firstIndex]
  nlinarith [Nat.zero_le (r*r)]

theorem first_index_lt_prime (r : ℕ) :
    firstIndex r < primeParameter r := by
  dsimp [firstIndex, primeParameter]
  omega

theorem first_resonance_identity (r : ℕ) :
    4*(resonanceIndex r) = (primeParameter r) * ((primeParameter r)+1) := by
  dsimp [resonanceIndex, primeParameter, firstIndex]
  ring

end H12.B4
