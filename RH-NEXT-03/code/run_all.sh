#!/usr/bin/env bash
# Reproduces every number quoted in RH-NEXT-03/result.md.  Run from RH-NEXT-03/code.
# Needs: python 3.13, mpmath 1.3, python-flint 0.9, numpy, scipy.  Time: about 3-5 minutes.  Timings vary +-40% with machine load.
set -u
LOG=../results/run_all.log
: > "$LOG"
run() { echo "### $*" | tee -a "$LOG"; "$@" 2>&1 | grep -v -i warn | tee -a "$LOG"; }
run python cont_bench.py A      # threshold: continuity of Q(L) and the rank-one derivative jump
run python cont_bench.py B      # singular values of Q(23.5) - Q(23.0): full numerical rank
run python cont_bench.py C      # lambda_min, d ln lambda_min / dL, Weyl step
run python cont_bench.py D      # widest c-interval certifiable by ONE interval LDL^T
run python cont_bench.py E      # certified bisection vs bracketed tracking + 2 certificates (DH, N=60)
run python dbg_interval.py      # diagnosis of the first (wrong) reading of experiment D
