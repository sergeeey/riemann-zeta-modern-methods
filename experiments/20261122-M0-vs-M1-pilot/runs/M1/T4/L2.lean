inductive Tree where
  | leaf : Tree
  | node : Tree → Nat → Tree → Tree

def Tree.mirror : Tree → Tree
  | .leaf => .leaf
  | .node l v r => .node r.mirror v l.mirror

def Tree.size : Tree → Nat
  | .leaf => 0
  | .node l _ r => l.size + 1 + r.size

theorem mirror_mirror (t : Tree) : t.mirror.mirror = t := by
  induction t with
  | leaf => rfl
  | node l v r ihl ihr =>
    show Tree.node l.mirror.mirror v r.mirror.mirror = Tree.node l v r
    rw [ihl, ihr]
