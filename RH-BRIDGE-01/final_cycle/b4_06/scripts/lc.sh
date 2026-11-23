#!/bin/bash
# usage: lc.sh <file.lean>  -- compile one file with the pinned Lean/Mathlib; prints output and exit code
export PATH="$HOME/.elan/bin:/usr/local/bin:/usr/bin:/bin"
cd "$HOME/h12/rh" || exit 1
f="$1"
case "$f" in /*) ;; *) f="$HOME/h12/b4_06/$f";; esac
( time lake env lean "$f" ) 2>&1 | cut -c1-400 | head -${2:-80}
echo "EXIT=${PIPESTATUS[0]}"
