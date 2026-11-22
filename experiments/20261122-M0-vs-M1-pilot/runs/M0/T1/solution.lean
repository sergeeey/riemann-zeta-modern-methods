def oddSum : Nat → Nat
  | 0 => 0
  | n+1 => oddSum n + (2*n+1)

theorem T1 (n : Nat) : oddSum n = n * n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    show oddSum k + (2*k+1) = (k+1)*(k+1)
    rw [ih]
    rw [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.two_mul]
    omega
