# H-12 · Riemann Zeta — Modern Methods

> A personal computational experiment exploring the Riemann Hypothesis using modern numerical methods, custom algorithms, and AI-assisted analysis.  
> **No proof claims** — just an open, curiosity-driven experiment with rigorous methodology.

---

## What This Is

Systematic investigation of the Riemann Hypothesis by **atomization** — breaking the problem into 14 independent sub-problems (atoms), studying each one separately, then synthesizing.

This is not a race to announce a proof. It's a methodical research process:

1. **Fix the foundation** — original 1859 formulation + everything proven
2. **Atomize** — 14 independent atoms, each with a known status
3. **Study each atom** — computational experiments + Falsification Ladder methodology
4. **Synthesize** — combine results

---

## Project Structure

```
.
├── README.md
├── CLAUDE.md                    # Project rules + methodology (AI-assisted sessions)
├── .claude/memory/
│   ├── riemann_foundation.md    # Original hypothesis + all proven theorems [VERIFIED]
│   ├── riemann_atoms.md         # 14 atoms: status, priority, experiment plan
│   └── riemann_approaches.md    # All approaches 1859–2026, failure patterns
├── experiments/                 # Falsification Ladder experiments per atom
│   └── _template/               # FL experiment template
└── src/                         # Python code for computational experiments
    └── zeta/                    # Core zeta function toolkit
```

---

## The 14 Atoms

| ID | Atom | Status |
|----|------|--------|
| A-01..A-06 | Functional equation, trivial zeros, critical strip, Hardy's theorem, connection to primes, equivalent formulations | ✓ **PROVEN** |
| A-07..A-09 | Fraction of zeros on Re=½ (41.28%), zero-free region, RMT statistics | ~ **PARTIAL** |
| A-10 | First 2×10¹³ zeros verified on critical line | ✓ **VERIFIED (computational)** |
| A-11..A-14 | The full conjecture, Hilbert-Pólya operator, GRH, geometric approaches | ❓ **OPEN** |

Full details: [`.claude/memory/riemann_atoms.md`](.claude/memory/riemann_atoms.md)

---

## Methodology

Every experiment follows the **Falsification Ladder** (FL Full-Ladder):

- Zero-Signal Gate: entity + falsifiable predicate + measurable outcome
- EstimandOps: classify question type (structural/mathematical)
- Controls: positive + negative
- Stress tests
- Decision: promote / repeat / reject → `null_results/` if rejected

No claim is accepted without `[VERIFIED]` evidence from real data.

---

## Status

**Phase 1 complete** (2026-06-14): Foundation fixed, 14 atoms defined, all approaches documented.  
**Phase 2**: Choose first atom → first experiment.

---

## Resources

- [LMFDB — L-functions and Modular Forms Database](https://www.lmfdb.org)
- [Odlyzko's zero tables](https://www.dtc.umn.edu/~odlyzko/zeta_tables/)
- [The Riemann Hypothesis (Clay Math Institute)](https://www.claymath.org/millennium-problems/riemann-hypothesis/)

---

*Curiosity-driven. Methodologically rigorous. No shortcuts.*
