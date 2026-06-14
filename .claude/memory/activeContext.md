# activeContext — H-12 Гипотеза Римана
Обновлено: 2026-06-14

## Current Focus
**Phase 3: Синтез**
A-10 ✅ · A-09 ✅ · A-12 ✅(calib) · A-04 ✅ SOLID · A-07 ✅ · A-05 ✅ · Grant ✅ REJECT
6 атомов готовы. Идёт синтез проекта.

## A-05 итог (prime error, 2026-06-14)
- π(x) точно (sympy) vs li(x) до 10⁷. Ошибка li−π внутри границы фон Коха/Schoenfeld.
- ratio |err|/bound убывает 0.47→0.17 (x≥2657) — ошибка растёт медленнее √x·lnx. RH-consistent.
- "Что RH даёт": наименьшая ошибка в ТПЧ O(√x·lnx). Реальный результат (не тавтология), но классический.
- Skeptic [WEAKENED]: bias li>π НЕ универсален (Littlewood, Skewes ~10³¹⁶) — усилено warning в выводе+фигуре. Reviewer LGTM.
- Папка: experiments/20260614-A05-prime-error/

## A-07 итог (Levinson density + Speiser, 2026-06-14)
- Обзор: ceiling ~41% СТРУКТУРНЫЙ (нули ζ' в полоске ½≤σ<½+a/lnT). Рекорд PRZZ 41.7% (2020), не Pratt.
- Speiser численно до Im=50: слева от прямой 0 нулей ζ' (⟺ RH), справа 5 нулей все Re>½ (совпали с эталоном 1e-6).
- ζ' API проверен (vs mp.diff 1e-15). Skeptic [WEAKENED]: "иллюстрирует Левинсона" завышено (Speiser≠mollifier); результат не новый. Честно ослаблено.
- **CONVERGENCE (главный вывод сессии):** A-09 (GUE=evidence) + A-12 (нет оператора) + A-07 (density упирается в стену) → ВСЕ классические пути упираются в одно: поведение нулей вплотную к прямой (a/lnT strip).
- Папка: experiments/20260614-A07-levinson-density/

## A-04 итог (Hardy Z + Turing, 2026-06-14)
- Верификатор RH-в-окне: 138 нулей до T=300, все на Re=½. **SOLID-IN-WINDOW**.
- Два независимых алгоритма: смены знака Hardy Z(t) == mp.nzeros (Turing) → off-line нулей нет.
- skeptic NEEDS-STRICTER (точечный S(T) ≠ интеграл Тьюринга) → усилен mp.nzeros → SOLID.
- Caveat: НЕ доказательство (окно); известно с Hutchinson 1925; не cross-library (оба mpmath).
- sandbox → promoted `experiments/20260614-A04-hardy-Z/` (claim/controls/decision).
- Next (опц.): T=1000+ ИЛИ argument-principle contour (cross-library независимость).

## Инфра сессии (коммит 0254706)
- sandbox/ (буфер) + null_results/ (Grant REJECT) + parked/ (Zenodo A-12) + ROADMAP.md + Excel-зеркало
- ⚠️ Коммит ушёл на ветку **feature/a07-levinson-density**, НЕ master. Решить merge/rename при возврате.

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
- [2026-06-14 14:26] `1ce20b6`: feat(A-07): Levinson density + Speiser — the 41% wall is structural
- [2026-06-14 14:07] `0254706`: feat(H-12): research infra + A-04 verifier; Grant REJECT, Zenodo parked
- [2026-06-14 13:56] `3118809`: feat(A-12): Hilbert-Polya — operator direction closed for proof
- [2026-06-14] `bd3736e` init · `c915e98`/`dfa6770` A-10
