def ins (x : Nat) : List Nat → List Nat
  | [] => [x]
  | y :: ys => if x ≤ y then x :: y :: ys else y :: ins x ys

def isort : List Nat → List Nat
  | [] => []
  | x :: xs => ins x (isort xs)

def Sorted : List Nat → Prop
  | [] => True
  | [_] => True
  | x :: y :: zs => x ≤ y ∧ Sorted (y :: zs)

theorem ins_sorted (x : Nat) : ∀ (l : List Nat), Sorted l → Sorted (ins x l)
  | [], _ => by simp [ins, Sorted]
  | y :: ys, h => by
    by_cases hxy : x ≤ y
    · have e : ins x (y :: ys) = x :: y :: ys := by simp [ins, hxy]
      rw [e]
      exact ⟨hxy, h⟩
    · have e : ins x (y :: ys) = y :: ins x ys := by simp [ins, hxy]
      rw [e]
      cases ys with
      | nil => simp [ins, Sorted]; omega
      | cons z zs =>
        have ih := ins_sorted x (z :: zs) h.2
        by_cases hxz : x ≤ z
        · have e2 : ins x (z :: zs) = x :: z :: zs := by simp [ins, hxz]
          rw [e2] at ih ⊢
          exact ⟨by omega, ih⟩
        · have e2 : ins x (z :: zs) = z :: ins x zs := by simp [ins, hxz]
          rw [e2] at ih ⊢
          exact ⟨h.1, ih⟩

theorem T6 (l : List Nat) : Sorted (isort l) := by
  induction l with
  | nil => exact trivial
  | cons x xs ih => exact ins_sorted x _ ih
