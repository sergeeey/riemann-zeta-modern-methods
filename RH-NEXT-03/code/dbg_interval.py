import cert_chi as cc
from flint import arb, ctx

prec, N = 1500, 16
ctx.prec = prec
for k in (60, 30, 10, 3):
    w = arb(10) ** (-k)
    mid = (arb(23) + w / 2).str(40 + k, radius=False)
    rad = (w / 2).str(10, radius=False)
    cb = arb(mid, rad)
    A, DIM, K = cc.build_arb("chi3", 23, N, prec, c_arb=(mid, rad))
    r_entry = max(float(A[i][j].rad()) for i in range(DIM) for j in range(DIM))
    npos, nneg, und, piv = cc.ldlt_inertia(A, DIM)
    print(
        f"k={k}: mid={mid[:30]}.. rad={rad}  c-ball={cb}  max entry rad (float)={r_entry:.2e}  -> n_pos={npos} n_neg={nneg} und={und}"
    )
    if und is not None:
        print(
            "   failing pivot ball:",
            piv[-1].str(8) if piv else None,
            " last good pivots:",
            [p.str(5) for p in piv[-3:]],
        )
# control: the same call with a point string
A, DIM, K = cc.build_arb("chi3", 23, N, prec, c_arb="23")
print("point '23':", cc.ldlt_inertia(A, DIM)[:3])
A, DIM, K = cc.build_arb("chi3", 23, N, prec, c_arb=("23", "0"))
print("tuple ('23','0'):", cc.ldlt_inertia(A, DIM)[:3])
