# H12-B4-06 | Lean formalization sprint, 2026-11-23

Source: `H12-PADIC-B4-06-PROOF.md`, archived in Google Drive.
Target: a kernel-checked proof of the unique exceptional \(\varphi_q\) coefficient and \(p a_{n_1}\equiv-a_{n_0}\) for every prime p≡3 mod 4.

## Output in this execution

- `ResonanceParameters.lean`: five arithmetic/parameter lemmas, intentionally requiring no new axioms or `sorry`. **Not compiled**; source code only. It proves only elementary index relations, not the all-primes congruence.
- `verification/exact_test.py`: completely exact rational checker of unique p-adic exceptional coefficient up to p=103 and the wp recurrence congruence for p=3,7,11,19,23,31. Python test passed, no floating point arithmetic.
- `PROOF_OBLIGATIONS.md`: exact remaining Lean obligations and necessary mathlib infrastructure.
- `verification/run.log`: reproducible execution output and environment snapshot.

## Do not overstate

No Lean executable is installed here, so `KERNEL_CHECKED=NO`. The general congruence is still a paper proof supported by numerical checks, not machine-verified. In particular, formalizing solely the parameter relations does **not** prove B4-06. Full B4 remains open.

## Suggested execution in the local pinned project

```bash
lake env lean ResonanceParameters.lean
python3 verification/exact_test.py
```

Do not compile `Main` for this local test. Before escalating to `TheoremFSharp` or main GRH chain, match the author's exact coordinate / beta normalization.
