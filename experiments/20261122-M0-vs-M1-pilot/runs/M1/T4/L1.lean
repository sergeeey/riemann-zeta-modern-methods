inductive Tree where
  | leaf : Tree
  | node : Tree → Nat → Tree → Tree

def Tree.mirror : Tree → Tree
  | .leaf => .leaf
  | .node l v r => .node r.mirror v l.mirror

def Tree.size : Tree → Nat
  | .leaf => 0
  | .node l _ r => l.size + 1 + r.size

theorem size_mirror (t : Tree) : t.mirror.size = t.size := by
  induction t with
  | leaf => rfl
  | node l v r ihl ihr =>
    show r.mirror.size + 1 + l.mirror.size = l.size + 1 + r.size
    rw [ihl, ihr]; omega
