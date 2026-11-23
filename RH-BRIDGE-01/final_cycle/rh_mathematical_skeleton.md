# Карта каркаса доказательства `riemannHypothesis` (этап B1, 2026-11-23)

**Статус: `SOURCE_TRACED`.** Это граф ссылок по тексту исходников Lean, коммит `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` (175 187 файлов). Ядро Lean не запускалось, полная сборка и новый скан экспорта не делались. Соответствие большого экспорта этому коммиту по хэшу не установлено (`OPEN`).

Код и данные: `skeleton/` (`skel_graph.py`, `skeleton_result.json`, `edge_lines.out`, `bypass_paths.json`, `check_first_alt.out`, `defs.out`, `tree_children.out`). Запуск: `bash skeleton/run_skel.sh` в WSL (одно ядро, около 6 мин).

## 0. Что именно здесь утверждается

Три уровня, которые нельзя смешивать:

| Уровень | Что означает | Чем подтверждается здесь |
|---|---|---|
| **Синтаксическая ссылка** | идентификатор B стоит в тексте объявления A | автоматически для каждого ребра путей и вручную по строке исходника (`edge_lines.out`) |
| **Декларационная зависимость** | терм доказательства A содержит константу B | `SOURCE_TRACED` для рёбер в терм-режиме; для `by`-блоков и `first | exact …` это правдоподобно, но без элаборации не доказано |
| **Математическая незаменимость** | без B утверждение A доказать нельзя | **нигде не установлена**; доминатор в графе — только кандидат |

Доминатор узла `t` — узел `d`, через который проходит каждый путь `rhOfAll → t` в графе. Если граф неполон (не учтены неявные использования), настоящий обход мог не попасть в граф, и `d` ложно выглядит обязательным. Поэтому каждый доминатор ниже помечен как кандидат, а не как необходимая зависимость.

## 1. Как построено

Узлы — короткие имена объявлений (последний компонент) в `src/`; ребро A→B, если B встречается словом в тексте объявления A (комментарии вырезаны). Корень — `rhOfAll`, то есть единственный вызов в `Main.lean:4` (`riemannHypothesis := rhOfAll`).

- **strict**: рёбра в имена, объявленные в `src` больше одного раза, отброшены. Достижимо 252 121 имя из 759 411 (повторяет результат `rh_attribution.md`: 252 121). Контроль: 0 из 4 имён, которых нет в экспорте, достижимы.
- **mid** (проверка устойчивости): strict плюс рёбра в имена с 2–5 объявлениями. В нём отброшено 6 121 791 рёбер из достижимых вершин, поэтому он ловит обходы через неоднозначные имена, но порождает и ложные.

## 2. Верхний слой (все рёбра проверены по строкам исходника)

| # | узел | файл:строка | что делает |
|---|---|---|---|
| 0 | `rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi` | `Supplements/Kernels/MainTheorems.lean:9` | RH из утверждения `EveryCharacter` |
| 1 | `allChi : EveryCharacter := FinalTheorems.everyCharacter` | `MainTheorems.lean:7` | |
| 2 | `everyCharacter := everyCharacter_of_row Gal.Int.galoisLocalGlobalStrong_recParameter` | `CharacterBoxes/MainConclusion.lean:11` | подставляет источник строки `Row0b` |
| 3 | `everyCharacter_of_row (h : Row0b recT) := every_character_of_literature_of_vWin ⟨h, recTExists, h⟩ (vwin_of_row h)` | `MainConclusion.lean:8` | строит `OpenLiteratureStatements` из `h` и окно `VWin` |
| 4 | `every_character_of_literature_of_vWin (O) (hV : VWin)` | `…/EveryCharacterOfLiteratureOfVWin.lean:810` | строка 811: `every_character_of_theta_integrals_local_matching (published_results_eigen O) …` |
| 5 | `every_character_of_theta_integrals_local_matching (P F hA hM hX hL hV)` | `…/SiegelEisensteinSecondTermHypotheses.lean:69` | строки 72–73: `every_character_of_green_v_win` и `nonempty_hyps_definite_side_of_closed_bound` |

Смысл узлов (определения из `defs.out`):
- `EveryCharacter` — для всех `N`, характеров Дирихле `χ` по модулю `N` и `s` с `Re s > 1/2` (кроме полюса) `L(χ, s) ≠ 0`. RH выводится из него через `N = 1` (`CritLine.lean:29`).
- `OpenLiteratureStatements` — структура из трёх полей: `Row` (Carayani local-global), `RecTExists` (локальная Ленглендсова), `Row` (Галуа для поляризованной пары).
- `Row0b` — существование галуа-представления с нужными свойствами для всех CM-полей `E` и поляризованных пар `(π, χ)`; источник — `galoisRepresentations_of_thetaLift tLiftK` (`RowSrc.lean:6`).
- `VWin` — `∀ ψ, VWinAt ψ 401`: окно по характерам.

