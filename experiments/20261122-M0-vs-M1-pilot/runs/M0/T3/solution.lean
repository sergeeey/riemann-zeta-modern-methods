def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n+2 => fib n + fib (n+1)

def fibSum : Nat → Nat
  | 0 => 0
  | n+1 => fibSum n + fib n

theorem T3 (n : Nat) : fibSum n + 1 = fib (n+1) := by
  induction n with
  | zero => decide
  | succ k ih =>
    show fibSum k + fib k + 1 = fib (k+2)
    show fibSum k + fib k + 1 = fib k + fib (k+1)
    omega
