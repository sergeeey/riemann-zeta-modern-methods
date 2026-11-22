"""Scan the Davenport-Heilbronn Galerkin matrix inertia (cutoff-free interval LDL^T) over c, at fixed N.
Prints certified (n_pos, n_neg) or UNDETERMINED after precision escalation.  Controls: chi3 (RH holds) on the same grid.
Usage: python dh_scan.py <name> <N> c1 c2 ...
"""

import sys
import time

import cert_chi as cc


def certify(name, c, N, prec0=1200, prec_max=9600):
    prec = prec0
    while prec <= prec_max:
        A, DIM, _K = cc.build_arb(name, c, N, prec)
        npos, nneg, und, _piv = cc.ldlt_inertia(A, DIM)
        if und is None:
            return npos, nneg, prec, None
        prec *= 2
    return None, None, prec // 2, und


if __name__ == "__main__":
    name, N = sys.argv[1], int(sys.argv[2])
    for c in [int(x) for x in sys.argv[3:]]:
        t0 = time.time()
        npos, nneg, prec, und = certify(name, c, N)
        if npos is None:
            print(
                f"{name} c={c} N={N}: UNDETERMINED at pivot {und} even with {prec} bits  ({time.time() - t0:.0f}s)",
                flush=True,
            )
        else:
            print(
                f"{name} c={c} N={N} prec={prec}: CERTIFIED n_pos={npos} n_neg={nneg}  ({time.time() - t0:.0f}s)",
                flush=True,
            )
