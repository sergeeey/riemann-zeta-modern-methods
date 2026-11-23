#!/bin/bash
cd ~/h12/rh/src || exit 1
for n in szRow_numAt szRow_sizesAt sizes_sizeKRel szRow_sizeKRel SizeKRel; do
  echo "== files naming $n:"; grep -rlw --include=*.lean -- "$n" . | sed 's|.*/||'
done