## 3. Дерево по доминируемым поддеревьям (strict, корень `rhOfAll`)

Размер — число имён, чьи все пути проходят через узел. Видно, где сосредоточен вес:

```
rhOfAll                                         252121
└ allChi → everyCharacter                       220878
   ├ everyCharacter_of_row                      205127
   │  ├ every_character_of_literature_of_vWin   172181
   │  │  ├ every_character_of_theta_integrals_local_matching  115739
   │  │  │  ├ nonempty_hyps_definite_side_of_closed_bound      97799
   │  │  │  │  ├ hypotheses_nonempty_of_unramified_exponents_alt  26575
   │  │  │  │  │   (allRows_of_open0_alt 11841; large_unramified_exponent_bundles_exist_alt 9654)
   │  │  │  │  ├ ontoX_and_lamLow_of_unitaryGroupHypotheses'  10415
   │  │  │  │  └ open0_of_unitary_group_hypotheses             5151 → open_orbit_of_unramified_exponents_alt 5150
   │  │  │  └ every_character_of_green_v_win                      8325 → zero_free_all_of_green_v_win 8321
   │  │  ├ topCovolSlim2_use_alt_alt        15596
   │  │  ├ published_results_arithmetic      2405;  toroidalForFanKS 2671
   │  │  └ published_results_eigen           1808
   │  └ vwin_of_row                          13860 → automorphic_window_of_inputs → … → vwin_of_hypotheses_H_E_alt (цепочка окна)
   └ galoisLocalGlobalStrong_recParameter     8037
```

Вес разделён на три крупные ветви под `everyCharacter_of_row`: основная машина через `every_character_of_literature_of_vWin` (172 тыс.), ветвь окна `vwin_of_row` (13,9 тыс.) и источник строки (8 тыс.). Ветвь окна соответствует критерию окна, который разбирался раньше (`windowHyp_of_rpow`, `zeroFree_of_rpow_window` из экспортного скана принадлежат этой ветви).

## 4. Три ветви к целевым именам

Пути ниже — кратчайшие в strict; каждое ребро проверено по строке исходника (`edge_lines.out`, колонка «closure = True»: модуль B входит в импорт-замыкание модуля A).

### 4.1. `szRow_sizeKRel` (16 звеньев)

`rhOfAll → allChi → everyCharacter → everyCharacter_of_row → every_character_of_literature_of_vWin → every_character_of_theta_integrals_local_matching → nonempty_hyps_definite_side_of_closed_bound → open0_of_unitary_group_hypotheses → open_orbit_of_unramified_exponents_alt → real_group_inputs_combined_alt_alt → at_row_hLamP_alt_alt → evP_params → szRow_numAt → szRow_sizesAt → sizes_sizeKRel → szRow_sizeKRel`

Опорные строки:
- `OpenOrbitOfUnramifiedExponents.lean:56`: `hLam := real_group_inputs_combined_alt_alt …`;
- `RealGroupInputsCombined.lean:23`: `obtain ⟨c1, hN⟩ := szRow_numAt eps he he52 C hStd`;
- `SzRowElevenLeSplitBound.lean:39`: `szRow_sizesAt` собирается как цепочка `.and` из `sizes_sizeN_…`, `sizes_sizeKRel`, … (одна из конъюнкций набора размеров);
- `SzRowSizeKRelStatement.lean:8`: `sizes_sizeKRel := first | exact @szRow_sizeKRel | exact szRow_sizeKRel | (intros; apply szRow_sizeKRel <;> assumption)`.

Доминаторы (strict): `…`, `nonempty_hyps_definite_side_of_closed_bound`, `szRow_numAt` (поддерево 121), `szRow_sizesAt` (30), `sizes_sizeKRel` (4), `szRow_sizeKRel` (2). Узкая шея в mid-графе (обходов нет): **`szRow_sizesAt` и `sizes_sizeKRel`**. Это подтверждено и по исходнику: `szRow_sizeKRel` называется только в двух файлах (`SzRowSizeKRel.lean`, `SzRowSizeKRelStatement.lean`), `sizes_sizeKRel` — только в `SzRowSizeKRelStatement.lean` и `SzRowElevenLeSplitBound.lean`.

Вывод: `szRow_sizeKRel` входит в доказательство только как одна из конъюнкций набора `SizesAt`, сам набор используется в доказательстве `szRow_numAt`. Узлы выше `szRow_sizesAt` (включая `szRow_numAt`) обязательными не показаны: есть обход через `topCovolSlim2_use_alt_alt → … → val_sizes_at_alt → szRow_sizesAt` (в mid-графе, одно звено неоднозначное, `parameters_scale_rank_gap_bounds`, три объявления; путь правдоподобен, не проверен).

