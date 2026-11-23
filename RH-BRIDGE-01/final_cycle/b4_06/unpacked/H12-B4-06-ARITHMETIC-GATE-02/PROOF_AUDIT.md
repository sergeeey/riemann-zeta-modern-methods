# H12 B4-06 — arithmetic gate 02 | 2026-11-23

STATUS: mathematical derivation audited; Lean source drafted, NOT kernel checked.

## Goal
For prime p ≡ 3 mod 4 prove that amongst phi_j = binom(2j,j)/(4^j(4j+1)), 0 ≤ j ≤ n1=p(p+1)/4, exactly phi_q with q=(p²-1)/4 has negative p-adic valuation; prove v_p(phi_q) = -1 and p phi_q ≡ -1 (mod p). This is a necessary component of B4-06, not full B4.

## New independent, elementary proof of uniqueness
Write p=4r+3, n0=r+1, q=(p²-1)/4, n1=p(r+1). Let j≤n1 and suppose p | 4j+1. Put d=(4j+1)/p. Then d ≡ 3 (mod 4) because p ≡3 mod4; also

    4j+1 ≤ 4n1+1 = p(p+1)+1.

Since d and p are integers with p≥3, d≤p+1. As d≡p≡3 mod4, this forces d<p or d=p. If d=p, 4j+1=p² and j=q exactly, with v_p(4q+1)=2.

If d<p, write d=4h+3 (with 0≤h≤r-1). Then

    j = h p + s,      s=3r+2=(3p-1)/4,
    0<s<p and 2s ≥ p.

The base-p sum of j+j has a carry in the units digit, so p | binom(2j,j) by Kummer's theorem. Since d<p, v_p(4j+1)=1, whereas v_p(binomial)≥1. Thus phi_j is p-integral. If p∤4j+1 the denominator is prime to p and phi_j is p-integral as well.

For j=q=r p+s, note 2q=t p+t, t=2r+1, and 2s= p+t. Exactly one carry occurs in q+q, so v_p(binomial(2q,q))=1. As v_p(4q+1)=2, v_p(phi_q)=-1.

## Normalized residue, independent factorial derivation
Let r=(p-3)/4, s=(3p-1)/4=p-1-r and t=(p-1)/2. For N=A p+B with A,B<p, the p-unit factorial satisfies

    N!/p^A ≡ (-1)^A A! B! (mod p).

Because q=r p+s and 2q=t p+t, t-2r=1, this gives

    binom(2q,q)/p ≡ - (t!/(r! s!))² mod p.

Wilson gives r! s! ≡ (-1)^(r+1) and (t!)² ≡1 mod p (t odd). Therefore binom(2q,q)/p ≡-1 mod p. Since 4q+1=p² and 4^q≡1 mod p (q multiple of p-1):

    p phi_q = [binom(2q,q)/p]/4^q ≡-1 mod p.

All modular reductions here are taken after cancellation, not on nonintegral rational expressions.

## What Lean module contains
`ExceptionalIndexGate.lean` contains candidate proofs of the elementary index classification, modulo-four quotient, upper bound, exceptional equality, carry inequality and representation of j. It does not contain the Kummer, Wilson or factorial-unit theorems; these are next formal proof obligations.

## Independent execution
`verification/check_index_gate.py`: exact arithmetic only, 24 primes up to 199, every j≤n1; PASS. Largest n1=9950. No kernel check, no claim of universal proof from finite tests.

## Remaining proof gate to make it kernel-checked
1. Compile `ExceptionalIndexGate.lean` with pinned Lean 4.33.1 and Mathlib; repair elaboration errors without changing theorem scope.
2. Link small-divisor representation to Mathlib's Kummer/Legendre factorial valuation lemma and prove p divides central binomial coefficient.
3. Formalize the factorial p-unit congruence, obtaining `p phi_q ≡ -1 mod p` after p-integrality.
4. Formalize truncated power-series passage `p*a_n1 ≡ -a_n0`.
5. Formalize sigma/t logarithm and beta normalizations; independently verify B4-05 two-source coefficient identity at frozen SHA.

## Scope
No new mathematical theorem about RH/GRH; first-resonance arithmetic only. The user's WSL worktree and original `LemmaZAlgebra.lean` are not accessible in this execution. The previous B4-06 paper proof remains the source for full first-resonance statement.
