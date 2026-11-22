def rev {α : Type} : List α → List α
  | [] => []
  | x :: xs => rev xs ++ [x]

theorem rev_append_aux {α : Type} (a b : List α) : rev (a ++ b) = rev b ++ rev a := by
  induction a with
  | nil => simp [rev]
  | cons x xs ih => simp [rev, ih, List.append_assoc]

theorem T2 {α : Type} (l : List α) : rev (rev l) = l := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    show rev (rev xs ++ [x]) = x :: xs
    rw [rev_append_aux, ih]
    rfl
