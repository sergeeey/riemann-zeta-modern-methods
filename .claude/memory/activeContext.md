# activeContext — H-12 Гипотеза Римана
Обновлено: 2026-07-19

## Current Focus

**[2026-07-19, "давай всё по очереди"] Все 4 открытых пункта закрыты за один заход:**
1. PR #9, #10 смёржены в master (riemann-zeta-modern-methods) — потребовался доп. PR #11 (плюмбинг).
2. skeptic-engine-manuscript: 143MB CSV обойдён БЕЗ переписывания истории (cherry-pick на
   чистую ветку от origin/main) — PR #2 + попутный фикс предсуществующего ruff-бага PR #3,
   оба смёржены в Skeptic-Engine-2026-.
3. G3: `LANDSCAPE-NOTE.md` — draft v1 написан и закоммичен, синтез A-04..A-12 + B-01..B-07,
   НЕ прогнан через Submission Gate (это следующий шаг, если готовить к внешней публикации).
4. B-03 revival (близкая пара нулей): нашёл реальную задокументированную Lehmer-пару
   (γ≈7005.063/7005.101, WebSearch-подтверждена), 2 честные попытки трекинга под H_t —
   обе уткнулись в предел разрешения текущей числовой схемы на этом масштабе (тот же
   класс проблемы, что B-06). PARKED с конкретным revival condition в decision.md.

**Локальная ветка `feat/h12-track-c1-evidence-gate` всё ещё не запушена** — содержит
Track H, B-06, B-07, B-03 (+ revival attempt), LANDSCAPE-NOTE.md. Решение о PR/push — за
пользователем.


**[2026-07-19] Прогнаны 13 инструментов (skills/agents) на реальном материале проекта
(эксперимент пользователя "протестировать и оценить инструменты"). Track H (гигиена,
все находки инструментов) ЗАКРЫТ:**
- PLAN-2026H2.md §2 чекбоксы Track 0 отмечены (были невыполнены, хотя Track 0 назван DONE).
- ROADMAP.md БЛОК 1 синхронизирован (A-05..A-09,A-12 показывали 0%, хотя закрыты).
- SYNTHESIS.md: убран A-08 из "остающихся" (§6, противоречил §3), уточнена формулировка
  "три независимых подхода" (A-07/A-09/A-12 — НЕ включает A-06/B-02, которые производные).
- null_results/20260614-grant-rh-audit.md: добавлена запись о повторном source-audit
  (2026-07-19) — циркулярность подтверждена, НО sub-агент ошибочно заявил "два PDF
  идентичны" (проверено напрямую: pdfinfo/MD5 — разные файлы, 95стр/14стр, оригинальная
  запись от 14.06 была точна). Урок: чужой [VERIFIED] = наш [INFERRED] до проверки.
- requirements.txt создан (mpmath==1.3.0, sympy==1.14.0) — не было НИ ОДНОГО файла
  пиннинга зависимостей во всём проекте.
- src/zeta/toolkit.py: docstring `count_zeros_expected()` исправлен (была мёртвая функция
  с обещанием "completeness check", нигде не вызывается; A-04 использует mp.nzeros() вместо неё).
- sandbox/INDEX.md: dh-negative-control-battery — revival condition выполнено (Track C
  закрыт), помечено разблокированным, но ЕЩЁ НЕ НАЧАТО; rh-failure-taxonomy получил
  next_check дату (2026-08-15) вместо бессрочного "—".
- ~/.claude/hooks/estimand_guard.py (ГЛОБАЛЬНЫЙ хук, не project-scoped): исправлен баг —
  не парсил markdown-таблицы/заголовки-с-доп-текстом для MCID/ICE, давал false positive
  на всех 7 атомах в начале ЭТОЙ сессии. Проверено 7/7 позитивный + 1 негативный контроль
  (шаблон с настоящими плейсхолдерами всё ещё даёт unfilled=True).

**F1 (Speiser extended-T) ПОПРОБОВАН И PARKED в тот же заход.** Переиспользовал устойчивый
contour-метод A-07, расширил T=50→800. Результат: численная нестабильность (residual от
целого растёт 0.03→7), НЕ находка нулей ζ' слева от прямой. 2 диагностики (dps 30→50 —
улучшение ~40×; +сегментация контура — не сошлось за >15 мин). Оценка combinatorial-creativity
("дёшево, одна сессия") оказалась НЕВЕРНОЙ — тот же паттерн переоценки, что был у B-01/Connes.
Park: `sandbox/20260719-B06-speiser-extended-T/step1_verdict.md`. Revival: адаптивная точность
O(T) ИЛИ другой (не contour) метод счёта нулей ζ', отдельная сессия.

