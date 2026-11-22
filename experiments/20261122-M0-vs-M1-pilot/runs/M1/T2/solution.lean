def rev {α : Type} : List α → List α
  | [] => []
  | x :: xs => rev xs ++ [x]

theorem rev_append {α : Type} (xs ys : List α) : rev (xs ++ ys) = rev ys ++ rev xs := by
  induction xs with
  | nil => simp [rev]
  | cons x xs ih => simp [rev, ih, List.append_assoc]

theorem T2 {α : Type} (l : List α) : rev (rev l) = l := by
  induction l with
  | nil => simp [rev]
  | cons x xs ih => simp [rev, rev_append, ih]
