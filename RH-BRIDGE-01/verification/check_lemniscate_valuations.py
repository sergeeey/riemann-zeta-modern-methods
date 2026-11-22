"""EXACT_COMPUTED check of the lemniscate numbers in zeta-paper.pdf, Part II sec. 6.3, (II.32)-(II.34), p. 40.

s(z) = inverse of t -> int_0^t (1-u^4)^(-1/2) du, A_j = s^(j)(0); s'' = -2 s^3 with s(0) = 0, s'(0) = 1.
Exponential generating function s = sum A_j z^j / j!.  Integer recursion (II.33): A_{j+2} = -2 sum_{a+b+c=j} j!/(a! b! c!) A_a A_b A_c.
Claims checked: A_5 = -12, A_9 = 3024, A_17 = 21224560896 = 2^8 3^6 7^2 11 211, p-adic valuations of A_17 at 3, 7, 11 are (6, 2, 1),
valuations at j = 201 for p = 3, 7 are (75, 29); only j = 1 mod 4 are nonzero.  Also the inequality of the model in sec. 2: for each prime p = 3 mod 4 the
valuation of A_j is compared with j (1/p + 1/p^3 + ...) (the PDF says this is the model prediction, not a theorem for A_j).
Run: python -I check_lemniscate_valuations.py
"""

import sys
from math import comb

sys.stdout.reconfigure(encoding="utf-8")

N = 205
A = [0] * (N + 1)
A[1] = 1
S2 = [0] * (N + 1)  # coefficients of s^2 in the sense sum_{a+b=n} C(n,a) A_a A_b
S3 = [0] * (N + 1)  # sum_{a+b=n} C(n,a) A_a S2_b
# s'' = -2 s^3  =>  A_{n+2} = -2 * S3[n]
for n in range(0, N - 1):
    S2[n] = sum(comb(n, a) * A[a] * A[n - a] for a in range(n + 1))
    S3[n] = sum(comb(n, a) * A[a] * S2[n - a] for a in range(n + 1))
    A[n + 2] = -2 * S3[n]


def vp(n, p):
    if n == 0:
        return None
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def factor_small(n):
    f, d = {}, 2
    n = abs(n)
    while d * d <= n and d < 10**6:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


print("A_1, A_5, A_9, A_13:", A[1], A[5], A[9], A[13])
print("A_5 == -12:", A[5] == -12, "| A_9 == 3024:", A[9] == 3024)
print(
    "A_17 =",
    A[17],
    "| == 21224560896:",
    A[17] == 21224560896,
    "| factorisation:",
    factor_small(A[17]),
)
print(
    "nonzero only for j = 1 mod 4 (j <= 201):",
    all((A[j] == 0) == (j % 4 != 1) for j in range(0, 202)),
)
print("valuations of A_17 at 3, 7, 11:", [vp(A[17], p) for p in (3, 7, 11)], "(PDF: 6, 2, 1)")
print("valuations of A_201 at 3, 7:", [vp(A[201], p) for p in (3, 7)], "(PDF: 75, 29)")
print("valuation of A_17 at split primes 5, 13:", [vp(A[17], p) for p in (5, 13)], "(PDF: 0, 0)")
for p in (3, 7, 11):
    model = lambda j: j * sum(1 / p ** (2 * i + 1) for i in range(0, 40))  # noqa: E731
    rows = [(j, vp(A[j], p), round(model(j), 2)) for j in (17, 101, 201) if A[j] != 0 and j <= N]
    print(f"p={p}: (j, v_p(A_j), model j(1/p+1/p^3+...)):", rows)
