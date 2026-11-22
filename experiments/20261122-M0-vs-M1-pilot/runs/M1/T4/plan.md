# Plan
L1 size_mirror (t : Tree) : t.mirror.size = t.size   -- induction; uses Nat.add_comm via omega. deps: none
L2 mirror_mirror (t : Tree) : t.mirror.mirror = t     -- induction. deps: none
T4 := ⟨size_mirror t, mirror_mirror t⟩                -- deps: L1, L2
