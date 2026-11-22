def pow2 : Nat → Nat
  | 0 => 1
  | n+1 => 2 * pow2 n

theorem T5 (n : Nat) : n < pow2 n := by
  sorry
