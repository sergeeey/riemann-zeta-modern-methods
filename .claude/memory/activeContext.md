# activeContext — H-12 Гипотеза Римана
Обновлено: 2026-06-14

## Current Focus
**Phase 2: Эксперименты по атомам**
A-10 ✅ PROMOTE · A-09 ✅ PROMOTE · Grant-audit ✅ REJECT
Следующий: A-12 (Hilbert-Pólya) / A-05 (простые числа).

## A-09 итог (RMT-статистика, 2026-06-14)
- 2000 нулей (T 14–2515): level repulsion, GUE не Poisson
- KS_gue=0.041 vs KS_poisson=0.317 (p=10⁻¹⁷⁸); <s²>=1.15 (GUE 1.18, Poisson 2.0)
- 5 sub-bands все → GUE; 2 независимых Poisson-контроля → Poisson (pipeline честный)
- scipy независимо подтвердил все числа (skeptic_attack.py)
- skeptic [WEAKENED]: claim = evidence не proof; surmise ≠ exact GUE; finite-T
- reviewer LGTM. Папка: experiments/20260614-A09-rmt-statistics/
- Вывод: эмпирическая опора Гильберта-Пойа (A-12)

## A-10 итог (вычислительная база, 2026-06-14)
- Toolkit src/zeta/ построен и валидирован (skeptic + reviewer)
- 100 нулей на Re=½, Turing-полнота до T≈237, off-line детектор (контур) до T≈66
- Reviewer P0 (findroot) был latent, исправлен. Папка: experiments/20260614-A10-computational-base/

## Grant-audit ЗАВЕРШЁН — REJECT (2026-06-14)
HD-MAVP аудит двух Grant (2026) PDF про RH. Вердикт: ОБА не доказывают RH.
- Doc A (Эйзенштейн, 14стр): циркулярен — §9 Step 4 кладёт |Σx^ρ/ρ|=O(√x) = сама RH (von Koch)
- Doc B (iHarmonic, 95стр): условен по тексту АВТОРА (стр.87); Spectral Isomorphism = Conjecture
- Thm 5.3 численно ЛОЖНА [VERIFIED-tool]; нумерология (α в границе счёта простых)
- Запись: `null_results/20260614-grant-rh-audit.md`. Grant papers НЕ фундамент.

## Phase 1 (завершена)
Оригинал 1859, что доказано, атомизация (14 атомов A-01..A-14), deep research.
Файлы: riemann_foundation.md, riemann_atoms.md, riemann_approaches.md

## Запрещено делать сейчас
- Открывать Grant papers как источник истины (проверено: REJECT)

## Auto-commit log
- [2026-06-14] `bd3736e` init · `c915e98`/`dfa6770` A-10
