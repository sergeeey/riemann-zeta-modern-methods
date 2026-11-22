# Plan
Main: T5 (n : Nat) : n < pow2 n, by induction; step needs n+1 < 2*pow2 n from n < pow2 n.
- L1 pow2_succ (n) : pow2 (n+1) = 2 * pow2 n   -- deps: none (rfl)
- L2 pow2_pos (n) : 0 < pow2 n                  -- deps: L1 (induction, omega)
- T5 : deps L1, L2 (induction; omega using ih, L2, L1)
