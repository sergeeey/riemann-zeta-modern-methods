# Карта зависимостей: от RiemannHypothesis до арифметических входов (H12-BRIDGE-DISCOVERY-01)

Дата: 2026-11-22. Ветка `bridge-discovery-01` (worktree от `71259e7`). Уровень вопроса (L0): структурный, дедуктивная математика. Ничто здесь не доказывает RH.

**Источники.**
- PDF: Rubinstein et al., «The Alpöge–Claude proof of the Riemann hypothesis explained for the Riemann zeta function», рабочий черновик 21.11.2026. Локальный файл `C:\Users\serge\Downloads\zeta-paper.pdf`, 1 627 433 байт, SHA-256 `667d88b3…b706`; размер совпадает с `Content-Length` онлайн-версии (дата `Last-Modified` 21.11.2026 20:34 GMT). Номера страниц ниже — страницы PDF.
- Lean: `CocoSgt/riemann-hypothesis-lean`, коммит `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`, клон проверен (`git rev-parse HEAD` совпал). Тулчейн `leanprover/lean4:v4.33.1`, Mathlib `0df444a3…`. Это зеркало авторского архива; автор оригинала — Levent Alpöge.
- Память H-12 v2 и индекс (Google Drive) — прошлые результаты. Всё, что помечено «память v2», я заново не проверял.

**Статусы:** `PROVED`, `KERNEL_CHECKED`, `EXACT_COMPUTED`, `SOURCE_TRACED`, `CONDITIONAL`, `OPEN`, `REFUTED`, `NOT_RUN`. Стрелка `A ⇐ B` означает «для A необходимо B как предпосылка», не эквивалентность.

## 1. Граф

```
RiemannHypothesis                                   (Mathlib def; Main.lean:4, MainTheorems.lean:9)
 ⇐ E0  нет нулей ζ при Re s > θ для всех θ ∈ (1/2, 1)  + симметрия ρ ↦ 1−ρ
    ⇐ E1  оконный критерий: G(x) ≤ x^θ на [Y, Y^{3/2}] для сколь угодно больших Y
       ⇐ E2  явная формула для сглаженной суммы по простым степеням G(x)
       ⇐ E3  редукция G = R_{q,d} − G_χq + G_χd + G_η                       (II.8)
          ⇐ E4  оценка B: |G_χ(x)| ≤ x^{1/2+ε} для χ ∈ {χ_q, χ_d, χ_qχ_d}
          ⇐ E6  оценка A: R_{q,d}(x) ≤ C x^{C_ε}(x/m + xm/k + m + k/n²)       (A)
             ⇐ E5  оценка C: |G_χ(y)| ≤ y^{exp(−κ x^{ε/8})} при y ≥ exp(x^ε/3)/3   (5.6)
             ⇐ E7  главное неравенство (M): (1/n)ΣΣΣ (P − M) ≤ E               [quoted]
                ⇐ E7a  размер тета-ядер: III.4, III.7, III.8, III.9
                ⇐ E7b  делимость в инертных простых: II.6.3–6.4, III.5         ⇐ гипотеза (B)
                ⇐ E7c  от производных к решёткам: III.6
                ⇐ E7d  построение отображений и весов, сборка (M)               [не начато]
                ⇐ E7e  гипотеза (B): целостность тета-ядер в координатах height-two log
```

## 2. Рёбра

Колонки: формулировка; источник (PDF / Lean); предпосылки и кванторы; используемые леммы; можно ли ослабить; статус.

