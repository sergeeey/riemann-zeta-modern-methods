#!/bin/bash
# Compile each B4-06 Lean candidate separately; log versions, command, exit code, full output, #print axioms.
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
SRC="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/unpacked"
W="$HOME/h12/b4_06"; mkdir -p "$W/logs" "$W/src"
cd "$HOME/h12/rh" || exit 1
{
  echo "date: $(date -u +%FT%TZ)"
  echo "toolchain file: $(cat lean-toolchain)"
  lake env lean --version
  echo "mathlib rev (manifest): $(grep -B2 -A8 '"name": "mathlib"' lake-manifest.json | grep '"rev"' | head -1)"
  echo "checkout HEAD: $(git rev-parse HEAD)"
} > "$W/logs/env.txt" 2>&1
cat "$W/logs/env.txt"
declare -A F=(
  [ResonanceParameters]="H12-B4-06-LEAN-STEP2-4/ResonanceParameters.lean"
  [ExceptionalIndexGate]="H12-B4-06-ARITHMETIC-GATE-02/ExceptionalIndexGate.lean"
  [FrobeniusResidueInterface]="H12-B4-06-FROBENIUS-03/FrobeniusResidueInterface.lean"
  [FrobeniusNilpotent]="H12-B4-06-FROBENIUS-04/FrobeniusNilpotent.lean"
)
for n in ResonanceParameters ExceptionalIndexGate FrobeniusResidueInterface FrobeniusNilpotent; do
  cp "$SRC/${F[$n]}" "$W/src/$n.lean"
  sha256sum "$W/src/$n.lean" | tee "$W/logs/$n.sha256"
  echo "--- compile as-is: lake env lean $W/src/$n.lean" | tee "$W/logs/$n.log"
  ( time lake env lean "$W/src/$n.lean" ) >> "$W/logs/$n.log" 2>&1
  echo "EXIT_CODE_AS_IS=$?" | tee -a "$W/logs/$n.log"
done
