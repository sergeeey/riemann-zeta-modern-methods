# ARRES-H12 / Cycle 01 — S1′
Date: 2026-11-23
Status: ABSTRACT_LEMMA_PROVED / S1PRIME_OPEN
Isolation: branch `arres-h12-cycle01-20261123` only. Based on `bridge-discovery-01` at `33ac6c8726328e10ba05f8b36893096f1022b41e`.
The newer local `H12-DISCOVERY-03` source is not present in this remote snapshot and has NOT been inspected.

## Norm–Reynolds lemma
Let `p` be prime, `R = Z_p[[x_1,...,x_d]]` (or an appropriate complete p-adic coefficient algebra) with augmentation ideal I, `G` a group of order N coprime to p acting continuously by Z_p-algebra automorphisms preserving I, and `U ∈ 1+I`. Define `P=(1/N)Σ_g g`. Then, in the rationalized formal series ring,

`exp(P(log U)) = (Π_g g(U))^(1/N) ∈ 1+I`.

Proof: `N P(log U) = Σ log(g U)=log(Πg U)`. Exponentiate and use the unique N-th root in `1+I`, since N is p-adically invertible. In particular `N=ℓ²−1` is invertible for p=ℓ.

This proves ONLY the abstract integrality lemma, not the specific S1′ identity.

## Five outstanding source-specific obligations
1. Establish `U=exp(de1 C_λ)∘L` is integral and normalized with constant term 1 for ALL coefficients.
2. Verify the source-specific `P` truly equals the average of the claimed automorphisms; identify the precise coefficient ring and action.
3. Check any claimed commutation `τ_k L=L τ_k` from the full formula for L, not only `ζ^(ℓ²)=ζ`. Note that commutation with L is unnecessary if U is independently integral.
4. Prove descent from a cyclotomic integral extension to the exact original coefficient ring if required.
5. Match the identity to the actual PDF and Lean formulation of S1′; no status upgrade until Lean checks the exact statement.

## Exact arithmetic diagnostic
In a separate sandbox, six exact-rational tests passed: p=3,N=8 and p=5,N=24; U=1+x, 1+x+x², 1+2x+3x²+x³, through degree 24. They compared `exp(P log U)` with `Res_z(z^N-1,U(zx))^(1/N)`, and found p-integral coefficients. Source script delivered separately to the chat. This is finite evidence for the abstract formula, not a verification of S1′.

## Next action
Read local `H12-DISCOVERY-03` and the precise S1′ PDF/Lean definitions; settle the five obligations and test by Lean in the authorized isolated worktree. Do not manufacture conclusions if the local source is inaccessible.
