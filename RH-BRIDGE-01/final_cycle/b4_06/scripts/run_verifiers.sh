#!/bin/bash
SRC="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/unpacked"
W="$HOME/h12/b4_06/verif"; rm -rf "$W"; mkdir -p "$W"; cp -r "$SRC"/. "$W"/
LOG="$HOME/h12/b4_06/logs/python_verifiers.log"; : > "$LOG"
run(){ d="$1"; f="$2"; echo "=== $d/$f ($(date -u +%FT%TZ))" | tee -a "$LOG"
  ( cd "$W/$d" && timeout 900 python3 -I "$f" ) >> "$LOG" 2>&1; echo "EXIT=$?" | tee -a "$LOG"; }
python3 --version | tee -a "$LOG"
run H12-PADIC-B4-06 verify.py
run H12-B4-06-LEAN-STEP2-4/verification exact_test.py
run H12-B4-06-ARITHMETIC-GATE-02/verification check_index_gate.py
run H12-B4-06-FROBENIUS-03 check_frobenius.py
run H12-B4-06-FROBENIUS-04 check_truncated_frobenius.py
tail -c 3000 "$LOG"
