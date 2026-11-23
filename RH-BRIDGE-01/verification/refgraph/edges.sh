#!/bin/bash
cd ~/h12/rh/src || exit 1
chk(){ f=$(grep -rlw --include=*.lean -E "(theorem|def|lemma|abbrev|structure) [^ ]*\b$1\b" . | head -1); echo "== $1 defined in $f"; awk -v n="$1" -v t="$2" 'BEGIN{p=0} $0 ~ "(theorem|def|lemma|abbrev|structure) [^ ]*"n"([ :]|$)"{p=1;next} p && /^(theorem|def|lemma|abbrev|structure|end )/{p=0} p && index($0,t){print "   uses " t ": " substr($0,1,160); exit}' "$f"; }
chk at_row_hLamP_alt_alt evP_params
chk evP_params szRow_numAt
chk szRow_numAt szRow_sizesAt
chk szRow_sizesAt sizes_sizeKRel
chk sizes_sizeKRel szRow_sizeKRel
chk real_group_inputs_combined_alt_alt at_row_hLamP_alt_alt