### E0. Нули справа от θ ⇒ RH
- **Формулировка.** Если для каждого θ ∈ (1/2, 1) функция ζ не имеет нулей при Re s > θ, то все нетривиальные нули лежат на Re s = 1/2.
- **Источник.** PDF §I.1, конец (p. 5); §II.3 «Conclusion» (p. 29). Lean: `rhOfAll := Formalism.VW.rh_of_every allChi`, `allChi := UpperTheory.FinalTheorems.everyCharacter` (`src/Supplements/Kernels/MainTheorems.lean:7,9`).
- **Предпосылки.** Функциональное уравнение: множество нулей инвариантно относительно ρ ↦ 1−ρ.
- **Ослабление.** Не требуется. Статус: `SOURCE_TRACED` (тип финальной теоремы — `RiemannHypothesis` из Mathlib, проверено чтением `Main.lean`, `Statements.lean`).

### E1. Оконный критерий (интервальная лемма Ландау)
- **Формулировка (PDF).** Пусть 0 < θ < 1. Если существуют сколь угодно большие Y, для которых G(x) ≤ x^θ при всех x ∈ [Y, Y^{3/2}], то ζ(s) ≠ 0 при Re s > θ.
- **Формулировка (Lean).** `Deduction.zeroFree_of_rpow_window (F : CharFamily) {θ δ C : ℝ} (hθ : 0 < θ) (hθ1 : θ < 1) (hδ : 0 < δ) (h : ∀ Y₀, ∃ Y, Y₀ ≤ Y ∧ ∀ y ∈ Set.Icc Y (Y^(1+δ)), Gm F y ≤ C * y^θ) : ZeroFree F θ` (`src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean:12–16`), через `lemmaL` и `windowHyp_of_rpow`. Замыкание импортов: 30 модулей, 2475 строк (подсчёт текстовый).
- **Источник (PDF).** Part II §1, pp. 26–27; формула (1.1), (II.2).
- **Предпосылки и кванторы.** F мероморфна, полюса при нулях ρ, все полюса с Re > 0 нереальные (ζ(σ) < 0 при 0 < σ < 1); грубая оценка |g(u)| ≪ e^{2u} вне окна (из |G(x)| ≪ x log x); σ ≥ 252; j ≈ (5/4)(σ−2)U.
- **Леммы.** Тождество Мелина (II.1); неравенство |g| + g = 2·max(g,0); концентрация плотности u^j e^{-(σ−2)u} около j/(σ−2); оценка Коши для производных голоморфной функции.
- **Что проверено мной.** Числовые константы доказательства пересчитаны с 50 знаками (`verification/check_interval_lemma_constants.py`): η = 0.982476903694…, log((1+η)/(2η)) = 0.0088782870…, c = 0.008 меньше; минимальное σ для θ → 0 равно 251.0013, значит σ = 252 достаточно, σ = 251 недостаточно; доля массы вне окна не превышает e^{−cj} с запасом в сотни порядков при U = 20…640. Логику шагов (1.1) → противоречие с полюсом я прочитал по тексту (pp. 26–27) и не нашёл разрыва: константы не зависят от j и t; неявная константа C₀ не зависит от U.
- **Ослабление (выяснено).**
  1. Отношение 3/2 заменяется любым фиксированным 1+δ (Lean уже так). `SOURCE_TRACED`.
  2. Поточечная оценка заменяется интегральной мажорантой (WindowHypU; RH-NEXT-01). `SOURCE_TRACED`.
  3. Окно ограниченной длины по u = log x **не годится**: для g(u) = e^{βu}cos(γu), β > θ (F(s) = (s−β)/((s−β)²+γ²), полюса нереальные), окна [U, U+L] с L < π/γ можно выбрать внутри фазы cos < 0, где g < 0. Строго элементарно. `PROVED` (см. `proof_or_counterexample/window_sharpness.md`).
  4. Положительная плотность хороших u вместо длинного окна не годится (тот же пример: плотность 1/2). `PROVED`.
  5. Минимальный рост длины окна L(U) → ∞ при фиксированной сложности F: `OPEN`.
