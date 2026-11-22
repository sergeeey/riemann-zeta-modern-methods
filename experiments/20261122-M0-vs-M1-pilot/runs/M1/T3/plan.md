# Plan
Math: fibSum n = sum_{i<n} fib i; claim fibSum n + 1 = fib (n+1).
Induction: fibSum (n+1) + 1 = fibSum n + fib n + 1 = fib(n+1) + fib n = fib(n+2).

L1: lemma fib_succ_succ (n) : fib (n+2) = fib n + fib (n+1) := rfl   (no deps)
L2: lemma fibSum_succ (n) : fibSum (n+1) = fibSum n + fib n := rfl  (no deps)
T3: induction n; base: rfl/decide; step uses L2, ih, L1 and omega.  deps: L1, L2
