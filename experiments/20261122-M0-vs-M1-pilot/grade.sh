#!/usr/bin/env bash
# usage: grade.sh <task.lean> <solution.lean>  -> prints PASS or FAIL:<reason>
# PASS = statement prefix identical to the task, compiles, no sorry/axiom tricks,
# #print axioms shows only propext / Classical.choice / Quot.sound.
task="$1"; sol="$2"
[ -f "$sol" ] || { echo "FAIL:no_file"; exit 1; }
name=$(grep -o '^theorem T[0-9]*' "$task" | awk '{print $2}')
# defs = everything before the theorem line; must open the solution unchanged.
# The exact theorem statement line must appear as a whole line. Helper lemmas may sit between.
tl=$(grep -n '^theorem T' "$task" | head -1 | cut -d: -f1)
defs=$(head -n $((tl-1)) "$task")
solhead=$(head -n $((tl-1)) "$sol")
[ "$defs" == "$solhead" ] || { echo "FAIL:definitions_modified"; exit 1; }
stmt=$(sed -n "${tl}p" "$task")
grep -qxF "$stmt" "$sol" || { echo "FAIL:statement_modified"; exit 1; }
if grep -n -E '\b(sorry|admit|native_decide|unsafe|implemented_by|extern|axiom|opaque|macro|elab|syntax|set_option|open Lean)\b' "$sol" >/dev/null; then
  echo "FAIL:forbidden_token"; exit 1; fi
tmp=$(mktemp --suffix=.lean)
cp "$sol" "$tmp"; printf '\n#print axioms %s\n' "$name" >> "$tmp"
out=$(timeout 120 lean "$tmp" 2>&1); rc=$?
rm -f "$tmp"
[ $rc -eq 0 ] || { echo "FAIL:compile:$(echo "$out" | head -2 | tr '\n' ' ')"; exit 1; }
echo "$out" | grep -q 'sorryAx' && { echo "FAIL:sorryAx"; exit 1; }
if ! echo "$out" | grep -q "does not depend on any axioms"; then
  lst=$(echo "$out" | grep -o '\[[^]]*\]' | tr -d '[],' | tr ' ' '
' | grep -v -E '^(propext|Classical.choice|Quot.sound|)$')
  [ -z "$lst" ] || { echo "FAIL:axioms:$lst"; exit 1; }
fi
echo PASS
