"""B-02: numerical check of Bettin-Conrey-Farmer Theorem 1 (arXiv:1211.5191).

V_N(s) = sum_{n=1}^N (1 - log(n)/log(N)) * mu(n) / n^s
I_N = (1/2pi) * integral_{-inf}^{inf} |1 - V_N(1/2+it)|^2 / (1/4+t^2) dt
Claim (RH-conditional, from the paper): I_N * log(N) -> C = 2 + gamma - log(4*pi)
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


def compute_I_N(n_max, mu, t_cutoff=400, verbose_label=None):
    V_N = make_V_N(n_max, mu)
    # even integrand in t (|1-V_N(1/2+it)|^2 is even in t since mu real, V_N(1/2-it)=conj(V_N(1/2+it)))
    val = mp.quad(lambda t: integrand(V_N, t), [0, 5, 20, 50, 100, t_cutoff])
    I_N = val / mp.pi  # 2 * (1/2pi) * integral_0^inf = (1/pi) * integral_0^inf
    if verbose_label:
        print(f"{verbose_label}: I_N = {mp.nstr(I_N, 10)}")
    return I_N


def main():
    C = 2 + mp.euler - mp.log(4 * mp.pi)
    print(f"Target constant C = 2 + gamma - log(4*pi) = {mp.nstr(C, 15)}")
    print()

    N_values = [10, 30, 100, 300, 1000]
    mu = mu_table(max(N_values))

    print(f"{'N':>6} {'I_N':>14} {'I_N*log(N)':>14} {'ratio to C':>12}")
    results = []
    for N in N_values:
        I_N = compute_I_N(N, mu)
        product = I_N * mp.log(N)
        ratio = product / C
        results.append((N, I_N, product, ratio))
        print(f"{N:>6} {mp.nstr(I_N, 8):>14} {mp.nstr(product, 8):>14} {mp.nstr(ratio, 8):>12}")

    print()
    print("Negative control: V_N = 0 (i.e. 'do nothing' polynomial), should give I_N = 1")
    print("(analytically: (1/2pi) * integral_R dt/(1/4+t^2) = (1/2pi) * 2pi = 1)")

    def V_zero(s):
        return mp.mpc(0)

    val = mp.quad(
        lambda t: (abs(1 - V_zero(mp.mpc(0.5, t))) ** 2) / (mp.mpf("0.25") + t**2),
        [0, 5, 20, 50, 100, 400],
    )
    I_zero = val / mp.pi
    print(
        f"I_N (V=0, negative control) = {mp.nstr(I_zero, 10)} (expect: does not shrink with N, unlike V_N)"
    )

    print()
    trend = (
        "DECREASING (matches theory)"
        if all(results[i][1] > results[i + 1][1] for i in range(len(results) - 1))
        else "NOT MONOTONE (investigate)"
    )
    ratio_trend = [mp.nstr(r[3], 6) for r in results]
    print(f"I_N trend: {trend}")
    print(f"ratio I_N*log(N)/C across N: {ratio_trend}")
    verdict = (
        "CONFIRMED (ratio approaching 1)"
        if abs(results[-1][3] - 1) < abs(results[0][3] - 1)
        else "FALSIFIED-or-slow-convergence"
    )
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
