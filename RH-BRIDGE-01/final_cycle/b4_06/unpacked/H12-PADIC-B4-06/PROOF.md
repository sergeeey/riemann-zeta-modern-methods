# H12-PADIC-B4-06 — all-primes first-resonance congruence

Date: 2026-11-22. **Status:** PROVED in formal rational power-series algebra (first resonance only); INDEPENDENT FINITE CROSS-CHECKS; full BHyp/B4 in all degrees remains OPEN. No proof assistant verification has been performed for this new theorem.

## Theorem

Let `p` be **any** rational prime with `p ≡ 3 (mod 4)`, including `p=3`. Define

```
n0=(p+1)/4, n1=p*(p+1)/4, k=(p^2-1)/4.
```

For the lemniscatic elliptic curve `E_c: Y²=X³−cX`, define the analytic coordinate
`m(z)=log(sigma_c(z)/t(z))`, `t(z)=−wp_c(z)/(wp'_c(z)/2)` and universal rational coefficients
`m(z)=Σ_{n≥1} h_n c^n z^(4n)`. Let

```
A_p=(p+1)*h[n0]
B_p=p*binom(p²+p,p)*h[n1].
```

Then **both** `p*A_p` and `p*B_p` lie in `Z_(p)` and

```
p*A_p ≡ p*B_p ≠ 0  (mod p).
```

More precisely, if `wp_c(z)=z^(-2)*Σ_{n≥0} a_n(c z⁴)^n`, `a_0=1`, then

```
p*A_p ≡ p*B_p ≡ −a[n0] ≠ 0  (mod p).
```

Consequently, using the exact two-source first-resonance identity previously proved in H12-PADIC-B4-05,

```
[X U^(p-1) Y^(p²)] H=A_p*c^n0+B_p*c^n1,
H=(Delta_1 beta)(L_p(X),L_p(U),L_p(Y)),
```

this coefficient is p-adically integral (for any unit `c ∈ Z_p[i]^×`) **if and only if**

```
c^((p²−1)/4) ≡ −1 (mod p).
```

This is an all-primes theorem *about one coefficient*, **NOT** full B4/Dwork integrality for all monomials.

## Proof — self-contained

All congruences involving rationals take place in `R=Z_(p)`; `≡` means reduction modulo `p` **after verifying p-integrality**. We use truncated formal power series. Set `c=1` when defining the universal coefficients `a_n,h_n`; dependence on general `c` is restored by homogeneous scaling.

### Step 1. Elliptic integral and Lagrange inversion

Put `v(z)=wp_1(z)^(-1/2)` with `v(z)=z+O(z^5)`. The Weierstrass equation
`(wp'_1)²=4wp_1³−4wp_1` gives

```
(dv/dz)²=1−v⁴,
 z=v*Phi(v⁴),
 Phi(u)=Σ_{j≥0} phi_j u^j,
 phi_j=binom(2j,j)/(4^j*(4j+1)).
```

The inverse `v(z)` has leading term `z`. Since `wp_1(z)=v(z)^(−2)`, the Laurent-version of Lagrange–Bürmann inversion gives, for every `n≥1`,

```
a_n=−1/(2n−1) * [u^n] Phi(u)^(−(4n−2)).           (1)
```

Indeed apply `[z^N] v(z)^m = (m/N)[v^(N−m)] Phi(v⁴)^(−N)` at `m=−2`, `N=4n−2`. Both sides are identities of formal Laurent series with rational coefficients. Independently, the ODE yields
`a_n=(6Σ_{1≤j<n}a_j a_{n−j}−2*[n=1])/((4n+1)(4n−6))`; the two formulas agree by exact computation through n=8.

### Step 2. Exactly one non-p-integral Phi coefficient before n1

Write `p=4r+3`, `s=3r+2=(3p−1)/4`, `t=2r+1=(p−1)/2`, and
`q=(p²−1)/4 = r*p+s`. Then `2q=t*p+t` and `n1=q+n0 < 2q` (true even at p=3).

