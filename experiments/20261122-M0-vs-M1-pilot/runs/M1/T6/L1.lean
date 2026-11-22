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

-- head of ins x l is x or head of l
theorem ins_head (x y : Nat) (ys : List Nat) :
    ∃ z zs, ins x (y :: ys) = z :: zs ∧ (z = x ∨ z = y) ∧ (z = x → x ≤ y) ∧ (z = y → y ≤ x ∨ True) := by
  unfold ins
  split
  · exact ⟨x, y :: ys, rfl, Or.inl rfl, fun _ => by assumption, fun _ => Or.inr trivial⟩
  · exact ⟨y, ins x ys, rfl, Or.inr rfl, fun _ => by omega, fun _ => Or.inr trivial⟩

theorem ins_sorted (x : Nat) : ∀ (l : List Nat), Sorted l → Sorted (ins x l)
  | [], _ => by simp [ins, Sorted]
  | y :: ys, h => by
    unfold ins
    split
    · rename_i hxy
      cases ys with
      | nil => exact ⟨hxy, trivial⟩
      | cons z zs => exact ⟨hxy, h⟩
    · rename_i hxy
      cases ys with
      | nil => simp [ins, Sorted]; omega
      | cons z zs =>
        have ih := ins_sorted x (z :: zs) h.2
        unfold ins at ih ⊢
        split
        · rename_i hxz
          exact ⟨by omega, ih⟩
        · rename_i hxz
          exact ⟨h.1, ih⟩

theorem T6 (l : List Nat) : Sorted (isort l) := by
  induction l with
  | nil => exact trivial
  | cons x xs ih => exact ins_sorted x _ ih