- **Ядерная проверка Lean (моя).** В изолированном WSL2-клоне на `7cbf7a0` (Lean 4.33.1, Mathlib `0df444a3…`) замыкание модуля `ZeroFreeOfRpowWindow` собрано целиком (30 модулей; 60 с; пик RSS 6.9 ГБ); `#print axioms` для `Deduction.zeroFree_of_rpow_window`, `Deduction.lemmaL`, `Deduction.windowHyp_of_rpow` даёт `[propext, Classical.choice, Quot.sound]` (`verification/check_window.out`). Смысл формулировки проверен через `#print`: `ZeroFree F θ := ∀ i s, θ < s.re → LFunction (F.χ i) s ≠ 0`; `Gm F y = Σ_i a_i·Re(Gchi (χ_i) y)` с положительными весами a_i; критерий `WindowHyp F θ δ` в интегральной форме: для всех η > 0 и Y₀ существует Y ≥ Y₀ и мажоранта R ≥ max(Gm, 0) на `[Y, Y^{1+δ}]` с ∫ R·y^{−θ−1} ≤ Y^η. Поточечная оценка `Gm ≤ C·y^θ` — частный случай (`windowHyp_of_rpow`).
- **Статус.** Константы `EXACT_COMPUTED`; формулировки Lean `KERNEL_CHECKED` (локальное замыкание, стандартные аксиомы); переход PDF → Lean по тексту `SOURCE_TRACED`.

### E2. Явная формула для G
- **Формулировка.** F(s) = −ζ′(s)/(s(s−1)ζ(s)) − 1/(s−1)² + (1+γ)/(s−1); G(x) = log 2π − Σ_ρ x^ρ/(ρ(ρ−1)) + O(x^{−2}).
- **Источник.** PDF (I.2)–(I.4), p. 4; (II.1), p. 26.
- **Что проверено мной.** Определение G через суммы по простым степеням: G(10³) = 1.530913, G(10⁶) = 11.04044 (сходится с таблицей PDF 1.531 и 11.040). Саму формулу и тождество Мелина я не пересчитывал. Статус: определение `EXACT_COMPUTED` на двух значениях, формула `SOURCE_TRACED`.

### E3. Редукция к одной сумме по простым
- **Формулировка.** R_{q,d}(x) = S_{q,d}(x) − x log x + (1 + γ + c_{χq} − c_{χd} − c_η)x = G(x) + G_{χq}(x) − G_{χd}(x) − G_η(x).
- **Источник.** PDF (II.7)–(II.8), p. 29; таблица (II.24), p. 35.
- **Предпосылки.** q ≡ 3 (mod 8), d ≡ 7 (mod 16), q | d+1; χ_q, χ_d — символы Лежандра; η = χ_qχ_d; c_χ = L′/L(1, χ).
- **Что проверено мной (независимая реализация).** Для q = 3, d = 23 при y = 10³ и 10⁶: c_{χ3} = 0.36828162, c_{χ23} = −0.42212095, c_η = 0.056522659; G_{χ3} = 1.039978, G_{χ23} = 1.331664, G_η = −5.704478; прямое вычисление R = 6.9437046 и комбинация G + G_{χ3} − G_{χ23} − G_η совпадают до 3·10⁻⁵⁷; при y = 10⁶ R = 749.849948. Все значения совпадают с таблицей (II.24) в её шести знаках (`verification/check_II8_identity.py`). Статус `EXACT_COMPUTED` (два значения y).
- **Ослабление.** Для верхней оценки G нужны односторонние оценки: G_{χd} ≤ ·, G_η ≤ ·, G_{χq} ≥ −·; PDF использует абсолютные оценки. Вывод тривиален из (II.8). `PROVED`, содержательной пользы не даёт: оценка B даёт абсолютную границу без дополнительных затрат.

