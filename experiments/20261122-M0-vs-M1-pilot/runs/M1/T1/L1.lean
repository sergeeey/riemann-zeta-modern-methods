def oddSum : Nat → Nat
  | 0 => 0
  | n+1 => oddSum n + (2*n+1)

theorem sq_step (n : Nat) : n * n + (2*n+1) = (n+1)*(n+1) := by
  simp [Nat.add_mul, Nat.mul_add, Nat.two_mul, Nat.mul_one, Nat.one_mul, Nat.add_assoc]
