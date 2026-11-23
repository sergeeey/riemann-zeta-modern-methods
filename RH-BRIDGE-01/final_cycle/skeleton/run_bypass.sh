#!/bin/bash
D="$(cd "$(dirname "$0")" && pwd)"
nice -n 19 python3 -I "$D/skel_bypass.py" > "$D/bypass_run.log" 2>&1
echo "exit $?" >> "$D/bypass_run.log"
