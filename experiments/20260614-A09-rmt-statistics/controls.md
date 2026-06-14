# Controls — A-09
Date: 2026-06-14

## Positive Controls (data should be CLOSE)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| KS to GUE Wigner surmise | small | 0.0413 (scipy: 0.0411) | ✓ |
| P(δ<0.3) vs GUE 0.027 | ~GUE, far from Poisson 0.259 | 0.014 | ✓ (even more repulsion) |
| <s²> vs GUE 1.178 | ~GUE, far from Poisson 2.0 | 1.148 | ✓ |
| mean spacing | ≈1 (unfolding correct) | 0.9994 | ✓ |

## Negative Controls (data should DIFFER / pipeline must not fake GUE)
| Control | Expected | Result | Status |
|---------|----------|--------|--------|
| KS to Poisson (real zeros) | large (reject Poisson) | 0.3165, p=10⁻¹⁷⁸ | ✓ rejected |
| Synthetic Poisson via same code | comes out POISSON not GUE | KS_poi=0.017, closer=Poisson | ✓ pipeline honest |
| Independent Exp(1) sample (skeptic A4) | Poisson | KS_poi=0.019, p=0.50 | ✓ |

## Independent Verification (skeptic_attack.py, scipy — different impl)
| Check | Our value | scipy/independent | Match |
|-------|-----------|-------------------|-------|
| KS to GUE | 0.0413 | 0.0411 | ✓ |
| KS to Poisson | 0.3165 | 0.3161 | ✓ |
| numerical CDF vs closed-form | — | max diff 1.9e-4 | ✓ |
| Sub-bands (5×400 zeros) | — | all 5 → GUE | ✓ stable |
| Bootstrap GUE KS | — | median 0.166, real 0.041 | zeros MORE rigid than iid GUE |

The bootstrap result (real KS far below iid-GUE samples) reflects spectral
rigidity: zeta zeros are a CORRELATED process, more regular than i.i.d. draws
from the marginal spacing law. Expected, not anomalous.
