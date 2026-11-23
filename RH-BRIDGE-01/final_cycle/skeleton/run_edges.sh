#!/bin/bash
D="$(cd "$(dirname "$0")" && pwd)"
python3 -I "$D/edge_lines.py"
