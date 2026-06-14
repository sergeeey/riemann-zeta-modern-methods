# activeContext — H-12 Гипотеза Римана
Обновлено: 2026-06-14

## Current Focus
**Phase 2: Эксперименты по атомам**
A-10 ✅ PROMOTE · A-09 ✅ PROMOTE · A-12 ✅ PROMOTE(calib) · Grant ✅ REJECT
Следующий: A-05 (простые числа) / A-07 (плотность Левинсона).

## A-12 итог (Hilbert-Pólya, 2026-06-14)
- Обзор 5 кандидатов на оператор: ВСЕ [HYPOTHESIS] или [REFUTED]. Оператор не построен за 110+ лет.
- Berry-Keating xp: даёт ПЛОТНОСТЬ нулей (сколько), НЕ положения (где). S(T) не воспроизводится.
- ВАЖНО (skeptic): результат НЕ новый — переоткрывает Berry-Keating 1999 + Selberg 1946.
  weyl_err·T=1/(48π) = тавтология (3-й член Stirling θ), подтверждено до T=5e5. Framing был завышен, исправлен.
- Ценность для проекта: honest boundary + калибровка toolkit. НЕ вклад.
- **Направление "построить оператор" ЗАКРЫТО для доказательства.** A-09 GUE = evidence, не путь.
- Папка: experiments/20260614-A12-hilbert-polya/

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
- Строить A-12 на Zenodo-самопубликациях 2025 (parked: 20260614-hilbert-polya-zenodo-cluster).
  Вход в A-12 — ТОЛЬКО через рецензируемое: BBM 2017 (PRL) + критика Bellissard, inverse-scattering 2002 (Springer), Connes/Berry-Keating.
- Тавтологичные numeric-тесты «спектр оператора = нули» при circular-входе (Validation Theater). Только negative-control / out-of-sample / self-adjointness.

## Auto-commit log
- [2026-06-14] `bd3736e` init · `c915e98`/`dfa6770` A-10