### E4. Оценка B (вспомогательные простые q, d)
- **Формулировка.** Для каждого большого Y найдутся q ≡ 3 (mod 8), d ≡ 7 (mod 16), q | d+1, такие что |G_χ(x)| ≤ x^{1/2+ε} при χ = χ_q, χ_d, χ_qχ_d, для всех x ∈ [Y, Y^{3/2}]; 0 < ε < 1/52.
- **Источник.** PDF §II.3 п. 2 (p. 29); Part III §III.1 (pp. 55–60), из четырёх цитируемых теорем (Q1)–(Q4); Lean: файлы [9, 10, 29] списка источников, леммы `QH.thinH`, `twistK`, `meanSqK`, `bad_share`, `tailK`, `count_bad`, `hostThickExists`, `topsChoiceH`.
- **Статус.** `CONDITIONAL` (на цитируемые теоремы); мной не проверялось (`NOT_RUN`).

### E5. Оценка C
- **Формулировка.** (5.6): |G_χ(y)| ≤ y^ϑ, ϑ = exp(−κ x^{ε/8}), для всех примитивных характеров таблицы и y ≥ exp(x^ε/3)/3; κ не зависит от x, q, d.
- **Источник.** PDF §5.4 (p. 36); Part III §III.2 (Теорема III.2.1) из трёх цитируемых теорем (Z1)–(Z3) и Теоремы III.1.1(e).
- **Статус.** `CONDITIONAL`; мной не проверялось (`NOT_RUN`).

### E6. Оценка A из (M), B, C
- **Формулировка.** Есть положительные целые m, k, n, зависящие от x, с R_{q,d}(x) ≤ C_ε x^{C_ε}(x/m + xm/k + m + k/n²); m = x^{1/2+O(ε)}, k = x^{9/2+O(ε)}, n = x^{2+O(ε)}. Тогда G(x) ≤ x^{1/2+C′ε}.
- **Источник.** PDF §§4–5, pp. 30–36, (II.15)–(II.16), (II.25)–(II.26); баланс x/m и m при √x.
- **Что проверено мной.** Показатели при ε → 0: x/m → x^{1/2}, xm/k → x^{−3}, m → x^{1/2}, k/n² → x^{1/2}; x/m + m ≥ 2√x при любом m, так что показатель 1/2 внутри этой бухгалтерии не улучшается (`verification/check_interval_lemma_constants.py`). Статус `EXACT_COMPUTED` для арифметики показателей; выводы (5.1)–(5.5) — `SOURCE_TRACED`. Численные значения (II.20) воспроизведены ранее в H-12 (задача M2, память v2); предмет замечания там: знак показателя характера в (II.21).

### E7. Главное неравенство (M)
- **Формулировка.** При δ ≥ x^{−ε}, |T|/n ≥ x^{−ε/8}/2, B = |T| m b δ/2: (1/n)Σ_{u∈H}Σ_{t∈T}Σ_{j=1}^m (P_{u,t,j} − M_{u,t,j}) ≤ E, E/B ≤ x^{Cε}(x/m + xm/k + m + k/n²), x ≥ x₀(ε).
- **Источник.** PDF (M), p. 32; построение Part II §6, pp. 37–53; Part III §III.4–III.9.
- **Статус по PDF (таблица p. 25 и pp. 54–55).** `OPEN` как полное доказательство: (M) процитировано, сборка «не начата». Что ниже доказано условно, см. E7a–E7e.

| Ребро | PDF | Что доказано в PDF | Что процитировано | Статус |
|---|---|---|---|---|
| E7a размер тета-ядер | III.4, III.7, III.8, III.9 | абстрактные оценки для блока, отображения и цепочки; из одиннадцати названных входов следует неравенство размера (III.75); оценка размерности из трёх утверждений Lean; шаг от оценки когомологий Галуа к знаменателям | то, что отображения конструкции — экземпляры абстрактных объектов; одиннадцать арифметических входов; три утверждения о следах, рангах, спариваниях; оценка когомологий | `CONDITIONAL`, четыре места условны |
| E7b делимость в инертных простых | II.6.3–6.4, III.5 | локальная оценка для степенных рядов для орбит длины два; для длинных нужен цитируемый факт двойственности | целостность тета-ядер (гипотеза (B)); метки и рамки | `CONDITIONAL` на (B) |
| E7c от производных к решёткам | III.6 | леммы о наклонах решёток, разбиение суммы по классам простых, оценки части членов | оценки одиннадцати сумм потерь; утверждение о значениях нормирования; теорема о склеенной решётке (условно) | `CONDITIONAL` |
| E7d построение и сборка | — | не начато | всё | `OPEN` |
| E7e гипотеза (B) | III.5; Lean `src/Formalism/GaussJetBounds/Statement.lean` (BHyp) | авторские конечные проверки первой части: степени 84/72/144 при ℓ = 3/7/11 | вторая часть и все степени | `OPEN` (память v2: условная симметрия двух дефектов; степень 12: z-модель проходит, t-модель нет; совпадение с авторской нормировкой не доказано) |

