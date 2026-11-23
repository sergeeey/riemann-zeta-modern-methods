#!/bin/bash
D="$(cd "$(dirname "$0")" && pwd)"
nice -n 19 python3 -I "$D/tree_children.py" > "$D/tree_children.out" 2>&1
