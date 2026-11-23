# Привязка найденных в экспорте имён к `riemannHypothesis` (2026-11-23)

**Статус: `SOURCE_TRACED`.** Это граф ссылок по тексту исходников на коммите `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`, без компиляции и без проверки ядром. Файлы лежат в `verification/refgraph/`; sha256 файла `refgraph_result.json`: `afc99055…a982`.

## Метод

Узлы графа — короткие имена объявлений (последний компонент) из 175 187 файлов `src/`. Ребро A→B ставится, если имя B, объявленное в `src`, встречается в тексте объявления A; комментарии предварительно вырезаются. Обход в ширину идёт от тела `riemannHypothesis` (`Main.lean:4`, `:= rhOfAll`). Граф построен за 122 с: 23 894 879 рёбер.

Используются два варианта графа:
- **strict**: ребро в имя, которое объявлено в `src` больше одного раза, отбрасывается. Ложных совпадений меньше, но часть путей теряется.
- **loose**: все совпадения по имени. Это верхняя оценка с ложными путями.

Ограничения. Неявно используемые объявления (instance, simp-леммы, нотация, макросы) рёбрами не становятся. Совпадение коротких имён из разных пространств имён в варианте loose создаёт ложные пути.

## Контроль по экспорту (Gate 3)

Скан экспорта проверял 46 имён: 42 найдены, 4 отсутствуют. Если граф верен, найденные имена должны достигаться из пяти теорем, а отсутствующие — нет.

| | strict | loose |
|---|---|---|
| отсутствуют в экспорте (4): `f_mul_m_le`, `miStar2_of_families`, `miStar2_of_allTrue`, `joint_star_product_nonvanishing` | недостижимы все 4 | 3 недостижимы, `f_mul_m_le` достижим через `le` и `h` — **ложный путь** |
| найдены в экспорте (42) | достижимы 33; не достигаются 9: у 3 имён (`SizesAt`, `SizeT`, `IndefiniteRealisationConstantBounds`) несколько объявлений, 2 имени (`ElevenLe`, `DesignS`) не объявлены как константы с таким последним компонентом, ещё 4 (`zeroFree_of_rpow_window`, `lemmaL`, `windowHyp_of_rpow`, `CountsIrreducibilityConstants`) достигаются только в loose | 40 |

Ложных срабатываний у strict-графа на отсутствующих именах нет (0 из 4). Loose-граф контроль не прошёл, поэтому выводы ниже опираются только на strict.

## Результат

Из **одной** `riemannHypothesis` (от `rhOfAll`, без остальных четырёх теорем) в strict-графе достигаются `SizeKRel`, `szRow_sizeKRel`, `sizes_sizeKRel`, `MIstar2`, `miStar2_of_allTrue_alt_alt`, `wire4F_alt`, `wire_sel_alt`, `published_results_eigen`, `open0_of_unitary_group_hypotheses`, `allRows_of_open0_alt`, `row_rRows_stage0_alt`, `row_rRows_of_parts_alt`. Замыкание от `riemannHypothesis` содержит 252 121 имя, от всех пяти теорем — 252 126. Значит, вопрос «какой из пяти теорем принадлежит зависимость» практически снимается: замыкания совпадают с точностью до 5 имён.

Пути (strict). Рёбра, помеченные ✓, проверены вручную по тексту исходника (`[CODE]`):

- **`szRow_sizeKRel`**: `rhOfAll` ✓ `allChi` ✓ `everyCharacter` ✓ `everyCharacter_of_row` ✓ `every_character_of_literature_of_vWin` ✓ `every_character_of_theta_integrals_local_matching` ✓ `nonempty_hyps_definite_side_of_closed_bound` → `open0_of_unitary_group_hypotheses` ✓ `open_orbit_of_unramified_exponents_alt` ✓ (`hLam := real_group_inputs_combined_alt_alt`) `real_group_inputs_combined_alt_alt` ✓ `at_row_hLamP_alt_alt` ✓ `evP_params` ✓ `szRow_numAt` ✓ `szRow_sizesAt` ✓ `sizes_sizeKRel` ✓ `szRow_sizeKRel`.
  Шаг `nonempty_hyps…` → `open0_…` проверен (строка 58 `SiegelEisensteinSecondTermHypotheses.lean`).
- **`miStar2_of_allTrue_alt_alt`**: … `open_orbit_of_unramified_exponents_alt` ✓ (`hMi := main_theorem_published_inputs_third_alt_alt`) → `miStarRow_alt_alt` ✓ → `main_theorem_published_inputs_variant_alt_alt` ✓ → `miStarRowClosing_alt_alt` → `main_theorem_published_results_final_alt_alt` → `miStar_row_alt_alt` → `main_theorem_from_published_results_alt_alt_alt_alt_alt` → `miAt_of_truePack_alt_alt` → `main_theorem_from_published_results_alt_alt_alt_alt` ✓ → `miStar2_of_allTrue_alt_alt`. Последние шесть шагов, кроме последнего, вручную не проверялись.
- **`wire4F_alt`**: … `every_character_of_theta_integrals_local_matching` ✓ → `every_character_of_green_v_win` → `zero_free_all_of_green_v_win` → `shape_closed_link_n_of_green` → `wire_sel_alt` ✓ → `wire4F_alt`.
- **`MIstar2`**: … `every_character_of_green_v_win` → `DefiniteSideCondition` → `CovolumeOntoIsometryConditions` → `MIstar2`. Это связь через типы: условие используется в формулировке.

**Поправка к `miStar2_trace.md`:** цепочка `hMi` → `miStar2_of_allTrue_alt_alt` там верна по существу, но сокращена. Между `main_theorem_published_inputs_third_alt_alt` и `miStar2_of_allTrue_alt_alt` восемь промежуточных объявлений.

## Что это значит и чего не значит

- `[INFERRED]`: в исходнике `7cbf7a0c` доказательство `riemannHypothesis` текстуально ссылается (strict-путь) на `szRow_sizeKRel` и `miStar2_of_allTrue_alt_alt`. Вместе со сканом экспорта это две независимые линии: экспорт содержит имена, граф объясняет, через какие объявления они нужны.
- Это не проверка ядром. Ребро означает «имя встречается в тексте», а не «терм использует эту константу после элаборации». Тактика `first | exact A | exact B` может выбрать другую ветку. Короткое имя может быть разрешено в другое пространство имён.
- Совпадение экспорта с коммитом `7cbf7a0c` по хэшу не установлено (`OPEN`). Есть только косвенный признак: на 46 именах предсказания strict-графа не противоречат экспорту.
- Математическую роль `SizeKRel` для доказательства RH это не устанавливает. Таблица B2 (существенны соотношения 1, 2, 4) теперь относится к объявлению, достижимому из `riemannHypothesis`, но вопрос о том, где именно доказательство тратит запас по показателю, остаётся открытым.

Условие опровержения из `next_research_decision.md` («`szRow_sizeKRel` и `MIstar2` достижимы только из других четырёх теорем») **не выполнено**: оба достижимы из `rhOfAll`.
