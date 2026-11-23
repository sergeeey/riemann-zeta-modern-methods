# H12-PADIC-B4-05 — first-resonance theorem and failed homogeneous truncation

Date: 2026-11-22. Pinned Lean mirror SHA: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

**Status:** one exact symbolic all-primes coefficient identity (**PROVED**); conditional first-resonance equivalence (**PROVED**); exact residue congruences for 6 specified primes (**COMPUTED, not proved for arbitrary prime**); complete multivariable Dwork checks to the first resonance for 3 primes (**FINITE VERIFIED**); all-degree B4 (**OPEN**). No implication toward RH without additional results.

## 1. Verified definition

Rubinstein's draft §III.5, p. 88 defines the analytic-coordinate quantity `m(z)=log(sigma_c(z)/t(z))`, with `E_c: Y^2=X^3-cX`, `t=-X/Y` and `\tilde beta(z,w)=m(z+w)-m(z)-m(w)`; `beta` is the invariant part under `(z,w)->(ζz,ζ^{-ell}w)`. For `ell=3 (mod 4)`, `M=ell²−1`. Lean's `Formalism/GaussJetBounds/Statement.lean` defines `de1`, `de2`, and the letter logarithm. At `d=2`, all letters receive `L_ell(T)=Σ_{e≥0} T^{ell^(2e)}/ell^e`.

Write `m(z)=Σ_{n≥1} h_n c^n z^{4n}`, with rational `h_n`. The recurrence for the h_n is inherited unchanged from H12-PADIC-B4-04 (source in this reproducible package); verified first terms `h1=-5/12`, `h2=-3/56`, `h3=-13/990`.

Let `Delta_1 beta(X,U,Y)=beta(X+U,Y)-beta(X,Y)-beta(U,Y)` and `H=(Delta_1 beta)(L_ell(X),L_ell(U),L_ell(Y))`.

## 2. PROVED: two-source first-resonance coefficient identity

For every odd prime `ell ≡3 mod 4` and arbitrary `c`, let

```
n0=(ell+1)/4, n1=ell*(ell+1)/4, k=n1-n0=(ell²−1)/4,
A_ell=(ell+1)*h[n0],
B_ell=ell*binom(ell²+ell,ell)*h[n1].
```

Then, as an exact identity over the rational Gaussian coefficient field,

```
[X^1 U^(ell-1) Y^(ell²)] H = A_ell*c^n0 + B_ell*c^n1.
```

**Derivation:** the factors `L(X)^j L(U)^(a−j)` can yield `X U^(ell−1)` only from `a=ell`, `j=1` and the linear term of each `L`, because all higher powers in `L` have degree at least `ell²`. The factor `L(Y)^b` can yield `Y^(ell²)` in exactly two ways: (i) `b=1` and choose the term `Y^(ell²)/ell`, or (ii) `b=ell²` and choose only the linear terms. These correspond to `4n=ell+1` and `4n=ell²+ell`, both satisfying the invariant congruence `ell−ell*b ≡0 mod(ell²−1)`. The binomial coefficients from `m(z+w)` and from the additive defect give exactly `A_ell` and `B_ell`. No other terms can contribute.

Since the monomial exponents `(1,ell−1,ell²)` are not all divisible by `ell`, the coefficient of the Frobenius expression `ell*H - phi(H)(X^ell,U^ell,Y^ell)` is exactly `ell*(A_ell c^n0+B_ell c^n1)`. Hence the Dwork gate at this monomial is equivalent to `A_ell c^n0+B_ell c^n1` belonging to `O=Z_ell[i]`.

**Conditional algebraic equivalence (all primes covered by its hypotheses):** if `ell*A_ell, ell*B_ell` are `ell`-adic units and have the SAME nonzero residue `r` in `F_ell`, and if `c` is a unit in `Z_ell[i]`, then the first-resonance Dwork gate is satisfied **if and only if**

```
c^((ell²−1)/4) ≡ -1 mod ell.
```

Proof: modulo `ell`, `ell*(A_ell c^n0+B_ell c^n1) ≡ r*c^n0*(1+c^k)`, and `r,c` are units. This matches the paper's choice of `c` exactly at the first resonance. The unit/residue hypotheses are COMPUTATIONALLY verified below, not proved for all primes.

## 3. Exact computations