## 3. Lean-хребет и проверка поставщика `l1b`

Цепочка (память v2: `SOURCE_TRACED`, мной выборочно проверено существование файлов и конечные формулировки): `rhOfAll` (MainTheorems.lean:9) ← `UpperTheory.FinalTheorems.everyCharacter` (CharacterBoxes/MainConclusion.lean) ← `every_character_of_literature_of_vWin` (ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean) ← `every_character_of_theta_integrals_local_matching` (SiegelEisensteinSecondTermHypotheses.lean) ← `every_character_of_green_v_win` (TopPlug.lean) ← `shape_closed_link_n_of_green` (TopShape.lean) → ветви CutUp и Tied (см. память v2).

**Мой независимый повторный разбор ветви, подающей поле `l1b`** (чтение исходников в клоне на `7cbf7a0`; `SOURCE_TRACED`):

1. `Formalism.L2.Top4Wire2.wire4F_alt` (`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/Wire4F.lean:26`) строит доказательство, передавая `Q := selI Fm … i` (элемент `IndefiniteRealisationChoice'`) в `RowDataTransport.packageOfPrimitiveLinks Q hok1 hsep C CH hP ra.pass`. Q не конструируется внутри теоремы: это выбор из входной структуры `selI`.
2. `packageOfPrimitiveLinks` — `abbrev` (`…/ThirdPlaceSeries/PtKOfReal.lean:19`), равный `primitivePackageFullHecke hOk hsep Q.Rl (faceT …) Q.sEE (hkCan P.A3) Cl CHl Q.charW hP hI`.
3. `primitivePackageFullHecke` (`src/Formalism/LocalToGlobal/IndefiniteReal/PrimitivePackageFullHecke.lean:29–37`) вызывает `packageFullHecke (base_lifts_package_of_primitive_links hOk hsep hC hP) …`.
4. `packageFullHecke` (`…/NearConstantMultiplicities.lean:58`) вызывает `basePackageFullHecke { toPrimitiveStatementsBaseLiftsOnly := hN, passage := passage3_of hN hP }`.
5. `basePackageFullHecke` (`…/PackageFromPrimitiveStatements.lean:120`) берёт поля спаривания и `L1e` из `(Classical.epsilon_spec hC.cols).1/.2`, где `zetaEps := Classical.epsilon …`.
6. `PrimitiveStatementsBaseLiftsOnly.cols` (`…/PackageFromPrimitiveStatements.lean:106`) — **теорема**, доказанная вызовом `X.exists_zeta_pairing_factors_through_periods … hC.miStar`.
7. `CxData.exists_zeta_pairing_factors_through_periods` (`src/Formalism/LocalToGlobal/IndefiniteReal/IsometricPeriodsOfUnitHypotheses.lean:194–201`) — теорема; поле `L1e` (то, что в памяти v2 названо `l1b`) приходит из `btVanish_of_miStar2` как `hL`, а `hL` поставляет `isometric_periods_of_unit_hypotheses`. Спаривание — из `cutPairing`.

