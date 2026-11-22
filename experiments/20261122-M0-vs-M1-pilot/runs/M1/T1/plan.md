Plan (dependency graph):
L1: oddSum_succ-free; main theorem follows by induction on n from
  step: (n*n) + (2*n+1) = (n+1)*(n+1)   [lemma sq_step, pure arithmetic, no deps]
T1 depends on sq_step (induction: oddSum (n+1) = oddSum n + (2n+1) = n*n+(2n+1) = (n+1)*(n+1)).
Lemmas: 1 (sq_step). Graph: sq_step -> T1.
