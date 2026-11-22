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
  | [y], _ => by
    by_cases hxy : x ≤ y
    · have : ins x [y] = [x, y] := by simp [ins, hxy]
      rw [this]; exact ⟨hxy, trivial⟩
    · have : ins x [y] = [y, x] := by simp [ins, hxy]
      rw [this]; exact ⟨by omega, trivial⟩
  | y :: z :: zs, h => by
    obtain ⟨hyz, hrest⟩ := h
    have ih := ins_sorted x (z :: zs) hrest
    by_cases hxy : x ≤ y
    · have : ins x (y :: z :: zs) = x :: y :: z :: zs := by simp [ins, hxy]
      rw [this]; exact ⟨hxy, hyz, hrest⟩
    · have e : ins x (y :: z :: zs) = y :: ins x (z :: zs) := by simp [ins, hxy]
      rw [e]
      have hyx : y ≤ x := by omega
      by_cases hxz : x ≤ z
      · have e2 : ins x (z :: zs) = x :: z :: zs := by simp [ins, hxz]
        rw [e2] at ih ⊢
        exact ⟨hyx, ih⟩
      · have e2 : ins x (z :: zs) = z :: ins x zs := by simp [ins, hxz]
        rw [e2] at ih ⊢
        exact ⟨hyz, ih⟩

theorem T6 (l : List Nat) : Sorted (isort l) := by
  induction l with
  | nil => simp [isort, Sorted]
  | cons x xs ih => exact ins_sorted x _ ih
