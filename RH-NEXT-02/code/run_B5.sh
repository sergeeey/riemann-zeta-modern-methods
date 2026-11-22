#!/usr/bin/env bash
# Variant B5: 20 fundamental discriminants x c in {79, 53} x N in {64, 48}.  Run from RH-NEXT-02/code.
# 10 parallel jobs; heaviest cells first (N = 64, c = 79).  stderr goes to a file.
set -u
OUT=../results/parity_B5.jsonl
ERR=../results/parity_B5.err
: > "$OUT"; : > "$ERR"
for spec in "79 64 300" "53 64 250" "79 48 200" "53 48 200"; do
  set -- $spec
  c=$1; N=$2; DPS=$3
  printf '%s\n' -3 -4 -7 -8 -11 -15 -19 -20 -23 -24 5 8 12 13 17 21 24 28 29 33 \
    | xargs -P 10 -I{} sh -c "python parity2.py {} $c $N $DPS 2000 2>>$ERR | grep '^{' >> $OUT"
  echo "finished c=$c N=$N: $(wc -l < "$OUT") cells so far"
done
echo "done: $(wc -l < "$OUT") cells"
