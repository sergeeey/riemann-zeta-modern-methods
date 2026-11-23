# H12 B4-06 — Exact Frobenius gate, stage 03

Status: **MATHEMATICAL REDUCTION + EXACT COMPUTATIONAL CHECKS. LEAN KERNEL NOT RUN.**

## Abstract finite-ring lemma that isolates the difficult step

Fix an odd prime p=4r+3, with n₀=r+1, q=(p²−1)/4, n₁=q+n₀,
M=4n₁−2=p(p+1)−2. Let R=Z_(p) and F∈R[[u]] with F(0)=1.
Put Φ=F+φ_q u^q modulo u^(n₁+1), and assume pφ_q∈R has residue −1.
Because 2q>n₁, a single exceptional factor can occur. Consequently,

    [u^n₁] Φ^(-M)
      = [u^n₁] F^(-M) − M φ_q [u^n₀] F^(-M−1).

Define a_n = −[u^n]Φ^(-(4n−2))/(2n−1), as in Lagrange inversion.
All coefficients of F^(-M) lie in R. Multiply by p and reduce:

    p a_n₁ ≡ (M/(2n₁−1)) · (pφ_q) · [u^n₀]F^(-M−1)
            ≡ −2 [u^n₀]F^(1−p(p+1)) (mod p).

In F_p[[u]], F^(p)=F(u^p). Since n₀<p, the coefficients of
F^(−p(p+1)) at positive degrees below p vanish; hence

    [u^n₀]F^(1−p(p+1)) ≡ [u^n₀]F (mod p).

At the small index n₀, 4n₀−2=p−1, and similarly

    a_n₀ ≡ −(2n₀−1)^(-1)[u^n₀]F^(−(p−1))
         ≡ 2[u^n₀]F (mod p).

Thus the key B4-06 congruence follows:

    p a_n₁ ≡ −a_n₀ (mod p).

This is a universal *mathematical* derivation conditional on the
Lagrange formula, exceptional-factor decomposition and pφ_q residue.
It does not assert a Lean kernel proof.

## What the check actually tests

The executable check constructs F modulo u^(n₀+1) over F_p and verifies:

  F^(1−p(p+1)) = F modulo u^(n₀+1)
  F^(−(p−1)) = F modulo u^(n₀+1)
  p a_n₁ + a_n₀ = 0 in F_p (using pφ_q=−1).

The first two are universal ring identities in characteristic p, *not*
claims inferred by numerical extrapolation. The test uses an explicit
inverse recurrence and binary exponentiation, which independently check
all polynomial coefficients in the necessary truncated ring.

## Two formal proof obligations still open

1. In Lean, prove the truncated-power-series identity for arbitrary
   F with constant coefficient 1, including the inverse Frobenius
   exponent in ZMod p. Use `PowerSeries` or finite `Polynomial`/
   `TruncatedPolynomial` and prove the coefficient-extraction lemma.
2. Prove the exceptional factor decomposition over `Z_(p)`, and its
   normalization pφ_q=−1 from valuation/factorial-unit lemmas.

Stage 03 cannot claim full congruence in kernel until both are closed.

## Tiny Lean bridge (UNCOMPILED)

`FrobeniusResidueInterface.lean` contains elementary algebra after
coefficient relations are supplied, a twist-equivalence using units,
and an exact p=3 coefficient example. The bridge is not the hard theorem.
