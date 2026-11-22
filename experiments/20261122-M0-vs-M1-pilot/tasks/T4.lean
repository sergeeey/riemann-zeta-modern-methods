inductive Tree where
  | leaf : Tree
  | node : Tree → Nat → Tree → Tree

def Tree.mirror : Tree → Tree
  | .leaf => .leaf
  | .node l v r => .node r.mirror v l.mirror

def Tree.size : Tree → Nat
  | .leaf => 0
  | .node l _ r => l.size + 1 + r.size

theorem T4 (t : Tree) : t.mirror.size = t.size ∧ t.mirror.mirror = t := by
  sorry