**B-07 (D-H negative control) СДЕЛАН в тот же заход, scoped down.** Реализовал D(s) через
Hurwitz zeta (формула перепроверена WebSearch, 2 независимых источника согласуются).
Функц. уравнение ξ(s)=ξ(1−s) верифицировано <1e-25 — [VERIFIED-tool]. Внелинейные нули
D(s) существуют по литературе (Davenport-Heilbronn 1936, AMS 2007) — [VERIFIED-REAL],
НЕ переоткрыты нами: 3/3 попытки grid+findroot (Im от 5 до 62) сошлись обратно на Re=0.5
ровно. Это 3-й раз за сессию (после B-01/Connes и F1/B-06/Speiser), когда оценка
"дёшево, одна сессия" от идея-генератора оказалась заниженной — стоит учитывать при
калибровке будущих оценок стоимости. Promoted: `experiments/20260719-B07-dh-negative-control/`.

**B-03 (de Bruijn-Newman heat flow) СДЕЛАН в тот же заход — PROMOTE, первый успех дня
с первой попытки.** Реализовал H_t(x)/Φ(u) (формула перепроверена WebSearch, MathWorld/
Wikipedia/arXiv:1801.05914 согласуются). Калибровка: H_0(2γ₁)≈-1.5e-19, H_0(2γ₂)≈2.3e-21
(против опубликованных нулей ζ — точное совпадение подтверждает формулу). Один хорошо
разделённый ноль отслежен на t∈[-0.05,0.05] — остаётся вещественным, движется монотонно,
БЕЗ Substrate Gate проблем (в отличие от B-06/B-07 сегодня). НЕ демонстрирует сам механизм
Rodgers-Tao (нужна близкая пара нулей — отдельная, более сложная задача, revival note в
decision.md). Promoted: `experiments/20260719-B03-de-bruijn-newman/`.

**PR #9 и #10 СМЁРЖЕНЫ в master (2026-07-19).** PR #10 базировался на ветке PR #9
(`chore/h12-track0-hygiene`), поэтому смёржился туда, не в master напрямую — потребовался
промежуточный PR #11 (чистый плюмбинг, тот же диф что #10, 0 нового контента) чтобы
довести до master. Итог: master = `5c342c6`, содержит Track 0 hygiene + Track C-1
evidence gate. Локальная ветка `feat/h12-track-c1-evidence-gate` с сегодняшними
коммитами (Track H, B-06, B-07, B-03) — НЕ запушена, ждёт решения пользователя
(новый PR или прямой push).

**Track R backlog на сегодня исчерпан** (B-01 parked вчера, B-02 weakened вчера, B-06
parked, B-07 promoted-scoped, B-03 promoted — 5 атомов за 2 дня). Следующий шаг: G3
(упаковка landscape note) — материала уже достаточно (SYNTHESIS.md + B-02 + B-03
иллюстрации), либо пауза, либо новый Track R кандидат (близкая пара нулей для B-03/
Rodgers-Tao — самый очевидный следующий шаг, если продолжать).

**skeptic-engine-manuscript ЗАКРЫТ (2026-07-19).** Проблема с 143MB CSV в истории
main решена БЕЗ переписывания истории: cherry-pick кейс-документа (2 файла, 128 строк)
на чистую ветку от origin/main → PR #2. Заодно CI поймал предсуществующий ruff-баг
в src/skeptic_toolkit/integrity.py (Optional[X] вместо X|None), не связанный с этим PR —
починен отдельным PR #3 (21/21 тестов прошли), смёржен первым, затем #2 обновлён и
смёржен тоже. Оба PR смёржены в https://github.com/sergeeey/Skeptic-Engine-2026-.
Локальная ветка `docs/h12-riemann-case-study` (со старой, проблемной историей) оставлена
как есть — не трогалась, не удалялась.

---

**[2026-07-19, ранее] B-02 ЗАКРЫТ — WEAKENED/illustration.** Сессия была прервана на диагностике
численного расхождения (I_N·log(N) растёт, не убывает к C=2+γ−log4π на N=10..3000),
продолжена и закрыта в тот же заход. Два контроля (negative control V=0→I=1; no-collapse
4 схемы квадратуры, разброс ≤0.03%) исключили баг реализации/интегрирования. Причина —
задокументированное самой статьёй (Bettin–Conrey–Farmer, §1: цитата про графики
Landreau–Richards) пред-асимптотическое поведение, тот же паттерн "стены", что в A-06/A-08.
Promoted: `experiments/20260717-B02-nyman-beurling/` (claim/estimand/controls/decision/
caveats/result_summary + run_b02.py + diagnose_quad.py). Реестры обновлены:
sandbox/INDEX.md (B-02 promoted), parked/INDEX.md (добавлена запись B-01, была пропущена
в предыдущей сессии).

