import Main

-- Full axiom audit of the five headline theorems and the central claim.  STATUS: NOT_RUN (needs `lake build Main` first, see run_full_main_build.sh).
-- A clean result lists only: propext, Classical.choice, Quot.sound.  Anything else (sorryAx, Lean.ofReduceBool, a custom axiom) is a defect.
-- Classical.choice is a Lean logical axiom, not an extra mathematical axiom; do not count it as a defect.
#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive
#print axioms UpperTheory.FinalTheorems.everyCharacter
