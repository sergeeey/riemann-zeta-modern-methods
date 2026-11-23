#!/bin/bash
# closure verification (new run): hashes, compile, axioms, git state. Appends to closure_verification.log
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
R="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01"
L="$R/final_cycle/closure/closure_verification.log"
mkdir -p "$R/final_cycle/closure"
{
echo "==== closure verification PRE (new run) $(date -u +%FT%TZ)"
echo "git HEAD: $(cd "$R" && git rev-parse --short HEAD) branch: $(cd "$R" && git branch --show-current)"
echo "-- expected hashes (from checkpoint.json) vs actual"
for p in "lean/B4_06_Universal.lean d1de8f15d2f311b334e48b380e052722e80739162d20121599b2b8065d8d5bc7" \
         "lean/L1.lean 9f7db200673e5f327c59511931bf661d54c8ce8b462e61135287ce602d70804f" \
         "lean/L2.lean 941e6c067ee83944c534835e672d061c358e8a3478c75a591ea89657af65c30a" \
         "lean/L3a.lean 380fadb593e96467320dc62aed8f7810ae64e153059d36da94c5271c353b6288" \
         "lean/L3b.lean 6adc5dd4a788c2106483e889bf665caac56a96d159b9a6da44e50acfabeb5c34"; do
  set -- $p
  a=$(sha256sum "$R/final_cycle/b4_06/$1" | cut -d' ' -f1)
  [ "$a" = "$2" ] && echo "OK   $1" || echo "MISMATCH $1 expected=$2 actual=$a"
done
cd "$HOME/h12/rh" || exit 1
echo "-- toolchain: $(lake env lean --version)"
echo "-- compile: lake env lean final_cycle/b4_06/lean/B4_06_Universal.lean (+ axioms footer in temp copy)"
T="$HOME/h12/b4_06/closure_tmp.lean"
cp "$R/final_cycle/b4_06/lean/B4_06_Universal.lean" "$T"
for t in B4_06_first_resonance L1_phi_integral L2_pphi_q L5_phi_n0_unit L3a_inv_pow_perturb L3b_frobenius_trunc L3c_reduction L3d_trunc_invariance; do echo "#print axioms H12.B4.$t" >> "$T"; done
( time lake env lean "$T" ) > "$HOME/h12/b4_06/closure_compile.txt" 2>&1; ec=$?
echo "exit_code=$ec"
grep -E "error|sorry|depends on axioms|real" "$HOME/h12/b4_06/closure_compile.txt" | cut -c1-200
echo "-- forbidden tokens in code of the delivered file"
grep -n -E "\bsorry\b|\badmit\b|native_decide|^\s*axiom |\bunsafe\b" "$R/final_cycle/b4_06/lean/B4_06_Universal.lean" | grep -v -E ":\s*(--|/-)" | grep -v "/-!" || echo "none"
echo "-- python evidence logs present"
tail -1 "$R/final_cycle/b4_06/logs/lagrange_vs_ode.log"
tail -1 "$R/final_cycle/novelty/check_reduction.log"
} >> "$L" 2>&1
cat "$L" | tail -30
