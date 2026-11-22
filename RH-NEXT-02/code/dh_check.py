"""Davenport-Heilbronn function: D(s) = sum a(n) n^-s, a(n) = Re chi(n) + kappa * Im chi(n), chi mod 5, chi(2)=i.
Checks: (i) first off-line zero near 0.8085 + 85.699 i (from memory: UNVERIFIED), (ii) functional equation, (iii) Lambda_D coefficients.
"""

import mpmath as mp

mp.mp.dps = 30
s5 = mp.sqrt(5)
kappa = (mp.sqrt(10 - 2 * s5) - 2) / (s5 - 1)
print("kappa =", mp.nstr(kappa, 20))
a_per = [0, 1, kappa, -kappa, -1]  # a(n) by n mod 5
D = lambda s: mp.dirichlet(s, a_per)

# functional equation check:  xi(s) = (pi/5)^(-s/2) Gamma((s+1)/2) D(s)  should satisfy xi(s) = xi(1-s)
xi = lambda s: (mp.pi / 5) ** (-s / 2) * mp.gamma((s + 1) / 2) * D(s)
for s in [mp.mpc(0.3, 2.1), mp.mpc(0.7, 5.5), mp.mpc(0.55, 12.3)]:
    print(
        "FE test s=",
        mp.nstr(s, 6),
        " xi(s)-xi(1-s) =",
        mp.nstr(abs(xi(s) - xi(1 - s)), 5),
        " |xi|=",
        mp.nstr(abs(xi(s)), 5),
    )

# off-line zero near 0.8085+85.699i
z = mp.findroot(D, mp.mpc(0.8085, 85.699))
print("zero near 0.8085+85.699i ->", mp.nstr(z, 15), " |D|=", mp.nstr(abs(D(z)), 3))
z2 = mp.findroot(D, mp.mpc(0.1915, 85.699))
print("mirror zero 1-conj ->", mp.nstr(z2, 15))

# Lambda_D(n) from -D'/D = sum Lambda_D(n) n^-s :  a(n) log n = sum_{d|n} Lambda(d) a(n/d)
a = lambda n: a_per[n % 5]
Lam = {}
for n in range(1, 41):
    s = a(n) * mp.log(n)
    for d in range(1, n):
        if n % d == 0:
            s -= Lam[d] * a(n // d)
    Lam[n] = s
print("Lambda_D(n), n=1..12:", [mp.nstr(Lam[n], 6) for n in range(1, 13)])
# sanity: -D'/D at s=4 from the series vs numerically
s0 = mp.mpf(4)
ser = sum(Lam[n] * mp.mpf(n) ** (-s0) for n in range(1, 41))
num = -mp.diff(D, s0) / D(s0)
print("-D'/D(4): series(40 terms) =", mp.nstr(ser, 12), " numeric =", mp.nstr(num, 12))
