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

theorem T6 (l : List Nat) : Sorted (isort l) := by
  sorry
