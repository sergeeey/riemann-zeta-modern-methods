#!/bin/bash
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
D="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/lean"
W="$HOME/h12/b4_06/final"; rm -rf "$W"; mkdir -p "$W"
cp "$D/B4_06_Universal.lean" "$W/B4_06_Universal.lean"
F="$W/B4_06_Universal.lean"
# extra #print axioms for every lemma in the chain
for t in L1_phi_integral L2_pphi_q L3a_inv_pow_perturb L3b_frobenius_trunc L3c_reduction L3d_trunc_invariance L5_phi_n0_unit B4_06_first_resonance; do
  echo "#print axioms H12.B4.$t" >> "$F"
done
echo "== sha256 (with axioms footer): $(sha256sum "$F" | cut -d' ' -f1)"
echo "== sha256 (merged source as in repo): $(sha256sum "$D/B4_06_Universal.lean" | cut -d' ' -f1)"
echo "== forbidden tokens in code (comments excluded)"
grep -n -E "\bsorry\b|\badmit\b|native_decide|^\s*axiom |\bunsafe\b|implemented_by|extern" "$F" | grep -v -E ":\s*(--|/-|\*)" | grep -v "SKELETON" || echo "none"
echo "== statement of the main theorem"
grep -n -A3 "^theorem B4_06_first_resonance" "$F" | cut -c1-200
cd "$HOME/h12/rh" || exit 1
echo "== compile"
( time lake env lean "$F" ) > "$W/compile.log" 2>&1
echo "EXIT_CODE=$?"
grep -E "error|sorry|depends on axioms|real" "$W/compile.log" | cut -c1-200
cp "$W/compile.log" "$HOME/h12/b4_06/logs/final_compile.log"
