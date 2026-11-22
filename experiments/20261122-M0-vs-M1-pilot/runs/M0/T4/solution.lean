inductive Tree where
  | leaf : Tree
  | node : Tree → Nat → Tree → Tree

def Tree.mirror : Tree → Tree
  | .leaf => .leaf
  | .node l v r => .node r.mirror v l.mirror

def Tree.size : Tree → Nat
  | .leaf => 0
  | .node l _ r => l.size + 1 + r.size


theorem Tree.size_mirror (t : Tree) : t.mirror.size = t.size := by
  induction t with
  | leaf => rfl
  | node l v r ihl ihr =>
    simp only [Tree.mirror, Tree.size, ihl, ihr]
    omega

theorem Tree.mirror_mirror (t : Tree) : t.mirror.mirror = t := by
  induction t with
  | leaf => rfl
  | node l v r ihl ihr =>
    simp only [Tree.mirror, ihl, ihr]

theorem T4 (t : Tree) : t.mirror.size = t.size ∧ t.mirror.mirror = t := by
  exact ⟨Tree.size_mirror t, Tree.mirror_mirror t⟩
