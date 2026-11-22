def pow2 : Nat → Nat
  | 0 => 1
  | n+1 => 2 * pow2 n

theorem pow2_succ (n : Nat) : pow2 (n+1) = 2 * pow2 n := rfl

theorem pow2_pos (n : Nat) : 0 < pow2 n := by
  induction n with
  | zero => decide
  | succ k ih => rw [pow2_succ]; omega
