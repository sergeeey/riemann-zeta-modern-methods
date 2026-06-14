"""A-08 — Zero-free region: the gap to Re=1/2 GROWS, it does not shrink.

Classical ZFR (de la Vallee-Poussin), explicit constant Mossinghoff-Trudgian-Yang
2022:  zeta(s) != 0 for sigma > 1 - 1/(R ln|t|),  R = 5.558691,  |t| >= 2.
Vinogradov-Korobov:  sigma > 1 - 1/(C (ln t)^{2/3} (lnln t)^{1/3}),  C = 55.241.

Key (corrects a common misconception): sigma_zf(t) is INCREASING in t — the proven
boundary moves toward Re=1, NOT toward Re=1/2. The gap sigma_zf - 1/2 GROWS toward
0.5 as t grows. No finite t (in the region of validity) brings it near 1/2.

We compute both boundaries, the gap, and the (astronomical) t where VK overtakes
the classical form — computed here, not taken on faith.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).resolve().parent

R_CLASSICAL = mp.mpf("5.558691")  # MTY 2022, |t|>=2
C_VK = mp.mpf("55.241")  # MTY 2022, |t|>=3

# Reference table from lit-review (for positive control)
REF = {2: 0.9609, 6: 0.9870, 30: 0.9974, 80: 0.9990}


def sigma_classical(log10_t):
    lt = mp.mpf(log10_t) * mp.log(10)
    return 1 - 1 / (R_CLASSICAL * lt)


def sigma_vk(log10_t):
    lt = mp.mpf(log10_t) * mp.log(10)
    return 1 - 1 / (C_VK * lt ** (mp.mpf(2) / 3) * mp.log(lt) ** (mp.mpf(1) / 3))


def vk_crossover_log10t():
    """Solve for t where VK boundary overtakes classical: R*ln t = C*(ln t)^{2/3}(lnln t)^{1/3}.

    => ln t = (C/R)^3 * lnln t. Solve L = k*ln(L), k=(C/R)^3, then log10 t = L/ln10.
    """
    # WHY bracket [1000, 20000]: L = k*ln(L) has TWO roots (k=981 > e) — a trivial
    # one near L=1 and the real crossover near L=8928. f(x)=x-k*ln(x) has a minimum
    # at x=k (f(k)<0); bracketing above k isolates the large root, ruling out the
    # spurious one regardless of solver. (reviewer P2)
    k = (C_VK / R_CLASSICAL) ** 3
    L = mp.findroot(lambda x: x - k * mp.log(x), [mp.mpf(1000), mp.mpf(20000)], solver="bisect")
    return float(L / mp.log(10)), float(k)


def main() -> None:
    mp.mp.dps = 30
    exps = [2, 3, 4, 6, 12, 30, 80, 130, 200]
    rows = []
    for e in exps:
        sc = sigma_classical(e)
        sv = sigma_vk(e)
        rows.append(
            {
                "log10_t": e,
                "sigma_classical": float(sc),
                "sigma_vk": float(sv),
                "gap_classical_to_half": float(sc - mp.mpf("0.5")),
                "vk_wider": bool(sv < sc),  # smaller sigma_zf = wider zero-free zone
                "ref": REF.get(e),
                "ref_match": (REF.get(e) is None) or (abs(float(sc) - REF[e]) < 1e-3),
            }
        )

    cross_log10t, kval = vk_crossover_log10t()

    # --- checks ---
    sc_list = [r["sigma_classical"] for r in rows]
    gap_list = [r["gap_classical_to_half"] for r in rows]
    monotone_up = all(sc_list[i + 1] > sc_list[i] for i in range(len(sc_list) - 1))
    gap_grows = all(gap_list[i + 1] > gap_list[i] for i in range(len(gap_list) - 1))
    ref_ok = all(r["ref_match"] for r in rows)
    in_strip = all(0.5 < r["sigma_classical"] < 1.0 for r in rows)
    # VK overtakes only at astronomical t (> 10^100)
    vk_astronomical = cross_log10t > 100
    # at our table (all < 10^200 except check), classical is wider (vk_wider False) below crossover
    vk_not_yet = all(not r["vk_wider"] for r in rows if r["log10_t"] < cross_log10t)

    verdict = (
        "PASS"
        if all([monotone_up, gap_grows, ref_ok, in_strip, vk_astronomical, vk_not_yet])
        else "FAIL"
    )

    result = {
        "experiment": "20260614-A08-zero-free-region",
        "constants": {"R_classical": float(R_CLASSICAL), "C_vk": float(C_VK)},
        "rows": rows,
        "vk_crossover": {
            "log10_t": round(cross_log10t, 1),
            "k_C_over_R_cubed": round(kval, 2),
            "note": "VK wider than classical only for t > 10^%.0f — astronomical" % cross_log10t,
        },
        "checks": {
            "sigma_zf_monotone_increasing": monotone_up,
            "gap_to_half_grows": gap_grows,
            "matches_reference": ref_ok,
            "boundary_in_critical_strip": in_strip,
            "vk_crossover_astronomical": vk_astronomical,
            "classical_wider_below_crossover": vk_not_yet,
        },
        "verdict": verdict,
        "interpretation": (
            "The proven zero-free boundary sigma_zf(t) moves toward Re=1 as t grows; "
            "the gap to Re=1/2 GROWS toward 0.5, it does NOT shrink. ZFR gives a sliver "
            "near Re=1, never near 1/2. VK beats classical only at t>10^%.0f. The gap to "
            "RH is QUALITATIVE — no better constant closes it; any sigma>1-f(t) with "
            "f(t)->0 yields sigma_zf->1. This is the 'wall' seen from the Re=1 side." % cross_log10t
        ),
    }
    (HERE / "metrics").mkdir(exist_ok=True)
    (HERE / "metrics" / "run.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # --- summary ---
    print("=" * 66)
    print(f"VERDICT: {verdict}")
    print("=" * 66)
    print(f"{'log10(t)':>9} {'sigma_zf':>10} {'sigma_VK':>10} {'gap to 1/2':>11} {'VK wider':>9}")
    for r in rows:
        print(
            f"{r['log10_t']:>9} {r['sigma_classical']:>10.5f} {r['sigma_vk']:>10.5f} "
            f"{r['gap_classical_to_half']:>11.5f} {str(r['vk_wider']):>9}"
        )
    print(f"\nsigma_zf monotone INCREASING (toward Re=1): {monotone_up}")
    print(f"gap to Re=1/2 GROWS (NOT shrinks): {gap_grows}")
    print(f"matches lit reference: {ref_ok}")
    print(f"VK overtakes classical only at t > 10^{cross_log10t:.0f} (k=(C/R)^3={kval:.1f})")
    print("\n-> ZFR boundary moves AWAY from Re=1/2. The gap is qualitative,")
    print("   not closable by better constants. The wall, seen from the Re=1 side.")


if __name__ == "__main__":
    main()