For `0≤j≤n1`, the denominator `4j+1` can be divisible by `p` only when `4j+1=d*p`, with `d≡3 (mod 4)`. Here `d≤p+1`, so either `d<p` or `d=p` (the next possible `d=p+4` is too large). If `d<p`, then `j mod p=s>p/2`; adding `j+j` in base `p` has a carry, hence `p | binom(2j,j)` (Kummer's elementary criterion, or Legendre's factorial formula). As `p²∤4j+1` in this case, `phi_j∈R`. If `d=p`, then `j=q` and `4q+1=p²`. Because `q=r*p+s` and `2q=t*p+t`, Legendre's formula gives exactly one p-factor in `binom(2q,q)`. Therefore `v_p(phi_q)=−1`. All remaining `phi_j` through `n1` are p-integral.

Thus, working modulo `u^(n1+1)`, we may write

```
Phi(u)=F(u)+phi_q*u^q,
F(u) ∈ R[[u]], F(0)=1,           (2)
```

and, since `2q>n1`, any coefficient through degree `n1` contains **at most one** occurrence of the exceptional factor `phi_q`.

### Step 3. The exceptional residue is −1 for EVERY p=3 mod 4

For integers `N=A*p+B<p²` with `0≤A,B<p`, the factorial after removing its `p^A` factor obeys

```
N! / p^A ≡ (−1)^A * A! * B!  (mod p).
```

Applied to `q=r*p+s` and `2q=t*p+t` (note `t−2r=1`), it yields

```
binom(2q,q)/p ≡ − (t!/(r!*s!))²  (mod p).         (3)
```

By Wilson, `r!*s!≡(−1)^(r+1) (mod p)`, because `s=p−1−r`. Again by Wilson,
`(p−1)!≡(−1)^t*(t!)²=−(t!)²≡−1`, as `t` is odd; hence `(t!)²≡1`. Therefore the right-hand side of (3) is `−1`.

Since `q=(p−1)(p+1)/4` is divisible by `p−1`, Fermat gives `4^q≡1`. Therefore

```
p*phi_q = (binom(2q,q)/p)/4^q ≡ −1  (mod p).       (4)
```

### Step 4. The wp coefficient congruence

Let `M=4*n1−2=p*(p+1)−2`. Substituting (2) into (1) and truncating at degree `n1` gives the **exact truncated identity**

```
[u^n1] Phi^(−M)
 = [u^n1] F^(−M) − M*phi_q*[u^n0] F^(−M−1),
```

because quadratic occurrences of `phi_q` begin at `u^(2q)>u^n1`. Multiply (1) by `p`, and reduce modulo `p` using that `F` is integral:

```
p*a_n1 ≡ (M/(2*n1−1)) * (p*phi_q) * [u^n0]F^(−M−1)
        = 2*(p*phi_q)*[u^n0]F^(1−p*(p+1))    (mod p).     (5)
```

The characteristic-p identity `F(u)^p≡F(u^p)` implies that, in degrees `<p`,
`F(u)^(1−p*(p+1))≡F(u)`. Since `n0<p`, the final coefficient in (5) is `phi_n0` modulo `p`. By (4),

```
p*a_n1 ≡ −2*phi_n0 (mod p).                       (6)
```

On the other hand, `(4*n0−2)=p−1`, and applying the same Frobenius simplification to (1) at `n0` yields

```
a_n0 ≡ −phi_n0/(2*n0−1) ≡ 2*phi_n0 (mod p),
```

because `2*n0−1=(p−1)/2`. Together with (6),

```
                    p*a_n1 ≡ −a_n0 (mod p).       (7)
```

The residue is **nonzero**: `phi_n0=binom(2n0,n0)/(4^n0*(p+2))` is a p-unit because `2n0=(p+1)/2<p`.

### Step 5. Passage from wp to the sigma/t logarithm

Set `f(u)=Σa_nu^n` and `g(u)=f(u)−2u*f'(u)`. Differentiation of `wp(z)=z^(−2)f(z⁴)` gives

```
t(z)/z=f(u)/g(u), u=z⁴.
```

Integrating `ζ'(z)=−wp(z)` and using `ζ(z)=1/z+O(z³)` gives the exact formal identity

```
h_n = −a_n/(4n*(4n−1)) + [u^n](log g(u)−log f(u)). (8)
```

