#!/bin/bash
# Manual check of the bypass  galoisLocalGlobalStrong_recParameter > recT > recX > recS > designS > szRow_numAt
cd ~/h12/rh/src || exit 1
echo "== files naming designS (word):"; grep -rlw --include=*.lean designS . | head
echo "== declarations of designS / recS / recX / recT:"
grep -rnE --include=*.lean "^[ ]*(theorem|def|abbrev|structure|lemma|noncomputable def)[ ]+[^ ]*\b(designS|recS|recX|recT)\b" . | cut -c1-210
echo "== galoisLocalGlobalStrong_recParameter body:"
cat Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/RowSrc.lean | cut -c1-260
echo "== uses of designS in file(s):"
for f in $(grep -rlw --include=*.lean designS . | head -4); do echo "-- $f"; grep -nw designS "$f" | cut -c1-230 | head -5; done
