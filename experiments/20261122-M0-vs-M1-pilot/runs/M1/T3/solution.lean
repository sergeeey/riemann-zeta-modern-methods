def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n+2 => fib n + fib (n+1)

def fibSum : Nat → Nat
  | 0 => 0
  | n+1 => fibSum n + fib n

theorem fib_succ_succ (n : Nat) : fib (n+2) = fib n + fib (n+1) := by
  rfl

theorem fibSum_succ (n : Nat) : fibSum (n+1) = fibSum n + fib n := by
  rfl

theorem T3 (n : Nat) : fibSum n + 1 = fib (n+1) := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [fibSum_succ, fib_succ_succ]
    omega
