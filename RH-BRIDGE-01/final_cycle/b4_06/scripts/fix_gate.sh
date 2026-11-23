#!/bin/bash
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
W="$HOME/h12/b4_06"; cd "$HOME/h12/rh" || exit 1
n=ExceptionalIndexGate
# only change: strengthen the auxiliary fact (0 < p  ->  3 <= p) used by nlinarith
sed 's/  have hp : 0 < p r := by simp \[p\]/  have hp : 3 ≤ p r := by dsimp [p]; omega/' "$W/fixed/$n.lean" > "$W/fixed/$n.v2.lean"
diff "$W/fixed/$n.lean" "$W/fixed/$n.v2.lean" > "$W/logs/$n.v2.diff"; cat "$W/logs/$n.v2.diff"
sha256sum "$W/fixed/$n.v2.lean" | tee "$W/logs/$n.v2.sha256"
L="$W/logs/$n.v2.log"
echo "--- compile: lake env lean $W/fixed/$n.v2.lean" > "$L"
lake env lean "$W/fixed/$n.v2.lean" >> "$L" 2>&1; echo "EXIT_CODE_V2=$?" >> "$L"
cp "$W/fixed/$n.v2.lean" "$W/fixed/$n.v2.axioms.lean"
for t in resonance_region divisor_mod_four quotient_below_or_exceptional divisor_equals_p_implies_exceptional quotient_upper_bound only_exceptional_divisor_or_small carry_remainder denominator_index_digit; do
  echo "#print axioms H12.B4.$t" >> "$W/fixed/$n.v2.axioms.lean"; done
A="$W/logs/$n.v2.axioms.log"
echo "--- compile+axioms: lake env lean $W/fixed/$n.v2.axioms.lean" > "$A"
lake env lean "$W/fixed/$n.v2.axioms.lean" >> "$A" 2>&1; echo "EXIT_CODE_V2_AXIOMS=$?" >> "$A"
cat "$L"; cut -c1-240 "$A"
