# H12-B4-06 — Step 2–4 Lean proof obligations

Status: `PARTIAL`, Lean not available in current container. No file is claimed kernel-checked.

## Formalized as a standalone Lean candidate

`ResonanceParameters.lean`: non-asymptotic parameter identities, isolated exceptional index inequality `n₁<2q`, and `n₀<p`, without `sorry`.

Before any kernel status is assigned, run in the matched Lean 4.33.1/Mathlib environment:

```bash
lake env lean ResonanceParameters.lean
```

## Unresolved core mathematics for a machine proof

1. `j≤n₁, j≠q ⇒ v_p(φ_j)≥0`, where `φ_j=choose(2j,j)/(4^j(4j+1))`. Formal proof needs divisibility of central binomial via carries and a careful treatment of denominators.
2. `v_p(φ_q)=−1` and `pφ_q ≡−1 (mod p)` in `ℤ_(p)` or `ℤ_[p]` / `ZMod p`, with `p` prime and `p%4=3`; factorial unit part modulo `p` is the delicate step. Avoid `ZMod p` reduction *before* cancelling p-denominators.
3. `p a[n₁] ≡−a[n₀] (mod p)`, using finite-power-series Lagrange inversion and an integrality-preserving coefficient truncation. The displayed `F(u)` is p-integral, but `Φ(u)` itself is not; separate its exceptional term *before* reduction modulo p.
4. Then Step 5: `p A ≡ p B ≡−a[n₀]` requires formal `log(g)-log(f)` valuations and coefficient identity. Do **not** assume this follows from (3) without checking denominators.
5. Dwork transfer uses B4-05 first-resonance coefficient identity and the *author's exact `β` normalization*. Verify equality with pinned source; prior z-vs-t distinction is load-bearing.

## Independent executable validation

Run `python verification/exact_test.py` to check prime-index valuation uniqueness and the all-prime normalized residues over a bounded set; this is finite evidence only, not universal proof.

## Target Lean theorem types

Rather than introducing arbitrary ad hoc axioms, first represent `φ : ℕ→ℚ`, then express `IsPIntegral p x` via `Rat.den x` being coprime to `p` (equivalently nondivisibility), and express reduction via `ZMod p` only after proving the denominator is a unit. The target claim is:

```
(p * φ q).den % p ≠ 0
and
(p * φ q) reduces to -1 in ZMod p
```

Then extend to the wp coefficient `a` and the `m(z)` logarithm coefficients `h`.
