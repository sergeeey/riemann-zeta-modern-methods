#!/bin/bash
# closure packaging: manifests, zip, archive verification (verification log goes OUTSIDE the archive)
R="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01"
W="$(dirname "$R")"
S="/mnt/c/Users/serge/AppData/Local/Temp/claude/47ae088cb00845dc/dfd56df9-0116-4660-be80-aa930329e743/scratchpad"
cd "$R" || exit 1
find "$W/RH-BRIDGE-01" "$W/RH-NEXT-01" "$W/RH-NEXT-02" "$W/RH-NEXT-03" -name __pycache__ -prune -exec rm -rf {} \; 2>/dev/null
# 1) historical manifest: refresh only the annotated checkpoint.json line
nh=$(sha256sum checkpoint.json | cut -d' ' -f1)
sed -i "s#^[0-9a-f]\{64\} \*checkpoint.json#${nh} *checkpoint.json#" SHA256SUMS.txt
# 2) final_cycle manifest
( cd final_cycle && find . -type f ! -name SHA256SUMS.txt | LC_ALL=C sort | tr '\n' '\0' | xargs -0 sha256sum > SHA256SUMS.txt )
# 3) manifest of the four archived folders (paths from the worktree root)
( cd "$W" && find RH-BRIDGE-01 RH-NEXT-01 RH-NEXT-02 RH-NEXT-03 -type f ! -name H12-FINAL-CYCLE-01-2026-11-23.zip ! -name SHA256SUMS-ALL.txt ! -name closure_archive_verification.log | LC_ALL=C sort | tr '\n' '\0' | xargs -0 sha256sum > RH-BRIDGE-01/SHA256SUMS-ALL.txt )
# 4) archive
python3 -I "$S/mkzip.py" "$R" > "$HOME/mkzip.out" 2>&1; cat "$HOME/mkzip.out"
# 5) verify the archive
V="$R/closure_archive_verification.log"
{
echo "==== archive verification $(date -u +%FT%TZ)"
echo "archive: $(cd "$R" && sha256sum H12-FINAL-CYCLE-01-2026-11-23.zip)"
echo "mkzip: $(tr '\n' ' ' < "$HOME/mkzip.out")"
T=$(mktemp -d)
python3 -I - "$R" "$T" <<'PY'
import sys, zipfile
z = zipfile.ZipFile(sys.argv[1] + "/H12-FINAL-CYCLE-01-2026-11-23.zip"); z.extractall(sys.argv[2]); print("extracted entries:", len(z.namelist()))
PY
echo "-- extracted: sha256sum -c RH-BRIDGE-01/SHA256SUMS-ALL.txt (from the archive root)"
( cd "$T" && sha256sum -c RH-BRIDGE-01/SHA256SUMS-ALL.txt 2>&1 | grep -v ": OK$" | head -5; echo "manifest lines: $(wc -l < RH-BRIDGE-01/SHA256SUMS-ALL.txt); lines above = failures (none if empty)" )
echo "-- extracted: final_cycle manifest"
( cd "$T/RH-BRIDGE-01/final_cycle" && sha256sum -c SHA256SUMS.txt 2>&1 | grep -v ": OK$" | head -5; echo "manifest lines: $(wc -l < SHA256SUMS.txt)" )
echo "-- extracted: historical manifest (SHA256SUMS.txt)"
( cd "$T/RH-BRIDGE-01" && sha256sum -c SHA256SUMS.txt 2>&1 | grep -v ": OK$" | head -5; echo "manifest lines: $(wc -l < SHA256SUMS.txt)" )
echo "-- archive vs working tree (byte compare)"
d=0; while IFS= read -r f; do cmp -s "$T/$f" "$W/$f" || { echo "DIFF $f"; d=$((d+1)); }; done < <(cd "$T" && find . -type f | sed 's#^\./##' | LC_ALL=C sort)
echo "files differing: $d"
echo "-- working tree: sha256sum -c RH-BRIDGE-01/SHA256SUMS-ALL.txt"
( cd "$W" && sha256sum -c RH-BRIDGE-01/SHA256SUMS-ALL.txt 2>&1 | grep -v ": OK$" | head -5; echo "done" )
rm -rf "$T"
} > "$V" 2>&1
cat "$V"
