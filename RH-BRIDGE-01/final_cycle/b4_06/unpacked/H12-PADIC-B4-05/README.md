# H12-PADIC-B4-05 reproducibility package

**Key result:** exact two-source identity at the first Dwork resonance, and a six-prime exact rational congruence that turns the paper's twist condition on `c` into a necessary-and-sufficient condition for that **single coefficient** (under the verified unit hypotheses). This is not an all-degree proof of B4.

```bash
python resonance.py
python test_resonance.py
sha256sum -c SHA256SUMS.txt
```

- `audit.md`: mathematical proof, hypotheses, rejected shortcuts, next question.
- `resonance.py`: exact six-prime certificates and JSON output.
- `test_resonance.py`: full original polynomial construction vs isolated first homogeneous term, for ell=3,7,11.
- `probe_leading.py`: intentionally incomplete homogeneous truncation — demonstrates why the naive approach fails.
- `b4_04_verify.py`: exact analytic-z verifier reused from H12-PADIC-B4-04.
- `results.json`: serialized exact arithmetic results.
- `SHA256SUMS.txt`: package checksum manifest (excluding itself).

No `lake`, no complete formalization of the new coefficient identity in Lean, no general Frobenius congruence proven.
