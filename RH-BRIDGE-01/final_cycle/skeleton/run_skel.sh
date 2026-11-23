#!/bin/bash
# usage: bash run_skel.sh   (WSL; 1 core, nice 19; ~3-6 min)
D="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/h12/work
nice -n 19 python3 -I "$D/skel_graph.py" "$D/skeleton_result.json" ~/h12/work/skel_dom.pkl > "$D/skeleton_run.log" 2>&1
echo "exit $?" >> "$D/skeleton_run.log"
