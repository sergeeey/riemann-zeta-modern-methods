def oddSum : Nat → Nat
  | 0 => 0
  | n+1 => oddSum n + (2*n+1)

theorem T1 (n : Nat) : oddSum n = n * n := by
  sorry
