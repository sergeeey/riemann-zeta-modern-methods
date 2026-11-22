import mpmath as mp

mp.mp.dps = 30
chi3 = [0, 1, -1]  # period-3 character mod 3, odd


def f(t):
    return mp.dirichlet(mp.mpc(0.5, t), chi3)


# locate first zero of L(1/2+it, chi_3): scan |L| for a minimum, then solve for a complex root
ts = [mp.mpf(i) / 50 for i in range(100, 700)]
vals = [abs(f(t)) for t in ts]
cand = [
    ts[i]
    for i in range(1, len(ts) - 1)
    if vals[i] < vals[i - 1] and vals[i] < vals[i + 1] and vals[i] < 0.2
]
print("candidates (local minima of |L| < 0.2) for t in [2,14]:", [mp.nstr(x, 5) for x in cand])
z = mp.findroot(lambda s: mp.dirichlet(s, chi3), mp.mpc(0.5, cand[0]))
print("first zero of L(s,chi_3):", mp.nstr(z, 25))
