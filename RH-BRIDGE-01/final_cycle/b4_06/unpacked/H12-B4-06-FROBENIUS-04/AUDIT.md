# H12-B4-06-FROBENIUS-04 — Universal nilpotent Frobenius bridge

Status: `MATH_PROVED`, `FINITE_TESTS_PASS`, `LEAN_SOURCE_PREPARED`,
`LEAN_KERNEL_NOT_RUN`, `B4_ALL_PRIMES_IN_LEAN_OPEN`.

## New contribution compared with FROBENIUS-03

Earlier Lean file `FrobeniusResidueInterface.lean` only assumed the
two normalized congruences and combined them. This file includes a
generic, mathematical Frobenius theorem over ANY commutative ring R
with prime characteristic p and a nilpotent x satisfying x^p=0.

For F=1+x:
    F^p = (1+x)^p = 1+x^p=1,
    F^(p(p+1))=1.

If G is an inverse of F, then:
    G^p=1,
    F * G^(p(p+1)) = F.

This implements the Frobenius step in B4-06, originally expressed as
    F(u)^(1-p(p+1)) ≡ F(u) (mod u^(n0+1)).
Taking R=F_p[u]/(u^p) is enough because n0<p. The current Lean proof
uses abstract nilpotence and *does not yet construct* this quotient or
its coefficient map. That construction remains a concrete open link.

## Exact finite checks

`check_truncated_frobenius.py` independently computes inverses and
powers in F_p[u]/(u^p) for 120 seeded random series across 24 primes
p≡3 (mod 4), up to p=199. All assertions passed.
Computations are diagnostic only, not verification by Lean kernel.

## Mathlib source

Mathlib.Algebra.CharP.Lemmas theorem:
    add_pow_char (x y : R) (p : Nat) [Fact (Nat.Prime p)]
      [CharP R p] : (x+y)^p=x^p+y^p.
See https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/CharP/Lemmas.html

## Separate hard gates / still open

1. Formal `ZMod p[X]/(X^(n0+1))` and reduction map from the rational
   p-integral subring, including exceptional `p*phi_q`.
2. Formal Laurent Lagrange inversion and coefficient extraction:
   p*a_n1 ≡ -a_n0 (mod p).
3. Transfer through sigma/t logarithm, and exact Lean beta definition.
4. Kernel compilation and `#print axioms` for all generated Lean files.
5. All-degree B4 (not implied).

Do not call this final formal certification of B4-06 or RH.