**Следующий шаг:** пересортировка Track R бэклога по CDT-score (PLAN-2026H2.md §5.1) —
кандидат B-03 (de Bruijn–Newman, приоритет 3) либо переход к упаковке G3 (landscape note),
т.к. B-01 parked + B-02 weakened = 2 подряд не-PROMOTE сессии, но НЕ 2 NULL (обе дали
реальные pearls/выводы, Stop-rule §5.3 не сработал буквально — решение по факту, не автоматом).


**[2026-07-17] Действует PLAN-2026H2.md** (корень проекта). **TRACK C ПОЛНОСТЬЮ ЗАКРЫТ:**
- Track 0 DONE: коммит `3db6f1f` → **PR #9** (https://github.com/sergeeey/riemann-zeta-modern-methods/pull/9).
- Track C-1 (evidence gate) DONE: 11/11 catches TRACE-OK. Числовые перепроверки (#8 crossover 10³⁸⁷⁷, #11 Robin 26 exceptions) PASS. V5 cross-model review (Codex gpt-5.5, независимая модель, Context Asymmetry) — 3/3 CONFIRMED (Grant Doc A 9/10, Thm 5.3 10/10, Li circularity 9/10). Коммит `ef8a19c` → **PR #10** (base: PR #9, мёржить после него) (https://github.com/sergeeey/riemann-zeta-modern-methods/pull/10).
- Track C-2 DONE: кейс перенесён в `E:\skeptic-engine-manuscript\docs\case-study-riemann-hypothesis.md` (+ запись в docs/README.md), коммит `8798149` на ветке `docs/h12-riemann-case-study` (main repo, Zenodo DOI). **НЕ запушено** — `origin/main` того репо на 12+ коммитов позади локального main из-за старого коммита `42709e6` с 143MB CSV (>GitHub лимит), блокирует push. Не трогать без явного решения пользователя (переписывание истории). Кейс явно помечен как cross-domain (логический review, не статистический AUC-детектор) — вопрос о product scope оставлен открытым в самом документе.

**gh auth фикс:** `GH_TOKEN` env var сломан (invalid), но keyring-токен рабочий → используй `env -u GH_TOKEN gh ...` для любых gh-команд в этой среде.

**Открыто:** PR #9 и #10 в riemann-zeta-modern-methods ждут ревью/мёржа пользователем. skeptic-engine-manuscript: large-file проблема в main — отдельная задача, не начата.

**Track R начат: B-01 PARKED (2026-07-17), не FALSIFIED.** Прочитал оба источника целиком
(arXiv:2602.04022 + arXiv:2106.01715 Connes-Consani) — claim реален, не выдумка, но точный
рецепт = многоступенчатый эмпирический pipeline (скан по α + D(α,k) + D₀(α) + eigenvector-
matching), не разовый скрипт. Реальная стоимость — недели, не сессии; kill criterion превышен
на порядок. Разбор: `sandbox/20260717-B01-connes-replication/step1_verdict.md`. Приоритет
Track R сдвинут: **B-02 (Nyman–Beurling численно) теперь #1** — см. PLAN-2026H2.md §4.

Внешний каталог 100 направлений (ChatGPT) запаркован: `sandbox/20260717-external-100-rh-programs.md`
(6/10). D-H negative-control идея parked (revival: после Track C — теперь свободна).

**Следующий шаг:** B-02 (Nyman–Beurling / Báez-Duarte численно) — новый Шаг 1 не начат.

Прежний фокус (Phase 4, 2026-06-14):
**Phase 4: H-12 → актив для Skeptic Engine (#1)**
8 атомов + Grant REJECT + SYNTHESIS.md + **SKEPTIC-ENGINE-CASE.md** (PR #8, master 5cf1685).
H-12 переосмыслен как demo-актив главного проекта: 11 пойманных циркулярностей/завышений
(2 у Grant + МОЯ A-06 + tautology/overclaim/bug). Headline: скептик поймал собственную
ошибку автора (A-06 = та же что Grant Doc A). H-12 как research закрыт; ценность = живой
proof-of-concept Skeptic Engine. Дальше: перенести кейс в E:\skeptic-engine-manuscript ИЛИ пауза.

## История атомов (8, все в master)
A-10 ✅ · A-09 ✅ · A-12 ✅(calib) · A-04 ✅ SOLID · A-07 ✅ · A-05 ✅ · A-08 ✅ · A-06 ✅ · Grant ✅ REJECT

## A-06 итог (Robin & Li, 2026-06-14)
- Robin: σ(n)<e^γ·n·ln ln n держится до 10⁴, 26 исключений (≤5040, не 27 — tool поправил MEMORY), ratio<1 для n≥5041. ГЕНУИННО (не использует нули).
- Li: первая версия ЦИРКУЛЯРНА (клал ρ=½+iγ = assumed RH) — skeptic поймал, ТА ЖЕ ошибка что у Grant Doc A! Исправлено: λ₁=0.0231 через zero-free формулу (genuine), from-zeros помечены illustrative.
- **Главный урок:** сессионный паттерн (assume Re=½ = circular) укусил МЕНЯ; skeptic-loop поймал собственную ошибку → доказательство что методология работает.
- Папка: experiments/20260614-A06-robin-li/
Главный вывод: стена = полоска a/lnT у прямой. Две грани: A-08 (сверху, ZFR→Re=1) ⊕ A-07 (снизу, 41.7% на ½).
Проект НЕ доказал RH (и не претендует) — картировал ландшафт + честная методология.
Дальше (опц.): publishable computational-landscape note / остальные атомы низкоценны / пауза.

## A-08 итог (zero-free region, 2026-06-14)
- σ_zf(t)=1−1/(R·ln t), R=5.558691 (MTY 2022). Граница УХОДИТ к Re=1, разрыв до ½ РАСТЁТ 0.46→0.4996.
- Опровергает заблуждение «ZFR приближается к ½». VK обгоняет классику лишь при t>10³⁸⁷⁷ (мой расчёт; агентский 10⁴³⁴ ОШИБОЧЕН, подтвердили skeptic+reviewer).
- Skeptic [WEAKENED] КРИТИЧНО: «не приближается к ½» только для POINTWISE ZFR; density+A-07 (41.7% на ½) — другое. Разграничено в CAVEAT-1.
- Reviewer LGTM (findroot bracket + mkdir). R на веру MTY 2022 (REF self-consistent).
- Папка: experiments/20260614-A08-zero-free-region/. SYNTHESIS.md обновлён (дуальность A-07/A-08).

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
- [2026-07-19 22:27] `3b99949`: docs(H-12): B-03 close-pair revival condition — attempted, parked
- [2026-07-19 22:17] `b1bc3c4`: docs(H-12): draft G3 landscape note synthesizing A-04..A-12 + B-01..B-07
- [2026-07-19 22:16] `ffdebaf`: docs(H-12): log skeptic-engine-manuscript CSV history fix
- [2026-07-19 22:06] `4d4f0f4`: docs(H-12): log PR #9/#10/#11 merge into master
- [2026-07-19 21:54] `4d4f0f4`: docs(H-12): log PR #9/#10/#11 merge into master
- [2026-07-19 21:44] `7c225d8`: feat(H-12): B-03 de Bruijn-Newman heat flow — PROMOTE (illustration)
- [2026-07-19 21:34] `1cb442c`: feat(H-12): B-07 Davenport-Heilbronn negative control (scoped down)
- [2026-07-19 21:15] `ffa70c0`: feat(H-12): B-06 Speiser extended-T — attempted, parked (numerical instability)
- [2026-07-19 20:43] `bb30f66`: chore(H-12): Track H hygiene — fix findings from 10-tool test pass
- [2026-07-19 19:24] `468ecc2`: feat(H-12): close B-02 Nyman-Beurling atom — WEAKENED/illustration + B-01 index entry
- [2026-07-17 05:55] `ef8a19c`: feat(H-12): close Track C-1 evidence gate — V5 cross-model review + numeric reruns
- [2026-07-17 05:39] `ef8a19c`: feat(H-12): close Track C-1 evidence gate — V5 cross-model review + numeric reruns
- [2026-07-17 05:27] `3db6f1f`: chore(H-12): Track 0 hygiene — commit evolution/ + sandbox recon, sync PLAN-2026H2
- [2026-06-14 15:37] `cfbf0d5`: docs: Skeptic Engine case study — 11 caught circularities & overclaims on RH
- [2026-06-14 15:25] `885cede`: chore(A-06): remove unverified skeptic draft script
- [2026-06-14 15:05] `531c67b`: feat(A-08): zero-free region — the gap to Re=1/2 grows, not shrinks
- [2026-06-14 14:43] `1e5e3d8`: docs: project synthesis — landscape map across 6 atoms
- [2026-06-14 14:41] `d1d3e71`: feat(A-05): prime error term — what RH buys
- [2026-06-14 14:26] `1ce20b6`: feat(A-07): Levinson density + Speiser — the 41% wall is structural
- [2026-06-14 14:07] `0254706`: feat(H-12): research infra + A-04 verifier; Grant REJECT, Zenodo parked
- [2026-06-14 13:56] `3118809`: feat(A-12): Hilbert-Polya — operator direction closed for proof
- [2026-06-14] `bd3736e` init · `c915e98`/`dfa6770` A-10
