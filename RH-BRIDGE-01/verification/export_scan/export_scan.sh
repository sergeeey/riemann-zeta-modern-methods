#!/usr/bin/env bash
# Stream the published export (math.mit.edu/~drew/grh/solution.ndjson.zst, 7,699,933,588 bytes, unpacked 61,570,595,788 bytes) through zstd and
# count name components of selected declarations.  lean4export emits a name only when an exported (reachable) constant needs it, so presence of a
# component string is evidence that a constant with that name is in the dependency closure of the five theorems.  Nothing is stored on disk.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
URL="https://math.mit.edu/~drew/grh/solution.ndjson.zst"
PAT='SizeKRel|szRow_sizeKRel|sizes_sizeKRel|SizesAt|SizeN|SizeM|SizeK|SizeT|f_mul_m_le|MIstar2|MIid|MIUnit2|AuNZ|MIDat|miStar2_of_anchored|miStar2_of_families|miStar2_of_allTrue|miStar2_of_allTrue_alt_alt|joint_star_product_nonvanishing|isometric_periods_of_unit_hypotheses|exists_zeta_pairing_factors_through_periods|RowMultiplicityCondition|RowsAtSelAlt|IndefiniteRealisationConstantBounds|wire4F_alt|wire_sel_alt|open0_of_unitary_group_hypotheses|published_results_eigen|zeroFree_of_rpow_window|lemmaL|windowHyp_of_rpow|harishChandraFinite|OpenParameterStatements|allRows_of_open0_alt|row_rRows_of_parts_alt|row_rRows_stage0_alt|ElevenLe|szTh|rankBudget|CountsIrreducibilityConstants|Win_at|RamRank_at|ChCode_at|ramShare_at_of|frame_at_of|DesignS'
START=$(date +%s)
echo "start $(date -u +%FT%TZ)" > "$D/export_scan.log"
curl -sS -L --retry 5 --retry-delay 10 "$URL" \
  | zstd -d --long=30 -c \
  | grep -a -o -E "\"str\":\"($PAT)\"" \
  | sort | uniq -c | sort -rn > "$D/export_scan.out"
RC=("${PIPESTATUS[@]}")
echo "pipe status: ${RC[*]}  elapsed $(( $(date +%s) - START )) s  finished $(date -u +%FT%TZ)" >> "$D/export_scan.log"