| ell | n0 | n1 | residue of ell*A | residue of ell*B | equality | first resonance degree |
|---:|---:|---:|---:|---:|---|---:|
| 3 | 1 | 3 | 1 | 1 | yes | 12 |
| 7 | 2 | 14 | 4 | 4 | yes | 56 |
| 11 | 3 | 33 | 10 | 10 | yes | 132 |
| 19 | 5 | 95 | 12 | 12 | yes | 380 |
| 23 | 6 | 138 | 21 | 21 | yes | 552 |
| 31 | 8 | 248 | 13 | 13 | yes | 992 |

All rational numbers are computed with `fractions.Fraction`; valuations and reductions use exact integer divisibility. The pair `ell*A,ell*B` consists of units in all six cases. Consequently, the first-resonance integrality criterion really enforces the **twist condition** in these six cases. For `c=1` (which does *not* satisfy the twist condition), the first-resonance gate fails in all six cases.

Independent multivariable check: for `ell=3,7,11`, `build_H` directly recovers the above coefficient at degrees `12,56,132`, respectively, and the full Dwork condition holds through these degrees for the three paper examples. In contrast, keeping ONLY the first homogeneous term of `beta` fails the Dwork condition **at precisely those first-resonance degrees**. `test_resonance.py` asserts all of this.

For `ell=3` the exact formula is

```
H_res(c) = -(5c+26c^3)/3.
```

At `c=-i` this becomes `-7i`, integral; with the leading `beta_4` alone it would be `5i/3`, nonintegral. The absent term `beta_12` contributes `-26i/3` and makes the cancellation. `3H_res` is the Dwork coefficient since the monomial is not a Frobenius image. In contrast `c=1` yields `-31/3`, nonintegral.

## 4. Further exact functional identity, but not sufficient

The Honda logarithm used in the Lean statement satisfies **in every degree**

```
ell*L_ell(T) - L_ell(T^(ell²)) = ell*T.
```

This is a pure reindexing of `Σ T^(ell^(2e))/ell^e`, not a new theorem. It shows why a height-two Frobenius/inert-ell formal-group structure is a plausible mechanism. It does **not** alone establish `ell H-phi(H)(X^ell,U^ell,Y^ell)` integral: the required comparison is one-Frobenius (with coefficient conjugation), while the Honda identity directly governs two Frobenius steps.

## 5. Failed attempted shortcut

**Invalid route:** first prove `exp(beta(L_ell(X),L_ell(Y)))` integral, then obtain the defect by quotienting units. Already at `ell=3`, `c=-i`, its `X^3 Y` coefficient equals `5i/3`. This is not integral. More generally, for the six tested primes the first coefficient at `X^ell Y` is `A_ell*c^n0` of valuation `−1` for unit `c`. The additive defect is essential.

**Another invalid route:** prove integrality of each homogeneous term of `beta` after forming the defect. Leading-only terms fail at degrees `ell²+ell`; integrality requires cancellations between the `4n=ell+1` and `4n=ell²+ell` pieces, and likely analogous families at larger degrees.

## 6. Strongest remaining mathematical conjecture

For all primes `ell≡3 mod4`, propose to prove the modular **first-resonance congruence**

```
ell*(ell+1)*h[(ell+1)/4]
  ≡ ell²*binom(ell²+ell,ell)*h[ell*(ell+1)/4]  (mod ell),
```

both displayed terms interpreted in `Z_(ell)` after extracting their common simple ell-denominator. Verified for six primes, but NOT proved generally. The congruence would explain the paper's condition on `c` at the first resonance. To prove B4 in all degrees one still needs a much stronger coherent Frobenius identity controlling **all resonance families**, possibly using a height-two formal `O_K`-module and a cubical theta trivialisation. Directly importing the Mazur–Tate canonical p-adic sigma-function for **ordinary** elliptic curves would be invalid in this supersingular inert setting without a corresponding theorem.

## 7. Sources and reproducibility

- Rubinstein, `zeta-paper.pdf`, working draft dated 21 Nov 2026, §III.5 p.88, https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf .
- Pinned Lean `Formalism/GaussJetBounds/Statement.lean`, https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/GaussJetBounds/Statement.lean .
- Blakestad & Grant, *On the universal p-adic sigma and Weierstrass zeta functions*, ordinary-reduction scope; https://www.sciencedirect.com/science/article/abs/pii/S0022314X23000380 .
- Earlier `H12-PADIC-B4-04` reproducible finite-check archive; this package includes the exact verifier source under `b4_04_verify.py` so it is self-contained.

Reproduce: `python resonance.py`; `python test_resonance.py`; `python probe_leading.py --ell 3 --degree 12`; `sha256sum -c SHA256SUMS.txt`.
