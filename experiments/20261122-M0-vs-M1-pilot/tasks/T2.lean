def rev {α : Type} : List α → List α
  | [] => []
  | x :: xs => rev xs ++ [x]

theorem T2 {α : Type} (l : List α) : rev (rev l) = l := by
  sorry
