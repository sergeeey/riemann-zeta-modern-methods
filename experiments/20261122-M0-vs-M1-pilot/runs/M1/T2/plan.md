# Plan
L1: rev_append : rev (xs ++ ys) = rev ys ++ rev xs   (deps: List.append_assoc, List.append_nil from core)
L2: rev_singleton-free; main: rev (rev l) = l by induction on l using L1  (deps: L1)
Main T2 depends on L1.
