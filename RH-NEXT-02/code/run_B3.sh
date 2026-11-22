#!/usr/bin/env bash
# Variant B3: 20 fundamental discriminants x (c, N) in {(13,32), (37,32), (23,16), (23,32)}.  Run from RH-NEXT-02/code.
# 10 parallel jobs.  stderr goes to a file (the first B2 run lost its diagnostics to /dev/null).
set -u
OUT=../results/parity_B3.jsonl
: > "$OUT"; : > ../results/parity_B3.err
for cell in "13 32" "37 32" "23 16" "23 32"; do
  set -- $cell
  c=$1; N=$2
  printf '%s\n' -3 -4 -7 -8 -11 -15 -19 -20 -23 -24 5 8 12 13 17 21 24 28 29 33 \
    | xargs -P 10 -I{} sh -c "python parity2.py {} $c $N 2>>../results/parity_B3.err | grep '^{' >> $OUT"
  echo "finished c=$c N=$N: $(wc -l < "$OUT") cells so far"
done
echo "done: $(wc -l < "$OUT") cells"
