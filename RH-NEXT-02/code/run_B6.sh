#!/usr/bin/env bash
# Variant B6: N = 96 for the small-conductor characters (14 cells, all in parallel; ~28 GB RAM was free when this was designed).
# Run from RH-NEXT-02/code.  Per-cell time limit 3600 s.  stderr goes to a file.
set -u
OUT=../results/parity_B6.jsonl
ERR=../results/parity_B6.err
: > "$OUT"; : > "$ERR"
{
  for D in -3 -4; do echo "$D 37 250"; done
  for c in 53 79; do
    dps=300; [ "$c" = 79 ] && dps=400
    for D in -3 -4 5 -7 -8 8; do echo "$D $c $dps"; done
  done
} | xargs -P 14 -L 1 sh -c "timeout 3600 python parity2.py \$0 \$1 96 \$2 2000 2>>$ERR | grep '^{' >> $OUT"
echo "done: $(wc -l < "$OUT") of 14 cells"