### 4.2. `miStar2_of_allTrue_alt_alt` (19 звеньев, чистая цепочка)

`… → nonempty_hyps_definite_side_of_closed_bound → open0_of_unitary_group_hypotheses → open_orbit_of_unramified_exponents_alt → main_theorem_published_inputs_third_alt_alt → miStarRow_alt_alt → main_theorem_published_inputs_variant_alt_alt → miStarRowClosing_alt_alt → main_theorem_published_results_final_alt_alt → miStar_row_alt_alt → main_theorem_from_published_results_alt_alt_alt_alt_alt → miAt_of_truePack_alt_alt → main_theorem_from_published_results_alt_alt_alt_alt → miStar2_of_allTrue_alt_alt`

- Каждое из 19 звеньев — доминатор, и все 17 внутренних узлов **выживают в mid-графе** (`rob_miStar2_chain.out`). Это самый устойчивый результат карты.
- Опорные строки: `OpenOrbitOfUnramifiedExponents.lean:50` (`hMi := main_theorem_published_inputs_third_alt_alt …`), затем `exact ⟨…, hMi.2, …⟩` в конце того же доказательства.
- Почти все звенья — обёртки: `X := first | exact @Y | exact Y | (intros; apply Y <;> assumption)` (`check_first_alt.out`: во всех шести случаях все три альтернативы называют одну и ту же константу, ветка не меняет зависимость). Содержательны только звенья с `have hE := …` и `exact …` без `first`: `miStarRow_alt_alt`, `miStarRowClosing_alt_alt`, `miStar_row_alt_alt`, `miAt_of_truePack_alt_alt`.
- **Поправка к `miStar2_trace.md`**: между `main_theorem_published_inputs_third_alt_alt` и `miStar2_of_allTrue_alt_alt` восемь промежуточных объявлений, а не прямая ссылка.

### 4.3. `MIstar2` (10 звеньев)

`… → every_character_of_theta_integrals_local_matching → every_character_of_green_v_win → DefiniteSideCondition → CovolumeOntoIsometryConditions → MIstar2`

- `TopPlug.lean:17`: `every_character_of_green_v_win … (h : Nonempty (HypsAlt … DefiniteSideCondition))`;
- `DefiniteSideCondition.lean:27`: `(hP : CovolumeOntoIsometryConditions …)`;
- `BaseLiftsPackageOfPrimitiveLinks.lean:237`: поле структуры `miStar : (R.toCx3 F).MIstar2 (F.eV …) sEE`.

Здесь `MIstar2` — **часть формулировки гипотезы** (тип поля), а не терм-доказательство. Доказательство экземпляра приходит по ветви 4.2 (`hMi.2` → поле `mi`). Доминаторов у `MIstar2` немного (7 до `every_character_of_theta_integrals_local_matching`), потому что до него есть вторая дорога через `nonempty_hyps_definite_side_of_closed_bound → DefiniteSideCondition` (так в графе; вхождение в текст формулировки этой теоремы вручную не проверено).

### 4.4. `wire4F_alt` (11 звеньев, чистая цепочка)

`… → every_character_of_theta_integrals_local_matching → every_character_of_green_v_win → zero_free_all_of_green_v_win → shape_closed_link_n_of_green → wire_sel_alt → wire4F_alt`

- `TopPlug.lean:18` → `zero_free_all_of_green_v_win`; `TopPlug.lean:15` → `shape_closed_link_n_of_green`;
- `TopShape.lean:46`: `… GlobalTheory.Top.wire_sel_alt 𝒜 sel selS …`;
- `WireSel.lean:50`: `exact Formalism.L2.Top4Wire2.wire4F_alt (…) hPA …`.

Это ветвь `zero_free_all_of_green_v_win` (`Formalism.HC.ZeroFreeAll`): нулевая свобода из зелёного условия и окна. Все 9 внутренних узлов выживают в mid-графе, обходов нет.

## 5. Устойчивость доминаторов (результат проверки в mid-графе)

| цель | цепочка | выживают в mid | обходы в mid |
|---|---|---|---|
| `szRow_sizeKRel` | 11 | `szRow_sizesAt`, `sizes_sizeKRel` | 7 верхних узлов (см. ниже) |
| `miStar2_of_allTrue_alt_alt` | 19 | все 17 внутренних | нет |
| `wire4F_alt` | 11 | все 9 внутренних | нет |
| `open0_of_unitary_group_hypotheses` | 8 | 6 верхних | нет |
| `published_results_eigen` | 6 | 4 верхних | нет |
| `MIstar2` | 7 | нет | 5 (в т. ч. оба верхних звена, см. 4.3) |
| `SizeKRel` (само определение) | 11 | нет | все; `SizeKRel` ещё входит в набор `SizesAt` (5 объявлений) |

