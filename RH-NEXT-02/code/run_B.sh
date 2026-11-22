#!/usr/bin/env bash
# Variant B (parity of the character).  Run from RH-NEXT-02/code.  One background job per character; 20 cells in total.
set -u
OUT=../results/parity_B.jsonl
: > "$OUT"
for ch in chi3 chi4 chim8 chi5 chi8; do
  (
    for c in 13 37; do
      for N in 16 32; do
        python parity.py "$ch" "$c" "$N" 2>/dev/null | grep '^{' >> "$OUT"
      done
    done
  ) &
done
wait
echo "done: $(wc -l < "$OUT") cells"