We must check that the logarithm terms do not affect the normalized residues. Here is the p-integrality justification (not merely an empirical observation): compositional inversion of `v*Phi(v⁴)` with unit linear coefficient, followed by forming `(z/v(z))²`, uses **integer polynomial operations on the Phi coefficients** in each fixed degree. By Step 2, for `n≤n1`, `a_n` is p-integral when `n<q`, and belongs to `p^(−1)R` when `q≤n≤n1`; at these degrees there can be at most one occurrence of `phi_q`. The same is true for coefficients of `g`, as they are `(1−2n)a_n`.

Accordingly, both `f` and `g`, modulo `u^(n1+1)`, can be written as `F0(u)+p^(−1)u^q G0(u)` with `F0,G0∈R[[u]]` and `F0(0)=1`. Since `2q>n1`, their logarithms split, to this order, as

```
log(F0+p^(−1)u^q G0) = log F0 + p^(−1)u^q G0/F0.
```

For integral `F0` with constant coefficient 1, `[u^n]log F0 ∈ p^(−1)R` for `n<p²` because in `log(1+w)=Σ(−1)^(j+1)w^j/j` the contributing `j` satisfy `j≤n<p²`, hence `v_p(j)≤1`. This proves

```
[u^n0](log g−log f) ∈ R,       n0<p and n0<q,
[u^n1](log g−log f) ∈ p^(−1)R, n1<p².
```

Using (8), at `4n0=p+1` and `4n1=p(p+1)`, therefore

```
p*h_n0 ≡ −a_n0/(p+1) ≡ −a_n0                 (mod p),
p²*h_n1 ≡ −p*a_n1/((p+1)*(p*(p+1)−1))
          ≡ p*a_n1 ≡ −a_n0                    (mod p).  (9)
```

Finally `binom(p²+p,p)≡1 (mod p)` by taking the `T^p` coefficient of
`(1+T)^(p²+p)≡(1+T^(p²))*(1+T^p)` in `F_p[T]`. Multiply (9) by the remaining factors to obtain

```
p*(p+1)*h_n0 ≡ p²*binom(p²+p,p)*h_n1 ≡ −a_n0 ≠0 (mod p).
```

This is the stated theorem. QED.

## Consequence for the B4 first-resonance Dwork gate

From the independently derived B4-05 two-source identity, the coefficient of `H` at the monomial `X U^(p−1)Y^(p²)` equals `A_p c^n0+B_p c^n1`. That monomial is **not** a p-Frobenius image, because its `X` exponent is 1. Its coefficient in `pH−phi(H)(X^p,U^p,Y^p)` is therefore `p(A_p c^n0+B_p c^n1)`. Setting `r=pA_p≡pB_p≠0 mod p`, we obtain

```
p*(A_p*c^n0+B_p*c^n1) ≡ r*c^n0*(1+c^k) (mod p).
```

For `c∈Z_p[i]^×`, this vanishes if and only if `c^k≡−1 (mod p)`. The Frobenius comparison at this monomial is equivalent to integrality of its coefficient of H; hence the theorem exactly characterizes this first gate.

## Scope, limitations, and novel contribution assessment

- General first-resonance congruence: **PROVED as mathematics by the displayed formal-series argument**; no machine-check of the new argument. Cross-checks do not substitute for the proof.
- Equality of the two residues: now **ALL PRIMES p≡3 mod 4**, not merely 6 tested primes.
- One nontrivial `c`-criterion for the first resonant coefficient: **PROVED**.
- Full BHyp (the Dwork condition for every monomial, both defects): **NOT PROVED**. Higher resonances may involve more than two source terms.
- RH/GRH: **NO claim**. This is a local statement about an elliptic demonstration related to B4.
- Scientific novelty relative to Bernoulli–Hurwitz/Katz congruence literature: **NOT established**. A separate prior-art comparison is required.

## Provenance

Base reconstruction: H12-PADIC-B4-04/05, analytic-z coordinate in Rubinstein §III.5, and Lean Formalism/GaussJetBounds/Statement.lean at commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. All definitions needed for the rational coefficient identity are restated in this report. Exact tests in `verify.py` and `results.json`.
