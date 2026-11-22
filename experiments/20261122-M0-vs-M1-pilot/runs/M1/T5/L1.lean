def pow2 : Nat → Nat
  | 0 => 1
  | n+1 => 2 * pow2 n

theorem pow2_succ (n : Nat) : pow2 (n+1) = 2 * pow2 n := rfl
