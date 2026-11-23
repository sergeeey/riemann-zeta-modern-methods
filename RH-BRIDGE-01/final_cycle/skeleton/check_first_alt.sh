#!/bin/bash
# For each (A,B) edge whose declaration A contains `first | ...`, print the `first |` line(s) mentioning B,
# to check that every alternative names the same constant B (so the branch choice cannot change the dependency).
cd ~/h12/rh/src || exit 1
chk() {  # A B
  f=$(grep -rl --include=*.lean -E "(theorem|def|lemma) [^ ]*\b$1\b" . | head -1)
  echo "== $1 -> $2   ($f)"
  grep -n -E "first \|" "$f" | grep -w "$2" | cut -c1-330
}
chk open0_of_unitary_group_hypotheses open_orbit_of_unramified_exponents_alt
chk real_group_inputs_combined_alt_alt at_row_hLamP_alt_alt
chk sizes_sizeKRel szRow_sizeKRel
chk main_theorem_published_inputs_third_alt_alt miStarRow_alt_alt
chk main_theorem_published_inputs_variant_alt_alt miStarRowClosing_alt_alt
chk main_theorem_published_results_final_alt_alt miStar_row_alt_alt
chk main_theorem_from_published_results_alt_alt_alt_alt_alt miAt_of_truePack_alt_alt
chk main_theorem_from_published_results_alt_alt_alt_alt miStar2_of_allTrue_alt_alt
