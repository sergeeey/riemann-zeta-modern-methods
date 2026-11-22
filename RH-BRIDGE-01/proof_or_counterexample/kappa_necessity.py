"""Necessity of the operator bound K_i <= (1+kappa) I in Lemma Z+ (exact rational arithmetic).

Instance: H = C^2, n+1 maps B_i : C -> C^2 (r_i = 1, gamma_i = 1).  B_1..B_n = e_1 (K_i = 1);  B_{n+1} = sqrt(n) e_2 (K = n, so kappa = n-1).
Q = diag(n, n):  Tr Q = 2n, Tr Q^2 = 2 n^2, eta = Tr Q^2 * D / (Tr Q)^2 - 1 = 0.  R = n+1, sum Tr K_i = 2n >= R  (e' = 0).
E_i = C for i <= n, E_{n+1} = 0  =>  sum codim E_i = 1, eps = 1/(n+1).  span(B_i E_i) = C e_1  =>  w = 1, D = 2.
Without a kappa-term the bound would read  w <= D (eta + 2 eps/(1-e')) = 4/(n+1)  <  1 = w for n >= 4: violated.
With kappa = n-1 it reads 2 * 2 n/(n+1) >= 2 >= w: not violated.
Run: python -I kappa_necessity.py
"""
from fractions import Fraction as F

for n in (4, 10, 100, 1000):
    D, R, w = 2, n + 1, 1
    eta = F(2 * n * n * D, (2 * n) ** 2) - 1
    eps = F(1, n + 1)
    e_prime = 1 - F(2 * n, R) if 2 * n < R else F(0)
    kappa = n - 1
    bound_no_kappa = D * (eta + 2 * eps / (1 - e_prime))
    bound_with_kappa = D * (eta + 2 * (1 + kappa) * eps / (1 - e_prime))
    print(
        f"n={n:5d}: eta={eta}, eps={eps}, w={w}; bound without kappa = {float(bound_no_kappa):.4f} "
        f"(violated: {w > bound_no_kappa}); bound with kappa = {float(bound_with_kappa):.4f} (violated: {w > bound_with_kappa})"
    )
