"""Exact check of the index/constant bookkeeping that reduces  p*a_{n1} = -a_{n0} (mod p)  to
Katz-Chellali (Bannai-Kobayashi arXiv 0804.4338, Thm 5.8 ii) at l = 0, n = p-1, m = n + (p^2-1).

Definitions (B-K section 5): wp(z) = z^-2 + sum_{n>=2} BH(n+2)/(n+2) z^n/n!,
L(n) = (1-b^{n+2})(1-p^n) / (gamma^n p^{floor(n p/(p^2-1))}) * BH(n+2)/(n+2),
gamma^{p^2-1} = -eps^{-1} (p^2)! / (p^{p+1} (p^2-1)),  Frobenius over F_{p^2} = -eps*p.
For y^2 = x^3 - x, p = 3 mod 4: Frobenius over F_{p^2} is -p, so eps = 1.
Our a_m = coefficient of z^{4m-2} = BH(4m)/(4m (4m-2)!)  =>  BH(n+2)/(n+2) = a_m * n!  for n = 4m-2.
Checks (all exact): for primes p = 3 mod 4 up to a bound,
 (1) n0=(p+1)/4: n = 4*n0-2 = p-1; n1=p*n0: n' = 4*n1-2 = p^2+p-2 = n + (p^2-1); n != 0 mod p^2-1.
 (2) floor(n p/(p^2-1)) = 0 and floor(n' p/(p^2-1)) = p.
 (3) v_p(n!) = 0, (p-1)! = -1 (mod p);  v_p(n'!) = p+1 and n'!/p^{p+1} = 1 (mod p).
 (4) v_p((p^2)!) = p+1 and (p^2)!/p^{p+1} = 1 (mod p)  => gamma^{p^2-1} = eps^{-1} = 1 (mod p).
 (5) 1 - b^{p^2+p} = 1 - b^{p+1} (mod p) for b in Z[i] prime to p  (b^{p+1} = N(b) in F_p).
Then L(n')/L(n) prefactors: L(n') = u1*p*a_{n1}, L(n) = -u0*a_{n0} (mod p) with u1 = u0 = (1-b^{p+1}) gamma^{-n} unit-compatible
(gamma^{n'-n} = gamma^{p^2-1} = 1), so L(n') = L(n) (mod p) <=> (1-b^{p+1}) (p*a_{n1} + a_{n0}) = 0 (mod p).
"""

from math import factorial
from fractions import Fraction


def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def primes(limit):
    s = [True] * (limit + 1)
    for i in range(2, limit + 1):
        if s[i]:
            for j in range(i * i, limit + 1, i):
                s[j] = False
    return [i for i in range(2, limit + 1) if s[i]]


bad = 0
for p in primes(60):
    if p % 4 != 3:
        continue
    n0 = (p + 1) // 4
    n1 = p * n0
    n = 4 * n0 - 2
    n2 = 4 * n1 - 2
    ok = []
    ok.append(n == p - 1 and n2 == p * p + p - 2 and n2 == n + (p * p - 1) and n % (p * p - 1) != 0)
    ok.append((n * p) // (p * p - 1) == 0 and (n2 * p) // (p * p - 1) == p)
    fn, fn2, fp2 = factorial(n), factorial(n2), factorial(p * p)
    ok.append(vp(fn, p) == 0 and fn % p == p - 1)
    ok.append(vp(fn2, p) == p + 1 and (fn2 // p ** (p + 1)) % p == 1)
    ok.append(vp(fp2, p) == p + 1 and (fp2 // p ** (p + 1)) % p == 1)
    # (5): b^{p+1} in F_p for b = x + y i  (norm), check b^{p^2+p} == b^{p+1} mod p on all small b
    good5 = True
    for x in range(p):
        for y in range(p):
            if (x * x + y * y) % p == 0:
                continue

            # compute (x+yi)^k mod p in Z[i]/p
            def pw(k):
                r = (1, 0)
                base = (x, y)
                while k:
                    if k & 1:
                        r = (
                            (r[0] * base[0] - r[1] * base[1]) % p,
                            (r[0] * base[1] + r[1] * base[0]) % p,
                        )
                    base = (
                        (base[0] * base[0] - base[1] * base[1]) % p,
                        (2 * base[0] * base[1]) % p,
                    )
                    k >>= 1
                return r

            if pw(p * p + p) != pw(p + 1) or pw(p + 1)[1] != 0:
                good5 = False
    ok.append(good5)
    status = "OK" if all(ok) else f"FAIL {ok}"
    if not all(ok):
        bad += 1
    print(f"p={p:3d} n={n} n'={n2} checks(1..5)={ok} -> {status}")
print("failures:", bad)
