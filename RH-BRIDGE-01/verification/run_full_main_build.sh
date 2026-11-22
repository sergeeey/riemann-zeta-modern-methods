#!/usr/bin/env bash
# STATUS: NOT_RUN.  Full kernel build of the pinned Lean mirror and the axiom audit.  Run inside WSL2/Linux (the Windows path limit is exceeded: max relative path 239 chars).
# Environment used for the partial builds in this mission: WSL2 Ubuntu, 8 cores, 23 GB RAM, Lean v4.33.1 (elan 4.4.0), Mathlib 0df444a360eaa60ab8c11dca51a86af692955474, checkout ~/h12/rh at 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
# Closure of Main: 174,764 of 175,187 modules, 17,329,808 lines (text-level import closure, computed in this mission).  See research_decision.md for the extrapolated cost.
set -u
export PATH="$HOME/.elan/bin:$PATH"
cd "$HOME/h12/rh" || exit 1
git rev-parse HEAD | grep -q 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4 || { echo "wrong commit"; exit 2; }
L="$HOME/h12/logs"; mkdir -p "$L"
( while true; do echo "$(date '+%F %T') $(free -m | awk 'NR==2{print "used_MB="$3" avail_MB="$7}')"; sleep 300; done ) > "$L/build_main.mem" 2>&1 &
MON=$!
/usr/bin/time -v lake build Main > "$L/build_main.log" 2> "$L/build_main.time"
RC=$?
kill $MON 2>/dev/null
echo "lake build Main exit=$RC"
[ "$RC" -eq 0 ] || exit "$RC"
# copy RH-BRIDGE-01/verification/CheckAxioms.lean into ~/h12/rh before running this script
[ -f CheckAxioms.lean ] || { echo "CheckAxioms.lean missing in the project root"; exit 3; }
lake env lean CheckAxioms.lean | tee "$L/check_axioms_main.out"
# optional independent replay of the compiled environment (https://github.com/leanprover/lean4checker, pin the version matching v4.33.1)
