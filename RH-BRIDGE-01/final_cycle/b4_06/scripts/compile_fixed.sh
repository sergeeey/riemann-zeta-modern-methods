#!/bin/bash
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
W="$HOME/h12/b4_06"; mkdir -p "$W/fixed"
cd "$HOME/h12/rh" || exit 1
declare -A T=(
  [ResonanceParameters]="exceptional_quadratic resonance_decomposition isolated_exceptional_support first_index_lt_prime first_resonance_identity"
  [ExceptionalIndexGate]="resonance_region divisor_mod_four quotient_below_or_exceptional divisor_equals_p_implies_exceptional quotient_upper_bound only_exceptional_divisor_or_small carry_remainder denominator_index_digit"
  [FrobeniusResidueInterface]="normalized_residue_bridge p3_normalized_coefficients"
  [FrobeniusNilpotent]="frobenius_one_add_of_nilpotent frobenius_large_power_of_nilpotent frobenius_inverse_truncation frobenius_step4_interface"
)
for n in ResonanceParameters ExceptionalIndexGate FrobeniusResidueInterface; do
  # only change: move 'import Mathlib' to the first line (Lean requires imports before any other command/doc comment)
  { echo "import Mathlib"; grep -v '^import Mathlib$' "$W/src/$n.lean"; } > "$W/fixed/$n.lean"
done
cp "$W/src/FrobeniusNilpotent.lean" "$W/fixed/FrobeniusNilpotent.lean"
for n in ResonanceParameters ExceptionalIndexGate FrobeniusResidueInterface FrobeniusNilpotent; do
  echo "######## $n"
  sha256sum "$W/fixed/$n.lean" | tee "$W/logs/$n.fixed.sha256"
  diff <(cat "$W/src/$n.lean") <(cat "$W/fixed/$n.lean") > "$W/logs/$n.fix.diff"; echo "diff lines: $(wc -l < "$W/logs/$n.fix.diff")"
  L="$W/logs/$n.fixed.log"
  echo "--- compile: lake env lean $W/fixed/$n.lean" > "$L"
  lake env lean "$W/fixed/$n.lean" >> "$L" 2>&1; echo "EXIT_CODE_FIXED=$?" >> "$L"
  # axioms run: copy + #print axioms
  cp "$W/fixed/$n.lean" "$W/fixed/$n.axioms.lean"
  for t in ${T[$n]}; do echo "#print axioms H12.B4.$t" >> "$W/fixed/$n.axioms.lean"; done
  A="$W/logs/$n.axioms.log"
  echo "--- compile+axioms: lake env lean $W/fixed/$n.axioms.lean" > "$A"
  lake env lean "$W/fixed/$n.axioms.lean" >> "$A" 2>&1; echo "EXIT_CODE_AXIOMS=$?" >> "$A"
  cat "$L"; cat "$A" | cut -c1-240
done
