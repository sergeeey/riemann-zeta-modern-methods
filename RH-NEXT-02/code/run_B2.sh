#!/usr/bin/env bash
# Variant B2: 20 fundamental discriminants x c in {13, 37}, N = 16.  Run from RH-NEXT-02/code.  10 parallel jobs.
set -u
OUT=../results/parity_B2.jsonl
: > "$OUT"; : > ../results/parity_B2.err
for c in 13 37; do
  printf '%s\n' -3 -4 -7 -8 -11 -15 -19 -20 -23 -24 5 8 12 13 17 21 24 28 29 33 \
    | xargs -P 10 -I{} sh -c "python parity2.py {} $c 16 2>>../results/parity_B2.err | grep '^{' >> $OUT"
done
echo "done: $(wc -l < "$OUT") cells"
