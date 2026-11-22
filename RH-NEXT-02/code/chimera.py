"""EXPLORATORY (not pre-registered) diagnostic for variant B: which part drives lambda_min, the archimedean kernel (a = 1/4 or 3/4)
or the prime weights chi(p)?  "Chimera" matrices combine the kernel of one parity with the weights of the other character.
They are NOT the Weil form of any L-function (no explicit formula holds), so only conditioning is interpreted, never the inertia as a statement about zeros.
Usage: python chimera.py <c> <N>
"""

import sys

import cert_chi as cc
import mpmath as mp

cc.CHARS["chi8_oddk"] = (1, 8, cc.CHARS["chi8"][2])  # chi8 weights, odd (a=3/4) kernel
cc.CHARS["chim8_evenk"] = (0, 8, cc.CHARS["chim8"][2])  # chim8 weights, even (a=1/4) kernel


def lam_min(name, c, N):
    A, DIM, _ = cc.build_arb(name, c, N, 2000)
    npos, nneg, und, _ = cc.ldlt_inertia(A, DIM)
    mp.mp.dps = 100
    M = mp.matrix(DIM, DIM)
    for i in range(DIM):
        for j in range(DIM):
            M[i, j] = mp.mpf(A[i][j].mid().str(120, radius=False))
    E = mp.eigsy(M, eigvals_only=True)
    return mp.nstr(min(E), 5), (npos, nneg, und)


if __name__ == "__main__":
    c, N = int(sys.argv[1]), int(sys.argv[2])
    for name, desc in (
        ("chi8", "even weights, even kernel (true chi8)"),
        ("chi8_oddk", "even weights, ODD kernel (chimera)"),
        ("chim8", "odd weights, odd kernel (true chi_-8)"),
        ("chim8_evenk", "odd weights, EVEN kernel (chimera)"),
    ):
        lam, inertia = lam_min(name, c, N)
        print(
            f"c={c} N={N} {name:12s} {desc:40s} lambda_min = {lam:>12s}  inertia={inertia}",
            flush=True,
        )
