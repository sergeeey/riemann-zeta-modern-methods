from fractions import Fraction as Fr
from math import comb


def phi(j):
    return Fr(comb(2 * j, j), 4**j * (4 * j + 1))


def mul(a, b, N):
    c = [Fr(0)] * (N + 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j in range(N + 1 - i):
            c[i + j] += x * b[j]
    return c


def inv(a, N):
    b = [Fr(0)] * (N + 1)
    b[0] = 1 / a[0]
    for n in range(1, N + 1):
        s = sum(a[k] * b[n - k] for k in range(1, n + 1))
        b[n] = -s / a[0]
    return b


def powr(a, e, N):
    r = [Fr(0)] * (N + 1)
    r[0] = Fr(1)
    base = a[:]
    while e:
        if e & 1:
            r = mul(r, base, N)
        base = mul(base, base, N)
        e >>= 1
    return r


def lagA(n, N):
    Phi = [phi(j) for j in range(N + 1)]
    G = inv(Phi, N)
    M = 4 * n - 2 if 4 * n >= 2 else 0  # Lean nat subtraction
    c = powr(G, M, N)[n]
    return -(Fr(1) / (2 * n - 1)) * c


def vp(x, p):
    if x == 0:
        return 10**9
    v = 0
    num, den = x.numerator, x.denominator
    while num % p == 0:
        num //= p
        v += 1
    while den % p == 0:
        den //= p
        v -= 1
    return v


# ODE recurrence independently derived: a_n((4n+1)(4n-6)) = 6 sum a_i a_{n-i} - 2[n=1]
def ode(Nmax):
    a = [Fr(1)]
    for n in range(1, Nmax + 1):
        s = sum(a[i] * a[n - i] for i in range(1, n))
        a.append((6 * s - (2 if n == 1 else 0)) / Fr((4 * n + 1) * (4 * n - 6)))
    return a


A = ode(100)
for n in range(1, 13):
    assert lagA(n, n) == A[n], n
print("lagA == ODE wp coefficients for n=1..12: OK")
print("lagA(0) (Lean nat-sub gives exponent 0):", lagA(0, 0))

for p in [3, 7, 11, 19]:
    n0 = (p + 1) // 4
    n1 = p * (p + 1) // 4
    q = (p * p - 1) // 4
    a0 = lagA(n0, n0)
    a1 = lagA(n1, n1)
    assert a0 == A[n0] and a1 == A[n1]
    x = p * a1
    y = -a0
    print(
        f"p={p} n0={n0} n1={n1} q={q} vp(a0)={vp(a0, p)} vp(p*a1)={vp(x, p)} vp(a1)={vp(a1, p)} vp(p*a1+a0)={vp(x - y, p)} vp(phi_q)={vp(phi(q), p)}"
    )
    if p == 3:
        print("  a_n0 =", a0)
        print("  a_n1 =", a1)
        print("  p*a_n1 + a_n0 =", x - y)
    # control: other primes/ indices should fail sometimes
# negative control: p=5 (1 mod 4) with same index formulas (non-integral division) skipped; use wrong sign
for p in [3, 7, 11]:
    n0 = (p + 1) // 4
    n1 = p * (p + 1) // 4
    a0 = lagA(n0, n0)
    a1 = lagA(n1, n1)
    print(f"control p={p}: vp(p*a1 - a0) (wrong sign) = {vp(p * a1 - a0, p)}")
