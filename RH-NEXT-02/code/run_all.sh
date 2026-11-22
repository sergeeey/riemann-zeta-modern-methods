#!/usr/bin/env bash
# Reproduces every number quoted in RH-NEXT-02/results.md.  Run from this directory (RH-NEXT-02/code).
# Needs: python 3.13, mpmath 1.3, python-flint 0.9.  Time on the author's machine: roughly 15-20 minutes.
set -u
LOG=../results/run_all.log
: > "$LOG"
run() { echo "### $*" | tee -a "$LOG"; "$@" 2>&1 | grep -v -i warn | tee -a "$LOG"; }
run python chi3_ref.py                                 # independent reference: first zero of L(s,chi_3)
run python cvs_u.py zeta 13 16 40                      # calibration, mpmath builder, zeta (gamma_1 to ~30 digits)
run python cvs_u.py chi3 23 16 40                      # calibration, mpmath builder, chi3
for a in "chi3 13 16 500" "chi3 23 16 500" "chi3 23 50 1500" "chi3 29 50 1500" "chi3 37 20 700"; do run python cert_chi.py $a; done
run python cert_chi.py chi3 13 6 300 --compare         # closed forms vs independent mpmath quadrature
run python dh_check.py                                 # DH function: functional equation, off-line zero, Lambda_D
run python id_test.py chi3 13 120                      # Weil identity calibration: ratio = 1/L
run python id_test.py chi3 37 120
run python id_test.py dh 13 120
run python id_test.py dh 37 120
run python dh_scan.py dh 120 13 29 30 31 32 36 37 113 523 1009 2003
run python dh_scan.py chi3 120 113 523 1009 2003       # controls (expected n_neg = 0)
run python dh_scan.py chi4 120 113 523
for n in 40 60 80 100 150; do run python dh_scan.py dh $n 113; done
run python dh_vec.py 113 60                            # where the negative direction lives (spectral weight by height)
run python selfcheck.py                                # independent checks requested by the code review (tau-form, inertia, Lambda_D, arb radius)
