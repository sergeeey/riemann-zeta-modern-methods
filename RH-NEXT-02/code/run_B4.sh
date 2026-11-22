#!/usr/bin/env bash
# Variant B4: convergence in N.  20 fundamental discriminants x c in {13, 23, 37} x N in {48, 64}.  Run from RH-NEXT-02/code.
# 10 parallel jobs; heaviest cells first (N = 64).  stderr goes to a file.
set -u
OUT=../results/parity_B4.jsonl
ERR=../results/parity_B4.err
: > "$OUT"; : > "$ERR"
for spec in "64 250" "48 160"; do
  set -- $spec
  N=$1; DPS=$2
  for c in 37 23 13; do
    printf '%s\n' -3 -4 -7 -8 -11 -15 -19 -20 -23 -24 5 8 12 13 17 21 24 28 29 33 \
      | xargs -P 10 -I{} sh -c "python parity2.py {} $c $N $DPS 2000 2>>$ERR | grep '^{' >> $OUT"
    echo "finished N=$N c=$c: $(wc -l < "$OUT") cells so far"
  done
done
echo "done: $(wc -l < "$OUT") cells"