**Разбор обходов для `szRow_sizeKRel`** (`bypass_paths.json`, проверка по исходнику):
- обход мимо `allChi` идёт `rh_of_every → rh_of_right → intro(4) → …`: имя `intro` (четыре объявления) — артефакт, сам `rh_of_every` явно получает `allChi` как аргумент (`MainTheorems.lean:9`);
- обходы мимо `everyCharacter_of_row`, `every_character_of_theta_integrals_local_matching`, `nonempty_hyps_definite_side_of_closed_bound` идут `galoisLocalGlobalStrong_recParameter → recT(5) → recX(3) → recS(2) → designS → szRow_numAt`. Проверено: в `galoisLocalGlobalStrong_recParameter` (`RowSrc.lean:6`) имеется в виду `recT` из `Development.lean:18` (`fun h rc => IsRecT h rc`), который `recX` не вызывает; остальные `recT`/`recX`/`recS` — другие объявления с теми же именами. **Артефакт склейки имён.**
- обход мимо `szRow_numAt` (через `topCovolSlim2_use_alt_alt`) не опровергнут.

## 6. Что из этого следует для рецензента

1. Основание `riemannHypothesis`: единственная терм-зависимость от `rh_of_every` и `allChi`; `EveryCharacter` доказана из `Row0b` для источника `tLiftK` плюс набор «опубликованных» входов `OpenLiteratureStatements`/`UnitaryGroupThirdPlaceHypotheses` (ветвь `published_results_eigen`, 1808 имён).
2. Наименьшие по размеру ветви, с которых удобнее начинать чтение: ветвь окна `vwin_of_row` (13,9 тыс. имён) и ветвь `zero_free_all_of_green_v_win` (8,3 тыс.), в которой лежит `wire4F_alt`.
3. Нагруженная часть: `nonempty_hyps_definite_side_of_closed_bound` (97,8 тыс. имён) — здесь строится `Nonempty (HypsAlt … DefiniteSideCondition)`; именно от неё зависят `open0_of_unitary_group_hypotheses` (5,2 тыс.), `allRows_of_open0_alt` (11,8 тыс.), цепочка `miStar2_of_allTrue_alt_alt` и ветвь размеров `szRow_*`.
4. Размеры `SizeKRel` и т. п. в доказательстве образуют блок `SizesAt` (набор конъюнкций), входящий в `szRow_numAt`. Из графа **не следует**, что соотношения №1, №2 и №4 из прежней таблицы B2 математически необходимы: граф показывает только присутствие объявления `szRow_sizeKRel` в замыкании, но не запас по показателю.

## 7. Неполнота и ограничения

- **Неявные зависимости не учтены**: instances, simp-наборы, нотация, макросы, `open`/`export`. Зависимость, которая идёт только через них, в графе отсутствует.
- **Короткие имена**: узлы — последние компоненты. В strict ребро в неоднозначное имя отброшено (6,1 млн рёбер), в mid оно добавлено вместе с ложными.
- **Тактики**: ссылки внутри `by`-блоков считаются, но без элаборации неизвестно, какая из них реально попала в терм; для `first | exact …` проверено, что альтернативы называют одну константу.
- **Экспорт не привязан к коммиту** (`OPEN`): граф описывает исходник `7cbf7a0c`, а не экспорт 7,7 ГБ. Косвенная проверка: на 46 именах скана строгий граф не противоречит экспорту (0 из 4 отсутствующих достижимы; подробности в `rh_attribution.md`).
- **Доминаторы — кандидаты.** Подтверждены для ветвей 4.2 и 4.4 (устойчивы в mid), для 4.1 только `szRow_sizesAt` и `sizes_sizeKRel`, для 4.3 нет. Математическая незаменимость не доказана ни для одного узла.

## 8. Статусы

| утверждение | статус |
|---|---|
| верхняя цепочка `rhOfAll → … → every_character_of_theta_integrals_local_matching` | `SOURCE_TRACED` (термы, строки приведены) |
| пути к `szRow_sizeKRel`, `miStar2_of_allTrue_alt_alt`, `MIstar2`, `wire4F_alt`, `published_results_eigen` | `SOURCE_TRACED` |
| доминаторные цепочки 4.2 и 4.4 | `SOURCE_TRACED`, устойчивы в mid-графе |
| `szRow_sizesAt`, `sizes_sizeKRel` — единственные пути к `szRow_sizeKRel` | `SOURCE_TRACED` + grep по всем файлам |
| остальные доминаторы | `CONDITIONAL` (кандидаты) |
| математическая необходимость `SizeKRel`/`MIstar2`/`wire4F_alt` | `OPEN` |
| привязка к экспорту по хэшу | `OPEN` |
| проверка ядром Lean | `NOT_RUN` |
