"""Exact check (Fractions): Lagrange formula (1) used in Lean (`lagA`) == ODE recurrence for wp coefficients a_n,
for c = 1, n = 1..N.  NUMERICALLY_CHECKED link only (this is the link NOT formalized in Lean).
a_n(ODE) = (6*sum_{1<=j<n} a_j a_{n-j} - 2*[n=1]) / ((4n+1)(4n-6))   (from H12-PADIC-B4-06-PROOF.md Step 1)
a_n(Lagrange) = -1/(2n-1) * [u^n] Phi(u)^{-(4n-2)},  Phi = sum phi_j u^j,  phi_j = C(2j,j)/(4^j (4j+1)).
"""

from fractions import Fraction as Fr
from math import comb
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40


def mul(a, b, n):
    out = [Fr(0)] * (n + 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if i + j > n:
                break
            out[i + j] += x * y
    return out


def inv(a, n):
    out = [Fr(0)] * (n + 1)
    out[0] = 1 / a[0]
    for k in range(1, n + 1):
        s = sum(a[i] * out[k - i] for i in range(1, min(k, len(a) - 1) + 1))
        out[k] = -s / a[0]
    return out


def power(a, e, n):
    res = [Fr(1)] + [Fr(0)] * n
    base = a[: n + 1] + [Fr(0)] * (n + 1 - len(a))
    while e:
        if e & 1:
            res = mul(res, base, n)
        base = mul(base, base, n)
        e >>= 1
    return res


phi = [Fr(comb(2 * j, j), 4**j * (4 * j + 1)) for j in range(N + 2)]
ode = {}
for n in range(1, N + 1):
    s = sum((ode[j] * ode[n - j] for j in range(1, n)), Fr(0))
    ode[n] = Fr(6 * s - (2 if n == 1 else 0)) / ((4 * n + 1) * (4 * n - 6))
bad = 0
for n in range(1, N + 1):
    inv_phi = inv(phi, n)
    lag = -Fr(1, 2 * n - 1) * power(inv_phi, 4 * n - 2, n)[n]
    if lag != ode[n]:
        bad += 1
        print("MISMATCH n =", n, lag, ode[n])
print(f"checked n=1..{N}: mismatches = {bad}; a_1={ode[1]}, a_2={ode[2]}")
