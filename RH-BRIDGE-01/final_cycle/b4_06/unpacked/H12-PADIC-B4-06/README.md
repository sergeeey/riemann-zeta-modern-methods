# H12-PADIC-B4-06

**Claim:** an all-primes mathematical proof of the first-resonance coefficient congruence (p=3 mod4). The general B4 theorem in all degrees remains unproved.

Files:
- `PROOF.md`: self-contained formal-power-series proof and limitations.
- `verify.py`: independent exact tests, generating `results.json`.
- `b4_04_verify.py`: previous exact m(z) verifier, included to make archive self-contained.
- `results.json`: recorded exact checks.
- `SHA256SUMS.txt`: integrity manifest.
- `CHECKLIST.md`: statuses.

Run `python verify.py`, then `sha256sum -c SHA256SUMS.txt` (note: rerunning verifier deterministically rewrites results.json).

Source: Rubinstein §III.5; https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf ; pinned Lean definition https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/GaussJetBounds/Statement.lean .
