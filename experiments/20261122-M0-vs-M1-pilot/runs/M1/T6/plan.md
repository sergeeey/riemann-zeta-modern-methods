# Plan
L1 ins_sorted : (x : Nat) (l : List Nat) -> Sorted l -> Sorted (ins x l)   (depends on L0)
L0 helper: ins_head : (x) (l) -> Sorted l -> ∃ ... ; need: for sorted y::ys, x<=y or y<=x handled by case.
   Strengthen: ins_cons_cases: Sorted (y::ys) -> Sorted (ins x (y::ys)) proven by induction on ys, generalizing y.
T6 : induction on l using L1.
Graph: L1 -> T6