**Ядерная проверка этой ветви (моя).** Замыкание модуля `PrimitivePackageFullHecke` собрано целиком: 1043 модуля, 225 009 строк, 28 мин 31 с на 8 ядрах (процессорное время 10 013 с user + 1 875 с sys), пик использования памяти 10,9 ГБ, 0 ошибок (`verification/build_l1b.*`). `#print axioms` для `CxData.exists_zeta_pairing_factors_through_periods`, `CxData.btVanish_of_miStar2`, `CxData.isometric_periods_of_unit_hypotheses`, `CxData.cutPairing`, `PrimitiveStatementsBaseLiftsOnly.cols`, `basePackageFullHecke`, `packageFullHecke`, `Links.primitivePackageFullHecke` — везде `[propext, Classical.choice, Quot.sound]` (`verification/check_l1b.out`). Это означает, что локальный поставщик поля не опирается на `sorryAx`, `Lean.ofReduceBool` и пользовательские аксиомы. Это не проверка того, что `ra.miStar` в финальной теореме выполняется: `MIstar2` остаётся гипотезой теорем, а её источник определяет `selI`.

**Вывод по ветви.** Конкретный поставщик поля — доказанная теорема `isometric_periods_of_unit_hypotheses`, питаемая гипотезой `MIstar2 eV sEE`, которая передаётся вниз как поле `miStar` структуры `CovolumeOntoIsometryConditions` (`Wire4F.lean`: `miStar := ra.miStar`). Голой аксиомы про `l1b` в этой ветке нет. Что остаётся открытым как исходный математический вход: происхождение `ra.miStar` (получается из `hRows` в `wire4F_alt`) и семантическая корректность `MIstar2` как арифметического утверждения (в терминологии PDF это «mean of periods = log Ω_E», вход (S4) §III.7). Это уточняет, но не заменяет аудит M-TRACE-05: финальный экземпляр Q в `RealTBAlt` по-прежнему определяется выбором `selI` на уровне TopShape. `SOURCE_TRACED` для маршрута; `KERNEL_CHECKED` — для перечисленных локальных деклараций. **`#print axioms riemannHypothesis` и `lake build Main` — `NOT_RUN`:** замыкание `Main` содержит 174 764 модуля и 17 329 808 строк; по измеренной скорости (≈ 18,9 строки на процессорную секунду: 225 009 строк за 11 888 с (user+sys)) полная сборка потребует 250–570 процессорных часов, то есть 37–82 часа на этой машине (оценка `INFERRED`, см. `research_decision.md`).

**Правка к памяти v2.** В памяти (M-TRACE-05) локальный конструктор назван цепочкой `Links.base_lifts_package_of_primitive_links → primitivePackageFullHecke → Cx.packageFullHecke → Cx.basePackageFullHecke`. Мой разбор подтверждает её порядок и добавляет два звена: `Wire4F.wire4F_alt → packageOfPrimitiveLinks` сверху и `PrimitiveStatementsBaseLiftsOnly.cols → exists_zeta_pairing_factors_through_periods → isometric_periods_of_unit_hypotheses` снизу.

## 4. Рёбра, пригодные для независимого доказательства

| Ребро | Почему реалистично | Что даст |
|---|---|---|
| E1 (оконный критерий) | замыкание 30 модулей; доказательство одностраничное; формулировка Lean есть | независимая ядерная проверка (`#print axioms`) и граница применимости (пп. 3–5 выше); новой теоремы не даёт |
| E7e (гипотеза (B), p-адическая целостность) | конечные точные тесты; метод Дворка (Фробениус φ(i) = −i для Z₃[i]); конкретная задача H12-PADIC-B4-04 | если доказать для всех степеней — закрывает одно из пяти условных мест E7b; выше моего текущего объёма |
| E4/E5 (оценки B и C) | доказываются из цитируемых классических теорем | проверка литературной части; не снимает (M) |

Ребро E7 (M) целиком: не реалистично в рамках этой миссии; описано как `OPEN`.
