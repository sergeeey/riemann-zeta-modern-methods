"""Diagnostic: is the mp.quad breakpoint scheme resolving oscillation correctly?
Fix N=10 (cheap), compare coarse vs progressively finer breakpoints.
"""

import mpmath as mp
from sympy import mobius

mp.mp.dps = 30


def mu_table(n_max):
    return {n: int(mobius(n)) for n in range(1, n_max + 1)}


def make_V_N(n_max, mu):
    log_N = mp.log(n_max)

    def V_N(s):
        total = mp.mpc(0)
        for n in range(1, n_max + 1):
            m = mu[n]
            if m == 0:
                continue
            weight = 1 - mp.log(n) / log_N
            total += weight * m * mp.e ** (-s * mp.log(n))
        return total

    return V_N


def integrand(V_N, t):
    s = mp.mpc(mp.mpf("0.5"), t)
    val = 1 - V_N(s)
    return (abs(val) ** 2) / (mp.mpf("0.25") + t**2)


def main():
    N = 10
    mu = mu_table(N)
    V_N = make_V_N(N, mu)

    def f(t):
        return integrand(V_N, t)

    schemes = {
        "original (coarse)": [0, 5, 20, 50, 100, 400],
        "linear fine to 400": list(range(0, 401, 2)),
        "linear fine to 1000": list(range(0, 1001, 2)),
        "very fine to 200": [i * 0.5 for i in range(0, 401)],
    }

    for name, pts in schemes.items():
        val = mp.quad(f, pts)
        I_N = val / mp.pi
        print(f"{name:>25}: I_N = {mp.nstr(I_N, 10)}  (n_points={len(pts)}, t_max={pts[-1]})")

    print()
    print("If these disagree significantly, the coarse breakpoint scheme is the bug.")
    print("Also checking tail contribution beyond t=400:")
    tail = mp.quad(f, [400, 1000, 5000])
    print(f"tail integral [400, 5000] = {mp.nstr(tail / mp.pi, 10)}")


if __name__ == "__main__":
    main()
